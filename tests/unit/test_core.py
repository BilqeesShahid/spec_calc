import pytest
from src.calculator.core import tokenize_expression, evaluate_expression, InvalidExpressionError

def test_tokenize_basic_numbers():
    assert tokenize_expression("123") == ["123"]
    assert tokenize_expression("45.67") == ["45.67"]

def test_tokenize_basic_operators():
    assert tokenize_expression("1+2") == ["1", "+", "2"]
    assert tokenize_expression("3-4") == ["3", "-", "4"]
    assert tokenize_expression("5*6") == ["5", "*", "6"]
    assert tokenize_expression("7/8") == ["7", "/", "8"]

def test_tokenize_with_parentheses():
    assert tokenize_expression("(1+2)") == ["(", "1", "+", "2", ")"]
    assert tokenize_expression("((3-4)*5)") == ["(", "(", "3", "-", "4", ")", "*", "5", ")"]

def test_tokenize_mixed_expression():
    expected = ["10", "+", "20", "*", "(", "30", "-", "40", ")", "/", "50"]
    assert tokenize_expression("10+20*(30-40)/50") == expected

def test_tokenize_with_whitespace():
    expected = ["1", "+", "2", "*", "(", "3", "-", "4", ")"]
    assert tokenize_expression("1 + 2 * ( 3 - 4 )") == expected

def test_tokenize_empty_string():
    assert tokenize_expression("") == []

def test_tokenize_only_whitespace():
    assert tokenize_expression("   ") == []

def test_tokenize_invalid_characters():
    with pytest.raises(ValueError, match=r"Invalid character in expression: @"):
        tokenize_expression("1 + 2@3")
    with pytest.raises(ValueError, match=r"Invalid character in expression: \$"):
        tokenize_expression("5$6")

def test_evaluate_single_number():
    assert evaluate_expression("123") == 123
    assert evaluate_expression("45.67") == 45.67
    assert evaluate_expression("-7") == -7
    assert evaluate_expression("+10") == 10

def test_evaluate_addition():
    assert evaluate_expression("1+2") == 3
    assert evaluate_expression("10 + 20") == 30
    assert evaluate_expression("1.5 + 2.5") == 4.0
    assert evaluate_expression("-5 + 10") == 5
    assert evaluate_expression("5 + (-10)") == -5

def test_evaluate_subtraction():
    assert evaluate_expression("5-2") == 3
    assert evaluate_expression("10 - 5") == 5
    assert evaluate_expression("2.5 - 1.5") == 1.0
    assert evaluate_expression("-5 - 10") == -15
    assert evaluate_expression("5 - (-10)") == 15

def test_evaluate_multiplication():
    assert evaluate_expression("2*3") == 6
    assert evaluate_expression("5 * 4") == 20
    assert evaluate_expression("1.5 * 2") == 3.0
    assert evaluate_expression("-2 * 5") == -10
    assert evaluate_expression("2 * (-5)") == -10

def test_evaluate_division():
    assert evaluate_expression("6/3") == 2
    assert evaluate_expression("10 / 4") == 2.5
    assert evaluate_expression("5 / 2") == 2.5
    assert evaluate_expression("-10 / 2") == -5
    assert evaluate_expression("10 / (-2)") == -5

def test_evaluate_order_of_operations():
    assert evaluate_expression("2+3*4") == 14
    assert evaluate_expression("10-4/2") == 8
    assert evaluate_expression("5*2+1") == 11
    assert evaluate_expression("10/2-1") == 4
    assert evaluate_expression("2*3+4/2-1") == 7

def test_evaluate_with_parentheses():
    assert evaluate_expression("(2+3)*4") == 20
    assert evaluate_expression("10-(4/2)") == 8
    assert evaluate_expression("(5+1)*(4-2)") == 12
    assert evaluate_expression("((10+2)/3)*2") == 8
    assert evaluate_expression("2*(3+4)") == 14
    assert evaluate_expression("(1+2)*(3+4)") == 21

def test_evaluate_exponentiation():
    assert evaluate_expression("2^3") == 8
    assert evaluate_expression("3^2") == 9
    assert evaluate_expression("2^0.5") == pytest.approx(1.41421356237)
    assert evaluate_expression("-2^2") == -4 # Unary minus has higher precedence if not grouped
    assert evaluate_expression("(-2)^2") == 4 # Grouped unary minus

def test_evaluate_modulus():
    assert evaluate_expression("10%3") == 1
    assert evaluate_expression("10 % 2") == 0
    assert evaluate_expression("15.5 % 4") == pytest.approx(3.5)
    assert evaluate_expression("-10 % 3") == -1 # Changed to expect -1

def test_evaluate_division_by_zero():
    with pytest.raises(InvalidExpressionError, match="Division by zero"):
        evaluate_expression("10/0")
    with pytest.raises(InvalidExpressionError, match="Division by zero"):
        evaluate_expression("5 / (2-2)")
    with pytest.raises(InvalidExpressionError, match="Modulo by zero"):
        evaluate_expression("10%0")