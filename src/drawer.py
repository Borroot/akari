from PIL import Image, ImageDraw, ImageFont

from constants import *


_MAGNIFIER = 500
_LINEWIDTH = _MAGNIFIER // 20


def _draw_background(draw):
    draw.rectangle((0, 0) + draw.im.size, fill='black')


def _draw_sizes(x, y):
    top = (x * _MAGNIFIER + _LINEWIDTH, y * _MAGNIFIER + _LINEWIDTH)
    size = ((x + 1) * _MAGNIFIER, (y + 1) * _MAGNIFIER)
    return top, size


def _draw_text(draw, x, y, text, color):
    top, size = _draw_sizes(x, y)
    middle = ((top[0] + size[0]) // 2 - _MAGNIFIER // 5, top[1])
    font = ImageFont.truetype('res/font/verdana.ttf', int(_MAGNIFIER * 0.7))
    draw.text(middle, text, font=font, fill=color)


def _draw_rectangle(draw, x, y, color):
    top, size = _draw_sizes(x, y)
    draw.rectangle(top + size, fill=color)


def _draw_cells(draw, width, height, puzzle):
    for x in range(width):
        for y in range(height):
            if puzzle[y][x] != N and puzzle[y][x] != B:
                _draw_text(draw, x, y, str(puzzle[y][x]), 'white')
            elif puzzle[y][x] != B:
                _draw_rectangle(draw, x, y, 'white')


def _draw_bulbs(im, solution):
    bulb = Image.open('res/sprites/bulb.jpg')
    bulb = bulb.resize((int(_MAGNIFIER * 0.6), int(_MAGNIFIER * 0.6)))

    for x, y in solution:
        top, size = _draw_sizes(x, y)
        middle = (top[0] + int(_MAGNIFIER * 0.17), top[1] + int(_MAGNIFIER * 0.2))
        im.paste(bulb, middle)


def _draw_all(im, width, height, puzzle, solution):
    draw = ImageDraw.Draw(im)

    _draw_background(draw)
    _draw_cells(draw, width, height, puzzle)

    if solution is not None:
        _draw_bulbs(im, solution)


def draw(puzzle, filename, magnifier=None, solution=None):
    if magnifier is not None:
        global _MAGNIFIER
        _MAGNIFIER = magnifier

    width, height = len(puzzle[0]), len(puzzle)
    size = (width * _MAGNIFIER + _LINEWIDTH, height * _MAGNIFIER + _LINEWIDTH)

    im = Image.new("1", size)
    _draw_all(im, width, height, puzzle, solution)
    im.save(filename + ".png")
