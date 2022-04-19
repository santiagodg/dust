class ArrayType:
    def __init__(self, type, length: int):
        self.__type = type
        self.__length: int = length
    
    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ArrayType:\n'
        type_str: str = self.__type.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}type: {type_str}\n'
        result += f'{space_padding}{space_indent}length: {self.__length}'
        return result
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
