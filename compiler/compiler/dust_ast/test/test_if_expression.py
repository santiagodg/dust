import unittest

from dust_ast import *

class TestIfExpression(unittest.TestCase):
    def test_to_string_without_false_block(self):
        expression = Expression(ExpressionWithoutBlock(LiteralExpression(BooleanLiteral(True))))
        true_block = BlockExpression([])
        false_block = None
        if_expression = IfExpression(expression, true_block, false_block)
        result = if_expression.to_string()

        expected = f"""IfExpression:
  expression: {expression.to_string(2, 2)}
  true_block: {true_block.to_string(2, 2)}
  false_block: None"""

        self.assertEqual(result, expected)

    def test_to_string_with_false_block(self):
        expression = Expression(ExpressionWithoutBlock(LiteralExpression(BooleanLiteral(True))))
        true_block = BlockExpression([])
        false_block = BlockExpression([])
        if_expression = IfExpression(expression, true_block, false_block)
        result = if_expression.to_string()

        expected = f"""IfExpression:
  expression: {expression.to_string(2, 2)}
  true_block: {true_block.to_string(2, 2)}
  false_block: {false_block.to_string(2, 2)}"""

        self.assertEqual(result, expected)
