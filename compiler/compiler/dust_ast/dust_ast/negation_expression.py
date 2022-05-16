from typing import Optional
import copy

from .dust_type import Type
from .integer_literal import IntegerLiteral
from .float_literal import FloatLiteral
from .primitive_type import PrimitiveType

class NegationExpression:
    def __init__(self, operator: str, expression, semantic_cube, temp_var_generator):
        """
        operator: str
        expression: Expression
        """
        
        self.__operator = operator
        self.__expression = expression
        self.__semantic_cube = semantic_cube

        self.__type: Optional[Type] = None
        return_type = None
        if operator == '-':
            return_type = self.__semantic_cube.search_unary_operation('uminus', self.__expression.type().type())
        elif operator == '!':
            return_type = self.__semantic_cube.search_unary_operation('!', self.__expression.type().type())

        if return_type != None:
            self.__type = Type(return_type)
        
        self.__temporary_variable = temp_var_generator.next()

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent

        result = [f'{type(self).__name__}:']

        for key, value in vars(self).items():
            key = key.replace(f'_{type(self).__name__}', '')

            if key == '__semantic_cube' or key == '__temporary_variable':
                continue

            if isinstance(value, (bool, int, float, str)):
                result += [f'{space_padding}{space_indent}{key}: {value}']
            elif isinstance(value, list):
                result += [f'{space_padding}{space_indent}{key}: [']
                for v in value:
                    result += [f'{space_padding}{space_indent * 2}{v.to_string(indent, padding + indent * 2)}']
                result += [f'{space_padding}{space_indent}]']
            else:
                print(f'key={key}, value={value}, type={type(value)}')
                result += [f'{space_padding}{space_indent}{key}: {value.to_string(indent, padding + indent)}']
        
        return '\n'.join(result)
    
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

        expression_operand = self.__expression.operand()
        quadruples = []

        


        if self.__operator == '-':
            if self.__expression.type().type() == PrimitiveType('i32'):
                quadruples = [[
                    self.__operator, 
                    expression_operand, 
                    IntegerLiteral(0),
                    self.__temporary_variable,
                ]]
            elif self.__expression.type().type() == PrimitiveType('f64'):
                quadruples = [[
                    self.__operator, 
                    expression_operand, 
                    FloatLiteral(0),
                    self.__temporary_variable,
                ]]
        elif self.__operator == '!':
            quadruples = [[
                self.__operator, 
                expression_operand, 
                None,
                self.__temporary_variable,
            ]]

        return quadruples

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
