import unittest

from dust_ast import *

class TestBooleanExpression(unittest.TestCase):
    def test_to_string(self):
        left_expression = Expression(ExpressionWithoutBlock(LiteralExpression(IntegerLiteral(1))))
        operator = '+'
        right_expression = Expression(ExpressionWithoutBlock(LiteralExpression(IntegerLiteral(2))))
        bolean_expression = BooleanExpression(left_expression, operator, right_expression)
        result = bolean_expression.to_string()

        expected = f"""BooleanExpression:
  left_expression: {left_expression.to_string(2, 2)}
  operator: '+'
  right_expression: {right_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
