import numpy as np
from numpy import random

from constants import *
from printer import display
from z3solver import z3solve, z3unique, z3solves


XAXIS = 0
YAXIS = 1
XYAXIS = 2


def _neighbours(puzzle, x, y):
    """ Count the number of wall neighbours for puzzle[y][x]. """
    count = 0
    for dx in [0, 1, -1, 2, -2]:
        for dy in [0, 1, -1, 2, -2]:
            if not (0 <= y+dy < len(puzzle) and 0 <= x+dx < len(puzzle[0])):
                count += 0.10
            elif puzzle[y + dy][x + dx] != N:
                count += 1 if dx == 0 or dy == 0 else 0.5
    return count


def _heuristic(puzzle, x, y, solutions=None):
    """ Assign a weight to every cell based on the number of walls around it
    and based on if it is close to a cell which makes two solutions different,
    this makes the convergence to a unique solution a lot faster. The lower the
    weight, the better the cell."""
    neighbours = _neighbours(puzzle, x, y)
    if solutions is None:
        return neighbours

    left = set(solutions[0]).symmetric_difference(set(solutions[1]))
    distances = [abs(x - _x) + abs(y - _y) for _x, _y in left]
    return neighbours + min(distances)


def _random_location(puzzle, poss, solutions=None):
    """ Pick a random location on the puzzle. This is done by making a
    distribution inverse to the heuristic. """
    choices = ([(x, y) for (x, y) in poss if puzzle[y][x] == N])
    distro = [_heuristic(puzzle, x, y, solutions) for (x, y) in choices]
    distro = [(max(distro) + 0.1 - x) ** 10 for x in distro]
    distro = [x / sum(distro) if sum(distro) > 0 else 1 / len(distro) for x in distro]

    index = random.choice(np.arange(len(choices)), p=distro)
    return choices[index]


def _place_block(puzzle, poss, symmetrical, solutions=None):
    """ Place a wall on a random location. If the symmetrical option is used
    then four walls are placed symmetrical to each other. """
    x, y = _random_location(puzzle, poss, solutions)
    puzzle[y][x] = B

    if symmetrical is not None:
        width, height = len(puzzle[0]) - 1, len(puzzle) - 1

        if symmetrical == XAXIS or symmetrical == XYAXIS:
            puzzle[height - y][x] = B
        if symmetrical == YAXIS or symmetrical == XYAXIS:
            puzzle[y][width - x] = B
        if symmetrical == XYAXIS:
            puzzle[height - y][width - x] = B


def _place_blocks(puzzle, poss, number, symmetrical, solutions=None):
    """ Place a number of random walls. """
    for _ in range(number):
        _place_block(puzzle, poss, symmetrical, solutions)


def _remove_all_numbers(puzzle, poss):
    """ Remove all the numbers from the walls. """
    for x, y in [(x, y) for (x, y) in poss if puzzle[y][x] != N]:
        puzzle[y][x] = B


def _remove_some_numbers(puzzle, poss):
    """ Remove all the numbers which are irrelevant for the uniqueness of the
    solution for the puzzle. """
    for x, y in [(x, y) for (x, y) in poss if puzzle[y][x] != N]:
        number = puzzle[y][x]
        puzzle[y][x] = B
        if not z3unique(puzzle):
            puzzle[y][x] = number


def _place_numbers(puzzle, poss):
    """ Place all the numbers on the walls corresponding to the solution. """
    solution = z3solve(puzzle)

    for x, y in [(x, y) for (x, y) in poss if puzzle[y][x] == B]:
        count = 0
        for dx, dy in DIRS:
            if (x + dx, y + dy) in solution:
                count += 1
        puzzle[y][x] = count


def generate(height, width, start=None, step=None, symmetrical=None, seed=None):
    puzzle = [[N for _ in range(width)] for _ in range(height)]
    poss = [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]
    if seed is not None: random.seed(seed)

    big = width if width > height else height
    start = big if start is None else min(start, (width * height) // 2)
    step = min(1, big // 3) if step is None else step

    _place_blocks(puzzle, poss, start, symmetrical)
    while len(solutions := z3solves(puzzle, 2)) > 1:
        _remove_all_numbers(puzzle, poss)
        _place_blocks(puzzle, poss, step, symmetrical, solutions)
        _place_numbers(puzzle, poss)

    _remove_some_numbers(puzzle, poss)
    return puzzle, z3solve(puzzle)
