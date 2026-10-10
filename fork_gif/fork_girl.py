"""Cartoon loop: the long-fork cream-puff challenge.

Renders frames with pycairo, then ffmpeg turns them into a GIF and an MP4.
Usage: python3 fork_girl.py <out_dir>
"""
import math
import os
import subprocess
import sys

import cairo

W, H = 540, 810
FR = 112          # frames in the loop
FPS = 22

OL = (0.16, 0.10, 0.08)            # outline
SKIN = (0.97, 0.80, 0.66)
SKIN_SH = (0.90, 0.68, 0.54)
HAIR = (0.12, 0.08, 0.07)
HAIR_HI = (0.33, 0.24, 0.21)
SWEATER = (0.33, 0.39, 0.20)
SWEATER_DK = (0.24, 0.29, 0.14)
SWEATER_HI = (0.42, 0.49, 0.27)
JEANS = (0.33, 0.45, 0.64)

S = (228, 468)     # fork-arm shoulder (her right, viewer left)
S2 = (432, 468)    # other shoulder
ARM = 190


# ---------------------------------------------------------------- helpers
def clamp(t):
    return max(0.0, min(1.0, t))


def lerp(a, b, t):
    return a + (b - a) * t


def seg(f, a, b):
    return clamp((f - a) / (b - a))


def ss(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def ease_out_back(t, k=1.9):
    t = clamp(t) - 1
    return 1 + (k + 1) * t ** 3 + k * t ** 2


def step_ease(t, n=4):
    """Telescope 'clicks': n quick snaps instead of one smooth slide."""
    t = clamp(t)
    if t >= 1:
        return 1.0
    i = math.floor(t * n)
    fr = clamp((t * n - i) * 1.8)
    return (i + ease_out_back(fr, 1.2)) / n


def d2r(d):
    return d * math.pi / 180


def polar(origin, p):
    dx, dy = p[0] - origin[0], p[1] - origin[1]
    return math.degrees(math.atan2(dy, dx)), math.hypot(dx, dy)


def rgb(c, a=1.0):
    return (*c, a)


def fill_stroke(ctx, fill, lw=3.0, line=OL):
    ctx.set_source_rgba(*rgb(fill) if len(fill) == 3 else fill)
    ctx.fill_preserve()
    ctx.set_line_width(lw)
    ctx.set_source_rgb(*line)
    ctx.stroke()


def ellipse(ctx, cx, cy, rx, ry):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()


def thick_line(ctx, a, b, w, color, cap=cairo.LINE_CAP_ROUND):
    ctx.set_line_cap(cap)
    ctx.set_line_width(w)
    ctx.set_source_rgba(*color) if len(color) == 4 else ctx.set_source_rgb(*color)
    ctx.move_to(*a)
    ctx.line_to(*b)
    ctx.stroke()


def heart(ctx, x, y, s, color, alpha):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(0, 6)
    ctx.curve_to(-14, -4, -8, -16, 0, -8)
    ctx.curve_to(8, -16, 14, -4, 0, 6)
    ctx.close_path()
    ctx.restore()
    ctx.set_source_rgba(*color, alpha)
    ctx.fill_preserve()
    ctx.set_source_rgba(*OL, alpha)
    ctx.set_line_width(2)
    ctx.stroke()


def sparkle(ctx, x, y, s, alpha, color=(1, 1, 1)):
    ctx.save()
    ctx.translate(x, y)
    ctx.move_to(0, -s)
    for k in range(4):
        a = k * math.pi / 2
        ctx.curve_to(0, 0, 0, 0, s * math.sin(a + math.pi / 2), -s * math.cos(a + math.pi / 2))
    ctx.close_path()
    ctx.restore()
    ctx.set_source_rgba(*color, alpha)
    ctx.fill()


def comic_text(ctx, txt, x, y, size, rot, fill, alpha=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    ext = ctx.text_extents(txt)
    ctx.move_to(-ext.width / 2 - ext.x_bearing, ext.height / 2)
    ctx.text_path(txt)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*OL, alpha)
    ctx.set_line_width(size * 0.22)
    ctx.stroke_preserve()
    ctx.set_source_rgba(*fill, alpha)
    ctx.fill()
    ctx.restore()


# ---------------------------------------------------------------- pose
def theta(f):
    """Angle of the stiff (taped-straight) fork arm around the shoulder."""
    if f < 14:
        return 140
    if f < 40:
        return lerp(140, 170, ss(seg(f, 14, 34)))
    if f < 88:
        return lerp(170, 226, ss(seg(f, 40, 56)))
    return lerp(226, 140, ss(seg(f, 88, 106)))


def bob(f):
    b = 2.2 * math.sin(2 * math.pi * f / FR * 4)
    chew = 0.0
    if 61 <= f < 90:
        env = ss(seg(f, 61, 64)) * (1 - ss(seg(f, 84, 90)))
        chew = 4.5 * math.sin((f - 61) * 1.15) * env
    return b + chew


def head_center(f):
    tilt = 0
    if 61 <= f < 90:
        tilt = 3 * math.sin((f - 61) * 0.55) * ss(seg(f, 61, 66)) * (1 - ss(seg(f, 84, 90)))
    return (330 + tilt, 300 + bob(f))


PUFF_TARGET = (356, 712)   # the cream puff she spears in the dish
PUFF_R = 35
IDLE_PHI, IDLE_LEN = -66, 72
PIERCE = 8


def hand_at(f):
    t = d2r(theta(f))
    return (S[0] + ARM * math.cos(t), S[1] + ARM * math.sin(t))


def eat_center(f):
    hc = head_center(f)
    return (hc[0] - 12, hc[1] + 64)


def tip_for_center(hand, c):
    a, _ = polar(hand, c)
    u = (math.cos(d2r(a)), math.sin(d2r(a)))
    tip = (c[0] + u[0] * PIERCE, c[1] + u[1] * PIERCE)
    return polar(hand, tip)


def fork(f):
    """Return (phi in degrees, fork length) for frame f."""
    h = hand_at(f)
    if f < 14:
        return IDLE_PHI + 3 * math.sin(f * 0.5), IDLE_LEN
    if f < 40:
        a_t, l_t = tip_for_center(h, PUFF_TARGET)
        phi = lerp(IDLE_PHI, a_t, ss(seg(f, 14, 21)))
        ln = lerp(IDLE_LEN, l_t, step_ease(seg(f, 19, 35)))
        if f >= 35:
            ln = l_t + 7 * math.sin(math.pi * seg(f, 36, 40))
        return phi, ln
    a0, l0 = tip_for_center(h, PUFF_TARGET)
    a1, l1 = tip_for_center(h, eat_center(f))
    if f < 54:
        t = ss(seg(f, 40, 54))
        phi = lerp(a0, a1, t) - 88 * math.sin(math.pi * t) ** 1.1
        ln = lerp(l0, l1 - 160, t)
        return phi, ln
    if f < 88:
        push = lerp(l1 - 160, l1, ease_out_back(seg(f, 54, 59), 1.4))
        jab = 5 * (math.sin(math.pi * seg(f, 60, 62)) + math.sin(math.pi * seg(f, 66, 68)))
        pull = 34 * ss(seg(f, 68, 74))
        return a1, push + jab - pull
    t = ss(seg(f, 88, 106))
    return lerp(a1, IDLE_PHI, t), lerp(l1 - 34, IDLE_LEN, t)


def tip_at(f):
    h = hand_at(f)
    phi, ln = fork(f)
    return (h[0] + ln * math.cos(d2r(phi)), h[1] + ln * math.sin(d2r(phi)))


def puff_on_fork(f):
    if not (36 <= f < 67):
        return None
    tip = tip_at(f)
    phi, _ = fork(f)
    return (tip[0] - PIERCE * math.cos(d2r(phi)), tip[1] - PIERCE * math.sin(d2r(phi)))


# ---------------------------------------------------------------- scenery
def draw_background(ctx):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.47, 0.44, 0.40)
    g.add_color_stop_rgb(0.18, 0.80, 0.75, 0.67)
    g.add_color_stop_rgb(1, 0.72, 0.66, 0.58)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()

    # left wall with the maroon stripe
    ctx.rectangle(0, 120, 168, 560)
    ctx.set_source_rgb(0.93, 0.90, 0.85)
    ctx.fill()
    ctx.rectangle(0, 372, 168, 62)
    ctx.set_source_rgb(0.50, 0.11, 0.16)
    ctx.fill()
    ctx.rectangle(0, 372, 168, 6)
    ctx.set_source_rgba(1, 1, 1, 0.15)
    ctx.fill()
    ctx.rectangle(160, 120, 8, 560)
    ctx.set_source_rgba(0, 0, 0, 0.10)
    ctx.fill()

    # ceiling beam
    ctx.rectangle(0, 92, W, 30)
    ctx.set_source_rgb(0.76, 0.72, 0.66)
    ctx.fill()

    # window / door behind her
    ctx.rectangle(198, 150, 280, 520)
    ctx.set_source_rgb(0.93, 0.91, 0.85)
    ctx.fill_preserve()
    ctx.set_source_rgba(0, 0, 0, 0.25)
    ctx.set_line_width(2)
    ctx.stroke()
    panes = [(214, 166, 248, 82), (214, 262, 118, 400), (344, 262, 118, 400)]
    for x, y, w, h in panes:
        pg = cairo.LinearGradient(x, y, x + w, y + h)
        pg.add_color_stop_rgb(0, 0.30, 0.35, 0.28)
        pg.add_color_stop_rgb(1, 0.20, 0.24, 0.19)
        ctx.rectangle(x, y, w, h)
        ctx.set_source(pg)
        ctx.fill()
        ctx.save()
        ctx.rectangle(x, y, w, h)
        ctx.clip()
        ctx.move_to(x + w * 0.2, y + h)
        ctx.line_to(x + w * 0.55, y)
        ctx.line_to(x + w * 0.75, y)
        ctx.line_to(x + w * 0.4, y + h)
        ctx.set_source_rgba(1, 1, 1, 0.06)
        ctx.fill()
        ctx.restore()

    # right wall corner
    ctx.rectangle(478, 120, 62, 560)
    ctx.set_source_rgb(0.84, 0.79, 0.71)
    ctx.fill()


