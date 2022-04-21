from .integer_literal import IntegerLiteral

class ArrayType:
    def __init__(self, type, length: IntegerLiteral):
        """
        type: Type
        length: IntegerLiteral
        """
        
        self.__type = type
        self.__length: IntegerLiteral = length
    
    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ArrayType:\n'
        type_str: str = self.__type.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}type: {type_str}\n'
        length_str: str = self.__length.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}length: {length_str}'
        return result
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
