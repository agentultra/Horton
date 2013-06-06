import operator
import pygame
import random

from copy import deepcopy
from horton.grid import Grid
from horton.render.pg import render_grid

import entities

from utils import average, distance

MAZE_ROWS, MAZE_COLS = (10, 10)
MAZE_W, MAZE_H = (500, 500)

DEPTH_FACTOR = 2

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
    for obj in tile['objects']:
        obj.draw(surface, x, y, width, height)


def draw_wall_tile(surface, x, y, width, height):
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(x, y, width, height))


def draw_floor_tile(surface, x, y, width, height):
    pygame.draw.rect(surface, (180, 180, 180), pygame.Rect(x, y, width, height))


def draw_exit_tile(surface, x, y, width, height):
    pygame.draw.rect(surface, (0, 0, 255), pygame.Rect(x, y, width, height))


def tile_maze(maze):
    """
    Return a tile-based maze from a cell-based maze.

    The `maze` object is a Grid whose cells have four 'walls'. This
    function translates that Grid into a new grid that is tile-based.
    Each tile in the new grid is a distinct type: wall, floor, etc.
    """
    tiles = {'wall': {'draw': draw_wall_tile,
                      'passable': False,
                      'objects': []},
             'floor': {'draw': draw_floor_tile,
                       'passable': True,
                       'objects': []}}
    m_width, m_height = maze.dimensions
    tile_maze = Grid((m_width * 2) + 1, (m_height * 2) + 1, value=tiles['wall'])
    for i in xrange(maze.width):
        for j in xrange(maze.height):
            maze_cell = maze[i, j]
            tile_maze[(i * 2) + 1, (j * 2) + 1] = deepcopy(tiles['floor'])
            for d, v in maze_cell.items():
                if v is False:
                    if d == 'north':
                        tile_maze[(i * 2) + 1, (j * 2)] = deepcopy(tiles['floor'])
                    elif d == 'east':
                        tile_maze[(i * 2) + 2, (j * 2) + 1] = deepcopy(tiles['floor'])
                    elif d == 'south':
                        tile_maze[(i * 2) + 1, (j * 2) + 2] = deepcopy(tiles['floor'])
                    elif d == 'west':
                        tile_maze[(i * 2), (j * 2) + 1] = deepcopy(tiles['floor'])
    return tile_maze


def enemies_for_depth(depth):
    return [entities.Enemy()
            for _ in range(random.randint(depth + 1,
                                          (depth * DEPTH_FACTOR) + 1))]


def place_enemies_randomly(level, depth):
    level.enemies = enemies_for_depth(depth)
    for enemy in level.enemies:
        while enemy.position == (0, 0):
            random_point = (random.randint(1, level.width - 1),
                            random.randint(1, level.height - 1))
            random_location = level.get(*random_point)
            if random_location['passable'] and len(random_location['objects']) == 0:
                random_location['objects'].append(enemy)
                enemy.position = random_point


def place_player_at_start(level):
    """
    Place the Player in the starting position for the level.

    Choose a location along an edge of the map that is furthest from
    all of the enemies.
    """
    p = entities.Player()
    edge_tiles = set([])
    for x in range(1, level.width):
        n, s = (x, 1), (x, level.height - 1)
        if level[n]['passable']:
            edge_tiles.add(n)
        if level[s]['passable']:
            edge_tiles.add(s)
    for y in range(1, level.height):
        w, e = (1, y), (level.width - 1, y)
        if level[w]['passable']:
            edge_tiles.add(w)
        if level[e]['passable']:
            edge_tiles.add(e)

    enemy_edge_distances = []
    for coordinate in edge_tiles:
        enemy_edge_distances.append((coordinate,
                                     average(*[distance(coordinate, enemy.position)
                                               for enemy in level.enemies])))

    enemy_edge_distances.sort(key=operator.itemgetter(1), reverse=True)
    start_position = enemy_edge_distances[0][0]
    p.position = start_position
    level.player = p
    level[start_position]['objects'].append(p)


def place_exit(level):
    """
    Place the exit tile somewhere on the opposite side of the level
    from the player.
    """
    pos = (-level.player.x % level.width, -level.player.y % level.height)
    print(pos)


def satisfactory_placement(level):
    """
    Return True if the placement of the enemies in relation to the
    player meets our requirements.

    A satisfactory placement consists of the following rules:
      - There is no enemy within a 5-tile radius of the player
      - There is no object in a 1 tile radius of an enemy
    """
    p_pos = level.player.position
    p_coords = [(x, y)
                for x in range(p_pos[0] - 2, p_pos[0] + 3)
                for y in range(p_pos[1] - 2, p_pos[1] + 3)
                if level._is_valid_location(x, y)
                and level[x, y]['passable']
                and (x, y) != p_pos]
    if any([level[coord]['objects'] for coord in p_coords]):
        return False

    for enemy in level.enemies:
        e_pos = enemy.position
        e_coords = [(x, y)
                    for x in range(e_pos[0] - 1, e_pos[0] + 2)
                    for y in range(e_pos[1] - 1, e_pos[1] + 2)
                    if level._is_valid_location(x, y)
                    and level[x, y]['passable']
                    and (x, y) != e_pos]
        if any([level[coord]['objects'] for coord in e_coords]):
            return False
    return True


def clear_level(level):
    level.enemies = []
    level.player = None
    level.exit = None
    for tile in level:
        tile['objects'] = []


def generate_level(depth):
    maze = generate_maze()
    level = tile_maze(maze)
    level.placement_finished = False

    while not level.placement_finished:
        place_enemies_randomly(level, depth)
        place_player_at_start(level)
        place_exit(level)
        if satisfactory_placement(level):
            level.placement_finished = True
        else:
            clear_level(level)

    return level


def render_level(surface, level):
    render_grid(surface, level,
                0, 0, MAZE_W, MAZE_H,
                render_cell=draw_maze_tile)
