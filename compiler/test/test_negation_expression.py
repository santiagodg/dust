import unittest

from dust_ast import *

class TestNegationExpression(unittest.TestCase):
    def test_to_string(self):
        operator = '!'
        expression = Expression(ExpressionWithoutBlock(LiteralExpression('true')))
        negation_expression = NegationExpression(operator, expression)
        result = negation_expression.to_string()

        expected = f"""NegationExpression:
  operator: '{operator}'
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
