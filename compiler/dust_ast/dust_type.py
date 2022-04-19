from .primitive_type import PrimitiveType
from .array_type import ArrayType

class Type:
    def __init__(self, type: PrimitiveType | ArrayType):
        self.__type: PrimitiveType | ArrayType = type
    
    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'Type:\n'
        type_str: str = self.__type.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}type: {type_str}'
        return result
    
    def __eq__(self, other):
        if other == None:
            return False

        return self.__dict__ == other.__dict__
