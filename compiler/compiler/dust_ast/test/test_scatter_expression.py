import unittest

from dust_ast import *

class TestScatterExpression(unittest.TestCase):
    def test_to_string(self):
        expression_0 = Expression(ExpressionWithoutBlock(ArrayExpression([
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(1.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(2.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(3.0)))),
        ])))
        expression_1 = Expression(ExpressionWithoutBlock(ArrayExpression([
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(2.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(3.0)))),
            Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(4.0)))),
        ])))
        scatter_expression = ScatterExpression(expression_0, expression_1)
        result = scatter_expression.to_string()

        expected = f"""ScatterExpression:
  expression_0: {expression_0.to_string(2, 2)}
  expression_1: {expression_1.to_string(2, 2)}"""

        self.assertEqual(result, expected)
