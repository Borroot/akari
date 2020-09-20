from z3 import *

from constant import *


def _validposition(puzzle, x, y):
    return 0 <= y < len(puzzle) and 0 <= x < len(puzzle[0])


def _constraints_wall(puzzle, solver, bvars, x, y):
    number = puzzle[y][x]

    neighbours = []
    for dx, dy in DIRECTIONS:
        newx, newy = x + dx, y + dy
        if _validposition(puzzle, newx, newy):
            neighbours.append((bvars[newx, newy], 1))

    solver.add(PbEq(neighbours, number))


def _constraints_walls(puzzle, solver, bvars, positions):
    walls = [(x, y) for (x, y) in positions if 0 <= puzzle[y][x] <= 4]
    for x, y in walls:
        _constraints_wall(puzzle, solver, bvars, x, y)


def _constraints_lines(puzzle, solver, bvars, positions):
    for x, y in [(x, y) for (x, y) in positions if puzzle[y][x] == N]:
        lightup = [(bvars[x, y], 1)]  # make sure every cell is lit up

        for dx, dy in DIRECTIONS:
            mostone = [(bvars[x, y], 1)]  # make sure no light bulbs cross

            newx, newy = x + dx, y + dy
            while _validposition(puzzle, newx, newy) and puzzle[newy][newx] == N:
                lightup.append((bvars[newx, newy], 1))
                mostone.append((bvars[newx, newy], 1))
                newx, newy = newx + dx, newy + dy

            if len(mostone) > 1:
                solver.add(PbLe(mostone, 1))

        solver.add(PbGe(lightup, 1))


def constraints_all(puzzle, solver, positions, bvars):
    _constraints_walls(puzzle, solver, bvars, positions)
    _constraints_lines(puzzle, solver, bvars, positions)
