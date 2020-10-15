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
        # puzzle, solution = generate(5, 5, 0, 1, YAXIS)
        # display(puzzle)
        # writecodex('misc/generated/5x5', puzzle)

    # for index in range(20):
        # puzzle = loadpuzzle('misc/generated/30x30', index, 30, 30)
        # for _ in range(9):
            # solutions = z3solves(puzzle)
            # print(len(solutions), end='\t', flush=True)
        # print()

    puzzle = [
        [B,1,N,1,N,1,B],
        [0,N,N,N,N,N,0]]
    solution = tracksolve(puzzle)
    display(puzzle, solution)

    # for index in range(22, 23):
        # puzzle = loadpuzzle('misc/generated/5x5', index, 5, 5)
        # for _ in range(0, 3):
            # solutions = z3solves(puzzle)
            # for solution in solutions:
                # print()
                # # display(puzzle, solution)
            # print('---------')
        # print()


if __name__ == '__main__':
    main()
