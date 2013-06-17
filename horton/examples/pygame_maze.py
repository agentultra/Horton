import pygame
import random

from copy import copy
from functools import partial
from horton.grid import Grid
from horton.render.pg import render_grid
from pygame.locals import *


SCREEN_W, SCREEN_H = (640, 480)
SCREEN_BLANK_COLOUR = (255, 255, 255)
MAZE_W, MAZE_H = (400, 400)
MAZE_ROWS, MAZE_COLS = (40, 40)
MAZE_WALL_COLOUR = (0, 0, 0)
FONT_COLOUR = (0, 0, 255)


# We can store any Python object in a Grid.  Most maze generation
# algorithms use a cell object with four "walls" in the typical
# cardinal directions.

default_cell = {'north': True,
                'south': True,
                'east': True,
                'west': True,
                'visited': False}

# We then need to tell Horton's pygame renderer how to draw our Cell
# objects.  Horton just needs a function that takes a
# pygame.surface.Surface, a cell object from the Grid, and some
# arguments to tell it where to draw the cell: x, y, width, and
# height.  We pass this function to render_grid.

def draw_maze_cell(surface, cell, x, y, width, height):
    draw_line = partial(pygame.draw.line, surface, MAZE_WALL_COLOUR)
    if cell['north']:
        draw_line((x, y), (x + width, y), 2)
    if cell['east']:
        draw_line((x + width, y), (x + width, y + height), 2)
    if cell['south']:
        draw_line((x, y + height), (x + width + 1, y + height), 2)
    if cell['west']:
        draw_line((x, y), (x, y + height), 2)


# And of course our maze-generation algorithm...

def unvisited_neighbours(grid, location):
    x, y = location
    offsets = [(0, -1), (1, 0),
               (0, 1), (-1, 0)]
    return [(x + offset_x, y + offset_y)
            for offset_x, offset_y in offsets
            if grid._is_valid_location(x + offset_x,
                                       y + offset_y)
            and grid[x + offset_x, y + offset_y]['visited'] == False]


def remove_wall_between(source, target, grid):
    sx, sy = source
    tx, ty = target

    if sx == tx:
        if sy > ty:
            grid[source]['north'] = False
            grid[target]['south'] = False
        else:
            grid[source]['south'] = False
            grid[target]['north'] = False
    elif sy == ty:
        if sx > tx:
            grid[source]['west'] = False
            grid[target]['east'] = False
        else:
            grid[source]['east'] = False
            grid[target]['west'] = False


def generate_maze():
    grid = Grid(MAZE_ROWS, MAZE_COLS, value=lambda: copy(default_cell))
    stack = []
    current_cell = random.choice(grid.coordinates)
    grid[current_cell]['visited'] = True
    stack.append(current_cell)

    while stack:
        ns = unvisited_neighbours(grid, current_cell)
        if ns:
            n = random.choice(ns)
            remove_wall_between(current_cell, n, grid)
            stack.append(current_cell)
            current_cell = n
            grid[current_cell]['visited'] = True
        else:
            current_cell = stack.pop()

    return grid


def draw_maze(surface, maze):
    screen.fill(SCREEN_BLANK_COLOUR)
    render_grid(screen, maze,
                (SCREEN_W / 2) - (MAZE_W / 2),
                (SCREEN_H / 2) - (MAZE_H / 2),
                MAZE_W, MAZE_H,
                render_cell=draw_maze_cell)

# Demo setup

pygame.init()
pygame.font.init()
pygame.key.set_repeat(100, 50)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
font = pygame.font.Font(None, 18)

running = True
maze = generate_maze()
draw_maze(screen, maze)


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                maze = generate_maze()
            elif event.key == K_RIGHT:
                MAZE_W += 1
            elif event.key == K_LEFT:
                if MAZE_W > 1:
                    MAZE_W -= 1
            elif event.key == K_UP:
                MAZE_H += 1
            elif event.key == K_DOWN:
                if MAZE_H > 1:
                    MAZE_H -= 1
            draw_maze(screen, maze)

    grid_w = font.render("MAZE_W: %s" % MAZE_W, True, FONT_COLOUR)
    grid_h = font.render("MAZE_H: %s" % MAZE_H, True, FONT_COLOUR)
    screen.blit(grid_w, (0, SCREEN_H - 40))
    screen.blit(grid_h, (0, SCREEN_H - 25))
    pygame.display.flip()


pygame.quit()
