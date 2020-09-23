from constant import *


def loadpuzzle(filename, index, height, width):
    codex = _loadline(filename, index)
    return _codextopuzzle(codex, height, width)


def loadhans(filename):
    with open(filename) as fp:
        width = height = int(fp.readline())
        puzzle = [list(range(width)) for _ in range(height)]

        count = 0
        for _ in range(height):
            for c in fp.readline():
                if c == '*':
                    puzzle[count // height][count % width] = B
                    count += 1
                elif c in '01234':
                    puzzle[count // height][count % width] = ord(c) - ord('0')
                    count += 1
                elif c == '-':
                    puzzle[count // height][count % width] = N
                    count += 1

        return puzzle


def writecodex(filename, puzzle):
    with open(filename, 'a') as fp:
        fp.write(_puzzletocodex(puzzle) + '\n')


def writehans(filename, puzzle):
    pass


def _loadline(filename, index):
    with open(filename) as fp:
        for i, line in enumerate(fp):
            if i == index:
                return line.rstrip()


def _codextopuzzle(codex, height, width):
    puzzle = [[N for _ in range(width)] for _ in range(height)]

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


def _puzzletocodex(puzzle):
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


def _puzzletohans(puzzle):
    pass
