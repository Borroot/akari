from z3 import *

from printer import display
from loader import *
from z3solver import z3solve, z3solves, z3unique


def main():
    for index in range(999):
        puzzle = loadpuzzle('misc/14x14_hard', index, 14, 14)
        solutions, time = z3solves(puzzle, True)
        print(index, len(solutions), time)


if __name__ == '__main__':
    main()
