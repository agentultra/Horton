from collections import namedtuple
from functools import partial

from grid import Grid


Coordinate = namedtuple("Coordinate", "x y")


def get_at(world, coord):
    """ Return a value from the world at the coordinate or None."""
    try:
        return world[coord.x, coord.y]
    except KeyError:
        return None


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
    coordinates in the eight cardinal directions.

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
    0
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
    0 1 0
    0 1 0
    0 1 0
    >>> gen_2 = step(gen_1)
    >>> Grid.pprint(gen_2)
    0 0 0
    1 1 1
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
    >>> seed[0, 1] = 1
    >>> seed[1, 1] = 1
    >>> seed[2, 1] = 1
    >>> for g, world in generations(3, seed):
    ...     print(g)
    ...     Grid.pprint(world)
    0
    0 0 0
    1 1 1
    0 0 0
    1
    0 1 0
    0 1 0
    0 1 0
    2
    0 0 0
    1 1 1
    0 0 0

   :param num: The number of generations to yield
   :param starting_world: The initial world to kick off with
   :returns: A generator that yields successive generations of starting_world
    """
    world = Grid.copy(starting_world)
    for generation in xrange(num):
        yield generation, world
        world = step(world)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
