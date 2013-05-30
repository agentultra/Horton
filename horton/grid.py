from collections import Mapping
from copy import copy, deepcopy


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
        g = cls(other.width, other.height)
        g._grid = deepcopy(other._grid)
        return g

    @classmethod
    def from_array(cls, width, height, arr, copy=True):
        assert len(arr) == width * height, ("Array dimensions do not "
                                            "match length of array.")
        g = cls(width, height)
        a = deepcopy(arr) if copy else arr
        g._grid = a
        return g

    @staticmethod
    def pprint(grid):
        for y in range(grid.height):
            print(" ".join(str(grid[x, y]) for
                           x in range(grid.width)))

    @property
    def dimensions(self):
        return (self.width, self.height)

    @property
    def coordinates(self):
        if self._coordinates:
            return self._coordinates
        else:
            self._coordinates = [(x, y) for y in range(self.height)
                                 for x in range(self.width)]
            return self._coordinates

    @property
    def values(self):
        return deepcopy(self._grid)

    def items(self):
        return zip(self.coordinates, self.values)

    def iter_items(self):
        for coordinate in self.coordinates:
            yield (coordinate, self.__getitem__(coordinate))

    def get(self, x, y, default=None):
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
        return self.width * self.height

    def __eq__(self, other):
        assert isinstance(other, Grid)
        return self._grid == other._grid

    def __add__(self, other):
        assert isinstance(other, Grid)
        assert self.dimensions == other.dimensions

        g = Grid(*self.dimensions)
        for idx, val in enumerate(self._grid):
            g._grid[idx] = val + other._grid[idx]

        return g

    def __sub__(self, other):
        assert isinstance(other, Grid)
        assert self.dimensions == other.dimensions

        g = Grid(*self.dimensions)
        for idx, val in enumerate(self._grid):
            g._grid[idx] = val - other._grid[idx]

        return g

    def __iter__(self):
        return iter(self._grid)

    def __contains__(self, value):
        return value in self._grid

    def __getitem__(self, *args):
        if not self._is_valid_location(*args[0]):
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                *args[0]))
        x, y = args[0]
        try:
            return self._grid[y * self.width + x]
        except IndexError:
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                *args[0]))

    def __setitem__(self, *args):
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
        x = args[0][0] % self.width
        y = args[0][1] % self.height

        return self._grid[y * self.height + x]

    def __setitem__(self, *args):
        x = args[0][0] % self.width
        y = args[0][1] % self.height

        self._grid[y * self.height + x] = args[1]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
