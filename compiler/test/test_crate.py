import unittest

from dust_ast import *

class TestCrate(unittest.TestCase):
    def test_to_string_empty(self):
        items = []
        crate = Crate(items)
        result = crate.to_string()

        expected = f"""Crate:
  items: []"""

        self.assertEqual(result, expected)

    def test_to_string_with_items(self):
        items = [Item(StaticItem('id1', Type(PrimitiveType('bool'))))]
        crate = Crate(items)
        result = crate.to_string()
        separator = "    \n"

        expected = f"""Crate:
  items: [
    {separator.join([item.to_string(2, 4) for item in items])}
  ]"""

        self.assertEqual(result, expected)
