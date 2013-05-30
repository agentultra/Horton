Introduction
============

Grids are very neat.  Horton gives them a nice Python API::

  >>> from horton import grid
  >>> g = grid.Grid(3, 3)
  >>> g[0, 0] = 1
  >>> g[2, 2] = 2
  >>> grid.Grid.pprint(g)
  1 0 0
  0 0 0
  0 0 2

The grid dimensions are inclusive but notice that the indices start
at 0.  Trying to access a location in the grid that isn't there will
result in a KeyError::

  >>> g[100, 200]
  Traceback (most recent call last):
    ...
  KeyError: '(100, 100) is an invalid co-ordinate'

However there are grids for which that wouldn't be a problem::

  >>> t = grid.Torus(3, 3)
  >>> t[0, 0] = 1
  >>> grid.Grid.pprint(t)
  1 0 0
  0 0 0
  0 0 0
  >>> t[3, 0]
  1

This is because a Torus grid wraps around at the poles::

  >>> t[9, 0]
  1

Grids provide the Mapping interface from the `collections.abc` module.
You can iterate over them in all the usual ways::

  >>> for coordinate, value in g.items():
  ...     print("X: %d, Y: %d is %d" % (coordinate[0], 
  ...                                   coordinate[1], 
  ...                                   value))
  ...
  X: 0, Y: 0 is 1
  X: 1, Y: 0 is 0
  X: 2, Y: 0 is 0
  X: 0, Y: 1 is 0
  X: 1, Y: 1 is 0
  X: 2, Y: 1 is 0
  X: 0, Y: 2 is 0
  X: 1, Y: 2 is 0
  X: 2, Y: 2 is 2
  
  >>> print(" ".join(cell for cell in g))
  1 0 0 0 0 0 0 0 2
  
Grids also have some extra attributes that are useful when working
with them::

  >>> small_grid = Grid(2, 2)
  >>> small_grid.coordinates
  [(0, 0), (1, 0), (0, 1), (1, 1)]
  >>> small_grid.dimensions
  (2, 2)

Assuming you've installed the *optional* dependency, `pygame`, you can
easily start rendering your Grid objects. See :doc:`pygame` for more
information.
