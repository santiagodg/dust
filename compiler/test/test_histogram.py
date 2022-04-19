import unittest

from dust_ast import *

class TestHistogramExpression(unittest.TestCase):
    def test_to_string(self):
        expression = Expression(ExpressionWithoutBlock(ArrayExpression([
            Expression(ExpressionWithoutBlock(LiteralExpression(1.0))),
            Expression(ExpressionWithoutBlock(LiteralExpression(2.0))),
            Expression(ExpressionWithoutBlock(LiteralExpression(3.0))),
        ])))
        histogram_expression = HistogramExpression(expression)
        result = histogram_expression.to_string()

        expected = f"""HistogramExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
