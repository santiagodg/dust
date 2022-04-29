import unittest

from dust_ast import *

class TestExpressionWithBlock(unittest.TestCase):
    def test_to_string(self):
        if_expression = LoopExpression(InfiniteLoopExpression(BlockExpression([])))
        expression_with_block = ExpressionWithBlock(if_expression)
        result = expression_with_block.to_string()

        expected = f"""ExpressionWithBlock:
  expression: {if_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
