import pytest
from .pycalculator import Calculator


@pytest.fixture(scope='session')
def calculator():
    return Calculator()


def test_add_a_to_b(calculator):
    assert calculator.add(2, 3) == 5


def test_substract_b_from_a(calculator):
    assert calculator.substract(3, 2) == 1


def test_devide_a_to_b(calculator):
    assert calculator.divide(4,2) == 2


def test_devide_num_to_0_fils(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.divide(2, 0)

