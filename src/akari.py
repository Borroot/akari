from z3 import *
import time

from printer import display
from loader import *
from constants import *
from drawer import draw
from generator import generate, XAXIS, YAXIS, XYAXIS
from z3solver import z3solve, z3solves, z3unique
from tracksolver import tracksolve, tracksolves, trackunique


def main():
    # puzzle = loadpuzzle('misc/web/14x14_easy', 0, 14, 14)
    # solution = z3solve(puzzle)
    # draw(puzzle, 'test', 500, solution)

    # for index in range(100):
        # puzzle, solution = generate(40, 40, 170, 3, YAXIS)
        # display(puzzle)
        # print(index, '\n')
        # writecodex('misc/generated/40x40', puzzle)

    # puzzle = loadpuzzle('misc/web/7x7_easy', 0, 7, 7)
    # solution, time, (whole, part) = tracksolve(puzzle, True)
    # display(puzzle, solution)
    # print(time, whole, part, part / whole)

    # for index in range(40):
        # puzzle = loadpuzzle('misc/generated/30x30', index, 30, 30)
        # unique, time = z3unique(puzzle, stats=True)
        # print(index, time, unique, len(z3solves(puzzle, 2)))

    for index in range(10):
        puzzle = loadpuzzle('misc/generated/30x30', index, 30, 30)
        for _ in range(8):
            solutions = z3solves(puzzle, 2)
            print(len(solutions), end='\t', flush=True)
        # print()
        # display(puzzle, solutions[0])
        # for solution in solutions[1:]:
            # print(set(solution) - set(solutions[0]))
            # display(puzzle, solution)

    # for i in range(1, 10):
        # puzzle = loadhans('misc/hans/r' + str(i) + 's')
        # solution, time = z3solve(puzzle, True)
        # print(f'r{i}s', time)


if __name__ == '__main__':
    main()
