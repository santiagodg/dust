import copy
from typing import Optional

from .char_literal import CharLiteral
from .integer_literal import IntegerLiteral
from .float_literal import FloatLiteral
from .boolean_literal import BooleanLiteral
from .dust_type import Type

class LiteralExpression:
    def __init__(self, literal: CharLiteral | IntegerLiteral | FloatLiteral | BooleanLiteral):
        self.__literal = literal
        self.__type = self.__literal.type()

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'LiteralExpression:\n'
        literal_str = self.__literal.to_string(indent, padding + indent)
        result += f"{space_padding}{space_indent}literal: {literal_str}"
        return result
    
    def type(self) -> Optional[Type]:
        return copy.deepcopy(self.__type)
    
    def operand(self):
        """
        :rtype: TemporaryVariable | Identifier | BooleanLiteral | IntegerLiteral | FloatLiteral | CharLiteral | None
        """
        
        return self.__literal.operand()

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
