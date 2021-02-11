from z3 import *
import time

from printer import display
from loader import loadcodex, loadgrid, loadverify, writecodex
from constants import *
from drawer import draw
from generator import generate, XAXIS, YAXIS, XYAXIS
from z3solver import z3solve, z3solves, z3unique
from tracksolver import *
from verifier import verify_all


def main():
    puzzle = loadcodex('misc/internet/10x10_easy', 0, 10)
    solution = z3solve(puzzle)

    display(puzzle, solution)
    # draw(puzzle, 'puzzle', solution = solution, magnifier = 300)


if __name__ == '__main__':
    main()
