import unittest

from dust_ast import *

class TestBooleanLiteral(unittest.TestCase):
    def test_to_string(self):
        b = True
        boolean_literal = BooleanLiteral(b)
        result = boolean_literal.to_string()

        expected = f"""BooleanLiteral:
  boolean: {b}"""

        self.assertEqual(result, expected)
