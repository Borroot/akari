from PIL import Image, ImageDraw, ImageFont

from constants import *


_MAGNIFIER = 800
_LINEWIDTH = _MAGNIFIER // 20


def _draw_background(draw):
    draw.rectangle((0, 0) + draw.im.size, fill='black')


def _draw_rectangle(draw, x, y, rectcolor, text=None, textcolor=None):
    top = (x * _MAGNIFIER + _LINEWIDTH, y * _MAGNIFIER + _LINEWIDTH)
    size = ((x + 1) * _MAGNIFIER, (y + 1) * _MAGNIFIER)
    draw.rectangle(top + size, fill=rectcolor)

    if text is not None:
        middle = ((top[0] + size[0]) // 2 - _MAGNIFIER // 5, top[1])
        font = ImageFont.truetype('res/font/verdana.ttf', int(_MAGNIFIER * 0.7))
        draw.text(middle, text, font=font, fill=textcolor, align='center')


def _draw_cells(draw, width, height):
    for x in range(width):
        for y in range(height):
            _draw_rectangle(draw, x, y, 'white')


def _draw_walls(draw, width, height, puzzle):
    for x in range(width):
        for y in range(height):
            if puzzle[y][x] != N:
                text = None if puzzle[y][x] == B else str(puzzle[y][x])
                _draw_rectangle(draw, x, y, 'black', text, 'white')


def draw(puzzle, filename):
    width, height = len(puzzle[0]), len(puzzle)

    size = (width * _MAGNIFIER + _LINEWIDTH, height * _MAGNIFIER + _LINEWIDTH)
    im = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)

    _draw_background(draw)
    _draw_cells(draw, width, height)
    _draw_walls(draw, width, height, puzzle)

    im.save(filename + ".png", "PNG")
