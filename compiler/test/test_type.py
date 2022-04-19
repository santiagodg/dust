import unittest

from dust_ast import *

class TestType(unittest.TestCase):
    def test_to_string(self):
        primitive_type = PrimitiveType('bool')
        type = Type(primitive_type)
        result = type.to_string()

        expected = f"""Type:
  type: {primitive_type.to_string(2, 2)}"""

        self.assertEqual(result, expected)