def draw_counter(ctx):
    top = 648
    g = cairo.LinearGradient(0, top, 0, H)
    g.add_color_stop_rgb(0, 0.30, 0.30, 0.33)
    g.add_color_stop_rgb(1, 0.20, 0.20, 0.23)
    ctx.rectangle(0, top, W, H - top)
    ctx.set_source(g)
    ctx.fill()
    ctx.set_line_width(1.6)
    veins = [((0, 690), (120, 670), (210, 720), (330, 700)),
             ((140, 810), (220, 760), (330, 790), (540, 740)),
             ((260, 660), (330, 690), (420, 672), (540, 700))]
    for p0, p1, p2, p3 in veins:
        ctx.move_to(*p0)
        ctx.curve_to(*p1, *p2, *p3)
        ctx.set_source_rgba(0.6, 0.6, 0.65, 0.25)
        ctx.stroke()
    ctx.rectangle(0, top, W, 4)
    ctx.set_source_rgba(1, 1, 1, 0.18)
    ctx.fill()


DISH_PUFFS = [(110, 726, 36, 0.3), (196, 704, 34, 1.7), (178, 760, 36, 2.6),
              (276, 738, 37, 4.1), (440, 728, 35, 5.2), (400, 764, 35, 0.9)]


def dish_path(ctx, inset=0):
    ctx.new_path()
    ctx.move_to(78 + inset, 656 + inset)
    ctx.line_to(462 - inset, 656 + inset)
    ctx.curve_to(486 - inset, 656 + inset, 500 - inset, 668, 504 - inset, 690)
    ctx.line_to(510 - inset, 770 - inset)
    ctx.curve_to(512 - inset, 788 - inset, 500 - inset, 796 - inset, 484 - inset, 796 - inset)
    ctx.line_to(56 + inset, 796 - inset)
    ctx.curve_to(40 + inset, 796 - inset, 28 + inset, 788 - inset, 30 + inset, 770 - inset)
    ctx.line_to(36 + inset, 690)
    ctx.curve_to(40 + inset, 668, 54 + inset, 656 + inset, 78 + inset, 656 + inset)
    ctx.close_path()


