class IndexExpression:
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
        result += f'IndexExpression:\n'
        left_expression_str: str = self.__left_expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}left_expression: {left_expression_str}\n'
        right_expression_str: str = self.__right_expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}right_expression: {right_expression_str}'
        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
