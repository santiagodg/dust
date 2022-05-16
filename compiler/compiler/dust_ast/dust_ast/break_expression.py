from typing import Optional

from .dust_type import Type

class BreakExpression:
    def __init__(self):
        pass

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        return 'BreakExpression'
    
    def type(self) -> Optional[Type]:
        return None
    
    def operand(self):
        """
        :rtype: TemporaryVariable | Identifier | BooleanLiteral | IntegerLiteral | FloatLiteral | CharLiteral | None
        """

        return None
    
    def quadruples(self):
        """
        :rtype: List[Tuple[str, str, str, str]]
        """

        return [(
            f'{type(self).__name__} unimplemented', 
            None, 
            None,
            None
        )]

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