def draw_dish_back(ctx):
    dish_path(ctx)
    ctx.set_source_rgba(0.80, 0.95, 0.97, 0.16)
    ctx.fill()
    # shadow under dish
    ellipse(ctx, 270, 800, 250, 12)
    ctx.set_source_rgba(0, 0, 0, 0.25)
    ctx.fill()


def draw_dish_front(ctx):
    dish_path(ctx)
    ctx.set_line_width(7)
    ctx.set_source_rgba(0.85, 0.97, 1.0, 0.55)
    ctx.stroke()
    dish_path(ctx, 9)
    ctx.set_line_width(2.5)
    ctx.set_source_rgba(0.85, 0.97, 1.0, 0.35)
    ctx.stroke()
    # handles
    for x0, s in ((30, -1), (510, 1)):
        ctx.move_to(x0 + s * 2, 680)
        ctx.curve_to(x0 + s * 22, 682, x0 + s * 22, 720, x0 + s * 4, 722)
        ctx.set_line_width(6)
        ctx.set_source_rgba(0.85, 0.97, 1.0, 0.5)
        ctx.stroke()
    # front glass glare
    ctx.move_to(70, 785)
    ctx.line_to(200, 785)
    ctx.set_line_width(4)
    ctx.set_source_rgba(1, 1, 1, 0.55)
    ctx.stroke()
    ctx.move_to(230, 785)
    ctx.line_to(250, 785)
    ctx.stroke()


def draw_puff(ctx, cx, cy, r, seed=0.0, scale=1.0, bite=0, bite_dir=0.0, squash=1.0):
    if scale <= 0.01:
        return
    r *= scale

    def outline():
        ctx.new_path()
        n = 60
        for i in range(n + 1):
            a = 2 * math.pi * i / n
            rr = r * (1 + 0.035 * math.sin(5 * a + seed) + 0.015 * math.sin(11 * a + seed * 2))
            x = cx + rr * math.cos(a) / squash
            y = cy + rr * math.sin(a) * 0.9 * squash
            if i == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        ctx.close_path()

    ctx.push_group()
    outline()
    g = cairo.RadialGradient(cx - r * 0.35, cy - r * 0.4, r * 0.1, cx, cy, r * 1.15)
    g.add_color_stop_rgb(0, 1.0, 0.90, 0.62)
    g.add_color_stop_rgb(0.5, 0.96, 0.72, 0.30)
    g.add_color_stop_rgb(1, 0.76, 0.47, 0.16)
    ctx.set_source(g)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.50, 0.29, 0.08)
    ctx.set_line_width(2.4)
    ctx.stroke()
    # craquelin cracks
    ctx.set_line_width(1.4)
    ctx.set_source_rgba(0.62, 0.36, 0.10, 0.7)
    for k in range(4):
        a = seed + k * 1.6
        x0 = cx + r * 0.45 * math.cos(a)
        y0 = cy + r * 0.35 * math.sin(a) - r * 0.15
        ctx.move_to(x0, y0)
        ctx.rel_curve_to(r * 0.12, -r * 0.08, r * 0.2, r * 0.04, r * 0.3, -r * 0.05)
        ctx.stroke()
    # shine
    ellipse(ctx, cx - r * 0.38, cy - r * 0.42, r * 0.28, r * 0.15)
    ctx.set_source_rgba(1, 1, 1, 0.55)
    ctx.fill()
    # cream peeking out
    a = seed * 1.3
    ellipse(ctx, cx + r * 0.62 * math.cos(a), cy + r * 0.25 + r * 0.25 * math.sin(a), r * 0.2, r * 0.13)
    ctx.set_source_rgb(1, 0.99, 0.95)
    ctx.fill()
    # powdered sugar
    for k in range(7):
        a = seed * 3 + k * 0.9
        ctx.arc(cx + r * 0.6 * math.cos(a), cy - r * 0.35 + r * 0.25 * math.sin(a * 1.7), 1.3, 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 1, 0.8)
        ctx.fill()

    if bite:
        bx = cx + math.cos(bite_dir) * r * (1.05 if bite == 1 else 0.2)
        by = cy + math.sin(bite_dir) * r * (1.05 if bite == 1 else 0.2)
        br = r * (0.78 if bite == 1 else 1.05)
        # cream filling showing along the bite edge
        ctx.save()
        outline()
        ctx.clip()
        ctx.arc(bx, by, br + 7, 0, 2 * math.pi)
        ctx.set_source_rgb(1, 0.98, 0.90)
        ctx.fill()
        ctx.restore()
        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.arc(bx, by, br, 0, 2 * math.pi)
        ctx.fill()
        for k in (-1, 0, 1):   # tooth scallops
            a = bite_dir + math.pi + k * 0.55
            ctx.arc(bx + br * math.cos(a), by + br * math.sin(a), 5, 0, 2 * math.pi)
            ctx.fill()
        ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source()
    ctx.paint()


