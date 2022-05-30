import copy
from typing import Optional
import sys

from .dust_type import Type, ArrayType


class IndexExpression:
    def __init__(self, identifier, expressions, temporary_variable):
        """
        expression: Expression
        index: INTEGER_LITERAL
        """
        self.__identifier = identifier
        self.__expressions = expressions
        subtype = self.__identifier.type().type()
        if not isinstance(subtype, ArrayType):
            print(
                'Creating an index expression with a non-array type identifier is not allowed.')
            sys.exit(1)
        while isinstance(subtype, ArrayType):
            subtype = subtype.type().type()
        self.__type = Type(subtype)
        self.__temporary_variable = temporary_variable

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += 'IndexExpression:\n'
        result += f'{space_padding}{space_indent}identifier: {self.__identifier.to_string(indent, padding + indent)}'
        if len(self.__expressions) == 0:
            result += f'{space_padding}{space_indent}expressions: []'
        else:
            result += f'{space_padding}{space_indent}expressions: [\n'
            for expression in self.__expressions:
                expressions_str: str = expression.to_string(
                    indent, padding + indent * 2)
                result += f'{space_padding}{space_indent}{space_indent}{expressions_str}\n'
            result += f'{space_padding}{space_indent}]'
        result += f'{space_padding}{space_indent}type: {self.__type.to_string(indent, padding + indent)}'
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

        return []

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
