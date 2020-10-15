import time

from constants import *
from printer import display


def _initialize(puzzle):
    """ Initialize some lists. The shadows and candidates list start with all
    the empty cells. The shadows list indicates which cell is not lit up. The
    candidates list indicates at which poss a light could be placed. """
    poss = [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]
    shadows = {(x, y) for (x, y) in poss if puzzle[y][x] == N}
    candidates = {(x, y) for (x, y) in poss if puzzle[y][x] == N}
    return poss, shadows, candidates


def _validpos(puzzle, x, y):
    """ Check if the given x and y indices are on the puzzle. """
    return 0 <= y < len(puzzle) and 0 <= x < len(puzzle[0])


def _remove_list(x, y, collection):
    """ Remove the given cell from the given list, if possible. """
    try:
        collection.remove((x, y))
    except KeyError:
        pass


def _remove_cell(x, y, shadows, candidates):
    _remove_list(x, y, shadows)
    _remove_list(x, y, candidates)


def _remove_zeros(puzzle, poss, shadows, candidates):
    """ Remove cells next to a zero constraint from the candidates list. """
    for x, y in [(x, y) for (x, y) in poss if puzzle[y][x] == 0]:
        for dx, dy in DIRECTIONS:
            if _validpos(puzzle, x + dx, y + dy):
                _remove_list(x + dx, y + dy, candidates)


def _place_bulb(puzzle, x, y, shadows, candidates):
    """ Place a light bulb on the puzzle at the given coordinates by updating
    the shadows and candidates list accordingly. """
    _remove_cell(x, y, shadows, candidates)

    for dx, dy in DIRECTIONS:
        newx, newy = x + dx, y + dy
        while _validpos(puzzle, newx, newy) and puzzle[newy][newx] == N:
            _remove_cell(newx, newy, shadows, candidates)
            newx, newy = newx + dx, newy + dy

        # TODO If the light is adjacent to a number constraint cell and that
        # constraint cell is now satisfied, then we need to remove all adjacent
        # cells of this constraint cell from the candidates list.


def _neighbours(puzzle, x, y):
    """ Generate a list with all the coordinates of the neighbours for the
    given cell. """
    return [(x+dx, y+dy) for dx, dy in DIRECTIONS if _validpos(puzzle, x+dx, y+dy)]


def _trivialsolve(puzzle, poss, shadows, candidates):
    """ Place all the light bulbs which can be placed for sure. This can be
    done if there are exactly 'n' candidates neighbour of a 'n' constrained
    wall. Repeat this process until it does not work anymore. """
    _remove_zeros(puzzle, poss, shadows, candidates)
    solution = []

    walls = [(x, y) for x, y in poss if 0 <= puzzle[y][x] <= 4]
    done = False

    while not done:
        done = True

        for x, y in walls:
            neighbours = _neighbours(puzzle, x, y)
            number = puzzle[y][x] - len([n for n in neighbours if n in solution])
            neighbours = [n for n in neighbours if n in candidates]

            if len(neighbours) < number:  # no possible solution
                print(x, y)
                return None

            if len(neighbours) == number:  # place light bulbs
                done = False
                walls.remove((x, y))
                for _x, _y in neighbours:
                    _place_bulb(puzzle, _x, _y, shadows, candidates)
                    solution.append((_x, _y))

    return solution


def _backtracksolve(puzzle, shadows, candidates, solution, solutions, number):
    if len(solutions) == number:
        return

    if len(shadows) == 0:
        solutions.append(solution.copy())
        return

    if len(candidates) == 0:
        return

    # TODO Pop first from candidates list and try with and without a light bulb
    # on that cell. Send a copy of the shadows and candidates list in the call.


def trackdifficulty(puzzle):
    solutions, difficulty = _trackanalyse(puzzle, number)
    return difficulty


def trackunique(puzzle):
    solutions = tracksolves(puzzle, 2, stats)
    return len(solutions) == 1 if len(solutions) > 0 else None


def tracksolve(puzzle):
    solutions = tracksolves(puzzle, 1)
    return solutions[0] if len(solutions) == 1 else None


def tracksolves(puzzle, number=None):
    solutions, difficulty = _trackanalyse(puzzle, number)
    return solutions


def _trackanalyse(puzzle, number=None):
    poss, shadows, candidates = _initialize(puzzle)
    whole = len(candidates)

    solution = _trivialsolve(puzzle, poss, shadows, candidates)
    part = len(candidates)

    solutions = []
    if solution is not None:
        # TODO Sort the candidates list with number constraint cells first.
        _backtracksolve(puzzle, shadows, candidates, solution, solutions, number)

    return solutions, (whole, part)
