import unittest

from dust_ast import *

class TestStatement(unittest.TestCase):
    def test_to_string(self):
        expression = Expression(ExpressionWithBlock(LoopExpression(InfiniteLoopExpression(BlockExpression([])))))
        statement = Statement(expression)
        result = statement.to_string()

        expected = f"""Statement:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
