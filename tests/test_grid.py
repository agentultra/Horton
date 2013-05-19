import unittest

from horton import grid


class TestGrid(unittest.TestCase):

    def setUp(self):
        self.g = grid.Grid(5, 5)

    def test_grid_len(self):
        self.assertEqual(len(self.g), 5 * 5)

    def test_grid_dimensions(self):
        self.assertEqual(self.g.dimensions, (5, 5))

    def test_grid_copy(self):
        gc = grid.Grid.copy(self.g)
        self.assertEqual(gc, self.g)
        self.assertFalse(gc is self.g)

    def test_grid_getitem(self):
        self.assertEqual(self.g[0, 0], 0)
        g = grid.Grid(3, 8)
        self.assertEqual(g[1, 6], 0)

    def test_grid_setitem(self):
        self.g[0, 0] = 1
        self.assertEqual(self.g[0, 0], 1)

    def test_grid_default_value(self):
        g = grid.Grid(3, 3, value="foo")
        self.assertEqual(g[0, 0], "foo")

    def test_grid_default_value_is_copied(self):
        default_value = {'foo': "bar"}
        g = grid.Grid(3, 3, value=default_value)
        self.assertEqual(g[0, 0]['foo'], "bar")
        g[0, 0]['foo'] = "baz"
        self.assertEqual(g[0, 0]['foo'], "baz")

    def test_grid_get_invalid_location(self):
        try:
            self.g[10, 10]
        except KeyError:
            return True
        else:
            raise AssertionError("Was able to retrieve an invalid location")
