import unittest

from dust_ast import *

class TestFunction(unittest.TestCase):
    def test_to_string_empty(self):
        identifier = 'id1'
        parameters = []
        return_type = None
        let_statements = []
        block_expression = BlockExpression([])
        function = Function(identifier, parameters, return_type, let_statements, block_expression)
        result = function.to_string()

        expected = f"""Function:
  identifier: '{identifier}'
  parameters: []
  return_type: None
  let_statements: []
  block: {block_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
    
    def test_to_string_with_data(self):
        identifier = 'id1'
        parameters = [FunctionParameter('id2', Type(PrimitiveType('bool')))]
        return_type = Type(PrimitiveType('bool'))
        let_statements = [LetStatement('id3', Type(PrimitiveType('bool')))]
        block_expression = BlockExpression([])
        function = Function(identifier, parameters, return_type, let_statements, block_expression)
        result = function.to_string()
        separator = "    \n"

        expected = f"""Function:
  identifier: '{identifier}'
  parameters: [
    {separator.join([parameter.to_string(2, 4) for parameter in parameters])}
  ]
  return_type: {return_type.to_string(2, 2)}
  let_statements: [
    {separator.join([let_statement.to_string(2, 4) for let_statement in let_statements])}
  ]
  block: {block_expression.to_string(2, 2)}"""

        self.assertEqual(result, expected)
