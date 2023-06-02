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


import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from queue import PriorityQueue
import others as o
import time


pygame.init()
WIDTH1 = 500
HEIGHT1=700
# WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("CSINTSY MCO1: MAZEBOT")

# Function for calculating Heuristic; uses manhattan distance
def h(p1, p2):
    # Manhattan Distance is used as heuristic 
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

# Main Algorithm Function
def a_star(draw, grid, start, end, win):
    # Create list/queue for open nodes
    global finalpath
    count = 0
    open_set = PriorityQueue()
    cell_number=1
    # Adding of Start Node
    open_set.put((0, count, start))

    came_from = {}
    
    # Initializing starting values
    g_score = {spot:float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot:float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # To keep track of whether an item is in the PriorityQueue
    open_set_hash = {start}

    # Loop until the open list is empty
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        # Getting least cost node as open is a priority queue
        current = open_set.get()[2]
        current.make_text(str(cell_number))
        open_set_hash.remove(current)

        # Check if we have reached the goal, return the path (From Current Node to Start Node)
        if current == end:
            finalpath = o.reconstruct_path(came_from, end, draw, win)
            end.make_end()
            start.make_start()
            return True

        # Loop through neighbors of node
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

        # Check if neighbor is in open list and if it has a lower f value
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                # Calculate cost to goal
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], current, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        time.sleep(0.2)           
        draw()
        
        if current!=start:
            current.make_closed()

        cell_number+=1
    # Return False; no path is found
    return False

def main(win, width, lines):
    # reads contents of maze.txt file
    maze = lines
    
    dim1= int(maze[0]) # sets the dimension/size of maze
    maze.pop(0) # removes size from list for easier reading
        
    ROWS = dim1
    grid = o.make_grid(ROWS, width)

    start = None
    end = None

    run = True

    coords_visible = False

    #change font size mejo done

    while run:
        o.draw(win, grid, ROWS, width, coords_visible)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Creates Maze; placing of barriers, start, and goal
            for x in range(dim1):
                for y in range(dim1):
                    # print(lines[x][y])
                    if(maze[x][y] == "#"): 
                        grid[y][x].make_barrier()
                    if(maze[x][y] == "G"):
                        end = grid[y][x]
                        grid[y][x].make_end()
                    if(maze[x][y]=="S"):
                        start = grid[y][x]
                        grid[y][x].make_start()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    # running of actual algo
                    check= a_star(lambda: o.draw(win, grid, ROWS, width, coords_visible), grid, start, end, win)
                    o.draw(win, grid, ROWS, width, coords_visible)
                    if not check: # no path
                        o.displayInfo(win, check, "")
                        print("No Path/Solution Found!")
                    else: # path is found
                        o.displayInfo(win, check, finalpath)
                        
                
                # toggles coords
                if event.key == pygame.K_c:
                    coords_visible = not coords_visible

                # clear
                if event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    grid = o.make_grid(ROWS, width)
    

    pygame.quit()

def run(lines):
    WIN1 = pygame.display.set_mode((500,700))
    main(WIN1, 500, lines)
