import weakref

from collections import Mapping
from copy import copy, deepcopy


class GridSliceProxy(object):

    def __init__(self, grid, topleft, bottomright):
        self._grid_ref = weakref.proxy(grid)
        self.x1, self.y1 = topleft.start, topleft.stop
        self.x2, self.y2 = bottomright.start, bottomright.stop

    def __getitem__(self, *args):
        target = args[0]
        dx, dy = (self.x1 + target[0], self.y1 + target[1])
        if (dx, dy) > (self.x2, self.y2) or target < (0, 0):
            raise KeyError("{0} is out of slice bounds".format(
                str(target)))
        if all([isinstance(_, int) for _ in target]):
            return self._grid_ref.__get_coordinate__(dx, dy)

    def __setitem__(self, *args):
        target = args[0]
        dx, dy = (self.x1 + target[0], self.y1 + target[1])
        if (dx, dy) > (self.x2, self.y2) or target < (0, 0):
            raise KeyError("{0} is out of slice bounds".format(
                str(target)))
        self._grid_ref.__setitem__((dx, dy), args[1])


class Grid(Mapping):
    """
    A Grid is a two-dimensional data-structure.

    It provides the Python Mapping interface whose keys are tuples
    representing co-ordinates in the Grid.
    """

    def __init__(self, width, height, value=0):
        self.width = width
        self.height = height
        self._grid = [copy(value) for _ in range(width * height)]
        self._coordinates = None

    @classmethod
    def copy(cls, other):
        """
        Return a new Grid as a copy of *other*.
        """
        g = cls(other.width, other.height)
        g._grid = deepcopy(other._grid)
        return g

    @classmethod
    def from_array(cls, width, height, arr, copy=True):
        """ Create a Grid from an array."""
        assert len(arr) == width * height, ("Array dimensions do not "
                                            "match length of array.")
        g = cls(width, height)
        a = deepcopy(arr) if copy else arr
        g._grid = a
        return g

    @staticmethod
    def pprint(grid):
        """ Pretty print a Grid object."""
        for y in range(grid.height):
            print(" ".join(str(grid[x, y]) for
                           x in range(grid.width)))

    @property
    def dimensions(self):
        """ Return the dimensions tuple."""
        return (self.width, self.height)

    @property
    def coordinates(self):
        """ Return the list of coordinates.

        *This value is cached internally after the initial call*.
        """
        if self._coordinates:
            return self._coordinates
        else:
            self._coordinates = [(x, y) for y in range(self.height)
                                 for x in range(self.width)]
            return self._coordinates

    @property
    def values(self):
        """ Return a copy of the grid values."""
        return deepcopy(self._grid)

    def items(self):
        """ Return a list of co-ordinate, value pairs."""
        return zip(self.coordinates, self.values)

    def iter_items(self):
        """ Yield successive co-ordinate, value pairs."""
        for coordinate in self.coordinates:
            yield (coordinate, self.__getitem__(coordinate))

    def get(self, x, y, default=None):
        """ Return a value at *x*, *y*.

        *Return a default value if the key cannot be found.*
        """
        try:
            return self.__getitem__((x, y))
        except KeyError:
            return default

    def _is_valid_location(self, x, y):
        if x < 0 or x > self.width - 1:
            return False
        if y < 0 or y > self.height - 1:
            return False
        return True

    def __len__(self):
        """ Return the total size."""
        return self.width * self.height

    def __eq__(self, other):
        """ Return True if equal to *other*.

        Two grids are considered equal if every value in the grids are
        equal.
        """
        assert isinstance(other, Grid)
        return self._grid == other._grid

    def __add__(self, other):
        """ Return a grid whose values are comprised by adding the
        values of two grids together.
        """
        assert isinstance(other, Grid)
        assert self.dimensions == other.dimensions

        g = Grid(*self.dimensions)
        for idx, val in enumerate(self._grid):
            g._grid[idx] = val + other._grid[idx]

        return g

    def __sub__(self, other):
        """ Return a grid whose values are comprised by subtracting
        the values from one by the other."""
        assert isinstance(other, Grid)
        assert self.dimensions == other.dimensions

        g = Grid(*self.dimensions)
        for idx, val in enumerate(self._grid):
            g._grid[idx] = val - other._grid[idx]

        return g

    def __iter__(self):
        """ Return an iterator over the values."""
        return iter(self._grid)

    def __contains__(self, value):
        """ Return True of *value* can be found in the grid."""
        return value in self._grid

    def __getitem__(self, *args):
        """ Return something from the grid.

        The first argument of args is a tuple. If the elements of the
        tuple are integers then fetch the value at the coordinate. If
        the elements are slices then return a Grid from the region
        defined by them.
        """
        if all([isinstance(_, int) for _ in args[0]]):
            return self.__get_coordinate__(*args[0])
        elif all([isinstance(_, slice) for _ in args[0]]):
            return self.__get_slice__(*args[0])
        else:
            raise TypeError("Unknown argument type: %r" % args[0])

    def __get_coordinate__(self, x, y):
        if not self._is_valid_location(x, y):
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                x, y))
        try:
            return self._grid[y * self.width + x]
        except IndexError:
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                x, y))

    def __get_slice__(self, topleft, bottomright):
        if topleft > bottomright:
            raise ValueError("The first slice should be the top-left "
                             "coordinate of the sub-grid")
        if topleft < slice(0, 0):
            raise KeyError("Negative slices are not supported")
        if bottomright > slice(self.width - 1, self.height - 1):
            raise KeyError("Selecting beyond grid bounds is not supported")
        return GridSliceProxy(self, topleft, bottomright)

    def __setitem__(self, *args):
        """ Set an item in the grid to a value.

        *The first argument is an (x, y) tuple and the second is the value.*
        """
        if not self._is_valid_location(*args[0]):
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                *args[0]))
        x, y = args[0]
        try:
            self._grid[y * self.width + x] = args[1]
        except IndexError:
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                *args[0]))


class Torus(Grid):
    """
    A Grid whose edges are connected.
    """

    def __getitem__(self, *args):
        """ Return an item from the grid.

        *The first argument is an (x, y) tuple.*
        """
        x = args[0][0] % self.width
        y = args[0][1] % self.height

        return self._grid[y * self.height + x]

    def __setitem__(self, *args):
        """ Set an item in the grid to a value.

        *The first argument is an (x, y) tuple and the second is a
        value.*"""
        x = args[0][0] % self.width
        y = args[0][1] % self.height

        self._grid[y * self.height + x] = args[1]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
