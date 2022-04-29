import unittest

from dust_ast import *

class TestMedianExpression(unittest.TestCase):
    def test_to_string(self):
        expression = Expression(ExpressionWithoutBlock(ArrayExpression([
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(1.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(2.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(3.0)))),
        ])))
        median_expression = MedianExpression(expression)
        result = median_expression.to_string()

        expected = f"""MedianExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
