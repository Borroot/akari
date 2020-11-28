from constraints import constraints_all
from z3 import *
import z3solver
from loader import loadverify
from printer import display


FOLDER = 'misc/verified'


GADGETS = ['not', 'or', 'split', 'true', 'wires']
Neq = lambda a, b: Or(And(a, Not(b)), And(Not(a), b))


def gadget_clause(name, inps, outs, bvars):
    """ Return a constraint specific for this gadget. """
    if name == 'not':
        return Neq(bvars[inps[0]], Not(bvars[outs[0]]))
    if name == 'or':
        return Neq(Or(bvars[inps[0]], bvars[inps[1]]), bvars[outs[0]])
    if name == 'split':
        return Or(Neq(bvars[inps[0]], bvars[outs[0]]), \
                  Neq(bvars[inps[0]], bvars[outs[1]]))
    if name == 'true':
        return Not(bvars[inps[0]])
    if name == 'wires':
        return Neq(bvars[inps[0]], bvars[outs[0]])


def verify_z3(gadget, name, inputs, outputs):
    """ Check if a given gadget is according to its specification. """
    poss, bvars = z3solver._initialize(gadget)
    constraints = constraints_all(gadget, poss, bvars)

    # Make sure that for every variable x we have x != x'.
    for var in inputs + outputs:
        constraints.append(Neq(bvars[var[0]], bvars[var[1]]))

    # Take out all x', for simplicity we now only construct with x.
    inputs  = [inp[0] for inp in inputs]
    outputs = [out[0] for out in outputs]

    constraints.append(gadget_clause(name, inputs, outputs, bvars))
    return z3solver._solver(constraints).check() == unsat


def verify_gadget(proof, name):
    """ Verify if all clauses for the given gadget are satisfied. """
    gadget, inputs, outputs = loadverify(f'{FOLDER}/{proof}/{name}')
    if verify_z3(gadget, name, inputs, outputs):
        print(f'CORRECT {proof}/{name}')
        return True
    else:
        print(f'INCORRECT {proof}/{name}')
        return False


def verify_proof(proof):
    """ Verify if all the gadgets for the given proof are satisfied. """
    return all(verify_gadget(proof, name) for name in GADGETS)


def verify_all():
    """ Verify if all the proofs are correct. """
    if all(verify_proof(proof) for proof in range(1,4)):
        print("All the gadgets are CORRECT!")
        return True
    else:
        return False
