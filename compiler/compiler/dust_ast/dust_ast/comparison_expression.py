import copy
from typing import Optional

from .dust_type import Type

class ComparisonExpression:
    def __init__(self, left_expression, operator: str, right_expression, semantic_cube, temp_var_generator):
        """
        left_expression: Expression
        operator: str
        right_expression: Expression
        """
        
        self.__left_expression = left_expression
        self.__operator = operator
        self.__right_expression = right_expression

        self.__type: Optional[Type] = None
        return_type = semantic_cube.search_binary_operation(self.__left_expression.type().type(), self.__operator, self.__right_expression.type().type())
        if return_type != None:
            self.__type = Type(return_type)

        self.__temporary_variable = temp_var_generator.next()

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ComparisonExpression:\n'
        left_expression_str: str = self.__left_expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}left_expression: {left_expression_str}\n'
        result += f"{space_padding}{space_indent}operator: '{self.__operator}'\n"
        right_expression_str: str = self.__right_expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}right_expression: {right_expression_str}'
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
        
        left_expression_temporary_variable = self.__left_expression.operand()
        right_expression_temporary_variable = self.__right_expression.operand()

        return [[
            self.__operator, 
            left_expression_temporary_variable, 
            right_expression_temporary_variable,
            self.__temporary_variable
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
