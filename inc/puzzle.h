#ifndef PUZZLE_H_
#define PUZZLE_H_

#include <vector>

using namespace std;

enum Cell {ZERO, ONE, TWO, THREE, FOUR, EMPTY, LIGHT, BLACK};
typedef vector<vector<Cell>> Puzzle;

#endif
