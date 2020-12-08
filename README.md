# Akari
Akari (Light Up) is a logic puzzle with simple rules and challenging solutions. In my Computing Science bachelor thesis I researched this game and variants, specifically I implemented various solvers for Akari and expanded the original NP-completeness proof of Akari to (more restrictive) variants of the game.

# Rules
The rules are simple. Akari is played on a rectangular grid. The grid has both black cells and white cells in it. The objective is to place light bulbs on the grid so that every white square is lit. A cell is illuminated by a light bulb if they're in the same row or column, and if there are no black cells between them. Also, no light bulb may illuminate another light bulb. Some of the black cells have numbers in them. A number in a black cell indicates how many light bulbs share an edge with that cell.

# Solvers
This repository contains a SAT solver implementation for Akari using the Z3 library as well as a backtrack solver and trivial (steps) solver. The trivial solver can often determine where light bulbs need to be placed around a number constraint wall.

# Drawer
This repository contains a drawer for Akari puzzles which draws a nice image representing a certain puzzle instance.

# Verifier
This repository also includes a verifier program which can be used to verify the correctness of the gadgets I made for the NP-completeness proofs of variants on Akari. Let Akari-_n_ be a variant of Akari which only contains walls without number constraint and walls with the number constraint _n_. I proved that Akari without any number constraint walls and Akari-4 is in P. I proved that Akari-1, Akari-2 and Akari-3 are all NP-complete.
