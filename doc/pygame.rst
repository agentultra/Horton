Pygame Integration
==================

Pictures speak a thousand words.  Horton comes with an optional module
for rendering grids using Pygame.  The goal is to make it super-easy
to start getting something on the screen and scale up as your project
gets a little more sophisticated.

The main function you should be aware of is
:py:func:`pygame.render.pg.render_grid`.

.. py:function:: render_grid(surface, grid, x, y, width, height [, padding=0, render_cell=draw_cell])

   Render a :py:class:`horton.grid.Grid` instance to the given *surface*.

   :param surface: A pygame.Surface object
   :param grid: A horton.grid.Grid instance
   :param x: The surface x-coordinate to place the grid at
   :param y: The surface y-coordinate to place the grid at
   :param width: The desired width of the rendered grid
   :param height: The desired height of the rendered grid
   :param padding: The optional padding to apply to the cells of the
                   grid
   :param render_cell: The function to call when rendering an
                       individual cell.

All you need is this function and a :py:class:`horton.grid.Grid`
instance to draw a grid to the screen. The default
:py:func:`horton.render.pg.draw_cell` will simply draw a filled-in
black box if the cell evaluates to :py:obj:`True`.  The minimal amount
of code you need to get a grid on the screen is::

  import pygame
  import sys
  
  from horton.grid import Grid
  from horton.render.pg import render_grid
  from pygame.locals import *

  g = Grid.from_array([1, 0, 1,
                       1, 1, 1,
                       1, 0, 1])
  pygame.init()

  screen = pygame.display.set_mode((640, 480))
  screen.fill((255, 255, 255))
  render_grid(screen, g, 10, 10, 100, 300)

  while True:
      for event in pygame.event.get():
          if event.type == QUIT:
              sys.exit()

      pygame.display.flip()

The *padding* parameter behaves much like padding in the CSS
box-model.  The position of the cell is relative to its position in
the grid and the padding is applied to the content.  In other words,
it will *reduce* the size of the content of your cell.

If you want to customize your grid beyond the defaults provided you
will have to supply your own :py:func:`draw_cell` function with the
following signature:

.. py:function:: draw_cell(surface, cell, x, y, width, height)

   Render a cell from a :py:class:`horton.grid.Grid` instance to the
   given *surface*.

   :param surface: A pygame.Surface instance
   :param cell: The value of the cell to draw
   :param x: The screen x-coordinate of the cell to draw
   :param y: The screen y-coordinate of the cell to draw
   :param width: The calculated width of the cell
   :param height: The calculated height of the cell

You then pass your function to the *render_cell* parameter of the
:py:func:`horton.render.pg.render_grid` function and let it do the
rest::

  import pygame
  import random
  import sys

  from horton.grid import Grid
  from horton.render.pg import render_grid
  from pygame.locals import *

  def random_colour_cell(surf, cell, x, y, w, h):
      if cell:
          colour = (random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255))
      else:
          colour = (255, 255, 255)

      pygame.draw.rect(surf, colour, pygame.Rect(x, y, w, h))

  g = Grid.from_array(3, 3,
                      [1, 0, 1,
                      1, 1, 1,
                      1, 0, 1])
  pygame.init()

  screen = pygame.display.set_mode((640, 480))
  screen.fill((255, 255, 255))

  while True:
      for event in pygame.event.get():
          if event.type == QUIT:
              sys.exit()

      render_grid(screen, g, 10, 10, 100, 300,
                  padding=2,
                  render_cell=random_colour_cell)

      pygame.display.flip()

These two functions alone can get you pretty far. Just check out the
``examples/`` folder in your horton distribution to see what is
possible.
