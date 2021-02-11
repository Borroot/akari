from z3 import *
import time

from printer import display
from loader import *
from constants import *
from drawer import draw
from generator import generate, XAXIS, YAXIS, XYAXIS
from z3solver import z3solve, z3solves, z3unique
from tracksolver import *
from verifier import verify_all


def main():
    name = 'circuit'
    puzzle = loadgrid('misc/showcase/' + name)

    draw(puzzle, name, magnifier = 300)
    solution = z3solve(puzzle)

    for i, solution in enumerate(z3solves(puzzle)):
        draw(puzzle, name + '_solve' + str(i), 300, solution)


if __name__ == '__main__':
    main()
