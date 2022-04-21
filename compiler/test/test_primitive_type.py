import unittest

from dust_ast import *

class TestPrimitiveType(unittest.TestCase):
    def test_to_string(self):
        type = 'bool'
        primitive_type = PrimitiveType(type)
        result = primitive_type.to_string()

        expected = f"""PrimitiveType:
  type: '{type}'"""

        self.assertEqual(result, expected)
