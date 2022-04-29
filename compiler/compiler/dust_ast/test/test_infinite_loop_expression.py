import unittest

from dust_ast import *

class TestInfiniteLoopExpression(unittest.TestCase):
    def test_to_string(self):
        block = BlockExpression([])
        infinite_loop_expression = InfiniteLoopExpression(block)
        result = infinite_loop_expression.to_string()

        expected = f"""InfiniteLoopExpression:
  block: {block.to_string(2, 2)}"""

        self.assertEqual(result, expected)
