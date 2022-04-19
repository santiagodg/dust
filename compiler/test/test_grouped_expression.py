import unittest

from dust_ast import *

class TestGroupedExpression(unittest.TestCase):
    def test_to_string(self):
        expression = Expression(ExpressionWithoutBlock(LiteralExpression(1)))
        grouped_expression = GroupedExpression(expression)
        result = grouped_expression.to_string()

        expected = f"""GroupedExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
