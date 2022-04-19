from .loop_expression import LoopExpression
from .if_expression import IfExpression

class ExpressionWithBlock:
    def __init__(self, expression: LoopExpression | IfExpression):
        self.__expression: LoopExpression | IfExpression = expression

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ExpressionWithBlock:\n'
        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}'
        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
