import unittest

from dust_ast import *

class TestTypeCastExpression(unittest.TestCase):
    def test_to_string(self):
        expression = Expression(ExpressionWithoutBlock(LiteralExpression(IntegerLiteral(1))))
        type = Type(PrimitiveType('float'))
        type_cast_expression = TypeCastExpression(expression, type)
        result = type_cast_expression.to_string()

        expected = f"""TypeCastExpression:
  expression: {expression.to_string(2, 2)}
  type: {type.to_string(2, 2)}"""

        self.assertEqual(result, expected)
