from z3 import *

from printer import display
from loader import *
from z3solver import z3solve, z3unique


def main():
    puzzle = loadpuzzle('misc/14x14_hard', 0, 14, 14)
    solution = z3solve(puzzle)
    display(puzzle, solution)
    print('The puzzle is unique.' if z3unique(puzzle) else 'The puzzle is not unique.')


if __name__ == '__main__':
    main()
