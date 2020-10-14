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
    # for index in range(100):
        # puzzle, solution = generate(40, 40, 170, 3, YAXIS)
        # display(puzzle)
        # print(index, '\n')
        # writecodex('misc/generated/40x40', puzzle)

    # puzzle = loadpuzzle('misc/web/7x7_easy', 0, 7, 7)
    # solution, time, (whole, part) = tracksolve(puzzle, True)
    # display(puzzle, solution)
    # print(time, whole, part, part / whole)

    for index in range(80):
        puzzle = loadpuzzle('misc/generated/30x30', index, 30, 30)
        for _ in range(9):
            solutions, time = z3solves(puzzle, 9)
            print(len(solutions), end='', flush=True)
        print()


if __name__ == '__main__':
    main()
