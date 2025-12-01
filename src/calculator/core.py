import re
from typing import List, Union

class InvalidExpressionError(ValueError):
    """Custom exception for invalid expressions during evaluation."""
    pass

# Define operator precedence and associativity
# Lower number means higher precedence (e.g., *, / are higher than +, -)
# 'left': left-associative, 'right': right-associative
OPERATORS = {
    '+': {'precedence': 1, 'associativity': 'left'},
    '-': {'precedence': 1, 'associativity': 'left'},
    '*': {'precedence': 2, 'associativity': 'left'},
    '/': {'precedence': 2, 'associativity': 'left'},
    '%': {'precedence': 2, 'associativity': 'left'}, # Modulus same precedence as mult/div
    '^': {'precedence': 3, 'associativity': 'right'}, # Exponentiation is right-associative
}

def tokenize_expression(expression: str) -> List[str]:
    """
    Tokenizes a mathematical expression string into a list of tokens.

    Args:
        expression: The input mathematical expression string.

    Returns:
        A list of strings, where each string is a token (number, operator, parenthesis).

    Raises:
        ValueError: If an unrecognized character is found in the expression.
    """
    if not expression or expression.isspace():
        return []

    token_specification = [
        ('NUMBER', r'\d+\.\d+|\d+'),  # Integer or decimal number
        ('OPERATOR', r'[+\-*/%^]'),    # Arithmetic operators
        ('PARENTHESIS', r'[()]'),     # Parentheses
        ('WHITESPACE', r'\s+'),       # Whitespace characters
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    get_token = re.compile(tok_regex)

    tokens = []
    pos = 0
    while pos < len(expression):
        match = get_token.match(expression, pos)
        if match:
            kind = match.lastgroup
            value = match.group(kind)
            if kind != 'WHITESPACE':
                tokens.append(value)
            pos = match.end(0)
        else:
            raise ValueError(f"Invalid character in expression: {expression[pos]}")
    return tokens


def shunting_yard(tokens: List[str]) -> List[str]:
    """
    Converts an infix expression (list of tokens) to Reverse Polish Notation (RPN)
    using the Shunting-yard algorithm.

    Args:
        tokens: A list of tokens representing the infix expression.

    Returns:
        A list of tokens representing the expression in RPN.

    Raises:
        InvalidExpressionError: If the expression has mismatched parentheses or invalid syntax.
    """
    output_queue = []
    operator_stack = []

    for token in tokens:
        # Check if the token is a number (integer, float, or signed number like -5, +10)
        is_number = (token.replace('.', '', 1).isdigit() or
                     (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()) or
                     (token.startswith('+') and token[1:].replace('.', '', 1).isdigit()))
        
        if is_number:
            output_queue.append(token)
        elif token in OPERATORS: # Operator
            o1 = token
            while (operator_stack and operator_stack[-1] != '(' and
                   (OPERATORS[operator_stack[-1]]['precedence'] > OPERATORS[o1]['precedence'] or
                    (OPERATORS[operator_stack[-1]]['precedence'] == OPERATORS[o1]['precedence'] and
                     OPERATORS[o1]['associativity'] == 'left'))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(o1)
        elif token == '(': # Left parenthesis
            operator_stack.append(token)
        elif token == ')': # Right parenthesis
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                raise InvalidExpressionError("Mismatched parentheses: No matching left parenthesis.")
            operator_stack.pop() # Discard the left parenthesis
        else:
            # This case should ideally not be reached if tokenize_expression is robust
            # but serves as a safeguard for unexpected tokens.
            raise InvalidExpressionError(f"Unexpected token in shunting-yard: {token}")

    while operator_stack:
        if operator_stack[-1] == '(':
            raise InvalidExpressionError("Mismatched parentheses: No matching right parenthesis.")
        output_queue.append(operator_stack.pop())
    return output_queue

def evaluate_rpn(rpn_tokens: List[str]) -> Union[int, float]:
    """
    Evaluates an expression in Reverse Polish Notation (RPN).

    Args:
        rpn_tokens: A list of tokens in RPN.

    Returns:
        The numerical result of the expression.

    Raises:
        InvalidExpressionError: If the RPN expression is invalid.
    """
    operand_stack = []

    for token in rpn_tokens:
        # Check if the token is a number (integer, float, or signed number like -5, +10)
        is_number = (token.replace('.', '', 1).isdigit() or
                     (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()) or
                     (token.startswith('+') and token[1:].replace('.', '', 1).isdigit()))

        if is_number:
            try:
                operand_stack.append(float(token))
            except ValueError:
                raise InvalidExpressionError(f"Invalid number in RPN: {token}")
        elif token in OPERATORS:
            if len(operand_stack) < 2:
                raise InvalidExpressionError(f"Insufficient operands for operator {token}")
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            result = 0
            if token == '+':
                result = operand1 + operand2
            elif token == '-':
                result = operand1 - operand2
            elif token == '*':
                result = operand1 * operand2
            elif token == '/':
                if operand2 == 0:
                    raise InvalidExpressionError("Division by zero")
                result = operand1 / operand2
            elif token == '%':
                # Python's % operator handles negative numbers as per spec (result has same sign as divisor)
                if operand2 == 0:
                    raise InvalidExpressionError("Modulo by zero")
                result = operand1 % operand2
            elif token == '^':
                result = operand1 ** operand2
            operand_stack.append(result)
        else:
            raise InvalidExpressionError(f"Unexpected token in RPN: {token}")

    if len(operand_stack) != 1:
        raise InvalidExpressionError("Invalid RPN expression: Too many operands or operators.")
    
    final_result = operand_stack[0]
    return int(final_result) if final_result.is_integer() else final_result


def evaluate_expression(expression: str) -> Union[int, float]:
    """
    Evaluates a mathematical expression string.

    Args:
        expression: The input mathematical expression string.

    Returns:
        The numerical result of the expression.

    Raises:
        InvalidExpressionError: If the expression is malformed or cannot be evaluated.
    """
    tokens = tokenize_expression(expression)
    if not tokens:
        raise InvalidExpressionError("Empty expression cannot be evaluated.")

    # Convert unary operators to binary by prepending '0'.
    processed_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        # Check if the current token is a '+' or '-' acting as a unary operator.
        # It's unary if:
        # 1. It's the very first token.
        # 2. It follows an operator.
        # 3. It follows an opening parenthesis.
        is_unary = False
        if token in ('+', '-') and (
            i == 0 or 
            (i > 0 and tokens[i-1] in OPERATORS) or 
            (i > 0 and tokens[i-1] == '(')
        ):
            is_unary = True
        
        if is_unary:
            processed_tokens.append('0')
        processed_tokens.append(token)
        i += 1

    rpn_tokens = shunting_yard(processed_tokens)
    return evaluate_rpn(rpn_tokens)