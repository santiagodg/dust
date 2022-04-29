import unittest

from dust_ast import *

class TestLoopExpression(unittest.TestCase):
    def test_to_string(self):
        expression = InfiniteLoopExpression(BlockExpression([]))
        loop_expression = LoopExpression(expression)
        result = loop_expression.to_string()

        expected = f"""LoopExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
