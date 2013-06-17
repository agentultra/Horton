import unittest

from horton import grid


class TestGrid(unittest.TestCase):

    def setUp(self):
        self.g = grid.Grid(5, 5)

    def test_copy_grid(self):
        new_g = grid.Grid.copy(self.g)
        self.assertTrue(new_g is not self.g)
        self.assertEqual(new_g, self.g)

    def test_grid_len(self):
        self.assertEqual(len(self.g), 25)

    def test_grid_dimensions(self):
        self.assertEqual(self.g.dimensions, (5, 5))

    def test_grid_copy(self):
        gc = grid.Grid.copy(self.g)
        self.assertEqual(gc, self.g)
        self.assertFalse(gc is self.g)

    def test_grid_from_array(self):
        g = grid.Grid.from_array(2, 2,
                                 [1, 0,
                                  0, 1])
        self.assertEqual([1, 0, 0, 1], list(g))

    def test_grid_items(self):
        g = grid.Grid(2, 2)
        self.assertEqual([((0, 0), 0),
                          ((1, 0), 0),
                          ((0, 1), 0),
                          ((1, 1), 0)],
                          g.items())

    def test_grid_getitem(self):
        self.assertEqual(self.g[0, 0], 0)
        g = grid.Grid(3, 8)
        self.assertEqual(g[1, 6], 0)
        g = grid.Grid(8, 3)
        self.assertEqual(g[5, 1], 0)

    def test_setitem(self):
        self.g[0, 0] = 1
        self.assertEqual(self.g[0, 0], 1)

    def test_setitem_invalid_location(self):
        try:
            self.g[10, 10] = "foo"
        except KeyError:
            return True
        else:
            raise AssertionError("__setitem__ should raise KeyError for "
                                 "an invalid location")

    def test_grid_default_value(self):
        g = grid.Grid(3, 3, value=lambda: "foo")
        self.assertEqual(g[0, 0], "foo")

    def test_grid_get_invalid_location(self):
        try:
            self.g[10, 10]
        except KeyError:
            return True
        else:
            raise AssertionError("Was able to retrieve an invalid location")

    def test_grid_equality(self):
        g = grid.Grid(5, 5)
        self.assertEqual(g, self.g)

    def test_grid_of_different_size_is_not_equal(self):
        g = grid.Grid(3, 3)
        self.assertNotEqual(g, self.g)

    def test_grid_of_different_value_is_not_equal(self):
        g = grid.Grid(5, 5)
        g[0, 0] = 1
        self.assertNotEqual(g, self.g)

    def test_grid_addition(self):
        self.g[0, 0] = 1
        g1 = grid.Grid(5, 5)
        g1[0, 0] = 1
        g2 = self.g + g1
        self.assertEqual(g2[0, 0], 2)

    def test_grid_subtraction(self):
        self.g[0, 0] = 2
        g1 = grid.Grid(5, 5)
        g1[0, 0] = 1
        g2 = self.g - g1
        self.assertEqual(g2[0, 0], 1)

    def test_coordinates(self):
        g = grid.Grid(2, 2)
        self.assertEqual(g.coordinates, [(0, 0), (1, 0), (0, 1), (1, 1)])

    def test_values(self):
        g = grid.Grid(2, 2)
        g[0, 0] = 2
        g[1, 1] = 1
        self.assertEqual(g.values, [2 , 0, 0, 1])

    def test_iter_items(self):
        g = grid.Grid(2, 2)
        g[1, 1] = 1
        items = list(g.iter_items())
        self.assertEqual(items,
                         [((0, 0), 0),
                          ((1, 0), 0),
                          ((0, 1), 0),
                          ((1, 1), 1)])

    def test_get(self):
        self.g[0, 1] = 2
        self.assertEqual(self.g.get(0, 1), 2)

    def test_get_with_default(self):
        self.assertEqual(self.g.get(10, 10, "foo"), "foo")

    def test_iter_grid(self):
        for cell in self.g:
            self.assertEqual(cell, 0)

    def test_contains(self):
        self.g[1, 1] = "foo"
        self.assertTrue("foo" in self.g)
