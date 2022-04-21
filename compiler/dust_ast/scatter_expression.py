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
        expression_0_str: str = self.__expression_0.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression_0: {expression_0_str}\n'
        expression_1_str: str = self.__expression_1.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression_1: {expression_1_str}'
        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
