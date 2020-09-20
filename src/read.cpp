#include <fstream>
#include <string>
#include "read.h"
#include "puzzle.h"

using namespace std;

/**
 * @brief Read from a file the line corresponding to the index given.
 */
string read(const string &filename, int index)
{
	ifstream file(filename.c_str());
	string codex;

	for (int i = 0; i < index; i++) {
		getline(file, codex);
	}
	getline(file, codex);
	file.close();

	return codex;
}

/**
 * @brief Convert the codex to an actual puzzle structure.
 *
 * `B' stands for a wall without number, 0-4 stands for a wall with the
 * corresponding number, a-z stands for consecutive empty cells reading from
 * top left to bottom right with a being 1, b is 2, etc.
 */
Puzzle convert(const string &codex, unsigned int rows, unsigned int columns)
{
	Puzzle puzzle(rows, vector<Cell>(columns));

	int count = 0;
	for (int index = 0; index < (int)codex.size(); index++) {
		char c = codex[index];
		switch (c) {
			case 'B':
				puzzle[count / rows][count % columns] = BLACK;
				count++;
				break;
			case '0':
			case '1':
			case '2':
			case '3':
			case '4':
				puzzle[count / rows][count % columns] = Cell(c - '0');
				count++;
				break;
			default:
				do {
					puzzle[count / rows][count % columns] = EMPTY;
					count++;
				} while (c-- > 'a');
		}
	}

	return puzzle;
}
