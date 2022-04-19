import unittest

from dust_ast import *

class TestArrayExpression(unittest.TestCase):
    def test_to_string_empty(self):
        array_expression = ArrayExpression([])
        result = array_expression.to_string()

        expected = f"""ArrayExpression:
  array_elements: []"""

        self.assertEqual(result, expected)

    def test_to_string_with_array_elements(self):
        array_elements = [Expression(ExpressionWithoutBlock(LiteralExpression(1)))]
        array_expression = ArrayExpression(array_elements)
        result = array_expression.to_string()
        separator = "    \n"

        expected = f"""ArrayExpression:
  array_elements: [
    {separator.join([array_element.to_string(2, 4) for array_element in array_elements])}
  ]"""

        self.assertEqual(result, expected)
