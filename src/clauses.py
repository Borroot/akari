""" These clauses describe what is the expected output for a given input. """

NOT = \
    [[[ True], [False]],
     [[False], [ True]]]


OR = \
    [[[False, False], [False]],
     [[False,  True], [ True]],
     [[ True, False], [ True]],
     [[ True,  True], [ True]]]


SPLIT = \
    [[[False], [False, False]],
     [[ True], [ True,  True]]]


TRUE = \
    [[[True], []]]


WIRES = \
    [[[False], [False]],
     [[ True], [ True]]]


CLAUSES = {'not':NOT, 'or':OR, 'split':SPLIT, 'true':TRUE, 'wires':WIRES}
GADGETS = ['not', 'or', 'split', 'true', 'wires']