# ---------------------------------------------------------------- character
def taped_arm(ctx, s, e, cuff=True):
    """Arm wrapped straight in gold satin (the 'tied hands' challenge)."""
    dx, dy = e[0] - s[0], e[1] - s[1]
    L = math.hypot(dx, dy)
    u = (dx / L, dy / L)
    n = (-u[1], u[0])
    wrist = (e[0] - u[0] * 18, e[1] - u[1] * 18)
    satin_end = (e[0] - u[0] * 44, e[1] - u[1] * 44)
    thick_line(ctx, s, satin_end, 52, OL)
    g = cairo.LinearGradient(s[0] + n[0] * 24, s[1] + n[1] * 24, s[0] - n[0] * 24, s[1] - n[1] * 24)
    g.add_color_stop_rgb(0, 0.58, 0.46, 0.30)
    g.add_color_stop_rgb(0.3, 0.90, 0.80, 0.62)
    g.add_color_stop_rgb(0.45, 0.98, 0.94, 0.84)
    g.add_color_stop_rgb(0.62, 0.80, 0.67, 0.46)
    g.add_color_stop_rgb(1, 0.52, 0.40, 0.25)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_width(46)
    ctx.set_source(g)
    ctx.move_to(*s)
    ctx.line_to(*satin_end)
    ctx.stroke()
    # satin creases
    ctx.set_line_width(2)
    for k in range(1, 6):
        t = k / 6.0
        p = (s[0] + dx * t * 0.8, s[1] + dy * t * 0.8)
        ctx.move_to(p[0] + n[0] * 20, p[1] + n[1] * 20)
        ctx.curve_to(p[0] + n[0] * 8 + u[0] * 14, p[1] + n[1] * 8 + u[1] * 14,
                     p[0] - n[0] * 6 - u[0] * 6, p[1] - n[1] * 6 - u[1] * 6,
                     p[0] - n[0] * 18 + u[0] * 10, p[1] - n[1] * 18 + u[1] * 10)
        ctx.set_source_rgba(0.45, 0.33, 0.18, 0.45)
        ctx.stroke()
    if cuff:
        thick_line(ctx, satin_end, wrist, 46, OL, cairo.LINE_CAP_BUTT)
        thick_line(ctx, satin_end, wrist, 40, SWEATER, cairo.LINE_CAP_BUTT)
        for k in range(-3, 4):
            a = (satin_end[0] + n[0] * k * 5.5, satin_end[1] + n[1] * k * 5.5)
            b = (wrist[0] + n[0] * k * 5.5, wrist[1] + n[1] * k * 5.5)
            thick_line(ctx, a, b, 1.6, SWEATER_DK)


def draw_back_hair(ctx, hc):
    x, y = hc
    ctx.new_path()
    ctx.move_to(x, y - 118)
    ctx.curve_to(x - 95, y - 120, x - 128, y - 50, x - 122, y + 40)
    ctx.curve_to(x - 118, y + 120, x - 140, y + 200, x - 118, y + 262)
    ctx.curve_to(x - 100, y + 285, x - 70, y + 270, x - 60, y + 250)
    ctx.line_to(x + 60, y + 250)
    ctx.curve_to(x + 72, y + 274, x + 108, y + 286, x + 122, y + 258)
    ctx.curve_to(x + 142, y + 200, x + 120, y + 120, x + 124, y + 40)
    ctx.curve_to(x + 130, y - 50, x + 95, y - 120, x, y - 118)
    ctx.close_path()
    fill_stroke(ctx, HAIR)


def draw_body(ctx, f):
    breathe = 1.2 * math.sin(2 * math.pi * f / FR * 2)
    # jeans
    ctx.rectangle(214, 596, 232, 70)
    fill_stroke(ctx, JEANS)
    for x in (262, 398):
        thick_line(ctx, (x, 598), (x, 616), 3, (0.25, 0.35, 0.52))
    # sweater
    ctx.new_path()
    ctx.move_to(282, 412)
    ctx.curve_to(240, 420, 206, 430, 200, 482)
    ctx.line_to(208, 606 + breathe)
    ctx.line_to(452, 606 + breathe)
    ctx.line_to(460, 482)
    ctx.curve_to(454, 430, 420, 420, 378, 412)
    ctx.close_path()
    g = cairo.LinearGradient(200, 0, 460, 0)
    g.add_color_stop_rgb(0, SWEATER_DK[0], SWEATER_DK[1], SWEATER_DK[2])
    g.add_color_stop_rgb(0.4, *SWEATER_HI)
    g.add_color_stop_rgb(1, *SWEATER_DK)
    ctx.set_source(g)
    ctx.fill_preserve()
    ctx.set_source_rgb(*OL)
    ctx.set_line_width(3)
    ctx.stroke()
    # cable knit
    for cx in (262, 312, 350, 400):
        y = 440
        while y < 590:
            ctx.move_to(cx - 7, y)
            ctx.curve_to(cx - 7, y + 8, cx + 7, y + 6, cx + 7, y + 14)
            ctx.move_to(cx + 7, y)
            ctx.curve_to(cx + 7, y + 5, cx + 2, y + 6, cx + 1, y + 7)
            y += 14
        ctx.set_source_rgba(*SWEATER_DK, 0.9)
        ctx.set_line_width(2.4)
        ctx.stroke()
        thick_line(ctx, (cx - 13, 440), (cx - 13, 590), 1.4, (*SWEATER_HI, 0.7))
        thick_line(ctx, (cx + 13, 440), (cx + 13, 590), 1.4, (*SWEATER_HI, 0.7))
    # ribbed hem
    ctx.rectangle(208, 590 + breathe, 244, 16)
    ctx.set_source_rgb(*SWEATER_DK)
    ctx.fill()
    for x in range(212, 452, 6):
        thick_line(ctx, (x, 592 + breathe), (x, 604 + breathe), 1.2, (*SWEATER, 1))
    # the little black pin
    ctx.arc(300, 505, 11, 0, 2 * math.pi)
    fill_stroke(ctx, (0.08, 0.08, 0.09), 2)
    ctx.arc(300, 505, 5, d2r(30), d2r(330))
    ctx.set_source_rgb(0.9, 0.9, 0.9)
    ctx.set_line_width(2)
    ctx.stroke()


