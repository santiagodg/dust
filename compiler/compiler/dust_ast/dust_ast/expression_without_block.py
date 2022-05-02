import copy
from typing import Optional

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
from .dust_type import Type

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
        self.__type = self.__expression.type()

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ExpressionWithoutBlock:\n'

        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}'

        return result
    
    def type(self) -> Optional[Type]:
        return copy.deepcopy(self.__type)
    
    def operand(self):
        """
        :rtype: TemporaryVariable | Identifier | BooleanLiteral | IntegerLiteral | FloatLiteral | CharLiteral | None
        """
        
        return self.__expression.operand()

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = f'{type(self).__name__}('
        attr_str = []
        for key, value in vars(self).items():
            prefix = key.replace(f"_{type(self).__name__}", '')
            attr_str += [f'{prefix}={str(value)}']
        result += ','.join(attr_str)
        result += ')'
        return result
