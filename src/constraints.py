from z3 import *

from constant import *


def _validposition(puzzle, x, y):
    """ Check if the given x and y indices are on the puzzle. """
    return 0 <= y < len(puzzle) and 0 <= x < len(puzzle[0])


def _constraints_wall(puzzle, solver, bvars, x, y):
    """ The given x and y values represent a wall on the board with a number,
    n, constraint. From the neighbours of this wall exactly n neighbours need
    to be true, this function adds this constraint. """
    number = puzzle[y][x]

    neighbours = []
    for dx, dy in DIRECTIONS:
        newx, newy = x + dx, y + dy
        if _validposition(puzzle, newx, newy) and puzzle[newy][newx] == N:
            neighbours.append((bvars[newx, newy], 1))

    solver.add(PbEq(neighbours, number))


def _constraints_walls(puzzle, solver, bvars, positions):
    """ Loop over all the walls with a number constraint and add the
    constraints. """
    walls = [(x, y) for (x, y) in positions if 0 <= puzzle[y][x] <= 4]
    for x, y in walls:
        _constraints_wall(puzzle, solver, bvars, x, y)


def _constraints_lines(puzzle, solver, bvars, positions):
    """ This function adds two types of constraints. It adds a constraint such
    that every cell is lit up _at least_ once. This is done by adding a
    constraint for every cell looking in all directions and demanding a light
    bulb in at least one of the directions (or at the place itself). It also
    adds a constraint such that no two light bulbs illuminate each other. This
    is done by making sure that for every straight line (horizontal or vertical)
    on the board (interrupted by walls) there is never more than one light
    bulb on that line. """
    for x, y in [(x, y) for (x, y) in positions if puzzle[y][x] == N]:
        atleastone = [(bvars[x, y], 1)]  # make sure every cell is lit up

        for dx, dy in DIRECTIONS:
            atmostone = [(bvars[x, y], 1)]  # make sure no light bulbs cross

            newx, newy = x + dx, y + dy
            while _validposition(puzzle, newx, newy) and puzzle[newy][newx] == N:
                atleastone.append((bvars[newx, newy], 1))
                atmostone.append((bvars[newx, newy], 1))
                newx, newy = newx + dx, newy + dy

            if len(atmostone) > 1:
                solver.add(PbLe(atmostone, 1))

        solver.add(PbGe(atleastone, 1))


def constraints_all(puzzle, solver, positions, bvars):
    _constraints_walls(puzzle, solver, bvars, positions)
    _constraints_lines(puzzle, solver, bvars, positions)
