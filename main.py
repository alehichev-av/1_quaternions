#!/usr/bin/env python

from quaternion import quaternion, qmath
from math import pi
from pprint import pprint

def main():
    """
    This example rotates a square 90 degrees clockwise.

    ^ y                     ^
    | .B    .C              |
    |                       |
    | .A    .D   x          |
 ---+------------>  ->   ---+------------>
    |         rot 90 deg    | .A    .B
    |                       |
                              .D    .C
    """
    points = [
        (1, 1, 0),
        (1, 3, 0),
        (3, 3, 0),
        (3, 1, 0)
    ]
    axis = (0, 0, 1)
    angle = - pi / 2

    new_points = list(map(lambda p: qmath.rotate(p, (axis, angle)), points))
    print("Before rotation")
    print(",\n".join(map(lambda x: "({:4.1f}, {:4.1f}, {:4.1f})".format(*x), points)))
    print("After  rotation")
    print(",\n".join(map(lambda x: "({:4.1f}, {:4.1f}, {:4.1f})".format(*x), new_points)))


if __name__ == "__main__":
    main()
