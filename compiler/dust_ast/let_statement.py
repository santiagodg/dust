from .dust_type import Type
from .identifier import Identifier

class LetStatement:
    def __init__(self, identifier: Identifier, type: Type):
        self.__identifier: Identifier = identifier
        self.__type: Type = type
    
    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'LetStatement:\n'
        identifier_str: str = self.__identifier.to_string(indent, padding + indent)
        result += f"{space_padding}{space_indent}identifier: {identifier_str}\n"
        type_str: str = self.__type.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}type: {type_str}'
        return result
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
