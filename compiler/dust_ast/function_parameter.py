from .dust_type import Type

class FunctionParameter:
    def __init__(self, identifier: str, type: Type):
        self.__identifier: str = identifier
        self.__type: Type = type
    
    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'FunctionParameter:\n'
        result += f"{space_padding}{space_indent}identifier: '{self.__identifier}'\n"
        type_str: str = self.__type.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}type: {type_str}'
        return result
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
