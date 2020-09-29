import numpy as np
from numpy import random

from constants import *
from printer import display
from z3solver import z3solve, z3unique, z3solves


XAXIS = 0
YAXIS = 1
XYAXIS = 2


def _initialize(puzzle):
    """ Generate a list with all the positions on the puzzle. """
    return [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]


def _validposition(puzzle, x, y):
    """ Check if the given x and y indices are on the puzzle. """
    return 0 <= y < len(puzzle) and 0 <= x < len(puzzle[0])


def _neighbours(puzzle, x, y):
    """ Count the number of wall neighbours for puzzle[y][x]. """
    count = 0
    for dx in [0, 1, -1, 2, -2]:
        for dy in [0, 1, -1, 2, -2]:
            if not _validposition(puzzle, x + dx, y + dy):
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


def _random_location(puzzle, positions, solutions=None):
    """ Pick a random location on the puzzle. This is done by making a
    distribution inverse to the heuristic. """
    choices = ([(x, y) for (x, y) in positions if puzzle[y][x] == N])
    distro = [_heuristic(puzzle, x, y, solutions) for (x, y) in choices]
    distro = [(max(distro) + 0.1 - x) ** 10 for x in distro]
    distro = [x / sum(distro) if sum(distro) > 0 else 1 / len(distro) for x in distro]

    index = random.choice(np.arange(len(choices)), p=distro)
    return choices[index]


def _place_block(puzzle, positions, symmetrical, solutions=None):
    """ Place a wall on a random location. If the symmetrical option is used
    then four walls are placed symmetrical to each other. """
    x, y = _random_location(puzzle, positions, solutions)
    puzzle[y][x] = B

    if symmetrical is not None:
        width, height = len(puzzle[0]) - 1, len(puzzle) - 1

        if symmetrical == XAXIS or symmetrical == XYAXIS:
            puzzle[height - y][x] = B
        if symmetrical == YAXIS or symmetrical == XYAXIS:
            puzzle[y][width - x] = B
        if symmetrical == XYAXIS:
            puzzle[height - y][width - x] = B


def _place_blocks(puzzle, positions, number, symmetrical, solutions=None):
    """ Place a number of random walls. """
    for _ in range(number):
        _place_block(puzzle, positions, symmetrical, solutions)


def _remove_all_numbers(puzzle, positions):
    """ Remove all the numbers from the walls. """
    for x, y in [(x, y) for (x, y) in positions if puzzle[y][x] != N]:
        puzzle[y][x] = B


def _remove_some_numbers(puzzle, positions):
    """ Remove all the numbers which are irrelevant for the uniqueness of the
    solution for the puzzle. """
    for x, y in [(x, y) for (x, y) in positions if puzzle[y][x] != N]:
        number = puzzle[y][x]
        puzzle[y][x] = B
        if not z3unique(puzzle):
            puzzle[y][x] = number


def _place_numbers(puzzle, positions):
    """ Place all the numbers on the walls corresponding to the solution. """
    solution = z3solve(puzzle)

    for x, y in [(x, y) for (x, y) in positions if puzzle[y][x] == B]:
        count = 0
        for dx, dy in DIRECTIONS:
            if (x + dx, y + dy) in solution:
                count += 1

        puzzle[y][x] = count

    display(puzzle)
    print()


def generate(height, width, start=None, step=None, symmetrical=None):
    puzzle = [[N for _ in range(width)] for _ in range(height)]
    positions = _initialize(puzzle)

    big = width if width > height else height
    start = big if start is None else min(start, (width * height) // 2)
    step = min(1, big // 3) if step is None else step

    _place_blocks(puzzle, positions, start, symmetrical)
    while len(solutions := z3solves(puzzle, 2)) > 1:
        _remove_all_numbers(puzzle, positions)
        _place_blocks(puzzle, positions, step, symmetrical, solutions)
        _place_numbers(puzzle, positions)

    print('removing the numbers...')
    _remove_some_numbers(puzzle, positions)
    return puzzle, z3solve(puzzle)
