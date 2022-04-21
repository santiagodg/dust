class Identifier:
    def __init__(self, identifier: str):
        self.__identifier: str = identifier

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'Identifier:\n'
        result += f"{space_padding}{space_indent}identifier: '{self.__identifier}'"
        return result

    def __eq__(self, other):
        if not isinstance(other, Identifier):
            return False

        return self.__dict__ == other.__dict__
