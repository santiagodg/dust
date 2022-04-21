import unittest

from dust_ast import *

class TestLiteralExpression(unittest.TestCase):
    def test_to_string_with_literal_char(self):
        char_literal = 'A'
        literal_expression = LiteralExpression(char_literal)
        result = literal_expression.to_string()

        expected = f"""LiteralExpression:
  literal: '{char_literal}'"""

        self.assertEqual(result, expected)
    
    def test_to_string_not_literal_char(self):
        int_literal = 1
        literal_expression = LiteralExpression(int_literal)
        result = literal_expression.to_string()

        expected = f"""LiteralExpression:
  literal: {int_literal}"""

        self.assertEqual(result, expected)
