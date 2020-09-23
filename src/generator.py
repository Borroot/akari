from random import choice

from constant import *
from printer import display
from z3solver import z3solve, z3unique


def _initialize(puzzle):
    return [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]


def _random_location(puzzle, positions):
    return choice([(x, y) for (x, y) in positions if puzzle[y][x] == N])


def _place_block(puzzle, positions, symmetrical):
    x, y = _random_location(puzzle, positions)
    puzzle[y][x] = B

    if symmetrical:
        width = len(puzzle[0]) - 1
        height = len(puzzle) - 1

        puzzle[height - y][x] = B
        puzzle[y][width - x] = B
        puzzle[height - y][width - x] = B


def _place_blocks(puzzle, positions, number, symmetrical):
    for _ in range(number):
        _place_block(puzzle, positions, symmetrical)


def _remove_all_numbers(puzzle, positions):
    for x, y in [(x, y) for (x, y) in positions if puzzle[y][x] != N]:
        puzzle[y][x] = B


def _remove_some_numbers(puzzle, positions):
    for x, y in [(x, y) for (x, y) in positions if puzzle[y][x] != N]:
        number = puzzle[y][x]
        puzzle[y][x] = B
        if not z3unique(puzzle):
            puzzle[y][x] = number


def _place_numbers(puzzle, positions):
    solution = z3solve(puzzle)

    for x, y in [(x, y) for (x, y) in positions if puzzle[y][x] == B]:
        count = 0
        for dx, dy in DIRECTIONS:
            if (x + dx, y + dy) in solution:
                count += 1

        puzzle[y][x] = count

    display(puzzle, solution)
    print()


def generate(height, width, start=None, step=None, symmetrical=True):
    puzzle = [[N for _ in range(width)] for _ in range(height)]
    positions = _initialize(puzzle)

    big = width if width > height else height
    start = big if start is None else max(start, (width * height) // 2)
    step = min(1, big // 3) if step is None else step

    _place_blocks(puzzle, positions, start, symmetrical)
    while not z3unique(puzzle):
        _remove_all_numbers(puzzle, positions)
        _place_blocks(puzzle, positions, step, symmetrical)
        _place_numbers(puzzle, positions)

    _remove_some_numbers(puzzle, positions)
    return puzzle, z3solve(puzzle)
