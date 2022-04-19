import unittest

from dust_ast import *

class TestBreakExpression(unittest.TestCase):
    def test_to_string(self):
        break_expression = BreakExpression()
        result = break_expression.to_string()
        expected = f"BreakExpression"
        self.assertEqual(result, expected)
