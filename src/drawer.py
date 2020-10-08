from PIL import Image, ImageDraw, ImageFont

from constants import *


_MAGNIFIER = 500
_LINEWIDTH = _MAGNIFIER // 20


def _draw_box(x, y):
    """ Return the top left coordinates and the bottom right coordinates of the
    requested cell. """
    top = (x * _MAGNIFIER + _LINEWIDTH, y * _MAGNIFIER + _LINEWIDTH)
    bot = ((x + 1) * _MAGNIFIER, (y + 1) * _MAGNIFIER)
    return top, bot


def _draw_background(draw):
    """ Draw a black square for the background. """
    draw.rectangle((0, 0) + draw.im.size, fill='black')


def _draw_text(draw, x, y, text, color):
    """ Draw the given text (number) in the given cell. """
    top, bot = _draw_box(x, y)
    middle = ((top[0] + bot[0]) // 2 - _MAGNIFIER // 5, top[1])
    font = ImageFont.truetype('res/font/verdana.ttf', int(_MAGNIFIER * 0.7))
    draw.text(middle, text, font=font, fill=color)


def _draw_rectangle(draw, x, y, color):
    """ Draw a rectangle with the provided color in the given cell. """
    top, bot = _draw_box(x, y)
    draw.rectangle(top + bot, fill=color)


def _draw_cells(draw, width, height, puzzle):
    """ Draw all the cells on the puzzle. Since we start with a black
    background we do not need to draw the black cells without a number. """
    for x in range(width):
        for y in range(height):
            if puzzle[y][x] != N and puzzle[y][x] != B:
                _draw_text(draw, x, y, str(puzzle[y][x]), 'white')
            elif puzzle[y][x] != B:
                _draw_rectangle(draw, x, y, 'white')


def _draw_bulbs(im, solution):
    """ Draw all the light bulbs from the solution using a sprite. """
    bulb = Image.open('res/sprites/bulb.jpg')
    bulb = bulb.resize((int(_MAGNIFIER * 0.6), int(_MAGNIFIER * 0.6)))

    for x, y in solution:
        top, bot = _draw_box(x, y)
        middle = (top[0] + int(_MAGNIFIER * 0.17), top[1] + int(_MAGNIFIER * 0.2))
        im.paste(bulb, middle)


def _draw_all(im, width, height, puzzle, solution):
    """ Draw the image for the given puzzle with a solution if provided. """
    draw = ImageDraw.Draw(im)

    _draw_background(draw)
    _draw_cells(draw, width, height, puzzle)

    if solution is not None:
        _draw_bulbs(im, solution)


def draw(puzzle, filename, magnifier=None, solution=None):
    """ Draw and save the image corresponding to the puzzle (and solution). """
    if magnifier is not None:
        global _MAGNIFIER
        _MAGNIFIER = magnifier

    width, height = len(puzzle[0]), len(puzzle)
    size = (width * _MAGNIFIER + _LINEWIDTH, height * _MAGNIFIER + _LINEWIDTH)

    im = Image.new("1", size)
    _draw_all(im, width, height, puzzle, solution)
    im.save(filename + ".png")
