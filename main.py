import svgpathtools as svg
import pygame as pg
import math
from typing import Callable
from tkinter import filedialog
import tkinter
from numpy import clip


root = tkinter.Tk()
root.withdraw()

def Main(filename):
    OFFSET_CIRCLES = False

    FOCUS = False
    CIRCLES = True
    GAMING = False

    w, h = 1000, 1000
    win = pg.display.set_mode((w, h))
    samples = 1000
    step = 1

    offset = w//2+ h//2 *1j
    zoom = 1

    paths, attributes = svg.svg2paths(filename)

    def Pt(c): return [c.real, c.imag]

    def Exp(t):
        # e ^ it
        #return cmath.exp(1j * t)

        # cos t + isin t
        return math.cos(t) + 1j * math.sin(t)

    def frange(start, end, step):
        p = start
        while abs(p) < abs(end):
            yield p
            p += step


    def generate_circle(n) -> Callable[[float], complex]:
        c = get_c(n)
        return lambda t: c * Exp(2 * math.pi * t * n)

    def get_c(n):
        sum = 0 + 0j
        path = paths[0]
        # for path in paths:
        for t in frange(0, 1, 0.001):
            sum += path.point(t) * Exp(-2 * math.pi * n * t)

        #return sum / (le n(paths) * 1000) * scale
        return (sum / 1000)

    circles = []

    def GenerateSamples():
        for i in range(0, samples // 2):
            circles.append(generate_circle(i * step))
            if (i == 0):
                continue
            circles.append(generate_circle(-i * step))

    GenerateSamples()




    def DrawCircles():
        lasto = circles[0](0) if OFFSET_CIRCLES else 0
        for o in circles[1:]:
            origin = lasto if lasto is not None else 0+0j
            c = o(t)
            lasto = c + origin
            pg.draw.circle(win, (255,0,0), Pt(origin * zoom + offset), abs(c * zoom), 1)
            pg.draw.line(win, (255,0,0), Pt(origin * zoom + offset), Pt((origin + c) * zoom + offset))

    def lerp(a, b, t):
        return (1 - t) * a + (t * b)

    def gradient(c):
        return math.sqrt(1-(c-1)**2)

    def tint(c):

        def channel(angle):
            return max(math.sqrt(abs(math.sin(v + angle))) * c, 255 * 0.4)

        gaming_speed = 1000 * speed * 2 * math.pi * 6
        v = t * gaming_speed
        r = channel(0)
        g = channel(math.pi / 2)
        # b = round(math.sqrt(abs(math.sin(v + math.pi / 2))) * c)
        b = 128
        # g = 1
        return (r, g, b)

    history = []
    def DrawPt():
        nonlocal offset
        s = 0
        for oi in range(len(circles)):
            if not OFFSET_CIRCLES and oi == 0: continue
            o = circles[oi]
            s += o(t)
        history.append(s)

        length = len(history)
        for pi in range(len(history)):
            p = history[pi]
            color = (pi + 1) / length if t > 1 else clip(lerp((1 - (length / (1 / speed))), 1, (pi + 1) / length), 0, 1)
            color = round(gradient(color) * 255)
            color = tint(color) if GAMING else (color, color, color)
            # pg.draw.rect(win, color, [p.real * zoom + offset.real, p.imag * zoom + offset.imag, 1, 1])
            if pi > 0:
                prev = history[pi - 1]
                pg.draw.line(win, color, [p.real * zoom + offset.real, p.imag * zoom + offset.imag], [prev.real * zoom + offset.real, prev.imag * zoom + offset.imag])

        if t > 1: history.pop(0)

        if FOCUS: offset = w // 2 + h // 2 * 1j - s * zoom

    def Draw():
        if CIRCLES:
            DrawCircles()
        DrawPt()

    def Zoom(amount=1):
        nonlocal zoom
        nonlocal offset

        if zoom + amount < 1:
            return

        oldzoom = zoom
        zoom += amount

        pos = pg.mouse.get_pos()

        # i have no clue why this works but it does
        # https://stackoverflow.com/questions/57556219/calculating-offset-and-zoom-in-a-graph-after-a-mouse-wheel-scroll

        newOffset_x = offset.real + (1 - (zoom / oldzoom)) * (pos[0] - offset.real)
        newOffset_y = offset.imag + (1 - (zoom / oldzoom)) * (pos[1] - offset.imag)

        offset = newOffset_x + newOffset_y*1j

    vel = 0+0j
    pivot = 0+0j
    last_pressed = False
    def Movement():
        nonlocal last_pressed
        nonlocal pivot
        nonlocal offset
        nonlocal vel

        is_pressed = pg.mouse.get_pressed(3)[0]
        pos = pg.mouse.get_pos()
        pos = pos[0] + pos[1] * 1j

        if is_pressed and not last_pressed:
            pivot = pos

        elif is_pressed:
            vel = pos - pivot
            offset += vel
            pivot = pos

        last_pressed = is_pressed

    t = 0
    speed = 0.001
    speed_sensitivity = 1.15
    update = True
    zoom_amount = 0.25
    fps = 30
    clock = pg.time.Clock()
    while update:
        clock.tick(fps)
        win.fill((0,0,0))
        update = not pg.event.get(pg.QUIT)

        Movement()

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button in [4, 5]:
                    Zoom(((event.button - 4) * -2 + 1) * zoom_amount)
                    zoom_amount += ((event.button - 4) * -2 + 1) * 0.05

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    speed *= speed_sensitivity

                if event.key == pg.K_g:
                    GAMING = not GAMING

                if event.key == pg.K_DOWN:
                    speed /= speed_sensitivity

                if event.key == pg.K_e:
                    FOCUS = not FOCUS

                if event.key == pg.K_q:
                    CIRCLES = not CIRCLES

                if event.key == pg.K_n:
                    return True

        #offset += 0.05
        #zoom += 0.005
        t += speed
        Draw()
        pg.display.update()

    return False

filename = filedialog.askopenfilename(initialdir="./svg/")
while Main(filename):
    filename = filedialog.askopenfilename(initialdir="./svg/")
