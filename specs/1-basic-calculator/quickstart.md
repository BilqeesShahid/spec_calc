# Quickstart Guide: Basic Calculator Core Library

This guide provides instructions to quickly get started with the Basic Calculator core library.

## Prerequisites

*   Python 3.12+ installed on your system.

## Installation (once packaged)

(Instructions for installing the library via pip or other package managers will go here once the project is packaged.)

## Usage (as a library)

Once the core calculator library is available, you can import and use its functionality in your Python code.

```python
from calculator.core import evaluate_expression

# Example usage
result1 = evaluate_expression("2 + 2")
print(f"2 + 2 = {result1}")

result2 = evaluate_expression("(5 * 3) - 1")
print(f"(5 * 3) - 1 = {result2}")

try:
    evaluate_expression("10 / 0")
except ValueError as e:
    print(f"Error: {e}")

try:
    evaluate_expression("invalid input")
except ValueError as e:
    print(f"Error: {e}")
```
(The exact function names and error handling might vary based on implementation.)