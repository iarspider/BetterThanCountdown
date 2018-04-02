# import argparse
# import codecs
# import configparser
import datetime

import sys
from math import floor

from PIL import Image, ImageDraw, ImageFont

import pygame

# canvas_size = (1920, 1080)
purisa = r"c:\Windows\Fonts\OpenSans-Regular.ttf"


def draw_text(d, text, font, align, canvas_size=None, offset=(0, 0), color=(255, 255, 255, 255)):
    def get_xy():
        if align[0] == "left":
            xpos = 0
        elif align[0] == "right":
            if canvas_size is None:
                raise RuntimeError("Need canvas_size for align=right!")
            xpos = canvas_size[0] - text_size[0]
        elif align[0] == "center":
            if canvas_size is None:
                raise RuntimeError("Need canvas_size for align=center!")
            xpos = (canvas_size[0] - text_size[0]) / 2
        else:
            raise RuntimeError("Invalid pos_x value {0}".format(align[0]))

        if align[1] == "top":
            ypos = 0
        elif align[1] == "bottom":
            if canvas_size is None:
                raise RuntimeError("Need canvas_size for align=bottom!")

            ypos = canvas_size[1] - text_size[1]
        elif align[1] == "center":
            if canvas_size is None:
                raise RuntimeError("Need canvas_size for align=center!")

            ypos = (canvas_size[1] - text_size[1]) / 2
        else:
            raise RuntimeError("Invalid pos_y value {0}".format(align[1]))

        return xpos + offset[0], ypos + offset[1]

    text_size = d.textsize(text, font=font)
    x, y = get_xy()
    d.text((x, y), text, font=font, fill=color)
    return x, y, text_size[0], text_size[1]


def sec2minsec(s):
    if s <= 0:
        return "--", "--"
    return "{0:02d}:".format(s // 60), "{0:02d}".format(s % 60)


def main(end):
    def draw_img():
        tmp_img = Image.new('RGBA', max_size, (0, 0x7f, 0, 0))
        tmp_d = ImageDraw.Draw(tmp_img)
        now = sec2minsec(s)
        nxt = sec2minsec(s - 1)

        if nxt[0] == '--' or nxt[1] == '--':
            draw_text(tmp_d, "Стрим начнётся через --:--", font=fnt, align=("left", "top"), offset=(0, 0))
        else:
            z = now[0]
            x, y, w, h = draw_text(tmp_d, 'Стрим начнётся через ' + z, font=fnt, align=("left", "top"), offset=(0, 0))

            y_now = floor(y + h * (frame / fps))
            y_nxt = floor(y_now - tmp_d.textsize("{0}".format(nxt[1]), font=fnt)[1])

            # print("Frame {0}/{1}: main label at ({2}, {3}), now at ({4}, {5}), next at ({6}, {7})".format(
            #    frame, fps, x, y, w, y_now, w, y_nxt-1
            # ))

            draw_text(tmp_d, nxt[1], fnt, align=("left", "top"), offset=(w, y_nxt - 10))
            draw_text(tmp_d, now[1], fnt, align=("left", "top"), offset=(w, y_now))

        canvas.paste(tmp_img, (0, 0, *max_size))

    CHROMAGREEN = 0, 255, 0

    fps = 25
    if end > datetime.datetime.now():
        s = (end - datetime.datetime.now()).seconds
    else:
        return

    frame = 0

    fnt = ImageFont.truetype(purisa, 100)

    canvas = Image.new('RGBA', (1920, 1080), (0, 64, 0, 0))
    d = ImageDraw.Draw(canvas)

    max_size = d.textsize("Стрим начнётся через 000:00", font=fnt)
    # max_pos = tuple(int(x) for x in get_xy(canvas_size, max_size, "center", "center", 0, 0))
    # max_xy = (max_pos[0], max_pos[1], max_pos[0] + max_size[0], max_pos[1] + max_size[1])
    # print("max_pos", max_pos)

    pygame.init()
    screen = pygame.display.set_mode(max_size)
    pygame.display.set_caption("Clock")

    clock = pygame.time.Clock()
    while 1:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(CHROMAGREEN)
        draw_img()

        mode = canvas.mode
        size = canvas.size
        data = canvas.tobytes()

        this_image = pygame.image.fromstring(data, size, mode)
        screen.blit(this_image, (0, 0))
        frame += 1
        if frame == fps:
            frame = 0

            if end > datetime.datetime.now():
                s = (end - datetime.datetime.now()).seconds
            else:
                s = 0

        pygame.display.flip()

def countdown_time(h, m = 0, s = 0):
    dnow = datetime.datetime.now()
    dend = datetime.datetime(dnow.year, dnow.month, dnow.day, h, m, s)
    main(dend)

def countdown_interval(m, s = 0):
    dnow = datetime.datetime.now()
    dend = dnow + datetime.timedelta(seconds=m*60+s)
    main(dend)

if __name__ == "__main__":
    # countdown_interval(15)
    countdown_time(20, 0)
