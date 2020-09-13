#include <iostream>
#include <string>
#include "debug.h"
#include "puzzle.h"
#include "read.h"

using namespace std;

int main(void)
{
	string codex = read("misc/7x7_easy", 0);
	Puzzle puzzle = convert(codex, 7, 7);
	cout << puzzle << endl;

	return 0;
}
