#!/usr/bin/env python
from __future__ import annotations
# to use quaternion as a type hint inside the quaternion class

from numbers import Real
import math

type Vec3 = tuple[Real, Real, Real] # j
"""
Type representing an axis of rotation or a vector which is rotated.

All functions where Vec3 represents an axis should theoretically expect normalized Vec3 values for speed improvements.
I decided to normalize them anyway in those functions.
"""

type Rotation = tuple[Vec3, Real]   # type representing rotation (axis, angle in radians)
# https://commons.wikimedia.org/wiki/File:Euler_AxisAngle.svg


class quaternion:
    """
    Class which represents quaternions

    https://en.wikipedia.org/wiki/Quaternion
    overloads same ariphmetic operators as expected by numbers.Complex
    https://docs.python.org/3/library/numbers.html#numbers.Complex
    """

    def __init__(self, a: Real = 0,
                       b: Real = 0,
                       c: Real = 0,
                       d: Real = 0):
        """
        Form a quaternion from real coefficients

        (a + bi + cj + dk)
        """
        self.a: Real = a
        self.b: Real = b
        self.c: Real = c
        self.d: Real = d

    def to_tuple(self) -> tuple[Real, Real, Real, Real]:
        """
        Return coefficients of a quaternion in a tuple.

        quaternion(a, b, c, d) -> tuple(a, b, c, d)    
        """
        return (self.a, self.b, self.c, self.d)

    def to_imag(self) -> quaternion:
        """
        Return imaginary part of a quaternion.

        quaternion(a, b, c, d) -> quaternion(0, b, c, d)
        """
        return quaternion(0, *(self.to_tuple()[1:]))

    def __add__(self, other: quaternion | Real) -> quaternion:
        """
        Add quaternion or a Real number to a quaternion.

        quaternion + (quaternion | Real)
        """
        if isinstance(other, quaternion):
            return quaternion(
                self.a + other.a,
                self.b + other.b,
                self.c + other.c,
                self.d + other.d)
        if isinstance(other, Real):
            return quaternion(other) + self

    def __radd__(self, other: Real) -> quaternion:
        """
        Add a quaternion to a real number

        Real + quaternion
        """
        if isinstance(other, Real):
            return self + other

    def __mul__(self, other: quaternion | Real) -> quaternion:
        """
        Multiply quaternion by a quaternion or a Real number.

        quaternion * (quaternion | Real)
        """
        if isinstance(other, Real):
            return self * (quaternion() + other)
        if isinstance(other, quaternion):
            return quaternion(
                self.a * other.a - self.b * other.b - self.c * other.c - self.d * other.d,
                self.a * other.b + self.b * other.a + self.c * other.d - self.d * other.c,
                self.a * other.c - self.b * other.d + self.c * other.a + self.d * other.b,
                self.a * other.d + self.b * other.c - self.c * other.b + self.d * other.a)

    def __rmul__(self, other: Real) -> quaternion:
        """
        Multiply a Real number by a quaternion.

        Real * quaternion
        """
        if isinstance(other, Real):
            return self * other

    def __abs__(self) -> Real:
        """
        Return an absolute value of a quaternion.

        abs(quaternion) -> |quaternion|
        """
        sqr = (self.a * self.a +
               self.b * self.b +
               self.c * self.c +
               self.d * self.d)
        return math.sqrt(sqr)

    def __bool__(self) -> bool:
        """Checks if a quaternion is strictly not equal to zero."""
        return any(*self.to_tuple())

    def __neg__(self) -> quaternion:
        """
        Return unary negative of a quaternion.

        -quaternion -> -1 * quaternion
        """
        return -1 * self

    def __pos__(self) -> quaternion:
        """
        Return unary positive of a quaternion. Identity function.

        +quaternion -> quaternion
        """
        return self

    def __sub__(self, other: quaternion | Real) -> quaternion:
        """
        Substruct quaternion or a Real number from a quaternion.

        quaternion - (quaternion | Real)
        """
        return self + (-other)
    
    def __rsub__(self, other: Real) -> quaternion:
        """
        Substruct a quaternion from a real number.

        Real - quaternion.u
        """
        if isinstance(other, Real):
            return other + (-self)

    def conjugate(self) -> quaternion:
        """
        Return conjugate of a quaternion.

        quaternion(a, b, c, d) -> quaternion(a, -b, -c, -d)
        """
        return quaternion(self.a, -self.b, -self.c, -self.d)

    def __truediv__(self, other: quaternion | Real) -> quaternion:
        """
        Return result of an algebraic division.

        Algebraic in a sense of: (b / a) * a = b
        Accepts both quaternion and Real.
        """
        if isinstance(other, Real):
            return self * (1 / other)
        if isinstance(other, quaternion):
            return self * qmath.invert(quaternion)

    def __rtruediv(self, other: Real) -> quaternion:
        """Return result of an algebraic division."""
        if isinstance(other, Real):
            return other * qmath.invert(self)

    def __pow__(self, other: quaternion | Real) -> quaternion:
        """Return result of exponentiation with a base self and exponent other."""
        return qmath.pow(self, other)

    def __rpow__(self, other: Real) -> quaternion:
        """Return result of exponentiation with a base other and exponent self."""
        if isinstance(other, Real):
            return qmath.pow(other, self)

    def __repr__(self) -> str:
        """Return representation of a quaternion as a string."""
        return "quaternion({}, {}, {}, {})".format(*self.to_tuple())
    
    @classmethod
    def from_rotation(cls, rotation: Rotation):
        """
        Form an appropriate quaternion from a Rotation.

        https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Using_quaternions_as_rotations
        """
        axis, radians = rotation
        return math.cos(radians / 2) + qmath.normalized(cls(0, *axis)) * math.sin(radians / 2)

    def to_rotation(self) -> Rotation:
        """
        Form the Rotation with an axis and an angle from a quaternion.

        Rotation should be normalized.
        https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Recovering_the_axis-angle_representation
        """
        return (qmath.normalized(self.to_imag())[1:], 2 * math.atan2(abs(self.to_imag()), self.a))


