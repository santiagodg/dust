from typing import Optional

from .dust_type import Type


class AssignmentExpression:
    def __init__(self, left_expression, right_expression):
        """
        left_expression: Expression
        right_expression: Expression
        """

        self.__left_expression = left_expression
        self.__right_expression = right_expression

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'AssignmentExpression:\n'
        left_expression_str: str = self.__left_expression.to_string(
            indent, padding + indent)
        result += f'{space_padding}{space_indent}left_expression: {left_expression_str}\n'
        right_expression_str: str = self.__right_expression.to_string(
            indent, padding + indent)
        result += f'{space_padding}{space_indent}right_expression: {right_expression_str}'
        return result

    def type(self) -> Optional[Type]:
        return None

    def quadruples(self):
        """
        :rtype: TemporaryVariable | Identifier | BooleanLiteral | IntegerLiteral | FloatLiteral | CharLiteral | None
        """

        left_expression_temporary_variable = self.__left_expression.operand()
        right_expression_temporary_variable = self.__right_expression.operand()

        size = 1
        if self.__right_expression.type().is_array():
            size = self.__right_expression.type(
            ).type().accumulated_magnitudes()[0]

        return [[
            '=',
            right_expression_temporary_variable,
            size,
            left_expression_temporary_variable
        ]]

    def __eq__(self, other):
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
