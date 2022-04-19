import unittest

from dust_ast import *

class TestArrayType(unittest.TestCase):
    def test_to_string(self):
        type = Type(PrimitiveType('i32'))
        length = 1
        array_type = ArrayType(type, length)
        result = array_type.to_string()

        expected = f"""ArrayType:
  type: {type.to_string(2, 2)}
  length: {length}"""

        self.assertEqual(result, expected)
