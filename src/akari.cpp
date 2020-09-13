#include <iostream>
#include <string>
#include "debug.h"
#include "puzzle.h"
#include "read.h"
#include "backtrack.h"

using namespace std;

int main(void)
{
	string codex = read("misc/7x7_easy", 0);
	Puzzle puzzle = convert(codex, 7, 7);
	Solution solution = solve_backtrack(puzzle);
	cout << puzzle << solution;

	return 0;
}
