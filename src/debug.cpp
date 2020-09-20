#include <iostream>
#include "puzzle.h"

ostream &operator<<(ostream &out, const Cell &cell)
{
	switch (cell) {
		case ZERO:  out << "0"; break;
		case ONE:   out << "1"; break;
		case TWO:   out << "2"; break;
		case THREE: out << "3"; break;
		case FOUR:  out << "4"; break;
		case EMPTY: out << "."; break;
		case LIGHT: out << "X"; break;
		case BLACK: out << "B"; break;
	}
	return out;
}

ostream &operator<<(ostream &out, const Puzzle &puzzle)
{
	for (int i = 0; i < (int)puzzle.size(); i++) {
		for (int j = 0; j < (int)puzzle[i].size(); j++) {
			out << puzzle[i][j] << " ";
		}
		out << endl;
	}
	return out;
}

ostream &operator<<(ostream &out, const Pos &pos)
{
	out << "(" << pos.x << "," << pos.y << ")";
	return out;
}
