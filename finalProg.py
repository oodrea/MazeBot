"""

 MCO1: Maze Bot
 
 @author Rain David
 @author Gio Estrada
 @author Salvador Lapuz
 @author Audrea Tabadero
 @since   2023-02-28 

 Contains Main Program and Algorithm(+Heuristic) Functions.

 External Modules/Libraries Needed:
 - pygame (used for GUI)

"""

import runMe as r
import runMeLarge as r2
import others as o

lines = o.readMaze()
n= int(lines[0]) 

if n > 15:
    r2.run2(lines)
elif n<15:
    r.run(lines)