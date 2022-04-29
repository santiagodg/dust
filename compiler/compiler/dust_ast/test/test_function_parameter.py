import unittest

from dust_ast import *

class TestFunctionParameter(unittest.TestCase):
    def test_to_string(self):
        identifier = Identifier('id1')
        type = Type(PrimitiveType('bool'))
        function_parameter = FunctionParameter(identifier, type)
        result = function_parameter.to_string()

        expected = f"""FunctionParameter:
  identifier: {identifier.to_string(2, 2)}
  type: {type.to_string(2, 2)}"""

        self.assertEqual(result, expected)
