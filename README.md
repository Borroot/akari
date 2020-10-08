# Akari
Akari (Light Up) is a logic puzzle with simple rules and challenging solutions.

# Rules
The rules are simple. Akari is played on a rectangular grid. The grid has both black cells and white cells in it. The objective is to place light bulbs on the grid so that every white square is lit. A cell is illuminated by a light bulb if they're in the same row or column, and if there are no black cells between them. Also, no light bulb may illuminate another light bulb. Some of the black cells have numbers in them. A number in a black cell indicates how many light bulbs share an edge with that cell.

# Solvers

## Z3

## Backtracking

# Generation
(Translate and explain the heuristic of choosing cells.)

1. Pak een leeg grid (evt met een aantal random blokjes).
2. Plaats een blokje random op het grid.
3. a. Plaats een lampje op het grid op een onverlichte cell.
   b. Als er nog lege plekken zijn ga naar 3a anders naar 4.
4. Zet in elk blokje het bijbehorende getal.
5. Als de puzzel een unieke oplossing heeft ga naar 6a anders naar 2.
6. a. Verwijder een getal in de blokjes.
   b. Als de puzzel een unieke oplossing heeft ga naar 6a anders naar 7.
7. Undo de laatste blok verwijdering en we hebben een puzzel!
