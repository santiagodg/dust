import unittest

from dust_ast import *

class TestWriteExpression(unittest.TestCase):
    def test_to_string(self):
        expression = Expression(ExpressionWithoutBlock(LiteralExpression(CharLiteral('A'))))
        write_expression = WriteExpression(expression)
        result = write_expression.to_string()

        expected = f"""WriteExpression:
  expression: {expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
