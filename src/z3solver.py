from z3 import *
import time

from constraints import constraints_all


def _solution(positions, model, bvars):
    return [(x, y) for (x, y) in positions if model[bvars[x, y]]]


def z3solve(puzzle):
    positions = [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]
    bvars = {(x, y): Bool("v{};{}".format(x, y)) for x, y in positions}

    solver = Solver()
    constraints_all(puzzle, solver, positions, bvars)

    start = time.time()
    solved = solver.check() == sat
    end = time.time()

    if solved:
        model = solver.model()
        solution = _solution(positions, model, bvars)
    else:
        solution = None

    return solved, solution, end - start
