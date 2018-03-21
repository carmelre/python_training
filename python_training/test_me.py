import pytest
from .pycalculator import Calculator


@pytest.fixture()
def calculator():
    return Calculator()


def test_add_a_to_b(calculator):
    assert calculator.add(2, 3) == 5


def test_add_string_to_string_raises(calculator):
    with pytest.raises(Exception):
        assert calculator.add("a", "b")


def test_subtract_b_from_a(calculator):
    assert calculator.subtract(3, 2) == 1


def test_divide_a_to_b(calculator):
    assert calculator.divide(4, 2) == 2


def test_divide_num_to_0_raises(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.divide(2, 0)


def test_multiply_a_by_b(calculator):
    assert calculator.multiply(2, 3) == 6


def test_save_number(calculator):
    calculator.set_saved_num(3)
    assert calculator.get_saved_number() == 3


def test_save_noninteger_raises(calculator):
    with pytest.raises(Exception):
        calculator.set_saved_num("a")


def test_use_unset_saved_number_raises(calculator):
    with pytest.raises(Exception):
        calculator.add(calculator.get_saved_number(), 3)