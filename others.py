"""

 MCO1: Maze Bot
 
 @author Rain David
 @author Gio Estrada
 @author Salvador Lapuz
 @author Audrea Tabadero
 @since   2023-02-28 

 Contains all other functions related to construction of GUI and the likes. 

 External Modules/Libraries Needed:
 - pygame (used for GUI)
 
"""

import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import tkinter as tk
from tkinter import filedialog

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,128)
ORANGE = (255,165,0)
PURPLE = (128,0,128)
DARK_GREEN = (0,154,68)
DARK_RED = (128,5,0)

#Node class for indiv cell
class Node:
    def __init__(self, row, col, width, total_rows, text):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.text = text

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
    
    def make_text(self, text):
        self.text = text

    def draw(self, win, coords):
        font = pygame.font.SysFont(None, self.width//2)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        if(self.color!=BLACK):
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.center = (self.x + self.width/2, self.y + self.width/2)
            win.blit(text_surface, text_rect)

        if(coords): # displays coords of individual cell
            font2 = pygame.font.SysFont(None, self.width//3)
            pos = str(self.get_pos())
            colour = BLACK
            if(self.color == BLACK):
                colour= WHITE
            text_surface2 = font2.render(pos, True, colour)
            text_rect2 = text_surface2.get_rect()
            
            text_rect2.bottomleft = (self.x+2, self.y + self.width)

            win.blit(text_surface2, text_rect2)
        
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
def reconstruct_path(came_from, current, draw, win):
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
    count=1
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i,j,gap,rows,"")
            grid[i].append(spot)
            count+=1

    return grid

def draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        pygame.draw.line(win, GREY, (i*gap,0), (i*gap,width))

def draw(win, grid, rows, width, showCoords):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win, showCoords)
    draw_grid(win, rows, width)
    displayInstructions(win)
    pygame.display.update()

# Reads Maze text file
def readMaze():
    path = choose_file("maze.txt")
    # with open(os.path.join(os.path.dirname(__file__), 'maze.txt'), 'r') as f:
    #     lines = f.read().splitlines()
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    return lines

# Displays instructions and specifics of legend
def displayInstructions(win):
    font = pygame.font.SysFont(None, 20)
    font2 = pygame.font.SysFont(None, 25)

    text_surface = font.render("START", True, (255, 255, 255))
    text_surface2 = font.render("GOAL", True, (255, 255, 255))
    text_surface3 = font.render("WALL", True, (255, 255, 255))
    text_surface4 = font.render("CLOSED", True, (255, 255, 255))
    text_surface5 = font.render("OPEN", True, (255, 255, 255))
    text_surface6 = font.render("PATH", True, (255, 255, 255))

    rect_surface = pygame.Surface((60, 50))
    rect_surface.fill((255, 165, 0))

    rect_surface2 = pygame.Surface((60, 50))
    rect_surface2.fill(BLUE)

    rect_surface3 = pygame.Surface((60, 50))
    rect_surface3.fill(BLACK)

    rect_surface4 = pygame.Surface((60, 50))
    rect_surface4.fill(RED)

    rect_surface5 = pygame.Surface((60, 50))
    rect_surface5.fill(GREEN)

    rect_surface6 = pygame.Surface((60, 50))
    rect_surface6.fill(PURPLE)

    text_x = (rect_surface.get_width() - text_surface.get_width()) // 2
    text_y = (rect_surface.get_height() - text_surface.get_height()) // 2
    
    rect_surface.blit(text_surface, (text_x, text_y))
    rect_surface2.blit(text_surface2, (text_x+2, text_y))
    rect_surface3.blit(text_surface3, (text_x+2, text_y))
    rect_surface4.blit(text_surface4, (text_x-6, text_y))
    rect_surface5.blit(text_surface5, (text_x+2, text_y))
    rect_surface6.blit(text_surface6, (text_x+3, text_y))

    text_surface7 = font2.render("SPACE: START", True, BLACK)
    text_surface8 = font2.render("BACKSPACE: CLEAR", True, BLACK)
    text_surface9 = font2.render("C: TOGGLE COORDS", True, BLACK)


    rect_surface7 = pygame.Surface((250, 100))
    rect_surface7.fill(WHITE)
    rect_surface7.blit(text_surface7, (text_x, text_y))
    rect_surface7.blit(text_surface8, (text_x, text_y+20))
    rect_surface7.blit(text_surface9, (text_x, text_y+40))

    
    rect_x = 10
    win.blit(rect_surface, (rect_x, 510))
    win.blit(rect_surface2, (rect_x, 570))
    win.blit(rect_surface3, (rect_x, 630))
    win.blit(rect_surface4, (rect_x+70, 510))
    win.blit(rect_surface5, (rect_x+70, 570))
    win.blit(rect_surface6, (rect_x+70, 630))

    win.blit(rect_surface7, (150, 500))

# Displays whether a path is found or not
def displayInfo(win, check, finalpath):
    font = pygame.font.SysFont(None, 50)

    if not check:
        display_text_and_wait(win, "No Path Found! :(", DARK_RED, "")
    
    else:
        display_text_and_wait(win, "Path Found! :D", DARK_GREEN, finalpath)

def display_text_and_wait(win, text, colour, finalpath):
    font = pygame.font.SysFont(None, 50)
    text_surface = font.render(text, True, colour)
    win.blit(text_surface, (160, 600))

    if(colour==DARK_RED):
        font2 = pygame.font.SysFont(None, 30)
        text_surface2 = font2.render("Quit or Press Enter to continue", True, BLACK)
        win.blit(text_surface2, (160, 650))
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
        font2 = pygame.font.SysFont(None, 30)
        pathstr = str(finalpath)
        finalpathpopup(win, pathstr, len(finalpath))
        text_surface2 = font2.render("Quit or Press Enter to continue", True, BLACK)
        win.blit(text_surface2, (160, 650))
        pygame.display.flip()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
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

# Popup Window for displaying Final Path
def finalpathpopup(win, pathstr, num):
    popup_width = 350
    popup_height = 200
    popup = pygame.Surface((popup_width, popup_height))
    popup.fill((255, 255, 255))  

    font2 = pygame.font.Font(None, 15)

    font_size = 32
    font = pygame.font.Font(None, font_size)

    text = str(pathstr)
    text_surface = font.render(text, True, PURPLE)

    while text_surface.get_width() > 350 or text_surface.get_height() > 200:
        font_size -= 1
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, PURPLE)

    text2 = font2.render("Final Path:", True, (0, 0, 0))
    text_rect2 = text2.get_rect(centerx=popup_width/2, top=50)
    text_rect = text_surface.get_rect(center=popup.get_rect().center, top=text_rect2.bottom + 10)

    cost = "Cost: "
    cost+=str(num)
    text3 = font2.render(cost, True, (0, 0, 0))
    text_rect3 = text3.get_rect(centerx=popup_width/2, top=text_rect.bottom + 10) 
    
    popup.blit(text_surface, text_rect)
    popup.blit(text2, text_rect2)
    popup.blit(text3, text_rect3)


    popup_rect = popup.get_rect(center=(500/2, 700/2))
    win.blit(popup, popup_rect)


    pygame.display.update()