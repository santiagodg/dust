import unittest

from dust_ast import *

class TestStaticItem(unittest.TestCase):
    def test_to_string(self):
        identifier = Identifier('id1')
        type = Type(PrimitiveType('bool'))
        static_item = StaticItem(identifier, type)
        result = static_item.to_string()

        expected = f"""StaticItem:
  identifier: {identifier.to_string(2, 2)}
  type: {type.to_string(2, 2)}"""

        self.assertEqual(result, expected)
