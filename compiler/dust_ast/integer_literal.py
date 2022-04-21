class IntegerLiteral:
    def __init__(self, integer: int):
        self.__integer: int = integer

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'IntegerLiteral:\n'
        result += f"{space_padding}{space_indent}integer: {self.__integer}"
        return result

    def __eq__(self, other):
        if not isinstance(other, IntegerLiteral):
            return False

        return self.__dict__ == other.__dict__