def draw_neck_collar(ctx, hc):
    x, y = hc
    ctx.rectangle(x - 26, y + 80, 52, 50)
    fill_stroke(ctx, SKIN)
    ellipse(ctx, x, y + 105, 26, 9)
    ctx.set_source_rgba(*SKIN_SH, 0.8)
    ctx.fill()
    # rib collar
    ctx.new_path()
    ctx.move_to(282, 412)
    ctx.curve_to(300, 432, 360, 432, 378, 412)
    ctx.curve_to(368, 404, 360, 410, 356, 414)
    ctx.curve_to(340, 426, 320, 426, 304, 414)
    ctx.curve_to(298, 410, 290, 404, 282, 412)
    ctx.close_path()
    fill_stroke(ctx, SWEATER, 2.5)


def mouth_state(f):
    if f < 14:
        return "smile"
    if f < 36:
        return "smirk"
    if f < 40:
        return "o"
    if f < 52:
        return "oo"
    if f < 61:
        return "wide"
    if f < 65:
        return "chew"
    if f < 67:
        return "wide"
    if f < 86:
        return "chew"
    return "grin"


def eye_mode(f):
    if 4 <= f < 7 or 108 <= f < 111:
        return "blink"
    if 61 <= f < 63 or 67 <= f < 88:
        return "happy"
    if 96 <= f < 104:
        return "wink"
    return "open"


def draw_face(ctx, f, look):
    hc = head_center(f)
    x, y = hc
    m = mouth_state(f)
    cheeks = m == "chew"
    chew_ph = math.sin((f - 61) * 1.15)

    # face + chipmunk cheeks (union outline trick)
    shapes = [("e", x, y, 96, 102)]
    if cheeks:
        puff = 26 + 3 * chew_ph
        shapes += [("c", x - 66, y + 56, puff, puff), ("c", x + 66, y + 56, puff, puff)]
    for _, cx, cy, rx, ry in shapes:
        ellipse(ctx, cx, cy, rx, ry)
        ctx.set_line_width(6)
        ctx.set_source_rgb(*OL)
        ctx.stroke()
    for _, cx, cy, rx, ry in shapes:
        ellipse(ctx, cx, cy, rx, ry)
        g = cairo.RadialGradient(x - 20, y - 20, 10, x, y + 20, 120)
        g.add_color_stop_rgb(0, 1.0, 0.86, 0.74)
        g.add_color_stop_rgb(1, *SKIN)
        ctx.set_source(g)
        ctx.fill()

    # blush
    bl = 0.55 if (cheeks or m in ("grin", "smirk")) else 0.38
    for s in (-1, 1):
        ellipse(ctx, x + s * 60, y + 46, 19, 10)
        ctx.set_source_rgba(1.0, 0.48, 0.50, bl)
        ctx.fill()
        for k in range(3):
            thick_line(ctx, (x + s * 60 - 10 + k * 8, y + 48), (x + s * 60 - 6 + k * 8, y + 42), 1.5,
                       (0.85, 0.30, 0.32, bl))

    # eyes
    mode = eye_mode(f)
    brow_raise = {"smirk": (2, 10)}.get(m, (0, 0))
    if m in ("oo", "wide"):
        brow_raise = (7, 7)
    for i, s in enumerate((-1, 1)):
        ex, ey = x + s * 40, y + 8
        this_mode = mode
        if mode == "wink":
            this_mode = "happy" if s == 1 else "open"
        if this_mode in ("happy", "blink"):
            ctx.new_path()
            if this_mode == "happy":
                ctx.move_to(ex - 18, ey + 6)
                ctx.curve_to(ex - 8, ey - 14, ex + 8, ey - 14, ex + 18, ey + 6)
            else:
                ctx.move_to(ex - 19, ey + 2)
                ctx.curve_to(ex - 8, ey + 10, ex + 8, ey + 10, ex + 19, ey + 2)
            ctx.set_line_width(5)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgb(*OL)
            ctx.stroke()
            thick_line(ctx, (ex + s * 18, ey + 3), (ex + s * 25, ey - 3), 3, OL)
        else:
            ellipse(ctx, ex, ey, 21, 25)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill_preserve()
            ctx.save()
            ctx.clip()
            lx, ly = look
            ix, iy = ex + lx * 6, ey + ly * 6 + 2
            ig = cairo.RadialGradient(ix, iy + 6, 2, ix, iy, 17)
            ig.add_color_stop_rgb(0, 0.55, 0.33, 0.20)
            ig.add_color_stop_rgb(1, 0.18, 0.09, 0.05)
            ctx.arc(ix, iy, 17, 0, 2 * math.pi)
            ctx.set_source(ig)
            ctx.fill()
            ctx.arc(ix, iy, 8, 0, 2 * math.pi)
            ctx.set_source_rgb(0.05, 0.02, 0.02)
            ctx.fill()
            ctx.arc(ix + 6, iy - 7, 6, 0, 2 * math.pi)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill()
            ctx.arc(ix - 6, iy + 7, 3, 0, 2 * math.pi)
            ctx.fill()
            ctx.restore()
            # lid + lashes
            ctx.new_path()
            ctx.save()
            ctx.translate(ex, ey)
            ctx.scale(22, 26)
            ctx.arc(0, 0, 1, d2r(195), d2r(345))
            ctx.restore()
            ctx.set_line_width(5.5)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgb(*OL)
            ctx.stroke()
            ox = ex + s * 21
            thick_line(ctx, (ox, ey - 8), (ox + s * 9, ey - 15), 3.2, OL)
            thick_line(ctx, (ox - s * 3, ey - 15), (ox + s * 4, ey - 23), 3.2, OL)
            ctx.new_path()
            ctx.save()
            ctx.translate(ex, ey)
            ctx.scale(19, 24)
            ctx.arc(0, 0, 1, d2r(30), d2r(150))
            ctx.restore()
            ctx.set_line_width(1.5)
            ctx.set_source_rgba(*OL, 0.5)
            ctx.stroke()
        # bold brows (her signature)
        r = brow_raise[i]
        bx0, bx1 = ex - s * 20, ex + s * 26
        by = ey - 40 - r
        ctx.new_path()
        ctx.move_to(bx0, by + 1)
        ctx.curve_to(ex - s * 4, by - 10, ex + s * 14, by - 11, bx1, by + 5)
        ctx.curve_to(ex + s * 14, by - 3, ex - s * 4, by - 3, bx0, by + 8)
        ctx.close_path()
        ctx.set_source_rgb(0.10, 0.06, 0.05)
        ctx.fill_preserve()
        ctx.set_line_width(2.5)
        ctx.stroke()

    # nose
    ctx.new_path()
    ctx.move_to(x - 4, y + 38)
    ctx.curve_to(x - 1, y + 43, x + 4, y + 43, x + 6, y + 39)
    ctx.set_line_width(2.5)
    ctx.set_source_rgba(*OL, 0.7)
    ctx.stroke()

    # mouth
    mx, my = x, y + 62
    lip = (0.80, 0.33, 0.36)
    ctx.new_path()
    if m == "smile":
        ctx.move_to(mx - 16, my - 2)
        ctx.curve_to(mx - 8, my + 9, mx + 8, my + 9, mx + 16, my - 2)
        ctx.set_line_width(3.5)
        ctx.set_source_rgb(*OL)
        ctx.stroke()
    elif m == "smirk":
        ctx.move_to(mx - 14, my + 2)
        ctx.curve_to(mx - 4, my + 8, mx + 10, my + 6, mx + 18, my - 6)
        ctx.set_line_width(3.5)
        ctx.set_source_rgb(*OL)
        ctx.stroke()
    elif m in ("o", "oo", "wide"):
        rx, ry = {"o": (7, 8), "oo": (11, 13), "wide": (20, 22)}[m]
        ellipse(ctx, mx, my + 4, rx, ry)
        fill_stroke(ctx, (0.45, 0.10, 0.14), 3)
        ellipse(ctx, mx, my + 4 + ry * 0.5, rx * 0.7, ry * 0.4)
        ctx.set_source_rgb(0.95, 0.45, 0.50)
        ctx.fill()
        if m == "wide":
            ctx.rectangle(mx - 10, my - 17, 20, 6)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill()
    elif m == "chew":
        w = 10 + 2 * chew_ph
        ctx.move_to(mx - w, my + 4)
        ctx.curve_to(mx - w / 2, my - 3 + 2 * chew_ph, mx + w / 2, my + 9 - 2 * chew_ph, mx + w, my + 3)
        ctx.set_line_width(4)
        ctx.set_source_rgb(*OL)
        ctx.stroke()
        # crumbs on the lip
        for cx, cy in ((mx + 14, my + 8), (mx - 12, my + 12)):
            ctx.arc(cx, cy, 2, 0, 2 * math.pi)
            ctx.set_source_rgb(0.92, 0.66, 0.28)
            ctx.fill()
    elif m == "grin":
        ctx.move_to(mx - 20, my - 3)
        ctx.curve_to(mx - 12, my + 22, mx + 12, my + 22, mx + 20, my - 3)
        ctx.close_path()
        fill_stroke(ctx, (0.45, 0.10, 0.14), 3)
        ctx.rectangle(mx - 14, my - 2, 28, 5)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()
        ellipse(ctx, mx, my + 11, 8, 4)
        ctx.set_source_rgb(0.95, 0.45, 0.50)
        ctx.fill()
    _ = lip


