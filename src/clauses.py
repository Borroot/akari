NOT =
    [[[ True], [False]],
     [[False], [ True]]]


OR =
    [[[False, False], [False]],
     [[False,  True], [ True]],
     [[ True, False], [ True]],
     [[ True,  True], [ True]]]


SPLIT =
    [[[False], [False, False]],
     [[ True], [ True,  True]]]


TRUE =
    [[[True], []]]


WIRES =
    [[[False], [False]],
     [[ True], [ True]]]


ALL = {'not':NOT, 'or':OR, 'split':SPLIT, 'true':TRUE, 'wires':WIRES}
