class CharLiteral:
    def __init__(self, char: str):
        self.__char: str = char

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'CharLiteral:\n'
        result += f"{space_padding}{space_indent}char: '{self.__char}'"
        return result

    def __eq__(self, other):
        if not isinstance(other, CharLiteral):
            return False

        return self.__dict__ == other.__dict__