def draw_front_hair(ctx, f):
    x, y = head_center(f)
    sway = 2.5 * math.sin(2 * math.pi * f / FR * 4 + 0.6)
    # top cap with a soft side part
    ctx.new_path()
    ctx.move_to(x - 102, y + 30)
    ctx.curve_to(x - 118, y - 70, x - 60, y - 124, x + 4, y - 122)
    ctx.curve_to(x + 76, y - 120, x + 120, y - 66, x + 102, y + 30)
    ctx.curve_to(x + 96, y - 14, x + 78, y - 48, x + 40, y - 66)
    ctx.curve_to(x + 20, y - 74, x - 2, y - 80, x - 16, y - 82)
    ctx.curve_to(x - 26, y - 66, x - 58, y - 50, x - 82, y - 22)
    ctx.curve_to(x - 92, y - 8, x - 98, y + 10, x - 102, y + 30)
    ctx.close_path()
    fill_stroke(ctx, HAIR)
    # anime shine ring
    ctx.new_path()
    ctx.arc(x - 6, y - 10, 104, d2r(222), d2r(262))
    ctx.set_line_width(7)
    ctx.set_source_rgba(*HAIR_HI, 0.9)
    ctx.stroke()
    ctx.arc(x - 6, y - 10, 104, d2r(272), d2r(300))
    ctx.stroke()
    # part line
    ctx.move_to(x - 16, y - 82)
    ctx.curve_to(x - 12, y - 100, x - 8, y - 112, x - 2, y - 120)
    ctx.set_line_width(2)
    ctx.set_source_rgba(*HAIR_HI, 0.9)
    ctx.stroke()

    # long side locks falling over the shoulders
    for s in (-1, 1):
        ctx.new_path()
        ctx.move_to(x + s * 100, y - 20)
        ctx.curve_to(x + s * 122, y + 60, x + s * 104 + sway, y + 140, x + s * 126 + sway, y + 210)
        ctx.curve_to(x + s * 132 + sway, y + 236, x + s * 112 + sway, y + 252, x + s * 96 + sway, y + 236)
        ctx.curve_to(x + s * 104 + sway, y + 210, x + s * 84 + sway, y + 150, x + s * 90, y + 92)
        ctx.curve_to(x + s * 94, y + 50, x + s * 92, y + 10, x + s * 86, y - 20)
        ctx.close_path()
        fill_stroke(ctx, HAIR)
        ctx.move_to(x + s * 104, y + 20)
        ctx.curve_to(x + s * 112, y + 90, x + s * 100 + sway, y + 150, x + s * 114 + sway, y + 214)
        ctx.set_line_width(2)
        ctx.set_source_rgba(*HAIR_HI, 0.8)
        ctx.stroke()


