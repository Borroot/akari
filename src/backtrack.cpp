#include "puzzle.h"

static void preprocess(Puzzle &puzzle, Solution &solution)
{

	//solution.push_back(Pos{1, 2});
}

Solution solve_backtrack(const Puzzle &puzzle)
{
	Solution solution;
	// TODO: make a copy of the puzzle which can be altered.

	preprocess(puzzle, solution);
	return solution;
}
