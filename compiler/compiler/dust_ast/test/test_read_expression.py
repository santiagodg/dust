import unittest

from dust_ast import *

class TestReadExpression(unittest.TestCase):
    
    def test_to_string_with_index_expression(self):
        identifier_expression = Identifier('id1')
        read_expression = ReadExpression(identifier_expression)
        result = read_expression.to_string()

        expected = f"""ReadExpression:
  variable: {identifier_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
