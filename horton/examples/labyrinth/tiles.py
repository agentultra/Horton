import pygame

from abc import abstractmethod, abstractproperty


class Tile(object):

    objects = []

    @abstractproperty
    def passable(self):
        """
        Return wether an object can enter the tile.
        """

    @abstractmethod
    def draw(self, surface, x, y, width, height):
        """
        Draw the tile to the given Pygame surface.
        """


class Wall(Tile):

    passable = False

    def draw(self, surface, x, y, width, height):
        pygame.draw.rect(surface, (0, 0, 0),
                         pygame.Rect(x, y, width, height))


class Floor(Tile):

    passable = True

    def draw(self, surface, x, y, width, height):
        pygame.draw.rect(surface, (180, 180, 180),
                         pygame.Rect(x, y, width, height))
