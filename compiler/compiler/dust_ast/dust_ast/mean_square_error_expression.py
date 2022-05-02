import copy
from typing import Optional

from .dust_type import Type
from .primitive_type import PrimitiveType

class MeanSquareErrorExpression:
    def __init__(self, expression_0, expression_1):
        self.__expression_0 = expression_0
        self.__expression_1 = expression_1
        self.__type = Type(PrimitiveType('f64'))

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'MeanSquareErrorExpression:\n'
        expression_0_str: str = self.__expression_0.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression_0: {expression_0_str}\n'
        expression_1_str: str = self.__expression_1.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression_1: {expression_1_str}'
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
