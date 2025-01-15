#!/usr/bin/env python
from __future__ import annotations
# to use quaternion as a type hint inside the quaternion class

from numbers import Real
import math

type Vec3 = tuple[Real, Real, Real] # type for axis of rotation
type Rotation = tuple[Vec3, Real]   # type for rotation (axis, angle)
# https://commons.wikimedia.org/wiki/File:Euler_AxisAngle.svg


class quaternion:
    """
    Class which represents quaternions

    https://en.wikipedia.org/wiki/Quaternion
    overloads same ariphmetic operators as in numbers.Complex
    https://docs.python.org/3/library/numbers.html#numbers.Complex
    """
    def __init__(self, a: Real = 0,
                       b: Real = 0,
                       c: Real = 0,
                       d: Real = 0):
        """
        Form a quaternion from real coefficients

        a + bi + cj + dk
        """
        self.a: Real = a
        self.b: Real = b
        self.c: Real = c
        self.d: Real = d

    def to_tuple(self) -> tuple[Real, Real, Real, Real]:
        return (self.a, self.b, self.c, self.d)

    def to_imag(self) -> quaternion:
        return quaternion(0, *(self.to_tuple()[1:]))

    def __add__(self, other: quaternion | Real) -> quaternion:
        if isinstance(other, quaternion):
            return quaternion(
                self.a + other.a,
                self.b + other.b,
                self.c + other.c,
                self.d + other.d)
        if isinstance(other, Real):
            return quaternion(other) + self

    def __radd__(self, other: Real) -> quaternion:
        if isinstance(other, Real):
            return self + other

    def __mul__(self, other: quaternion | Real) -> quaternion:
        if isinstance(other, Real):
            return self * (quaternion() + other)
        if isinstance(other, quaternion):
            return quaternion(
                self.a * other.a - self.b * other.b - self.c * other.c - self.d * other.d,
                self.a * other.b + self.b * other.a + self.c * other.d - self.d * other.c,
                self.a * other.c - self.b * other.d + self.c * other.a + self.d * other.b,
                self.a * other.d + self.b * other.c - self.c * other.b + self.d * other.a)

    def __rmul__(self, other: Real) -> quaternion:
        if isinstance(other, Real):
            return self * other

    def __abs__(self) -> Real:
        sqr = (self.a * self.a +
               self.b * self.b +
               self.c * self.c +
               self.d * self.d)
        return math.sqrt(sqr)

    def __bool__(self) -> bool:
        return any(*self.to_tuple())

    def __neg__(self) -> quaternion:
        return -1 * self

    def __pos__(self) -> quaternion:
        return self

    def __sub__(self, other: quaternion | Real) -> quaternion:
        return self + (-other)
    
    def __rsub__(self, other: Real) -> quaternion:
        if isinstance(other, Real):
            return other + (-self)

    def conjugate(self) -> quaternion:
        return quaternion(self.a, -self.b, -self.c, -self.d)

    def __truediv__(self, other: quaternion | Real) -> quaternion:
        if isinstance(other, Real):
            return self * (1 / other)
        if isinstance(other, quaternion):
            return self * qmath.invert(quaternion)

    def __rtruediv(self, other: Real) -> quaternion:
        if isinstance(other, Real):
            return other * qmath.invert(self)

    def __pow__(self, other: quaternion | Real) -> quaternion:
        return qmath.pow(self, other)

    def __rpow__(self, other: Real) -> quaternion:
        if isinstance(other, Real):
            return qmath.pow(other, self)

    def __repr__(self) -> str:
        return "quaternion({}, {}, {}, {})".format(*self.to_tuple())
    
    @classmethod
    def from_rotation(cls, rotation: Rotation):
        axis, radians = rotation
        return math.cos(radians / 2) + qmath.normalized(cls(0, *axis)) * math.sin(radians / 2)

    def to_rotation(self) -> Rotation:
        return (qmath.normalized(self.to_imag())[1:], 2 * math.atan2(abs(self.to_imag()), self.a))


class qmath:
    @staticmethod
    def normalized(num: quaternion) -> quaternion:
        return num / abs(num)

    @staticmethod
    def exp(num: quaternion) -> quaternion:
        v = num.to_imag()
        av = abs(v)
        return pow(math.e, num.a) * (math.cos(av) + normalized(v) * math.sin(av))

    @staticmethod
    def log(num: quaternion, base: quaternion | Real = math.e) -> quaternion:
        if isinstance(base, Real):
            return (math.log(num) + normalized(num.to_imag()) * math.acos(num.a / abs(num))) / math.log(base)
        if isinstance(base, quaternion):
            return qmath.log(num) / qmath.log(base)

    @staticmethod
    def pow(base: quaternion | Real, exponent: quaternion | Real):
        if isinstance(base, Real):
            base = quaternion(base)
        return qmath.exp(qmath.log(base) * exponent)

    @staticmethod
    def invert(num: quaternion) -> quaternion:
        if not num:
            raise ZeroDivisionError("Cannot invert (0+0i+0j+0k)")
        sqr: Real = (num.a * num.a +
                     num.b * num.b +
                     num.c * num.c +
                     num.d * num.d)
        return num.conjugate() / sqr
    
    @staticmethod
    def rotate_by_quaternion(vec: Vec3, q: quaternion) -> Vec3:
        return (q * quaternion(0, *vec) / q).to_rotation()[0]

    @staticmethod
    def rotate(vec: Vec3, rotation: Rotation) -> Vec3:
        q = quaternion.from_rotation(rotation)
        return (q * quaternion(0, *vec) * q.conjugate()).to_rotation()[0]

