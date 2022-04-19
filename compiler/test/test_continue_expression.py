import unittest

from dust_ast import *

class TestContinueExpression(unittest.TestCase):
    def test_to_string(self):
        continue_expression = ContinueExpression()
        result = continue_expression.to_string()
        expected = f"ContinueExpression"
        self.assertEqual(result, expected)
