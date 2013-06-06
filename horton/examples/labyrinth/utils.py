import math


def distance(p1, p2):
    """
    Return the distance between two points on a 2D plane.

    :param p1: A tuple representing a point.
    :param p2: A tuple representing another point.
    :returns: A float representing the distance.
    """
    # c^2 = a^2 + b^2
    a = p1[0] - p2[0]
    b = p1[1] - p2[1]
    c = a**2 + b**2
    return math.sqrt(c)
