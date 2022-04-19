class PrimitiveType:
    def __init__(self, type: str):
        self.__type: str = type
    
    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'PrimitiveType:\n'
        result += f'{space_padding}{space_indent}type: {self.__type}'
        return result
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
