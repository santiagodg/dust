import unittest

from dust_ast import *

class TestSumExpression(unittest.TestCase):
    def test_to_string(self):
        expression = MinExpression(Expression(ExpressionWithoutBlock(ArrayExpression([
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(1.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(2.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(3.0)))),
        ]))))
        sum_expression = SumExpression(expression)
        result = sum_expression.to_string()

        expected = f"""SumExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
