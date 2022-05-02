import copy

from .primitive_type import PrimitiveType
from .dust_type import Type

class FloatLiteral:
    def __init__(self, f: float):
        self.__float: float = f
        self.__type: Type = Type(PrimitiveType('f64'))

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'FloatLiteral:\n'
        result += f"{space_padding}{space_indent}float: {self.__float}"
        return result
    
    def type(self) -> Type:
        return copy.deepcopy(self.__type)
    
    def value(self) -> float:
        return self.__float
    
    def operand(self):
        """
        :rtype: TemporaryVariable | Identifier | BooleanLiteral | IntegerLiteral | FloatLiteral | CharLiteral | None
        """
        
        return self

    def __eq__(self, other):
        if not isinstance(other, FloatLiteral):
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
