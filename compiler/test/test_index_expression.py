import unittest

from dust_ast import *

class TestIndexExpression(unittest.TestCase):
    def test_to_string(self):
        left_expression = Expression(ExpressionWithoutBlock('id1'))
        right_expression = Expression(ExpressionWithoutBlock(LiteralExpression(0)))
        index_expression = IndexExpression(left_expression, right_expression)
        result = index_expression.to_string()

        expected = f"""IndexExpression:
  left_expression: {left_expression.to_string(2, 2)}
  right_expression: {right_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
