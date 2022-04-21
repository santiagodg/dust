import unittest

from dust_ast import *

class TestOperatorExpression(unittest.TestCase):
    def test_to_string(self):
        expression = NegationExpression('!', Expression(ExpressionWithoutBlock(LiteralExpression('true'))))
        operator_expression = OperatorExpression(expression)
        result = operator_expression.to_string()

        expected = f"""OperatorExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
