import time

from constants import *
from printer import display


def _validposition(puzzle, x, y):
    """ Check if the given x and y indices are on the puzzle. """
    return 0 <= y < len(puzzle) and 0 <= x < len(puzzle[0])


def _initialize(puzzle):
    """ Initialize some lists. The shadows and candidates list start with all
    the empty cells. The shadows list indicates which cell is not lighted up.
    The candidates list indicates at which positions a bulb could be placed.  """
    positions = [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]
    shadows = {(x, y) for (x, y) in positions if puzzle[y][x] == N}
    candidates = {(x, y) for (x, y) in positions if puzzle[y][x] == N}
    return positions, shadows, candidates


def _remove_list(x, y, collection):
    """ Remove the given cell from the given list, if possible. """
    try:
        collection.remove((x, y))
    except KeyError:
        pass


def _remove_cell(x, y, shadows, candidates):
    _remove_list(x, y, shadows)
    _remove_list(x, y, candidates)


def _remove_zeros(puzzle, positions, shadows, candidates):
    """ Remove cells next to a zero constraint from the candidates list. """
    for x, y in [(x, y) for (x, y) in positions if puzzle[y][x] == 0]:
        for dx, dy in DIRECTIONS:
            if _validposition(puzzle, x + dx, y + dy):
                _remove_list(x + dx, y + dy, candidates)


def _place_bulb(puzzle, x, y, shadows, candidates):
    """ Place a light bulb on the puzzle at the given coordinates by updating
    the shadows and candidates list accordingly. """
    _remove_cell(x, y, shadows, candidates)

    for dx, dy in DIRECTIONS:
        newx, newy = x + dx, y + dy
        while _validposition(puzzle, newx, newy) and puzzle[newy][newx] == N:
            _remove_cell(newx, newy, shadows, candidates)
            newx, newy = newx + dx, newy + dy


def _neighbours(puzzle, x, y):
    """ Generate a list with all the coordinates of the neighbours for the
    given cell. """
    return [(x+dx, y+dy) for dx, dy in DIRECTIONS if _validposition(puzzle, x+dx, y+dy)]


def _trivialsolve(puzzle, positions, shadows, candidates):
    """ Place all the light bulbs which can be placed for sure. This can be
    done if there are exactly 'n' candidates neighbour of a 'n' constrained
    wall. Repeat this process until it does not work anymore. """
    _remove_zeros(puzzle, positions, shadows, candidates)
    solution = []

    walls = [(x, y) for (x, y) in positions if puzzle[y][x] != N and puzzle[y][x] != B]
    done = False

    while not done:
        done = True

        for x, y in walls:
            neighbours = _neighbours(puzzle, x, y)
            number = puzzle[y][x] - len([n for n in neighbours if n in solution])
            neighbours = [n for n in neighbours if n in candidates]

            if len(neighbours) < number:  # no possible solution
                return None

            if len(neighbours) == number:  # place light bulbs
                done = False
                walls.remove((x, y))
                for _x, _y in neighbours:
                    _place_bulb(puzzle, _x, _y, shadows, candidates)
                    solution.append((_x, _y))

    return solution


def _backtracksolve(puzzle, shadows, candidates, solution, solutions, number):
    pass


def trackunique(puzzle, stats=False):
    if stats:
        solutions, time, perc = tracksolves(puzzle, 2, stats)
        return len(solutions) == 2, time, perc
    else:
        return len(tracksolves(puzzle, 2, stats)) == 2


def tracksolve(puzzle, stats=False):
    if stats:
        solutions, time, perc = tracksolves(puzzle, 1, stats)
        return solutions[0] if len(solutions) == 1 else None, time, perc
    else:
        solutions = tracksolves(puzzle, 1, stats)
        return solutions[0] if len(solutions) == 1 else None


def tracksolves(puzzle, number=None, stats=False):
    positions, shadows, candidates = _initialize(puzzle)

    whole = len(candidates)
    start = time.time()

    solution = _trivialsolve(puzzle, positions, shadows, candidates)
    part = len(candidates)

    solutions = []
    if solution is not None:
        _backtracksolve(puzzle, shadows, candidates, solution, solutions, number)

    end = time.time()

    return solutions, end - start, (whole, part) if stats else solutions
