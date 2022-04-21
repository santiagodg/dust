import unittest

from dust_ast import *

class TestPredicateLoopExpression(unittest.TestCase):
    def test_to_string(self):
        expression = Expression(ExpressionWithoutBlock(LiteralExpression('true')))
        block = BlockExpression([])
        predicate_loop_expression = PredicateLoopExpression(expression, block)
        result = predicate_loop_expression.to_string()

        expected = f"""PredicateLoopExpression:
  expression: {expression.to_string(2, 2)}
  block: {block.to_string(2, 2)}"""

        self.assertEqual(result, expected)
