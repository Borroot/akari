from z3 import *

from printer import display
from loader import *
from z3solver import z3solve


def main():
    puzzle = loadpuzzle('misc/25x25_hard', 0, 25, 25)
    solved, solution, time = z3solve(puzzle)


if __name__ == '__main__':
    main()
