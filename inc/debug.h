#ifndef DEBUG_H_
#define DEBUG_H_

#include <iostream>
#include "puzzle.h"

using namespace std;

template <class T>
ostream &operator<<(ostream &out, const vector<T> &vector)
{
	out	<< "[";
	for (int i = 0; i < (int)vector.size(); i++) {
		out << vector[i];
		if (i < (int)vector.size() - 1) {
			out << ",";
		}
	}
	out << "]" << endl;
	return out;
}

ostream &operator<<(ostream &out, const Cell &cell);
ostream &operator<<(ostream &out, const Puzzle &puzzle);
ostream &operator<<(ostream &out, const Pos &pos);

#endif
