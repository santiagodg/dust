from .index_expression import IndexExpression

class ReadExpression:
    def __init__(self, variable: str | IndexExpression):
        self.__variable: str | IndexExpression = variable

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ReadExpression:\n'

        if isinstance(self.__variable, str):
            result += f"{space_padding}{space_indent}variable: '{self.__variable}'"    
        else:
            variable_str: str = self.__variable.to_string(indent, padding + indent)
            result += f'{space_padding}{space_indent}variable: {variable_str}'

        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
