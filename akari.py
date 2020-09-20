from z3 import *
import time

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
L = -1
B = 5
N = 6

def read(filename, index):
    with open(filename) as fp:
        for i, line in enumerate(fp):
            if i == index:
                return line
        return

def convert(codex, height, width):
    puzzle = [list(range(width)) for _ in range(height)]

    count = 0
    for c in codex:
        if c == 'B':
            puzzle[count // height][count % width] = B
            count += 1
        elif c in '01234':
            puzzle[count // height][count % width] = ord(c) - ord('0')
            count += 1
        else:
            while c >= 'a':
                puzzle[count // height][count % width] = N
                count += 1
                c = chr(ord(c) - 1)

    return puzzle

def constraints_wall(puzzle, solver, bvars, x, y):
    number = puzzle[y][x]

    neighbours = []
    for dx, dy in DIRECTIONS:
        newx, newy = x + dx, y + dy
        if 0 <= newy < len(puzzle) and 0 <= newx < len(puzzle[0]):
            neighbours.append((bvars[newx, newy], 1))

    solver.add(PbEq(neighbours, number))

def constraints_walls(puzzle, solver, bvars, positions):
    walls = [(x, y) for (x, y) in positions if puzzle[y][x] != N and puzzle[y][x] != B]
    for x, y in walls:
        constraints_wall(puzzle, solver, bvars, x, y)

def constraints_lines(puzzle, solver, bvars, positions):
    for x, y in [(x, y) for (x, y) in positions if puzzle[y][x] == N]:
        lightup = [(bvars[x, y], 1)]  # make sure every cell is light up

        for dx, dy in DIRECTIONS:
            mostone = [(bvars[x, y], 1)]  # make sure no light bulbs cross each other

            newx, newy = x + dx, y + dy
            while 0 <= newy < len(puzzle) and 0 <= newx < len(puzzle[0]) and puzzle[newy][newx] == N:
                lightup.append((bvars[newx, newy], 1))
                mostone.append((bvars[newx, newy], 1))
                newx, newy = newx + dx, newy + dy

            if len(mostone) > 1:
                solver.add(PbLe(mostone, 1))

        solver.add(PbGe(lightup, 1))

def constraints_all(puzzle, solver, positions, bvars):
    constraints_walls(puzzle, solver, bvars, positions)
    constraints_lines(puzzle, solver, bvars, positions)

def show(puzzle, model, bvars):
    inv_bvars = {v: k for k, v in bvars.items()}

    for y, row in enumerate(puzzle):
        for x, cell in enumerate(row):
            if model[bvars[x, y]]:
                print('X', end='')
            elif puzzle[y][x] == N:
                print('.', end='')
            elif puzzle[y][x] == B:
                print('B', end='')
            else:
                print(puzzle[y][x], end='')
            print(' ', end='')
        print()

def main():
    codex = read('misc/25x25_hard', 0)
    puzzle = convert(codex, 25, 25)

    positions = [(x, y) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]
    bvars = {(x, y): Bool("v{};{}".format(x, y)) for x, y in positions}

    solver = Solver()
    constraints_all(puzzle, solver, positions, bvars)

    start = time.time()
    result = solver.check()
    end = time.time()
    print(result, end - start)

    if result == sat:
        model = solver.model()
        show(puzzle, model, bvars)

if __name__ == '__main__':
    main()
