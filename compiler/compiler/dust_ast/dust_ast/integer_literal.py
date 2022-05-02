import copy
from typing import Optional

from .primitive_type import PrimitiveType
from .dust_type import Type

class IntegerLiteral:
    def __init__(self, integer: int):
        self.__integer: int = integer
        self.__type: Type = Type(PrimitiveType('i32'))

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'IntegerLiteral:\n'
        result += f"{space_padding}{space_indent}integer: {self.__integer}"
        return result
    
    def value(self) -> int:
        return self.__integer
    
    def type(self) -> Optional[Type]:
        ":rtype: Optional[Type]"
        return copy.deepcopy(self.__type)

    def __eq__(self, other):
        if not isinstance(other, IntegerLiteral):
            return False

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
