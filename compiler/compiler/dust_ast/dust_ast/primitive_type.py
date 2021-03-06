import copy

class PrimitiveType:
    def __init__(self, type: str):
        self.__type: str = type
    
    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'PrimitiveType:\n'
        result += f"{space_padding}{space_indent}type: '{self.__type}'"
        return result
    
    def canonical(self) -> str:
        return copy.deepcopy(self.__type)
    
    def __eq__(self, other):
        if not isinstance(other, PrimitiveType):
            return False
        
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = f'{type(self).__name__}('
        attr_str = []
        for key, value in vars(self).items():
            prefix = key.replace(f"_{type(self).__name__}", '')
            attr_str += [f'{prefix}={str(value)}']
        result += ','.join(attr_str)
        result += ')'
        return result
    
    def __hash__(self):
        return hash(self.canonical())
