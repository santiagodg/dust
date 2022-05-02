import copy
from typing import Optional

from .primitive_type import PrimitiveType
from .dust_type import Type

class SumExpression:
    def __init__(self, expression):
        "expression: Expression"
        self.__expression = expression
        self.__type = Type(PrimitiveType('f64'))

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'SumExpression:\n'
        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}'
        return result
    
    def type(self) -> str:
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
