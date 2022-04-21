class NegationExpression:
    def __init__(self, operator: str, expression):
        """
        operator: str
        expression: Expression
        """
        
        self.__operator = operator
        self.__expression = expression

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'NegationExpression:\n'
        result += f"{space_padding}{space_indent}operator: '{self.__operator}'\n"
        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}'
        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__