from .expression_without_block import ExpressionWithoutBlock
from .expression_with_block import ExpressionWithBlock

class Expression:
    def __init__(self, expression: ExpressionWithoutBlock | ExpressionWithBlock):
        self.__expression: Expression = expression

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'Expression:\n'
        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}'
        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
