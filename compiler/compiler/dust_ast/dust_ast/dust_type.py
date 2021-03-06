import copy

from .primitive_type import PrimitiveType
from .array_type import ArrayType


class Type:
    def __init__(self, type: PrimitiveType | ArrayType):
        self.__type: PrimitiveType | ArrayType = type

    def canonical(self) -> str:
        return self.__type.canonical()

    def is_primitive(self) -> bool:
        return isinstance(self.__type, PrimitiveType)

    def is_array(self) -> bool:
        return isinstance(self.__type, ArrayType)

    def type(self) -> PrimitiveType | ArrayType:
        return copy.deepcopy(self.__type)

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'Type:\n'
        type_str: str = self.__type.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}type: {type_str}'
        return result

    def __eq__(self, other):
        if not isinstance(other, Type):
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
