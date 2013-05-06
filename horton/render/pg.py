import pygame


def draw_cell(surface, cell, x, y, width, height):
    if cell:
        colour = (0, 0, 0)
    else:
        colour = (255, 255, 255)

    pygame.draw.rect(surface, colour, pygame.Rect(x, y, width, height))


def render_grid(surface, grid, x, y, width, height, padding=0, render_cell=draw_cell):
    assert grid.width > 0
    assert grid.height > 0

    cell_width = (width / grid.width)
    cell_height = (height / grid.height)

    cell_width = cell_width if cell_width > 1 else 1
    cell_height = cell_height if cell_height > 1 else 1

    for grid_x in range(grid.width):
        for grid_y in range(grid.height):
            screen_x = x + (grid_x * cell_width)
            screen_y = y + (grid_y * cell_height)

            render_cell(surface, grid[grid_x, grid_y],
                        screen_x + padding, screen_y + padding,
                        cell_width - (padding * 2), cell_height - (padding * 2))
