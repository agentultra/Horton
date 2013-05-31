import pygame
import random

from horton.grid import Grid

import enemy

MAZE_ROWS, MAZE_COLS = (10, 10)
MAZE_W, MAZE_H = (500, 500)

default_cell = {'north': True,
                'south': True,
                'east': True,
                'west': True,
                'visited': False}


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
    grid = Grid(MAZE_ROWS, MAZE_COLS, value=default_cell)
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


def draw_maze_tile(surface, tile, x, y, width, height):
    """
    Draw the cell's tile to the surface.
    """
    tile['draw'](surface, x, y, width, height)


def draw_wall_tile(surface, x, y, width, height):
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(x, y, width, height))


def draw_floor_tile(surface, x, y, width, height):
    pygame.draw.rect(surface, (180, 180, 180), pygame.Rect(x, y, width, height))


def tile_maze(maze):
    """
    Return a tile-based maze from a cell-based maze.

    The `maze` object is a Grid whose cells have four 'walls'. This
    function translates that Grid into a new grid that is tile-based.
    Each tile in the new grid is a distinct type: wall, floor, etc.
    """
    tiles = {'wall': {'draw': draw_wall_tile,
                      'passable': False},
             'floor': {'draw': draw_floor_tile,
                       'passable': True,
                       'objects': []}}
    m_width, m_height = maze.dimensions
    tile_maze = Grid((m_width * 2) + 1, (m_height * 2) + 1, value=tiles['wall'])
    for i in xrange(maze.width):
        for j in xrange(maze.height):
            maze_cell = maze[i, j]
            tile_maze[(i * 2) + 1, (j * 2) + 1] = tiles['floor']
            for d, v in maze_cell.items():
                if v is False:
                    if d == 'north':
                        tile_maze[(i * 2) + 1, (j * 2)] = tiles['floor']
                    elif d == 'east':
                        tile_maze[(i * 2) + 2, (j * 2) + 1] = tiles['floor']
                    elif d == 'south':
                        tile_maze[(i * 2) + 1, (j * 2) + 2] = tiles['floor']
                    elif d == 'west':
                        tile_maze[(i * 2), (j * 2) + 1] = tiles['floor']
    return tile_maze


def generate_level(depth):
    maze = generate_maze()
    tiled_maze = tile_maze(maze)

    return tiled_maze
