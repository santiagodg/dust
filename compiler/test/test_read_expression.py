import unittest

from numpy import index_exp

from dust_ast import *

class TestReadExpression(unittest.TestCase):
    def test_to_string_with_identifier(self):
        identifier = 'id1'
        read_expression = ReadExpression(identifier)
        result = read_expression.to_string()

        expected = f"""ReadExpression:
  variable: '{identifier}'"""

        self.assertEqual(result, expected)
    
    def test_to_string_with_index_expression(self):
        index_expression = IndexExpression(Expression(ExpressionWithoutBlock(Identifier('id1'))), ExpressionWithoutBlock(LiteralExpression(0)))
        read_expression = ReadExpression(index_expression)
        result = read_expression.to_string()

        expected = f"""ReadExpression:
  variable: {index_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
