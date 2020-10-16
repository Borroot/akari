import time

from printer import display
from constants import *


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
    except ValueError:
        pass


def _remove_cell(x, y, shadows, candidates):
    _remove_list(x, y, shadows)
    _remove_list(x, y, candidates)


def _neighbours(puzzle, x, y):
    """ The coordinates of the neighbours for the given cell. """
    return [(x+dx, y+dy) for dx, dy in DIRS if _validpos(puzzle, x+dx, y+dy)]


def _remove_zeros(puzzle, poss, shadows, candidates):
    """ Remove cells next to a zero constraint from the candidates list. """
    for x, y in [(x, y) for (x, y) in poss if puzzle[y][x] == 0]:
        for neighbour in _neighbours(puzzle, x, y):
            _remove_list(*neighbour, candidates)


def _place_bulb(puzzle, x, y, shadows, candidates, solution):
    """ Place a light bulb on the puzzle at the given coordinates by updating
    the shadows and candidates list accordingly. So remove any candidate and
    shadow in line with the bulb and remove all candidates next to a just
    satisfied constraint cell. """
    _remove_cell(x, y, shadows, candidates)

    for dx, dy in DIRS:
        newx, newy = x + dx, y + dy

        if _validpos(puzzle, newx, newy) and 0 <= puzzle[newy][newx] <= 4:
            neighbours = _neighbours(puzzle, newx, newy)
            placed = len([n for n in neighbours if n in solution])
            if puzzle[newy][newx] == placed:
                for neighbour in neighbours:
                    _remove_list(*neighbour, candidates)
        else:
            while _validpos(puzzle, newx, newy) and puzzle[newy][newx] == N:
                _remove_cell(newx, newy, shadows, candidates)
                newx, newy = newx + dx, newy + dy


def _trivialsolve(puzzle, poss, shadows, candidates):
    """ Place all the light bulbs which can be placed for sure. This can be
    done if there are exactly 'n' candidates neighbour of a 'n' constrained
    wall. Repeat this process until it does not work anymore. """
    _remove_zeros(puzzle, poss, shadows, candidates)
    solution = []

    walls = [(x, y) for x, y in poss if 1 <= puzzle[y][x] <= 4]
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
                for neighbour in neighbours:
                    solution.append(neighbour)  # make sure to append first
                    _place_bulb(puzzle, *neighbour, shadows, candidates, solution)

    return solution


def _wall_unsatisfiable(puzzle, poss, solution, candidates):
    """ Check if there exists a constraint wall which cannot be satisfied. """
    walls = [(x, y) for x, y in poss if 1 <= puzzle[y][x] <= 4]
    for x, y in walls:
        neighbours = _neighbours(puzzle, x, y)
        number = puzzle[y][x] - len([n for n in neighbours if n in solution])
        if number > len([n for n in neighbours if n in candidates]):
            return True
    return False


def _walls_satisfied(puzzle, poss, solution):
    """ Check if all the constraint walls are satisfied. """
    walls = [(x, y) for x, y in poss if 1 <= puzzle[y][x] <= 4]
    for x, y in walls:
        neighbours = _neighbours(puzzle, x, y)
        if len([n for n in neighbours if n in solution]) != puzzle[y][x]:
            return False
    return True


def _sort_candidates(puzzle, candidates):
    """ Sort the candidates list such that the cells next to constraint walls
    are first, the lower the constraint the better. """
    def _key(cell):
        neighbours = _neighbours(puzzle, *cell)
        constraint = sum(1 for x, y in neighbours if 1 <= puzzle[y][x] <= 4)
        return (0, cell) if constraint else (1, cell)

    candidates.sort(key=_key, reverse=True)
    return candidates


def _backtracksolve(puzzle, poss, shadows, candidates, solution, solutions, number, branches):
    if len(solutions) == number:
        return

    if len(shadows) == 0 and _walls_satisfied(puzzle, poss, solution):
        solutions.append(solution.copy())
        branches.append(branches[0])
        return

    if len(candidates) == 0 or _wall_unsatisfiable(puzzle, poss, solution, candidates):
        return

    branches[0] += 1

    candidate = candidates.pop()
    _shadows, _candidates = shadows.copy(), candidates.copy()

    # Try with a light bulb at this place.
    _place_bulb(puzzle, *candidate, shadows, candidates, solution)
    solution.append(candidate)
    _backtracksolve(puzzle, poss, shadows, candidates, solution, solutions, number, branches)

    # Try with no light bulb at this place.
    solution.pop()
    _backtracksolve(puzzle, poss, _shadows, _candidates, solution, solutions, number, branches)


def trackdifficulty(puzzle, number=None):
    solutions, difficulty = _trackanalyse(puzzle, number)
    return difficulty


def trackunique(puzzle):
    solutions = tracksolves(puzzle, 2)
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
    branches = [0]
    if solution is not None:
        candidates = _sort_candidates(puzzle, list(candidates))
        _backtracksolve(puzzle, poss, shadows, candidates, solution, solutions, number, branches)

    return solutions, (whole, part, branches)
