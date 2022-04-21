import unittest

from dust_ast import *

class TestCharLiteral(unittest.TestCase):
    def test_to_string(self):
        char = 'A'
        char_literal = CharLiteral(char)
        result = char_literal.to_string()

        expected = f"""CharLiteral:
  char: '{char}'"""

        self.assertEqual(result, expected)
