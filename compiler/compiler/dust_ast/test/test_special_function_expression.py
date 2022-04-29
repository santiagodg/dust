import unittest

from dust_ast import *

class TestSkewnessExpression(unittest.TestCase):
    def test_to_string(self):
        expression = IoExpression(ReadExpression(Identifier('id1')))
        special_function_expression = SpecialFunctionExpression(expression)
        result = special_function_expression.to_string()

        expected = f"""SpecialFunctionExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
