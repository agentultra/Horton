"""
conway.py: An implementation of Conway's Game of Life

This module uses Python dictionaries to represent the world.  Keys in
this dictionary are integer coordinates on a two-dimensional Cartesian
plane while the values are either 0 or 1 for representing a dead or
alive cell respectively.

There is a convenient generator for iterating over successive
generations starting from a seed world (see the 'generations'
function).

However if you want to run the simulation your own way the function to
use is the 'step' function.

TODO: Allow the edges of the world to wrap around.

Copyright (C) 2012  James King

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "James King <james@agentultra.com>"
__version__ = "0.1.0"


from collections import namedtuple
from copy import deepcopy
from functools import partial


Coordinate = namedtuple("Coordinate", "x y")


def get_at(world, coord):
    try:
        return world[coord.y][coord.x]
    except KeyError:
        y, x = (coord.y, coord.x)
        if y < 0:
            y = max(world.keys())
        elif y > max(world.keys()):
            y = 0
        if x < 0:
            x = max(world[0].keys())
        elif x > max(world[0].keys()):
            x = 0
        return world[y][x]


def coordinates(world):
    """ Yield each Coordinate and cell from world.

    >>> world = {0: {0: 0, 1: 1, 2: 0},
    ...          1: {0: 1, 1: 1, 2: 1},
    ...          2: {0: 0, 1: 1, 2: 0}}
    >>> for coord, cell in coordinates(world):
    ...     print coord, cell
    Coordinate(x=0, y=0) 0
    Coordinate(x=1, y=0) 1
    Coordinate(x=2, y=0) 0
    Coordinate(x=0, y=1) 1
    Coordinate(x=1, y=1) 1
    Coordinate(x=2, y=1) 1
    Coordinate(x=0, y=2) 0
    Coordinate(x=1, y=2) 1
    Coordinate(x=2, y=2) 0
    """
    # TODO: There's the possibility this test may fail occasionally
    # due to dict ordering.
    for y, row in world.items():
        for x, cell in row.items():
            yield Coordinate(x, y), cell


def neighbours(world, coord):
    """
    Return the number of neighbours at a coordinate in the world.

    A neighbour is defined as the integer '1' in directly adjacent
    coordinates in the eight cardinal directions.  The world wraps
    around at the poles.

    >>> world = {0: {0: 0, 1: 1, 2: 0, 3: 0},
    ...          1: {0: 1, 1: 1, 2: 1, 3: 0},
    ...          2: {0: 0, 1: 1, 2: 0, 3: 0}}
    >>> c = Coordinate(1, 1)
    >>> neighbours(world, c)
    4
    >>> c2 = Coordinate(3, 1)
    >>> neighbours(world, c2)
    2

    :param coord: A Coordinate named-tuple
    :param world: A dictionary representing the world
    :returns: An integer representing the number of neighbours
    """
    cells = map(partial(get_at, world),
                [Coordinate(coord.x-1, coord.y),
                 Coordinate(coord.x+1, coord.y),
                 Coordinate(coord.x, coord.y-1),
                 Coordinate(coord.x, coord.y+1),
                 Coordinate(coord.x-1, coord.y-1),
                 Coordinate(coord.x+1, coord.y-1),
                 Coordinate(coord.x-1, coord.y+1),
                 Coordinate(coord.x+1, coord.y+1)])
    return sum(filter(lambda x: x is not None, cells))


def step(world):
    """
    Returns a new version of the world by applying the rules of the
    game to the old one.

    >>> world = {0: {0: 0, 1: 1, 2: 0},
    ...          1: {0: 0, 1: 1, 2: 0},
    ...          2: {0: 0, 1: 1, 2: 0}}
    >>> gen_1 = step(world)
    >>> gen_1
    {0: {0: 1, 1: 1, 2: 1}, 1: {0: 1, 1: 1, 2: 1}, 2: {0: 1, 1: 1, 2: 1}}
    >>> gen_2 = step(gen_1)
    >>> gen_2
    {0: {0: 0, 1: 0, 2: 0}, 1: {0: 0, 1: 0, 2: 0}, 2: {0: 0, 1: 0, 2: 0}}

    :param world: A dict object representing the world
    :returns: A dict representing a new world advanced by one step
    """
    new_world = deepcopy(world)
    for coord, cell in coordinates(world):
        ns = neighbours(world, coord)
        x, y = (coord.x, coord.y)
        if cell == 1:
            if ns < 2:
                new_world[y][x] = 0
            if ns == 2 or ns == 3:
                new_world[y][x] = 1
            if ns > 3:
                new_world[y][x] = 0
        else:
            if ns == 3:
                new_world[y][x] = 1
            else:
                new_world[y][x] = 0
    return new_world


def generations(num, starting_world):
    """ Yield successive generations starting from starting_world.

    The first generation is starting_world followed by successive
    applications of the 'step' function.

    >>> seed = {0: {0: 0, 1: 1, 2: 0},
    ...         1: {0: 1, 1: 1, 2: 0},
    ...         2: {0: 0, 1: 0, 2: 0}}
    >>> for g, world in generations(3, seed):
    ...     print g, world
    0 {0: {0: 0, 1: 1, 2: 0}, 1: {0: 1, 1: 1, 2: 0}, 2: {0: 0, 1: 0, 2: 0}}
    1 {0: {0: 1, 1: 1, 2: 1}, 1: {0: 1, 1: 1, 2: 1}, 2: {0: 1, 1: 1, 2: 1}}
    2 {0: {0: 0, 1: 0, 2: 0}, 1: {0: 0, 1: 0, 2: 0}, 2: {0: 0, 1: 0, 2: 0}}

   :param num: The number of generations to yield
   :param starting_world: The initial world to kick off with
   :returns: A generator that yields successive generations of starting_world
    """
    world = starting_world
    for generation in xrange(num):
        yield generation, world
        world = step(world)


if __name__ == '__main__':
    import doctest    
    doctest.testmod()