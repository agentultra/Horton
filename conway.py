"""
conway.py: An implementation of Conway's Game of Life

This module uses a Grid object to represent the world.  The Grid
object implements the Mapping ABC and uses tuples for keys to address
locations in the plane:

    >>> g = Grid(3, 3)
    >>> g[1, 1] = 1
    >>> g[1, 1]
    1

This simulation uses the integer 1 to represent a 'live' cell and 0 to
represent a 'dead' cell.

There is a convenient generator for iterating over successive
generations starting from a seed world (see the 'generations'
function).

However if you want to run the simulation your own way the function to
use is the 'step' function.  As much as possible this script tries to
adhere to a functional style so one should note that the step function
returns a new instance of a Grid object instead of modifying its
parameter.

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
__version__ = "0.2.0"


from collections import Mapping
from collections import namedtuple
from copy import deepcopy
from functools import partial


Coordinate = namedtuple("Coordinate", "x y")


class Grid(Mapping):

    def __init__(self, width, height, value=0):
        self.width = width
        self.height = height
        self._grid = [value for _ in range(width * height)]

    @staticmethod
    def copy(other):
        g = Grid(other.width, other.height)
        g._grid = deepcopy(other._grid)
        return g

    @staticmethod
    def pprint(grid):
        for y in range(grid.height):
            print(" ".join(str(grid[x, y]) for
                           x in range(grid.width)))

    def __len__(self):
        return len(self._grid)

    def __iter__(self):
        return iter(self._grid)

    def __contains__(self, value):
        return value in self._grid

    def __getitem__(self, *args):
        try:
            return self._grid[args[0][0] * self.width + args[0][1]]
        except IndexError:
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                *args[0]))

    def __setitem__(self, *args):
        try:
            self._grid[args[0][0] * self.width + args[0][1]] = args[1]
        except IndexError:
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                *args[0]))


def get_at(world, coord):
    """ Fetch a value from a Grid object and treat it as a torus."""
    return world[coord.x % world.width, coord.y % world.height]



def coordinates(world):
    """ Yield each Coordinate and cell from world.

    >>> world = Grid(3, 3)
    >>> world[0, 1] = 1
    >>> world[1, 0] = 1
    >>> world[0, 1] = 1
    >>> world[1, 1] = 1
    >>> world[2, 1] = 1
    >>> world[1, 2] = 1
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
    for y in range(world.height):
        for x in range(world.width):
            yield (Coordinate(x, y), world[x, y])


def neighbours(world, coord):
    """
    Return the number of neighbours at a coordinate in the world.

    A neighbour is defined as the integer '1' in directly adjacent
    coordinates in the eight cardinal directions.  The world wraps
    around at the poles.

    >>> world = Grid(4, 4)
    >>> world[1, 0] = 1
    >>> world[2, 0] = 1
    >>> world[1, 1] = 1
    >>> Grid.pprint(world)
    0 1 1 0
    0 1 0 0
    0 0 0 0
    0 0 0 0
    >>> c1 = Coordinate(2, 1)
    >>> neighbours(world, c1)
    3
    >>> c2 = Coordinate(1, 3)
    >>> neighbours(world, c2)
    2
    >>> c3 = Coordinate(2, 2)
    >>> neighbours(world, c3)
    1

    :param coord: A Coordinate named-tuple
    :param world: A Grid object representing the world
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

    >>> world = Grid(3, 3)
    >>> world[0, 1] = 1
    >>> world[1, 1] = 1
    >>> world[2, 1] = 1
    >>> gen_1 = step(world)
    >>> Grid.pprint(gen_1)
    1 1 1
    1 1 1
    1 1 1
    >>> gen_2 = step(gen_1)
    >>> Grid.pprint(gen_2)
    0 0 0
    0 0 0
    0 0 0

    :param world: A Grid object representing the world
    :returns: A new Grid object representing a new world advanced by one
              step
    """
    new_world = Grid.copy(world)
    for coord, cell in coordinates(world):
        ns = neighbours(world, coord)
        x, y = (coord.x, coord.y)
        if cell == 1:
            if ns < 2:
                new_world[x, y] = 0
            if ns == 2 or ns == 3:
                new_world[x, y] = 1
            if ns > 3:
                new_world[x, y] = 0
        else:
            if ns == 3:
                new_world[x, y] = 1
            else:
                new_world[x, y] = 0
    return new_world


def generations(num, starting_world):
    """ Yield successive generations starting from starting_world.

    The first generation is starting_world followed by successive
    applications of the 'step' function.

    >>> seed = Grid(3, 3)
    >>> seed[1, 0] = 1
    >>> seed[0, 1] = 1
    >>> seed[1, 1] = 1
    >>> for g, world in generations(3, seed):
    ...     print(g)
    ...     Grid.pprint(world)
    0
    0 1 0
    1 1 0
    0 0 0
    1
    1 1 1
    1 1 1
    1 1 1
    2
    0 0 0
    0 0 0
    0 0 0

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
