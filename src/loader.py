from constant import *


def loadpuzzle(filename, index, height, width):
    codex = _loadcodex(filename, index)
    return _convert(codex, height, width)


def _loadcodex(filename, index):
    with open(filename) as fp:
        for i, line in enumerate(fp):
            if i == index:
                return line


def _convert(codex, height, width):
    puzzle = [list(range(width)) for _ in range(height)]

    count = 0
    for c in codex:
        if c == 'B':
            puzzle[count // height][count % width] = B
            count += 1
        elif c in '01234':
            puzzle[count // height][count % width] = ord(c) - ord('0')
            count += 1
        else:
            while c >= 'a':
                puzzle[count // height][count % width] = N
                count += 1
                c = chr(ord(c) - 1)

    return puzzle
