import unittest

from dust_ast import *

example_block_expression_empty = BlockExpression([])

class TestBlockExpression(unittest.TestCase):
    def test_to_string_empty(self):
        block_expression = example_block_expression_empty
        result = block_expression.to_string()

        expected = f"""BlockExpression:
  statements: []"""

        self.assertEqual(result, expected)

    def test_to_string_with_statements(self):
        statements = [Statement(Expression(ExpressionWithoutBlock(LiteralExpression(1))))]
        block_expression = BlockExpression(statements)
        result = block_expression.to_string()
        separator = "    \n"

        expected = f"""BlockExpression:
  statements: [
    {separator.join([statement.to_string(2, 4) for statement in statements])}
  ]"""

        self.assertEqual(result, expected)
