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


def z3solve(puzzle, stats=False):
    """ Search for one solution for the given puzzle using z3. """
    positions, bvars, solver = _initialize(puzzle)

    start = time.time()
    result = solver.check()
    end = time.time()

    if result == sat:
        solution = _solution(positions, bvars, solver.model())
    else:
        solution = None

    return solution, end - start if stats else solution


def z3solves(puzzle, number=None, stats=False):
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
    return solutions, end - start if stats else solutions


def z3unique(puzzle, stats=False):
    """ Check if the given puzzle has exactly one unique solution using z3. """
    positions, bvars, solver = _initialize(puzzle)

    start = time.time()

    unique = None
    if solver.check() == sat:
        solution = _solution(positions, bvars, solver.model())
        solver.add(Not(And([bvars[x, y] for (x, y) in solution])))
        unique = solver.check() == unsat

    end = time.time()
    return unique, end - start if stats else unique
