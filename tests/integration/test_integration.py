import pytest
from src.calculator.core import evaluate_expression, InvalidExpressionError

def test_integration_basic_arithmetic():
    assert evaluate_expression("1+1") == 2
    assert evaluate_expression("10-5") == 5
    assert evaluate_expression("2*3") == 6
    assert evaluate_expression("10/2") == 5
    assert evaluate_expression("15%4") == 3 # Python's default behavior for positive numbers

def test_integration_order_of_operations():
    assert evaluate_expression("2+3*4") == 14
    assert evaluate_expression("10-4/2") == 8
    assert evaluate_expression("5*2+1") == 11
    assert evaluate_expression("10/2-1") == 4
    assert evaluate_expression("2*3+4/2-1") == 7

def test_integration_parentheses():
    assert evaluate_expression("(2+3)*4") == 20
    assert evaluate_expression("10-(4/2)") == 8
    assert evaluate_expression("(5+1)*(4-2)") == 12
    assert evaluate_expression("((10+2)/3)*2") == 8
    assert evaluate_expression("2*(3+4)") == 14
    assert evaluate_expression("(1+2)*(3+4)") == 21

def test_integration_exponentiation_modulus():
    assert evaluate_expression("2^3") == 8
    assert evaluate_expression("3^2") == 9
    assert evaluate_expression("10%3") == 1
    assert evaluate_expression("15.5 % 4") == pytest.approx(3.5)
    assert evaluate_expression("-2^2") == -4 # Per Python's precedence ** > unary -
    assert evaluate_expression("(-2)^2") == 4
    assert evaluate_expression("-10 % 3") == -1 # Per test_evaluate_modulus

def test_integration_float_numbers():
    assert evaluate_expression("1.5+2.5") == 4.0
    assert evaluate_expression("10.0/4.0") == 2.5
    assert evaluate_expression("3.14*2") == 6.28

def test_integration_signed_numbers():
    assert evaluate_expression("-5+10") == 5
    assert evaluate_expression("5+(-10)") == -5
    assert evaluate_expression("+7*2") == 14
    assert evaluate_expression("-(5+5)") == -10 # Explicit grouping for unary

def test_integration_whitespace_handling():
    assert evaluate_expression("1 + 2 * ( 3 - 4 )") == -1
    assert evaluate_expression("  10  /  2   ") == 5

def test_integration_invalid_input_errors():
    with pytest.raises(ValueError, match=r"Invalid character in expression: @"):
        evaluate_expression("1 + 2@3")
    with pytest.raises(InvalidExpressionError, match="Mismatched parentheses"):
        evaluate_expression("(1+2")
    with pytest.raises(InvalidExpressionError, match="Division by zero"):
        evaluate_expression("10/0")
    with pytest.raises(InvalidExpressionError, match="Modulo by zero"):
        evaluate_expression("10%0")
    with pytest.raises(InvalidExpressionError, match="Insufficient operands"):
        evaluate_expression("5 +") # Test for malformed RPN from shunting yard (e.g. 5 + )

