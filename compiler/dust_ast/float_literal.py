class FloatLiteral:
    def __init__(self, f: float):
        self.__float: float = f

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'FloatLiteral:\n'
        result += f"{space_padding}{space_indent}float: {self.__float}"
        return result

    def __eq__(self, other):
        if not isinstance(other, FloatLiteral):
            return False

        return self.__dict__ == other.__dict__
