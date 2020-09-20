from z3 import *
import time

from constraints import constraints_all


def _solution(positions, bvars, model):
    return [(x, y) for (x, y) in positions if model[bvars[x, y]]]


def _initialize(puzzle):
    positions = [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]
    bvars = {(x, y): Bool("v{};{}".format(x, y)) for x, y in positions}

    solver = Solver()
    constraints_all(puzzle, solver, positions, bvars)

    return positions, bvars, solver


def z3solve(puzzle, timed=False):
    positions, bvars, solver = _initialize(puzzle)

    if timed: start = time.time()
    result = solver.check()
    if timed: end = time.time()

    if result == sat:
        solution = _solution(positions, bvars, solver.model())
    else:
        solution = None

    if timed:
        return solution, end - start
    else:
        return solution


def z3unique(puzzle, timed=False):
    positions, bvars, solver = _initialize(puzzle)

    if timed: start = time.time()

    unique = None
    if solver.check() == sat:
        solution = _solution(positions, bvars, solver.model())
        constraints = Not(And([bvars[x, y] for (x, y) in solution]))
        solver.add(constraints)
        unique = solver.check() != sat

    if timed: end = time.time()

    if timed:
        return unique, end - start
    else:
        return unique
