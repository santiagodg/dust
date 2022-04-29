import unittest

from dust_ast import *

class TestIdentifier(unittest.TestCase):
    def test_to_string(self):
        id_str = 'id1'
        identifier = Identifier(id_str)
        result = identifier.to_string()

        expected = f"""Identifier:
  identifier: '{id_str}'"""

        self.assertEqual(result, expected)
