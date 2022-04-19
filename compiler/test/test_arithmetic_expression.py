import unittest

from dust_ast import *

class TestArithmeticExpression(unittest.TestCase):
    def test_to_string(self):
        left_expression = Expression(ExpressionWithoutBlock(LiteralExpression(1)))
        operator = '+'
        right_expression = Expression(ExpressionWithoutBlock(LiteralExpression(2)))
        arithmetic_exp = ArithmeticExpression(left_expression, operator, right_expression)
        result = arithmetic_exp.to_string()

        expected = f"""ArithmeticExpression:
  left_expression: {left_expression.to_string(2, 2)}
  operator: '{operator}'
  right_expression: {right_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
