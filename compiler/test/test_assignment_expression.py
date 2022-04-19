import unittest

from dust_ast import *

class TestAssignmentExpression(unittest.TestCase):
    def test_to_string(self):
        left_expression = Expression(ExpressionWithoutBlock(LiteralExpression(1)))
        right_expression = Expression(ExpressionWithoutBlock(LiteralExpression(2)))
        assignment_expression = AssignmentExpression(left_expression, right_expression)
        result = assignment_expression.to_string()

        expected = f"""AssignmentExpression:
  left_expression: {left_expression.to_string(2, 2)}
  right_expression: {right_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
