"""

 MCO1: Maze Bot
 
 @author Rain David
 @author Gio Estrada
 @author Salvador Lapuz
 @author Audrea Tabadero
 @since   2023-02-28 

 Contains Main Program and Algorithm(+Heuristic) Functions.
 Used for large mazes (n > 15).

 External Modules/Libraries Needed:
 - pygame (used for GUI)

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from queue import PriorityQueue
import others2 as o2

pygame.init()
WIDTH = 500
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("CSINTSY MCO1: MAZEBOT")

# Function for calculating Heuristic; uses manhattan distance
def h(p1, p2):
    # Manhattan Distance is used as heuristic 
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

# Main Algorithm Function
def a_star(draw, grid, start, end):
    # Create list/queue for open nodes
    global finalpath
    count = 0
    open_set = PriorityQueue()

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
        open_set_hash.remove(current)

        # Check if we have reached the goal, return the path (From Current Node to Start Node)
        if current == end:
            finalpath = o2.reconstruct_path(came_from, end, draw)
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
                    
        draw()
        
        if current!=start:
            current.make_closed()

    # Return False; no path is found
    return False

def text1():
    decay_font = pygame.font.SysFont('Comic Sans MS', 36)
    text_surface = decay_font.render('Tanginamo', True,(255,0,0))
    WIN.blit(text_surface, (WIDTH/4, WIDTH/4))

def main(win, width, lines):
    #reads contents of maze.txt file
    maze = lines
    
    dim1= int(maze[0]) #sets the dimension/size of maze
    maze.pop(0) #removes size from list for easier reading
        
    ROWS = dim1
    grid = o2.make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        o2.draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Creates Maze; placing of barriers, start, and goal
            for x in range(dim1):
                for y in range(dim1):
                    # print(lines[x][y])
                    if(maze[y][x] == "#"): 
                        grid[x][y].make_barrier()
                    if(maze[y][x] == "G"):
                        end = grid[x][y]
                        grid[x][y].make_end()
                    if(maze[y][x]=="S"):
                        start = grid[x][y]
                        grid[x][y].make_start()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    check = a_star(lambda: o2.draw(win, grid, ROWS, width), grid, start, end)
                    if check:
                        finaltext = "n = " +str(dim1)+"\n"
                        finaltext += "Final Path: "+ str(finalpath)
                        finaltext+="\nCost: " + str(len(finalpath))
                        # print(finaltext)
                        o2.displayInfo(win, check, finaltext,dim1)
                    else:
                        o2.displayInfo(win, check, "",dim1)

                # clear
                if event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    grid = o2.make_grid(ROWS, width)

    pygame.quit()

def run2(lines):
    main(WIN, WIDTH, lines)