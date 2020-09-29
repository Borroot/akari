from PIL import Image, ImageDraw


_MAGNIFIER = 100
_LINEWIDTH = 8
_LINEHALF = _LINEWIDTH // 2


def _draw_background(draw):
    draw.rectangle((0, 0) + draw.im.size, fill=(0, 0, 0))


def _draw_cells(draw, width, height):
    for x in range(width):
        for y in range(height):
            offset = (_LINEWIDTH // 2, _LINEWIDTH // 2)
            top = (x * _MAGNIFIER + _LINEWIDTH + offset[0], y * _MAGNIFIER + _LINEWIDTH + offset[1])
            size = ((x+1) * _MAGNIFIER - _LINEWIDTH + offset[0], (y+1) * _MAGNIFIER - _LINEWIDTH + offset[1])
            draw.rectangle(top + size, fill=(255, 255, 255))


def draw(puzzle, filename):
    width, height = len(puzzle[0]), len(puzzle)

    size = (width * _MAGNIFIER + _LINEWIDTH, height * _MAGNIFIER + _LINEWIDTH)
    im = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)

    _draw_background(draw)
    _draw_cells(draw, width, height)

    im.save(filename + ".png", "PNG")
