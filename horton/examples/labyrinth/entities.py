import pygame


class Entity(object):

    x, y = (0, 0)

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def position(self):
        """
        Return the tuple representing the entity's position.
        """
        return (self.x, self.y)

    @position.setter
    def position(self, position):
        self.x, self.y = position

    def draw(self, surface, x, y, width, height):
        """
        Render the entity on the surface.
        """
        pass

    def __str__(self):
        return "<%s at (%d, %d)>" % (self.__class__.__name__,
                                     self.x, self.y)

    def __repr__(self):
        return "<%s(x=%d, y=%d)>" % (self.__class__.__name__,
                                     self.x, self.y)


class Player(Entity):

    def __init__(self, x=0, y=0):
        super(Player, self).__init__(x, y)

    def draw(self, surface, x, y, width, height):
        pygame.draw.rect(surface, (0, 255, 0),
                         pygame.Rect(x + 2, y + 2,
                                     width - 4, height - 4))


class Enemy(Entity):

    valid_states = ['aggressive', 'passive']

    def __init__(self, x=0, y=0):
        self.state = 'passive'
        super(Enemy, self).__init__(x, y)

    def draw(self, surface, x, y, width, height):
        pygame.draw.rect(surface, (255, 0, 0),
                         pygame.Rect(x + 2, y + 2,
                                     width - 4, height - 4))
