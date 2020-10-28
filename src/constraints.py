from z3 import *

from constants import *


def _validpos(puzzle, x, y):
    """ Check if the given x and y indices are on the puzzle. """
    return 0 <= y < len(puzzle) and 0 <= x < len(puzzle[0])


def _constraints_wall(puzzle, constraints, bvars, x, y):
    """ The given x and y values represent a wall on the board with a number,
    n, constraint. From the neighbours of this wall exactly n neighbours need
    to be true, this function adds this constraint. """
    neighbours = []
    for dx, dy in DIRS:
        newx, newy = x + dx, y + dy
        if _validpos(puzzle, newx, newy) and puzzle[newy][newx] == N:
            neighbours.append((bvars[newx, newy], 1))

    constraints.append(PbEq(neighbours, puzzle[y][x]))


def _constraints_walls(puzzle, constraints, bvars, poss):
    """ Loop over all the walls with a number constraint and add the
    constraints. """
    walls = [(x, y) for (x, y) in poss if 0 <= puzzle[y][x] <= 4]
    for x, y in walls:
        _constraints_wall(puzzle, constraints, bvars, x, y)


def _constraints_lines_atleastone(puzzle, constraints, bvars, poss):
    """ Add a constraint such that every cell is lit up. This is done by adding
    a constraint for every cell looking in all directions and demanding a light
    bulb in at least one of the directions (or at the place itself). """
    for x, y in [(x, y) for (x, y) in poss if puzzle[y][x] == N]:
        atleastone = [bvars[x, y]]  # make sure every cell is lit up

        for dx, dy in DIRS:
            newx, newy = x + dx, y + dy
            while _validpos(puzzle, newx, newy) and puzzle[newy][newx] == N:
                atleastone.append(bvars[newx, newy])
                newx, newy = newx + dx, newy + dy

        constraints.append(Or(atleastone))


def _constraints_lines_atmostone(puzzle, constraints, bvars, poss):
    """ Add a constraint such that no two light bulbs illuminate each other.
    This is done by making sure that for every straight line (horizontal or
    vertical) on the board (interrupted by walls) there is never more than one
    light bulb on that line. """
    for dx, dy in DIRS[:2]:
        used = []

        for x, y in [(x, y) for (x, y) in poss if puzzle[y][x] == N]:
            if (x, y) in used:
                continue

            atmostone = [(bvars[x, y], 1)]  # make sure no light bulbs cross
            newx, newy = x + dx, y + dy

            while _validpos(puzzle, newx, newy) and puzzle[newy][newx] == N:
                atmostone.append((bvars[newx, newy], 1))
                used.append((newx, newy))
                newx, newy = newx + dx, newy + dy

            if len(atmostone) > 1:
                constraints.append(PbLe(atmostone, 1))


def constraints_all(puzzle, poss, bvars):
    constraints = []
    _constraints_walls(puzzle, constraints, bvars, poss)
    _constraints_lines_atleastone(puzzle, constraints, bvars, poss)
    _constraints_lines_atmostone(puzzle, constraints, bvars, poss)
    return constraints
