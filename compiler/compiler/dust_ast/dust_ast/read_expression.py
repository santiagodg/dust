from typing import Optional

from .dust_type import Type
from .index_expression import IndexExpression
from .identifier import Identifier

class ReadExpression:
    def __init__(self, variable: Identifier | IndexExpression):
        self.__variable: Identifier | IndexExpression = variable

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ReadExpression:\n'

        variable_str: str = self.__variable.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}variable: {variable_str}'

        return result
    
    def type(self) -> Optional[Type]:
        return None

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