def draw_fork_and_hand(ctx, f):
    h = hand_at(f)
    phi, ln = fork(f)
    u = (math.cos(d2r(phi)), math.sin(d2r(phi)))
    n = (-u[1], u[0])
    tip = (h[0] + u[0] * ln, h[1] + u[1] * ln)

    # handle grip
    a = (h[0] - u[0] * 18, h[1] - u[1] * 18)
    b = (h[0] + u[0] * 26, h[1] + u[1] * 26)
    thick_line(ctx, a, b, 16, OL)
    thick_line(ctx, a, b, 11, (0.25, 0.25, 0.30))

    # telescoping rod sections
    rod0 = b
    rod1 = (tip[0] - u[0] * 30, tip[1] - u[1] * 30)
    lr = max(1.0, math.hypot(rod1[0] - rod0[0], rod1[1] - rod0[1]))
    nsec = 5
    for i in range(nsec):
        w = 11 - 1.4 * i
        p0 = (rod0[0] + u[0] * lr * i / nsec, rod0[1] + u[1] * lr * i / nsec)
        p1 = (rod0[0] + u[0] * lr * (i + 1) / nsec, rod0[1] + u[1] * lr * (i + 1) / nsec)
        thick_line(ctx, p0, p1, w + 4, OL, cairo.LINE_CAP_BUTT)
        thick_line(ctx, p0, p1, w, (0.78, 0.81, 0.86), cairo.LINE_CAP_BUTT)
        o = -w * 0.22
        thick_line(ctx, (p0[0] + n[0] * o, p0[1] + n[1] * o), (p1[0] + n[0] * o, p1[1] + n[1] * o),
                   max(1.5, w * 0.3), (1, 1, 1, 0.85), cairo.LINE_CAP_BUTT)
    for i in range(1, nsec):
        w = 11 - 1.4 * (i - 1)
        c = (rod0[0] + u[0] * lr * i / nsec, rod0[1] + u[1] * lr * i / nsec)
        e = (c[0] + u[0] * 4, c[1] + u[1] * 4)
        thick_line(ctx, c, e, w + 6, OL, cairo.LINE_CAP_BUTT)
        thick_line(ctx, c, e, w + 2, (0.55, 0.58, 0.64), cairo.LINE_CAP_BUTT)

    # fork head (local coordinates)
    ctx.save()
    ctx.translate(*tip)
    ctx.rotate(d2r(phi))
    ctx.new_path()
    ctx.move_to(-31, -3)
    ctx.curve_to(-22, -3, -20, -11, -16, -11)
    ctx.line_to(-16, 11)
    ctx.curve_to(-20, 11, -22, 3, -31, 3)
    ctx.close_path()
    fill_stroke(ctx, (0.80, 0.83, 0.88), 2.5)
    for ty in (-9, -3, 3, 9):
        thick_line(ctx, (-17, ty), (0, ty * 1.05), 6.5, OL)
    for ty in (-9, -3, 3, 9):
        thick_line(ctx, (-17, ty), (0, ty * 1.05), 3.2, (0.86, 0.88, 0.92))
    ctx.restore()

    # fist over the handle
    ctx.arc(h[0], h[1], 20, 0, 2 * math.pi)
    fill_stroke(ctx, SKIN)
    for k in (-1, 0, 1):
        p = (h[0] + n[0] * 9 + u[0] * k * 8, h[1] + n[1] * 9 + u[1] * k * 8)
        ctx.arc(p[0], p[1], 6, 0, 2 * math.pi)
        fill_stroke(ctx, SKIN, 2)
    ellipse(ctx, h[0] - n[0] * 8 + u[0] * 6, h[1] - n[1] * 8 + u[1] * 6, 8, 6)
    fill_stroke(ctx, SKIN, 2)
    return tip, u


def look_vector(f, hc):
    eye = (hc[0], hc[1] + 8)
    if f < 14:
        target = (hc[0] + 60, hc[1] + 200)   # glance at the puffs
        if f < 8:
            return (0.15, 0.3)
    elif f < 61:
        target = puff_on_fork(f) or PUFF_TARGET
    else:
        return (0.15, 0.25)
    dx, dy = target[0] - eye[0], target[1] - eye[1]
    d = math.hypot(dx, dy) or 1
    return (dx / d, dy / d)


