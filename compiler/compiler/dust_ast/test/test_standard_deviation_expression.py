import unittest

from dust_ast import *

class TestStandardDeviationExpression(unittest.TestCase):
    def test_to_string(self):
        expression = Expression(ExpressionWithoutBlock(ArrayExpression([
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(1.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(2.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(3.0)))),
        ])))
        standard_deviation_expression = StandardDeviationExpression(expression)
        result = standard_deviation_expression.to_string()

        expected = f"""StandardDeviationExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
