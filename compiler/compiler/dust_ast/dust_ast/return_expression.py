import copy
from typing import Optional

from .dust_type import Type


class ReturnExpression:
    def __init__(self, expression):
        "expression: Optional[Expression]"
        self.__expression = expression
        if expression is None:
            self.__type = None
            return
        self.__type = self.__expression.type()

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ReturnExpression:\n'

        if self.__expression == None:
            result += f'{space_padding}{space_indent}expression: None'
        else:
            expression_str: str = self.__expression.to_string(
                indent, padding + indent)
            result += f'{space_padding}{space_indent}expression: {expression_str}'

        return result

    def type(self) -> Optional[Type]:
        return copy.deepcopy(self.__type)

    def operand(self):
        """
        :rtype: TemporaryVariable | Identifier | BooleanLiteral | IntegerLiteral | FloatLiteral | CharLiteral | None
        """

        return None

    def quadruples(self):
        """
        :rtype: List[Tuple[str, str, str, str]]
        """

        return [[
            f'{type(self).__name__} unimplemented',
            None,
            None,
            None,
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
