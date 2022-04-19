import unittest

from dust_ast import *

class TestExpression(unittest.TestCase):
    def test_to_string(self):
        expression_without_block = ExpressionWithoutBlock(LiteralExpression(1))
        expression = Expression(expression_without_block)
        result = expression.to_string()

        expected = f"""Expression:
  expression: {expression_without_block.to_string(2, 2)}"""

        self.assertEqual(result, expected)
