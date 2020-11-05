from z3 import *
import time

from constants import *
from constraints import constraints_all


def _initialize(puzzle):
    """ Initialize some usefull lists. """
    poss = [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]
    bvars = {(x, y): Bool("v{};{}".format(x, y)) for x, y in poss}
    return poss, bvars


def _solver(constraints):
    """ Initialize the solver with all the constraints. """
    solver = Solver()
    for constraint in constraints:
        solver.add(constraint)
    return solver


def z3unique(puzzle, trues=[], falses=[]):
    """ Check if the given puzzle has exactly one unique solution using z3. """
    solutions = z3solves(puzzle, 2, trues, falses=[])
    return len(solutions) == 1 if len(solutions) > 0 else None


def z3solve(puzzle, trues=[], falses=[]):
    """ Search for one solution for the given puzzle using z3. """
    solutions = z3solves(puzzle, 1, trues, falses)
    return solutions[0] if len(solutions) == 1 else None


def z3solves(puzzle, number=None, trues=[], falses=[]):
    """ Search for the given number of solutions for the given puzzle using z3,
    if no number is given then all solutions will be returned. The trues
    variable contains positions where light bulbs need to be placed, falses
    contains positions where no light bulb is allowed. """
    poss, bvars = _initialize(puzzle)

    constraints = constraints_all(puzzle, poss, bvars)
    constraints.append(And([bvars[x, y] for (x, y) in trues]))
    constraints.append(Not(Or([bvars[x, y] for (x, y) in falses])))

    solver = _solver(constraints)
    solutions = []
    while (number is None or len(solutions) < number) and solver.check()==sat:
        solution = [(x, y) for (x, y) in poss if solver.model()[bvars[x, y]]]
        solutions.append(solution)
        constraints.append(Not(And([bvars[x, y] for (x, y) in solution])))
        solver = _solver(constraints)

    return solutions
