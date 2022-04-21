import unittest

from dust_ast import *

class TestLetExpression(unittest.TestCase):
    def test_to_string(self):
        identifier = 'id1'
        type = Type(PrimitiveType('bool'))
        let_statement = LetStatement(identifier, type)
        result = let_statement.to_string()

        expected = f"""LetStatement:
  identifier: '{identifier}'
  type: {type.to_string(2, 2)}"""

        self.assertEqual(result, expected)
