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
    for index in range(300):
        puzzle = loadpuzzle('misc/generated/30x30', index, 30, 30)
        unique = z3unique(puzzle)
        print(index, unique, sep='\t')


if __name__ == '__main__':
    main()
