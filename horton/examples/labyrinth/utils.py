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
    return c


def average(*args):
    """
    Return the average from the list of args.
    """
    return sum(args) / len(args)


def neighbours(level, p, radius=1):
    """
    Return all neighbour coordinates within a given radius.

    Note that the coordinate `p` is left out of the results.
    """
    return [(x, y)
            for x in range(p[0] - radius, p[1] + (radius + 1))
            for y in range(p[1] - radius, p[1] + (radius + 1))
            if level._is_valid_location(x, y)
            and (x, y) != p]
