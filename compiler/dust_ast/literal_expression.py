from .char_literal import CharLiteral
from .integer_literal import IntegerLiteral

class LiteralExpression:
    def __init__(self, literal: CharLiteral | IntegerLiteral | float | bool):
        self.__literal: CharLiteral | IntegerLiteral | float | bool = literal

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'LiteralExpression:\n'

        if isinstance(self.__literal, (CharLiteral, IntegerLiteral)):
            literal_str = self.__literal.to_string(indent, padding + indent)
            result += f"{space_padding}{space_indent}literal: {literal_str}"    
        else:
            result += f'{space_padding}{space_indent}literal: {self.__literal}'

        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
