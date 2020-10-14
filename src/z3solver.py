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


def z3unique(puzzle):
    """ Check if the given puzzle has exactly one unique solution using z3. """
    solutions, time = z3solves(puzzle, 2)
    return len(solutions) == 1 if len(solutions) > 0 else None, time


def z3solve(puzzle):
    """ Search for one solution for the given puzzle using z3. """
    solutions, time = z3solves(puzzle, 1, stats)
    return solutions[0] if len(solutions) == 1 else None, time


def z3solves(puzzle, number=None):
    """ Search for the given number of solutions for the given puzzle using z3,
    if no number is given then all solutions will be returned. """
    positions, bvars, solver = _initialize(puzzle)

    start = time.time()

    # FIXME Behave deterministically.
    solutions = []
    while (number is None or len(solutions) < number) and solver.check() == sat:
        solution = _solution(positions, bvars, solver.model())
        solutions.append(solution)
        solver.add(Not(And([bvars[x, y] for (x, y) in solution])))

    end = time.time()
    return solutions, end - start
