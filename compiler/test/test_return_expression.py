import unittest

from numpy import index_exp

from dust_ast import *

class TestReturnExpression(unittest.TestCase):
    def test_to_string(self):
        expression = Expression(ExpressionWithoutBlock(LiteralExpression(0)))
        return_expression = ReturnExpression(expression)
        result = return_expression.to_string()

        expected = f"""ReturnExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
