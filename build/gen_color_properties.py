from contextlib import closing
import colorsys

import hsluv
from dbconn import DbConnect

HARDCODED_ORDER = ["[Unknown]", "[No Color/Any Color]", "Glow in Dark White", "White", "Black"]
GRAY_THRESHOLD = 20 / 255.0

UNKNOWN_COLOR_ID = -1
ANY_COLOR_ID = 9999


class Color:
    def __init__(self, id, name, rgb):
        self.id = id
        self.name = name
        self.r, self.g, self.b = [int(rgb[x: x + 2], 16) / 255.0 for x in [0, 2, 4]]

        if id in (UNKNOWN_COLOR_ID, ANY_COLOR_ID):
            self.lightness = None
        else:
            self.lightness = hsluv.rgb_to_hsluv((self.r, self.g, self.b))[2] / 100
        self.gray_diff = max(abs(self.r - self.g), abs(self.r - self.b), abs(self.g - self.b))

    def is_grayscale(self):
        if self.name == HARDCODED_ORDER[0] or self.name == HARDCODED_ORDER[1]:
            return None
        return self.gray_diff < GRAY_THRESHOLD


def color_sort_key(color):
    if color.name in HARDCODED_ORDER:
        return (1, HARDCODED_ORDER.index(color.name))

    h, s, v = colorsys.rgb_to_hsv(color.r, color.g, color.b)

    if color.is_grayscale():
        return (2, v, s, h)

    return (3, h, s, v)


def gen_color_properties(conn):
    print(":: generating color_properties ...")

    colors = []
    with closing(conn.cursor()) as cur:
        for id, name, rgb in cur.execute('SELECT id, name, rgb FROM colors'):
            colors.append(Color(id, name, rgb))

    sorted_colors = sorted(colors, key=color_sort_key)
    prev_key = None
    with conn, closing(conn.cursor()) as cur:
        pos = 0
        for color in sorted_colors:
            key = color_sort_key(color)
            if key != prev_key:
                pos += 1
                prev_key = key
            cur.execute('INSERT INTO color_properties VALUES (?, ?, ?, ?)',
                        (color.id, pos, color.lightness, color.is_grayscale()))


if __name__ == '__main__':
    with DbConnect() as conn:
        gen_color_properties(conn)
