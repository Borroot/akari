from z3 import *

from printer import display
from loader import *
from z3solver import z3solve, z3solves, z3unique


def main():
    # for index in range(999):
        # puzzle = loadpuzzle('misc/web/14x14_hard', index, 14, 14)
        # solution, time = z3solves(puzzle, True)
        # print(index, time)

    for i in range(1, 10):
        puzzle = loadhans('misc/hans/r' + str(i) + 's')
        solution, time = z3solve(puzzle, True)
        print(f'r{i}s', time)


if __name__ == '__main__':
    main()
