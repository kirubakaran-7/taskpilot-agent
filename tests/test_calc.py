"""Tests for the safe calculator. No API key or network needed."""
import math

import pytest

from agent.calc import safe_eval


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("2 + 3", 5),
        ("12 * (3 + 4) / 2", 42),
        ("2 ** 10", 1024),
        ("17 % 5", 2),
        ("17 // 5", 3),
        ("-5 + 2", -3),
        ("1000 * 0.18", 180.0),
    ],
)
def test_safe_eval_valid(expr, expected):
    assert math.isclose(safe_eval(expr), expected)


@pytest.mark.parametrize(
    "expr",
    [
        "__import__('os').system('echo hacked')",
        "open('secret.txt')",
        "x + 1",
        "print(1)",
        "1; 2",
    ],
)
def test_safe_eval_rejects_unsafe(expr):
    with pytest.raises((ValueError, SyntaxError)):
        safe_eval(expr)
