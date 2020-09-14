#include "puzzle.h"

static void preprocess(const Puzzle &puzzle, Solution &solution)
{
	//TODO: Place all of the lights which can be placed for sure.
}

static void backtrack(const Puzzle &puzzle, Solution &solution)
{

}

static void postprocess(const Puzzle &puzzle, Solution &solution)
{
	//TODO: Prepare and call the backtrack function.
}

Solution solve_backtrack(const Puzzle &puzzle)
{
	//solution.push_back(Pos{1, 2});
	Solution solution;

	preprocess (puzzle, solution);
	postprocess(puzzle, solution);

	return solution;
}
