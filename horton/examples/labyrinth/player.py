import pygame


class Player(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def position(self):
        return (self.x, self.y)

    @position.setter
    def position(self, position):
        self.x, self.y = position

    def draw(self, surface, x, y, width, height):
        pygame.draw.rect(surface, (0, 255, 0),
                         pygame.Rect(x + 2, y + 2,
                                     width - 4, height - 4))

    def __str__(self):
        return "<Player at (%d, %d)>" % (self.x, self.y)

    def __repr__(self):
        return "<Player(x=%d, y=%d)>" % (self.x, self.y)
