from constant import *


def display(puzzle, solution=None):
    for y, row in enumerate(puzzle):
        for x, cell in enumerate(row):
            if solution is not None and (x, y) in solution:
                print('X', end='')
            elif puzzle[y][x] == N:
                print('.', end='')
            elif puzzle[y][x] == B:
                print('B', end='')
            else:
                print(puzzle[y][x], end='')
            print(' ', end='')
        print()
