import unittest

from dust_ast import *

class TestMaxExpression(unittest.TestCase):
    def test_to_string(self):
        expression = Expression(ExpressionWithoutBlock(ArrayExpression([
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(1.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(2.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(3.0)))),
        ])))
        max_expression = MaxExpression(expression)
        result = max_expression.to_string()

        expected = f"""MaxExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
