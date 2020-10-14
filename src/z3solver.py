from z3 import *
import time

from constraints import constraints_all


def _initialize(puzzle):
    """ Initialize the solver with all the constraints. """
    poss = [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]
    bvars = {(x, y): Bool("v{};{}".format(x, y)) for x, y in poss}

    solver = Solver()
    constraints_all(puzzle, solver, poss, bvars)

    return poss, bvars, solver


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
    poss, bvars, solver = _initialize(puzzle)
    start = time.time()

    solutions = []
    while (number is None or len(solutions) < number) and solver.check() == sat:
        solution = [(x, y) for (x, y) in poss if solver.model()[bvars[x, y]]]
        solutions.append(solution)
        solver.add(Not(And([bvars[x, y] for (x, y) in solution])))

    end = time.time()
    return solutions, end - start
