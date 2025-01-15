import pytest
from quaternion import quaternion, qmath
import math

qeq = qmath.isclose

@pytest.fixture
def basis_qs():
    return list(quaternion(*[int(i == j) for j in range(4)]) for i in range 4)

@pytest.fixture
def other_qs():
    return map(lambda x: quaternion(*x), [
        [ 1,  1,  1,  1],
        [-1, -1,  1,  1],
        [ 1, -1, -1,  1],
        [-1,  1, -1,  1],
        [ 1,  1,  0,  0],
        [-1,  1,  0,  0],
        [ 0,  0, -1,  1],
        [ 0,  0,  1, -1]
    ])

@pytest.fixture
def nonzero_qs():
    return other_qs() + basis_qs()

@pytest.fixture
def zero_qs():
    return [quaternion(),]

@pytest.fixture
def all_qs():
    return nonzero_qs() + zero_qs()

def test_sanity(all_qs, basis_qs, zero_qs):
    assert all(qmath.isclose(i, i) for i in all_qs)
    assert map(lambda q: math.isclose(abs(q), 1), basis_qs)

