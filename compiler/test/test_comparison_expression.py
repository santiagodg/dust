import unittest

from dust_ast import *

class TestComparisonExpression(unittest.TestCase):
    def test_to_string(self):
        left_expression = Expression(ExpressionWithoutBlock(LiteralExpression(1)))
        operator = '=='
        right_expression = Expression(ExpressionWithoutBlock(LiteralExpression(2)))
        comparison_expression = ComparisonExpression(left_expression, operator, right_expression)
        result = comparison_expression.to_string()

        expected = f"""ComparisonExpression:
  left_expression: {left_expression.to_string(2, 2)}
  operator: '{operator}'
  right_expression: {right_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
