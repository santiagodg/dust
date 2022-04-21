from .literal_expression import LiteralExpression
from .operator_expression import OperatorExpression
from .grouped_expression import GroupedExpression
from .array_expression import ArrayExpression
from .index_expression import IndexExpression
from .call_expression import CallExpression
from .continue_expression import ContinueExpression
from .break_expression import BreakExpression
from .return_expression import ReturnExpression
from .special_function_expression import SpecialFunctionExpression
from .identifier import Identifier

class ExpressionWithoutBlock:
    def __init__(
        self, 
        expression: LiteralExpression 
            | Identifier
            | OperatorExpression
            | GroupedExpression
            | ArrayExpression
            | IndexExpression
            | CallExpression
            | ContinueExpression
            | BreakExpression
            | ReturnExpression
            | SpecialFunctionExpression
            ):

        self.__expression = expression

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ExpressionWithoutBlock:\n'

        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}'

        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
