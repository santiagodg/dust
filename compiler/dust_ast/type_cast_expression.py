from .dust_type import Type

class TypeCastExpression:
    def __init__(self, expression, type: Type):
        """
        expression: Expression
        type: Type
        """
        
        self.__expression = expression
        self.__type = type

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'TypeCastExpression:\n'
        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}\n'
        type_str: str = self.__type.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}type: {type_str}'
        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
