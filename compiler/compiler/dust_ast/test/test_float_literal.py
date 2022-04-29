import unittest

from dust_ast import *

class TestFloatLiteral(unittest.TestCase):
    def test_to_string(self):
        f = 1.1
        float_literal = FloatLiteral(f)
        result = float_literal.to_string()

        expected = f"""FloatLiteral:
  float: {f}"""

        self.assertEqual(result, expected)
