import unittest

from dust_ast import *

class TestPlotExpression(unittest.TestCase):
    def test_to_string(self):
        expression_0 = Expression(ExpressionWithoutBlock(ArrayExpression([
            Expression(ExpressionWithoutBlock(LiteralExpression(1.0))),
            Expression(ExpressionWithoutBlock(LiteralExpression(2.0))),
            Expression(ExpressionWithoutBlock(LiteralExpression(3.0))),
        ])))
        expression_1 = Expression(ExpressionWithoutBlock(ArrayExpression([
            Expression(ExpressionWithoutBlock(LiteralExpression(2.0))),
            Expression(ExpressionWithoutBlock(LiteralExpression(3.0))),
            Expression(ExpressionWithoutBlock(LiteralExpression(4.0))),
        ])))
        plot_expression = PlotExpression(expression_0, expression_1)
        result = plot_expression.to_string()

        expected = f"""PlotExpression:
  expression_0: {expression_0.to_string(2, 2)}
  expression_1: {expression_1.to_string(2, 2)}"""

        self.assertEqual(result, expected)
