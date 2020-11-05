from z3solver import z3solves
from clauses import *
from loader import loadverify
from printer import display


FOLDER = 'misc/verified'


def verify_clause(gadget, inputs, outputs, clause):
    given_trues  = []  # given to z3,  needs to be true
    given_falses = []  # given to z3,  needs to be false
    check_trues  = []  # for checking, needs to be true
    check_falses = []  # for checking, needs to be false

    # The only info given to z3 is if the (sending, x) input (not the
    # receiving input, x') needs to be true or false.
    for index, value in enumerate(clause[0]):
        if value:
            given_trues.append(inputs[index][0])
            check_falses.append(inputs[index][1])
        else:
            given_falses.append(inputs[index][0])
            check_trues.append(inputs[index][1])

    # Add all the output fields to be checked after solving the gadget.
    for index, value in enumerate(clause[1]):
        if value:
            check_trues.append(outputs[index][0])
            check_falses.append(outputs[index][1])
        else:
            check_falses.append(outputs[index][0])
            check_trues.append(outputs[index][1])

    solutions = z3solves(gadget, trues=given_trues, falses=given_falses)

    if len(solutions) == 0:
        return False

    for solution in solutions:
        if any(t not in solutions[0] for t in check_trues) or \
           any(f     in solutions[0] for f in check_falses):
            return False
    return True


def verify_gadget(proof, name):
    gadget, inputs, outputs = loadverify(f'{FOLDER}/{proof}/{name}')
    for clause in CLAUSES[name]:
        if verify_clause(gadget, inputs, outputs, clause):
            print(f'CORRECT {proof}/{name}')
        else:
            print(f'INCORRECT {proof}/{name}')
            return False
    return True


def verify_proof(proof):
    return all(verify_gadget(proof, name) for name in GADGETS)


def verify_all():
    if all(verify_proof(proof) for proof in range(1,4)):
        print("All gadgets are CORRECT!")
        return True
    else:
        return False
