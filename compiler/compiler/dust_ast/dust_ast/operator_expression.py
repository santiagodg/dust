from .negation_expression import NegationExpression
from .arithmetic_expression import ArithmeticExpression
from .comparison_expression import ComparisonExpression
from .boolean_expression import BooleanExpression
from .type_cast_expression import TypeCastExpression
from .assignment_expression import AssignmentExpression

class OperatorExpression:
    def __init__(
        self, 
        expression: NegationExpression 
            | ArithmeticExpression
            | ComparisonExpression
            | BooleanExpression
            | TypeCastExpression
            | AssignmentExpression):

        self.__expression = expression

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'OperatorExpression:\n'
        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}'
        return result

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
