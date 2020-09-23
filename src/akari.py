from z3 import *

from printer import display
from loader import *
from generator import generate
from z3solver import z3solve, z3solves, z3unique


def main():
    puzzle, solution = generate(10, 20, 10, 3)
    display(puzzle)
    print()
    display(puzzle, solution)

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