class qmath:
    """
    Fictitious class providing mathematical functions for quaternions.

    Python standard library provides analogous module 'cmath' with functions for complex numbers.
    This class tries to imitate 'cmath' module when possible.
    https://docs.python.org/3/library/cmath.html
    """

    @staticmethod
    def normalized(num: quaternion) -> quaternion:
        """Return proportional quaternion value with length 1."""
        return num / abs(num)

    @staticmethod
    def exp(num: quaternion) -> quaternion:
        """
        Return e raised to the power num, where e is the base of natural logarithms.

        https://en.wikipedia.org/wiki/Quaternion#Exponential,_logarithm,_and_power_functions
        """
        v = num.to_imag()
        av = abs(v)
        return pow(math.e, num.a) * (math.cos(av) + normalized(v) * math.sin(av))

    @staticmethod
    def log(num: quaternion, base: quaternion | Real = math.e) -> quaternion:
        """Returns the logarithm of num to the given base. If the base is not specified, returns the natural logarithm of num."""
        if isinstance(base, Real):
            return (math.log(num) + normalized(num.to_imag()) * math.acos(num.a / abs(num))) / math.log(base)
        if isinstance(base, quaternion):
            return qmath.log(num) / qmath.log(base)

    @staticmethod
    def pow(base: quaternion | Real, exponent: quaternion | Real):
        """Return base raised to the power exponent."""
        if isinstance(base, Real):
            base = quaternion(base)
        return qmath.exp(qmath.log(base) * exponent)

    @staticmethod
    def invert(num: quaternion) -> quaternion:
        """
        Return multiplicative inverse of a quaternion.

        https://en.wikipedia.org/wiki/Multiplicative_inverse
        """
        if not num:
            raise ZeroDivisionError("Cannot invert (0+0i+0j+0k)")
        sqr: Real = (num.a * num.a +
                     num.b * num.b +
                     num.c * num.c +
                     num.d * num.d)
        return num.conjugate() / sqr
    
    @staticmethod
    def rotate_by_quaternion(vec: Vec3, q: quaternion) -> Vec3:
        """
        Rotate a vector using a quaternion.

        vec - 3-dimentional vector to be rotated.
        q   - quaternion representing the rotation.

        returns a rotated vector.
        """
        return (q * quaternion(0, *vec) / q).to_rotation()[0]

    @staticmethod
    def rotate(vec: Vec3, rotation: Rotation) -> Vec3:
        """
        Rotate a vector using the Rotation type.

        vec      - 3-dimentional vector to be rotated.
        rotation - tuple of (axis, angle in radians).

        returns a rotated vector.
        """
        q = quaternion.from_rotation(rotation)
        return (q * quaternion(0, *vec) * q.conjugate()).to_rotation()[0]

