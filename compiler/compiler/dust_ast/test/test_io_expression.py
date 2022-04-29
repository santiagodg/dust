import unittest

from dust_ast import *

class TestIoExpression(unittest.TestCase):
    def test_to_string(self):
        read_expression = ReadExpression(Identifier('id1'))
        io_expression = IoExpression(read_expression)
        result = io_expression.to_string()

        expected = f"""IoExpression:
  expression: {read_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
