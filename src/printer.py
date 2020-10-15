from constants import *


def display(puzzle, solution=None):
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
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
