import pytest
from .pycalculator import Calculator


@pytest.fixture()
def calculator():
    return Calculator()


@pytest.fixture(params=[
    Calculator().add,
    Calculator().subtract,
    Calculator().multiply,
    Calculator().divide

])
def calculator_math_methods(request):
    return request.param


@pytest.mark.parametrize('x, y', [('a', 'b'),
                                  (1, 'a'),
                                  (1, None),
                                  ({'a': 1}, 2)])
def test_math_methods_invalid_input_raises(x, y, calculator_math_methods):
    with pytest.raises(TypeError):
        assert calculator_math_methods(x, y)


@pytest.mark.parametrize('x, y, expected', [
    (1, 2, 3),
    (2.2, 1.1, 3.3)])
def test_add_valid_input(x, y, expected, calculator):
    assert round(calculator.add(x, y), 2) == expected


@pytest.mark.parametrize('x, y, expected', [
    (2, 1, 1),
    (2.2, 1.1, 1.1)])
def test_subtract_valid_input(x, y, expected, calculator):
    assert round(calculator.subtract(x, y), 2) == expected


@pytest.mark.parametrize('x, y, expected', [
    (4, 2, 2),
    (4.4, 2.2, 2.0)])
def test_divide_valid_input(x, y, expected, calculator):
    assert calculator.divide(x, y) == expected


@pytest.mark.parametrize('x, y, expected', [
    (2, 2, 4),
    (1.0, 2.0, 2.0)])
def test_multiply_vlaid_input(x, y, expected, calculator):
    assert calculator.multiply(x, y) == expected


def test_divide_num_by_0_raises(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.divide(2, 0)


def test_save_number(calculator):
    calculator.set_saved_num(3)
    assert calculator.get_saved_number() == 3


@pytest.mark.parametrize('invalid_value', [
    "a",
    None,
    {'a': 1}
])
def test_save_invalid_value_raises(invalid_value, calculator):
    with pytest.raises(TypeError):
        calculator.set_saved_num(invalid_value)


def test_use_unset_saved_number_raises(calculator):
    with pytest.raises(TypeError):
        calculator.add(calculator.get_saved_number(), 3)
