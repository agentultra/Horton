import pygame


ENEMY_STATES = ['aggressive', 'passive']


class Enemy(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.state = 'passive'

    @property
    def position(self):
        return (self.x, self.y)

    @position.setter
    def position(self, position):
        self.x, self.y = position

    def draw(self, surface, x, y, width, height):
        pygame.draw.rect(surface, (255, 0, 0),
                         pygame.Rect(x + 2, y + 2,
                                     width - 4, height - 4))

    def __str__(self):
        return "<Enemy at (%s)>" % self.position

    def __repr__(self):
        return "<Enemy(x=%d, y=%d)>" % (self.x, self.y)
