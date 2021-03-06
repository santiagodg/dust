import unittest

from dust_ast import *

class TestCallExpression(unittest.TestCase):
    def test_to_string_with_call_params(self):
        identifier = Identifier('id1')
        call_params = [Expression(ExpressionWithoutBlock(LiteralExpression(IntegerLiteral(1))))]
        call_expression = CallExpression(identifier, call_params)
        result = call_expression.to_string()
        separator = "    \n"

        expected = f"""CallExpression:
  identifier: {identifier.to_string(2, 2)}
  call_params: [
    {separator.join([call_param.to_string(2, 4) for call_param in call_params])}
  ]"""

        self.assertEqual(result, expected)
