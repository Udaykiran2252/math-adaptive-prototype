# puzzle_generator.py
import random
from typing import Tuple

OPERATIONS = ["addition", "subtraction", "multiplication", "division"]

def _make_addition(difficulty: str) -> Tuple[str,int]:
    if difficulty == "Easy":
        a, b = random.randint(1,9), random.randint(1,9)
    elif difficulty == "Medium":
        a, b = random.randint(10,49), random.randint(5,49)
    else:  # Hard
        a, b = random.randint(50,199), random.randint(10,99)
    return f"{a} + {b}", a + b

def _make_subtraction(difficulty: str) -> Tuple[str,int]:
    if difficulty == "Easy":
        a, b = random.randint(2,9), random.randint(1, a:=random.randint(1,8))
        # ensure non-negative
        a, b = max(a,b), min(a,b)
    elif difficulty == "Medium":
        a, b = random.randint(10,80), random.randint(1,49)
        a, b = max(a,b), min(a,b)
    else:
        a, b = random.randint(80,199), random.randint(10,79)
        a, b = max(a,b), min(a,b)
    return f"{a} - {b}", a - b

def _make_multiplication(difficulty: str) -> Tuple[str,int]:
    if difficulty == "Easy":
        a, b = random.randint(1,5), random.randint(1,5)
    elif difficulty == "Medium":
        a, b = random.randint(3,12), random.randint(2,12)
    else:
        a, b = random.randint(10,25), random.randint(5,15)
    return f"{a} × {b}", a * b

def _make_division(difficulty: str) -> Tuple[str,int]:
    # produce integer division problems
    if difficulty == "Easy":
        b = random.randint(1,5)
        q = random.randint(1,9)
    elif difficulty == "Medium":
        b = random.randint(2,12)
        q = random.randint(2,12)
    else:
        b = random.randint(5,20)
        q = random.randint(5,25)
    a = b * q
    return f"{a} ÷ {b}", q

def generate_puzzle(difficulty: str = "Easy", operation: str = None) -> dict:
    """
    Returns: { 'question': str, 'answer': int, 'difficulty': str, 'operation': str }
    """
    if operation is None:
        operation = random.choice(OPERATIONS)
    if operation == "addition":
        q, a = _make_addition(difficulty)
    elif operation == "subtraction":
        q, a = _make_subtraction(difficulty)
    elif operation == "multiplication":
        q, a = _make_multiplication(difficulty)
    elif operation == "division":
        q, a = _make_division(difficulty)
    else:
        raise ValueError("Unknown operation")
    return {"question": q, "answer": a, "difficulty": difficulty, "operation": operation}
