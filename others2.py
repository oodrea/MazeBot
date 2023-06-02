"""

 MCO1: Maze Bot
 
 @author Rain David
 @author Gio Estrada
 @author Salvador Lapuz
 @author Audrea Tabadero
 @since   2023-02-28 

 Contains all other functions related to construction of GUI and the likes. 
 Used for large mazes (n > 15).

 External Modules/Libraries Needed:
 - pygame (used for GUI)
 
"""

import datetime
import sys
from tkinter import filedialog
import pygame
import os
import tkinter as tk

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,128)
ORANGE = (255,165,0)
TURQUOISE = (64,224,108)
PURPLE = (128,0,128)
DARK_GREEN = (0,154,68)
DARK_RED = (128,5,0)


#Node class for indiv cell
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == BLUE

    def reset(self):
        self.color = WHITE

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = BLUE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other):
        return False

# Constructs Final Path if meron
def reconstruct_path(came_from, current, draw):
    path=[]
    while current in came_from:
        current = came_from[current]
        current.make_path()
        path.append(current.get_pos())
        draw()
    path.reverse()
    # print("Final Path:{}\nPath Cost: {}".format(path, len(path)))
    return path

# Building of grid     
def make_grid(rows, width):
    grid = []
    gap = width//rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i,j,gap,rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        pygame.draw.line(win, GREY, (i*gap,0), (i*gap,width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

# Reads Maze text file
def readMaze():
    path = choose_file("maze.txt")
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    return lines

# For saving result text file
def write_text_to_file(text, n):
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"path{n}-{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(text)
    return filename

# Popup if path does not exist
def finalpathpopupNopath(win):
    popup_width = 350
    popup_height = 200
    popup = pygame.Surface((popup_width, popup_height))
    popup.fill((255, 255, 255))  

    font2 = pygame.font.Font(None, 32)

    text2 = font2.render("No Path Found! :(", True, DARK_RED)
    text_rect2 = text2.get_rect(centerx=popup_width/2, top=50)

    text3 = font2.render("Quit or Press Enter to Continue", True, (0, 0, 0))
    text_rect3 = text3.get_rect(centerx=popup_width/2, top=100)
    
    popup.blit(text2, text_rect2)
    popup.blit(text3, text_rect3)



    popup_rect = popup.get_rect(center=(500/2, 700/2))
    win.blit(popup, popup_rect)


    pygame.display.update()

# Popup if path exists
def finalpopup(win):
    popup_width = 350
    popup_height = 200
    popup = pygame.Surface((popup_width, popup_height))
    popup.fill((255, 255, 255))  

    font2 = pygame.font.Font(None, 32)
    font3 = pygame.font.Font(None, 28)

    text2 = font2.render("Path Found! :D", True, DARK_GREEN)
    text_rect2 = text2.get_rect(centerx=popup_width/2, top=50)

    text3 = font3.render("Press P to Save Final Path", True, (0, 0, 0))
    text_rect3 = text3.get_rect(centerx=popup_width/2, top=100)

    text4 = font3.render("Quit or Press Enter to Continue", True, (0, 0, 0))
    text_rect4 = text4.get_rect(centerx=popup_width/2, top=150)
    
    popup.blit(text2, text_rect2)
    popup.blit(text3, text_rect3)
    popup.blit(text4, text_rect4)



    popup_rect = popup.get_rect(center=(500/2, 500/2))
    win.blit(popup, popup_rect)


    pygame.display.update()

# Displays whether a path is found or not
def displayInfo(win, check, finaltext,n):
    if check:
        display_text_and_wait(win, DARK_GREEN, finaltext,n)
    else:
        display_text_and_wait(win, DARK_RED, finaltext,n)

def display_text_and_wait(win, colour, finaltext, n):
    if(colour==DARK_RED):
        finalpathpopupNopath(win)
        pygame.display.flip()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_RETURN:
                    break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    if(colour==DARK_GREEN):
        finalpopup(win)
        pygame.display.flip()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_p:
                    write_text_to_file(finaltext, n)
                    break
                if event.key== pygame.K_RETURN:
                    break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Selecting only files named "maze.txt"
def choose_file(filename):
    root = tk.Tk()
    root.withdraw() # hide root window
    
    currdir = os.getcwd()
    file_path = filedialog.askopenfilename(initialdir=currdir, title="Open maze.txt",
                                           filetypes=((f"{filename} files", f"*{filename}"), ("all files", "*.*")))
    
    return file_path