# ---------------------------------------------------------------- effects
def draw_fx(ctx, f, tip):
    # telescope clicks
    for k, fc in enumerate((22, 26, 30, 34)):
        a = seg(f, fc, fc + 5)
        if 0 < a < 1:
            sparkle(ctx, tip[0] + 6, tip[1] - 16, 9 * (1 - a) + 3, 1 - a)
    if 20 <= f < 37:
        a = seg(f, 20, 23) * (1 - seg(f, 33, 37))
        comic_text(ctx, "click click!", 250, 560 - 6 * math.sin(f), 26, -0.12, (1, 0.93, 0.55), a)
    # stab impact
    if 36 <= f < 42:
        a = 1 - seg(f, 36, 42)
        for k in range(6):
            ang = k * math.pi / 3 + 0.3
            r0, r1 = 36 + 10 * (1 - a), 50 + 14 * (1 - a)
            thick_line(ctx, (PUFF_TARGET[0] + r0 * math.cos(ang), PUFF_TARGET[1] + r0 * math.sin(ang)),
                       (PUFF_TARGET[0] + r1 * math.cos(ang), PUFF_TARGET[1] + r1 * math.sin(ang)),
                       3.5, (1, 0.95, 0.7, a))
    # swing speed lines
    if 41 <= f < 55:
        p, q = puff_on_fork(f), puff_on_fork(f - 2)
        if p and q:
            dx, dy = p[0] - q[0], p[1] - q[1]
            d = math.hypot(dx, dy) or 1
            ux, uy = dx / d, dy / d
            for k in (-1, 0, 1):
                ox, oy = -uy * k * 18, ux * k * 18
                a0 = (p[0] - ux * 44 + ox, p[1] - uy * 44 + oy)
                a1 = (p[0] - ux * (44 + 30 + 12 * (k == 0)) + ox, p[1] - uy * (44 + 30 + 12 * (k == 0)) + oy)
                thick_line(ctx, a0, a1, 4, (1, 1, 1, 0.8))
    # chomp
    for fc in (61, 67):
        a = seg(f, fc, fc + 5)
        if 0 < a < 1:
            hc = head_center(f)
            comic_text(ctx, "NOM!", hc[0] + 118, hc[1] + 30 - 20 * a, 30, 0.2, (1, 1, 1), 1 - a * a)
            for k in range(6):
                ang = k * 1.1 + fc
                cx = hc[0] - 10 + 50 * a * math.cos(ang)
                cy = hc[1] + 70 + 40 * a * math.sin(ang) + 30 * a * a
                ctx.arc(cx, cy, 3, 0, 2 * math.pi)
                ctx.set_source_rgba(0.93, 0.68, 0.30, 1 - a)
                ctx.fill()
    # mmm + hearts
    if 70 <= f < 100:
        hc = head_center(f)
        a = seg(f, 70, 74) * (1 - seg(f, 94, 100))
        sc = 1 + 0.08 * math.sin(f * 0.8)
        comic_text(ctx, "mmm~", hc[0] + 112, hc[1] - 112, 34 * sc, 0.18, (1, 0.72, 0.78), a)
    for k, (start, ox) in enumerate(((68, -120), (72, 130), (76, -95), (80, 105), (84, -140))):
        t = seg(f, start, start + 20)
        if 0 < t < 1:
            hc = head_center(f)
            hx = hc[0] + ox + 10 * math.sin(t * 7 + k)
            hy = hc[1] - 20 - 150 * t
            heart(ctx, hx, hy, 1.4 + 0.4 * math.sin(t * 10), (1.0, 0.36, 0.48), (1 - t) * min(1, t * 5))
    # refill sparkle for the loop
    if f < 10:
        a = 1 - seg(f, 0, 10)
        sparkle(ctx, PUFF_TARGET[0] + 30, PUFF_TARGET[1] - 30, 12 * a + 2, a)
        sparkle(ctx, PUFF_TARGET[0] - 34, PUFF_TARGET[1] - 10, 8 * a + 2, a)


# ---------------------------------------------------------------- frame
def render(f, path):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    hc = head_center(f)

    draw_background(ctx)
    draw_back_hair(ctx, hc)
    draw_body(ctx, f)
    # the other taped arm, sticking out stiff
    wob = 3 * math.sin(2 * math.pi * f / FR * 3)
    a2 = d2r(52 + wob)
    taped_arm(ctx, S2, (S2[0] + ARM * math.cos(a2), S2[1] + ARM * math.sin(a2)))
    ctx.arc(S2[0] - 4, S2[1] - 2, 30, 0, 2 * math.pi)
    fill_stroke(ctx, SWEATER, 0)
    draw_neck_collar(ctx, hc)
    draw_face(ctx, f, look_vector(f, hc))
    draw_front_hair(ctx, f)

    draw_counter(ctx)
    draw_dish_back(ctx)
    for (x, y, r, seed) in sorted(DISH_PUFFS + [(PUFF_TARGET[0], PUFF_TARGET[1], PUFF_R, 3.3)],
                                  key=lambda p: p[1]):
        if (x, y) == PUFF_TARGET:
            if f >= 36:
                continue
            scale = ease_out_back(seg(f, 0, 8), 2.2)
            draw_puff(ctx, x, y, r, seed, scale)
        else:
            draw_puff(ctx, x, y, r, seed)
    draw_dish_front(ctx)

    # fork arm on top of everything
    h = hand_at(f)
    taped_arm(ctx, S, h)
    ctx.arc(S[0] + 4, S[1] - 2, 30, 0, 2 * math.pi)
    ctx.set_source_rgb(*SWEATER)
    ctx.fill()
    tip, u = draw_fork_and_hand(ctx, f)

    p = puff_on_fork(f)
    if p:
        bite = 1 if f >= 61 else 0
        squash = 1 - 0.12 * math.sin(math.pi * seg(f, 36, 40))
        mouth_dir = math.atan2(head_center(f)[1] + 62 - p[1], head_center(f)[0] - p[0])
        draw_puff(ctx, p[0], p[1], PUFF_R, 3.3, 1.0, bite, mouth_dir, squash)

    draw_fx(ctx, f, tip)
    surf.write_to_png(path)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    frames = os.path.join(out, "frames")
    os.makedirs(frames, exist_ok=True)
    for f in range(FR):
        render(f, os.path.join(frames, f"f{f:03d}.png"))
    gif = os.path.join(out, "long_fork_girl.gif")
    mp4 = os.path.join(out, "long_fork_girl.mp4")
    pattern = os.path.join(frames, "f%03d.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", pattern,
                    "-vf", "split[a][b];[a]palettegen=max_colors=200:stats_mode=full[p];"
                           "[b][p]paletteuse=dither=bayer:bayer_scale=4",
                    "-loop", "0", gif], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "2", "-framerate", str(FPS),
                    "-i", pattern, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", mp4], check=True)
    print(gif, os.path.getsize(gif) // 1024, "KB")


if __name__ == "__main__":
    main()
