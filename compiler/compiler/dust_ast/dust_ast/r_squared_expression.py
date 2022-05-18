import copy
from typing import Optional

from .primitive_type import PrimitiveType
from .dust_type import Type

class RSquaredExpression:
    def __init__(self, expression_0, expression_1, temp_var_generator):
        """
        expression_0: Expression
        expression_1: Expression
        """

        self.__expression_0 = expression_0
        self.__expression_1 = expression_1
        self.__type = Type(PrimitiveType('f64'))
        self.__temporary_variable = temp_var_generator.next(self.__type)

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'RSquaredExpression:\n'
        expression_0_str: str = self.__expression_0.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression_0: {expression_0_str}\n'
        expression_1_str: str = self.__expression_1.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression_1: {expression_1_str}'
        return result
    
    def type(self) -> Optional[Type]:
        return copy.deepcopy(self.__type)
    
    def operand(self):
        """
        :rtype: TemporaryVariable | Identifier | BooleanLiteral | IntegerLiteral | FloatLiteral | CharLiteral | None
        """

        return self.__temporary_variable
    
    def quadruples(self):
        """
        :rtype: List[Tuple[str, str, str, str]]
        """

        return [[
            f'{type(self).__name__} unimplemented', 
            None,
            None,
            self.__temporary_variable,
        ]]

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
