from constants import *


def loadcodex(filename, index, height, width):
    """ Load the codex formatted puzzle from the specified line in the given file. """
    codex = _loadline(filename, index)
    return _codextopuzzle(codex, height, width)


def loadgrid(filename):
    """ Load the grid formatted puzzle from the given file. """
    grid = _loadlines(filename)
    return _gridtopuzzle(grid)


def writecodex(filename, puzzle):
    with open(filename, 'a') as fp:
        fp.write(_puzzletocodex(puzzle) + '\n')


def writegrid(filename, puzzle):
    pass


def _loadline(filename, index):
    """ Load the line with the given index from the file. """
    with open(filename) as fp:
        for i, line in enumerate(fp):
            if i == index:
                return line.rstrip()


def _loadlines(filename):
    """ Load all the lines in the file according to the grid format. """
    with open(filename) as fp:
        return [line.strip() for line in fp.readlines()]


def _codextopuzzle(codex, height, width):
    """ Create a puzzle from the given codex. """
    puzzle = [[N for _ in range(width)] for _ in range(height)]
    count = 0
    for c in codex:
        if c == 'B':
            puzzle[count // width][count % width] = B
            count += 1
        elif c in '01234':
            puzzle[count // width][count % width] = ord(c) - ord('0')
            count += 1
        else:
            while c >= 'a':
                puzzle[count // width][count % width] = N
                count += 1
                c = chr(ord(c) - 1)

    return puzzle


def _puzzletocodex(puzzle):
    """ Create a codex from the given puzzle. """
    builder = ''
    count = -1
    for row in puzzle:
        for cell in row:
            if cell == N:
                if count == 25:
                    builder += chr(ord('a') + count)
                    count = 0
                else:
                    count += 1
            else:
                if count >= 0:
                    builder += chr(ord('a') + count)
                    count = -1

                if cell == B:
                    builder += 'B'
                else:
                    builder += str(cell)

    if count >= 0:
        builder += chr(ord('a') + count)

    return builder


def _gridtopuzzle(grid):
    """ Create a puzzle from the given grid formatted string. """
    width = len(grid[0])
    puzzle = [list(range(width)) for _ in range(len(grid))]

    count = 0
    for line in grid:
        for c in line:
            if c == '*':
                puzzle[count // width][count % width] = B
                count += 1
            elif c in '01234':
                puzzle[count // width][count % width] = ord(c) - ord('0')
                count += 1
            elif c == '-':
                puzzle[count // width][count % width] = N
                count += 1

    return puzzle


def _puzzletogrid(puzzle):
    pass
