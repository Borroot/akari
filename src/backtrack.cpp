#include "puzzle.h"

static void preprocess(const Puzzle &puzzle, vector<Solution> &solutions)
{
	//TODO: Place all of the lights which can be placed for sure.
}

static void backtrack(const Puzzle &puzzle, vector<Solution> &solutions)
{
	//TODO: Run the actual backtracking algorithm.
}

static void process(const Puzzle &puzzle, vector<Solution> &solutions)
{
	//TODO: Prepare and call the backtrack function.
}

vector<Solution> solve_backtrack(const Puzzle &puzzle)
{
	//solution.push_back(Pos{1, 2});
	vector<Solution> solutions;

	preprocess(puzzle, solutions);
	process(puzzle, solutions);

	return solutions;
}
