#include "puzzle.h"

static void preprocess(Puzzle &puzzle, Solution &solution)
{

	//solution.push_back(Pos{1, 2});
}

Solution solve_backtrack(const Puzzle &puzzle)
{
	Solution solution;
	preprocess(puzzle, solution);
	return solution;
}
