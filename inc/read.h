#ifndef READ_H_
#define READ_H_

#include <string>
#include "puzzle.h"

string read(const string &filename, int index);
Puzzle convert(const string &codex, unsigned int rows, unsigned int columns);

#endif
