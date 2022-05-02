import copy
from typing import Optional

from .io_expression import IoExpression
from .statistic_expression import StatisticExpression
from .dust_type import Type

class SpecialFunctionExpression:
    def __init__(
        self, 
        expression: IoExpression 
            | StatisticExpression):

        self.__expression: IoExpression | StatisticExpression = expression
        self.__type = self.__expression.type()

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'SpecialFunctionExpression:\n'
        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}'
        return result
    
    def type(self) -> Optional[Type]:
        return copy.deepcopy(self.__type)

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
