from constants import *
from printer import display


def _validposition(puzzle, x, y):
    """ Check if the given x and y indices are on the puzzle. """
    return 0 <= y < len(puzzle) and 0 <= x < len(puzzle[0])


def _initialize(puzzle):
    positions = [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]

    # shadow: not lit up empty cells; candidate: cells which could have a bulb
    shadows = {(x, y) for (x, y) in positions if puzzle[y][x] == N}
    candidates = {(x, y) for (x, y) in positions if puzzle[y][x] == N}

    return positions, shadows, candidates


def _remove_list(x, y, collection):
    try:
        collection.remove((x, y))
    except KeyError:
        pass


def _remove_cell(x, y, shadows, candidates):
    _remove_list(x, y, shadows)
    _remove_list(x, y, candidates)


def _remove_zeros(puzzle, positions, shadows, candidates):
    for x, y in [(x, y) for (x, y) in positions if puzzle[y][x] == 0]:
        for dx, dy in DIRECTIONS:
            if _validposition(puzzle, x + dx, y + dy):
                _remove_list(x + dx, y + dy, candidates)


def _place_bulb(puzzle, x, y, shadows, candidates):
    _remove_cell(x, y, shadows, candidates)

    for dx, dy in DIRECTIONS:
        newx, newy = x + dx, y + dy
        while _validposition(puzzle, newx, newy) and puzzle[newy][newx] == N:
            _remove_cell(newx, newy, shadows, candidates)
            newx, newy = newx + dx, newy + dy


def _neighbours(puzzle, x, y):
    return [(x+dx, y+dy) for dx, dy in DIRECTIONS if _validposition(puzzle, x+dx, y+dy)]


def _trivialsolve(puzzle, positions, shadows, candidates):
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

            if len(neighbours) == number:
                done = False
                walls.remove((x, y))
                for _x, _y in neighbours:
                    _place_bulb(puzzle, _x, _y, shadows, candidates)
                    solution.append((_x, _y))

    return solution


def _backtracksolve(puzzle, shadows, candidates, solution):
    pass


def tracksolve(puzzle, timed=False):
    positions, shadows, candidates = _initialize(puzzle)

    solution = _trivialsolve(puzzle, positions, shadows, candidates)
    if solution is not None:
        _backtracksolve(puzzle, shadows, candidates, solution)

    return solution


def tracksolves(puzzle, number=None, timed=False):
    pass


def trackunique(puzzle, timed=False):
    pass
