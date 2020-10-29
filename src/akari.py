from z3 import *
import time

from printer import display
from loader import *
from constants import *
from drawer import draw
from generator import generate, XAXIS, YAXIS, XYAXIS
from z3solver import z3solve, z3solves, z3unique
from tracksolver import tracksolve, tracksolves, trackunique, trackdifficulty


def main():
    puzzle = generate(5, 5)
    display(puzzle, z3solve(puzzle))


if __name__ == '__main__':
    main()
