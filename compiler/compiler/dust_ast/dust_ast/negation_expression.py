from typing import Optional
import copy

from .dust_type import Type

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
        return_type = self.__semantic_cube.search_unary_operation(self.__operator, self.__expression.type().type())
        if return_type != None:
            self.__type = Type(return_type)
        
        self.__temporary_variable = temp_var_generator.next()

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'NegationExpression:\n'
        result += f"{space_padding}{space_indent}operator: '{self.__operator}'\n"
        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}'
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

        expression_operand = self.__expression.operand()

        return [(
            self.__operator, 
            expression_operand, 
            '',
            self.__temporary_variable
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
