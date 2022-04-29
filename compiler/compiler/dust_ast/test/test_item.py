import unittest

from dust_ast import *

class TestItem(unittest.TestCase):
    def test_to_string(self):
        static_item = StaticItem(Identifier('id1'), Type(PrimitiveType('bool')))
        item = Item(static_item)
        result = item.to_string()

        expected = f"""Item:
  item: {static_item.to_string(2, 2)}"""

        self.assertEqual(result, expected)
