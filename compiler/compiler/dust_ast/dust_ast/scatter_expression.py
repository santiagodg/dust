from typing import Optional

from .dust_type import Type


class ScatterExpression:
    def __init__(self, expression_0, expression_1):
        """
        expression_0: Expression
        expression_1: Expression
        """

        self.__expression_0 = expression_0
        self.__expression_1 = expression_1

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ScatterExpression:\n'
        expression_0_str: str = self.__expression_0.to_string(
            indent, padding + indent)
        result += f'{space_padding}{space_indent}expression_0: {expression_0_str}\n'
        expression_1_str: str = self.__expression_1.to_string(
            indent, padding + indent)
        result += f'{space_padding}{space_indent}expression_1: {expression_1_str}'
        return result

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

        size = self.__expression_0.type().type().length().value()
        return [[
            'scatter',
            self.__expression_0.operand(),
            self.__expression_1.operand(),
            size,
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
