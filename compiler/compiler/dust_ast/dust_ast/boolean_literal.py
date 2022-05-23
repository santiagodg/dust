import copy
from typing import Optional

from .primitive_type import PrimitiveType
from .dust_type import Type


class BooleanLiteral:
    def __init__(self, boolean: bool):
        self.__boolean: boolean = boolean
        self.__type: Type = Type(PrimitiveType('bool'))
        self.__virtual_address = None

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'BooleanLiteral:\n'
        result += f"{space_padding}{space_indent}boolean: {self.__boolean}"
        return result

    def value(self) -> bool:
        return self.__boolean

    def type(self) -> Optional[Type]:
        return copy.deepcopy(self.__type)

    def operand(self):
        """
        :rtype: TemporaryVariable | Identifier | BooleanLiteral | IntegerLiteral | FloatLiteral | CharLiteral | None
        """
        if self.__virtual_address is not None:
            return self.__virtual_address
        return self

    def set_virtual_address(self, virtual_address):
        self.__virtual_address = virtual_address

    def __eq__(self, other):
        if not isinstance(other, BooleanLiteral):
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
