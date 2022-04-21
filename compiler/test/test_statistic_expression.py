import unittest

from dust_ast import *

class TestStatisticExpression(unittest.TestCase):
    def test_to_string(self):
        expression = MinExpression(Expression(ExpressionWithoutBlock(ArrayExpression([
            Expression(ExpressionWithoutBlock(LiteralExpression(1.0))),
            Expression(ExpressionWithoutBlock(LiteralExpression(2.0))),
            Expression(ExpressionWithoutBlock(LiteralExpression(3.0))),
        ]))))
        statistic_expression = StatisticExpression(expression)
        result = statistic_expression.to_string()

        expected = f"""StatisticExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
