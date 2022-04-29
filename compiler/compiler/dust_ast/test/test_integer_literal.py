import unittest

from dust_ast import *

class TestIntegerLiteral(unittest.TestCase):
    def test_to_string(self):
        integer = 1
        integer_literal = IntegerLiteral(integer)
        result = integer_literal.to_string()

        expected = f"""IntegerLiteral:
  integer: {integer}"""

        self.assertEqual(result, expected)
