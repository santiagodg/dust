import unittest

from dust_ast import *

class TestExpressionWithoutBlock(unittest.TestCase):
    def test_to_string_with_identifier(self):
        identifier = 'id1'
        expression_without_block = ExpressionWithoutBlock(identifier)
        result = expression_without_block.to_string()

        expected = f"""ExpressionWithoutBlock:
  expression: '{identifier}'"""

        self.assertEqual(result, expected)

    def test_to_string_with_subexpression(self):
        literal_expression = LiteralExpression(1)
        expression_without_block = ExpressionWithoutBlock(literal_expression)
        result = expression_without_block.to_string()

        expected = f"""ExpressionWithoutBlock:
  expression: {literal_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
