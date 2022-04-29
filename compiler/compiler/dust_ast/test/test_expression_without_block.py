import unittest

from dust_ast import *

class TestExpressionWithoutBlock(unittest.TestCase):
    def test_to_string(self):
        identifier = Identifier('id1')
        expression_without_block = ExpressionWithoutBlock(identifier)
        result = expression_without_block.to_string()

        expected = f"""ExpressionWithoutBlock:
  expression: {identifier.to_string(2, 2)}"""

        self.assertEqual(result, expected)
