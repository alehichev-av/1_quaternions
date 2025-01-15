import pytest
from quaternion import quaternion, qmath
import math
import itertools as itt

qeq = qmath.isclose

@pytest.fixture
def basis_qs():
    return list(quaternion(*[int(i == j) for j in range(4)]) for i in range(4))

@pytest.fixture
def two_qs():
    return list(map(lambda x: quaternion(*x), [
        [ 1,  1,  0,  0],
        [-1,  1,  0,  0],
        [ 0,  0, -1,  1],
        [ 0,  0,  1, -1]
    ]))

@pytest.fixture
def four_qs():
    return list(map(lambda x: quaternion(*x), [
        [ 1,  1,  1,  1],
        [-1, -1,  1,  1],
        [ 1, -1, -1,  1],
        [-1,  1, -1,  1]
    ]))

@pytest.fixture
def nonzero_qs(two_qs, four_qs, basis_qs):
    return two_qs + four_qs + basis_qs

@pytest.fixture
def zero_qs():
    return [quaternion(),]

@pytest.fixture
def all_qs(nonzero_qs, zero_qs):
    return nonzero_qs + zero_qs

def test_sanity(all_qs):
    """Test whether same quaternions are equal and different are not equal."""
    assert all((a is b) == qmath.isclose(a, b) for a, b in itt.product(all_qs, repeat=2))

def test_abs(basis_qs, two_qs, four_qs, zero_qs):
    """Test quaternion's lengths against known values."""
    assert all(map(lambda q: math.isclose(abs(q), 1), basis_qs))
    assert all(map(lambda q: math.isclose(abs(q), pow(2, 1/2)), two_qs))
    assert all(map(lambda q: math.isclose(abs(q), 2), four_qs))
    assert all(map(lambda q: math.isclose(abs(q), 0), zero_qs))

def test_basis_multiplication(basis_qs):
    """
    Test whether quaternion multiplication conforms with definition.

    https://en.wikipedia.org/wiki/Quaternion
    """

    l, i, j, k = basis_qs
    mul_table = [
        [ l,  i,  j,  k],
        [ i, -l,  k, -j],
        [ j, -k, -l,  i],
        [ k,  j, -i, -l]]

    assert qmath.isclose(i * j * k, -l)
    assert all(qmath.isclose(mul_table[a][b], basis_qs[a] * basis_qs[b]) for a, b in itt.product(range(4), repeat=2))

def test_algebra(all_qs, nonzero_qs):
    """
    Test quaternion addition and multiplication.

    Addition should be associative and commutative.
    a + b + c = (a + b) + c = a + (b + c)
    a + b = b + a

    Multiplication should be associative, distributative and not commutative.
    a * b * c = (a * b) * c = a * (b * c)
    a * (b + c) = a * b + a * c
    (a + b) * c = a * c + b * c
    a + b != b + a

    Additive identity, multiplicative identity, additive inverse, multiplicative inverse.
    0 + a = a + 0 = a
    1 * a = a * 1 = a
    a + (-a) = 0
    a * inverse(a) = 1, a != 0

    https://en.wikipedia.org/wiki/Quaternion#Algebraic_properties
    """
    assert all(qmath.isclose((a + b) + c, a + (b + c)) for a, b, c in itt.product(all_qs, repeat=3))
    assert all(qmath.isclose(a + b, b + a) for a, b in itt.product(all_qs, repeat=2))

    assert all(qmath.isclose((a * b) * c, a * (b * c)) for a, b, c in itt.product(all_qs, repeat=3))
    assert all(qmath.isclose(a * (b + c), a * b + a * c) for a, b, c in itt.product(all_qs, repeat=3))
    assert all(qmath.isclose((a + b) * c, a * c + b * c) for a, b, c in itt.product(all_qs, repeat=3))
    assert any(not qmath.isclose(a * b, b * a) for a, b in itt.product(all_qs, repeat=2))

    assert all(qmath.isclose(quaternion() + a, a) and qmath.isclose(a + quaternion(), a) for a in all_qs)
    assert all(qmath.isclose(quaternion(1) * a, a) and qmath.isclose(a * quaternion(1), a) for a in all_qs)
    assert all(qmath.isclose(a + (-1 * a), quaternion()) for a in all_qs)
    assert all(qmath.isclose(a * qmath.invert(a), quaternion(1)) for a in nonzero_qs)
    assert all(qmath.isclose(qmath.invert(a) * a, quaternion(1)) for a in nonzero_qs) # idk if this should pass or not
    with pytest.raises(ZeroDivisionError):
        qmath.invert(quaternion())

