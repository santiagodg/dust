class LiteralExpression:
    def __init__(self, literal: str | int | float):
        self.__literal: str | int | float = literal

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'LiteralExpression:\n'
        literal_str: str = self.__literal.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}literal: {literal_str}'
        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
