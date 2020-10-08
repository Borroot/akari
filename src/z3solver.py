from z3 import *
import time

from constraints import constraints_all


def _solution(positions, bvars, model):
    """ Convert the model given by z3 to a list with light bulb positions. """
    return [(x, y) for (x, y) in positions if model[bvars[x, y]]]


def _initialize(puzzle):
    """ Initialize the solver with all the constraints. """
    positions = [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]
    bvars = {(x, y): Bool("v{};{}".format(x, y)) for x, y in positions}

    solver = Solver()
    constraints_all(puzzle, solver, positions, bvars)

    return positions, bvars, solver


def z3solve(puzzle, timed=False):
    """ Search for one solution for the given puzzle using z3. """
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


def z3solves(puzzle, number=None, timed=False):
    """ Search for the given number of solutions for the given puzzle using z3,
    if no number is given then all solutions will be returned. """
    positions, bvars, solver = _initialize(puzzle)

    if timed: start = time.time()

    solutions = []
    while (number is None or len(solutions) < number) and solver.check() == sat:
        solution = _solution(positions, bvars, solver.model())
        solutions.append(solution)
        constraints = Not(And([bvars[x, y] for (x, y) in solution]))
        solver.add(constraints)

    if timed: end = time.time()

    if timed:
        return solutions, end - start
    else:
        return solutions


def z3unique(puzzle, timed=False):
    """ Check if the given has exactly one unique solution using z3. """
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
