from z3 import *

from printer import display
from loader import *
from generator import generate, XAXIS, YAXIS, XYAXIS
from z3solver import z3solve, z3solves, z3unique


def main():
    for index in range(100):
        puzzle, solution = generate(30, 30, 100, 2, YAXIS)
        display(puzzle)
        print(index, '\n')
        writecodex('misc/generated/30x30', puzzle)

    # total = 0
    # for index in range(25):
        # puzzle = loadpuzzle('misc/web/25x25_hard', index, 25, 25)
        # solution, time = z3solve(puzzle, True)
        # print(index, time)
        # total += time
    # print('average', total / 25)

    # for i in range(1, 10):
        # puzzle = loadhans('misc/hans/r' + str(i) + 's')
        # solution, time = z3solve(puzzle, True)
        # print(f'r{i}s', time)


if __name__ == '__main__':
    main()
