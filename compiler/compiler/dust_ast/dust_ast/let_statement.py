import copy

from .dust_type import Type
from .identifier import Identifier

class LetStatement:
    def __init__(self, identifier: Identifier, type: Type):
        self.__identifier: Identifier = identifier
        self.__type: Type = type
    
    def identifier(self) -> Identifier:
        return copy.deepcopy(self.__identifier)
    
    def type(self) -> Type:
        return copy.deepcopy(self.__type)
    
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
