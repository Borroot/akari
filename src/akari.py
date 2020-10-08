from z3 import *
import time

from printer import display
from loader import *
from drawer import draw
from generator import generate, XAXIS, YAXIS, XYAXIS
from z3solver import z3solve, z3solves, z3unique
from tracksolver import tracksolve, tracksolves, trackunique


def main():
    puzzle = loadpuzzle('misc/web/14x14_easy', 0, 14, 14)
    solution = z3solve(puzzle)
    draw(puzzle, 'test', 500, solution)

    # for index in range(100):
        # puzzle, solution = generate(40, 40, 170, 3, YAXIS)
        # display(puzzle)
        # print(index, '\n')
        # writecodex('misc/generated/40x40', puzzle)

    # puzzle = loadpuzzle('misc/generated/40x40', 0, 40, 40)
    # solution = tracksolve(puzzle, True)
    # display(puzzle)
    # print()
    # display(puzzle, solution)

    # total = 0
    # for index in range(76):
        # puzzle = loadpuzzle('misc/generated/40x40', index, 40, 40)
        # solution, time = z3solve(puzzle, True)
        # print(index, time)
        # total += time
    # print('average', total / 76)

    # for i in range(1, 10):
        # puzzle = loadhans('misc/hans/r' + str(i) + 's')
        # solution, time = z3solve(puzzle, True)
        # print(f'r{i}s', time)


if __name__ == '__main__':
    main()
