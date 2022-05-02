class ArrayType:
    def __init__(self, type, length):
        """
        :param type: Type of the elements of the array
        :type type: Type
        :param length: Length of the array
        :type length: IntegerLiteral
        """
        
        self.__type = type
        self.__length = length
    
    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ArrayType:\n'
        type_str: str = self.__type.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}type: {type_str}\n'
        length_str: str = self.__length.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}length: {length_str}'
        return result
    
    def canonical(self) -> str:
        return f'[{self.__type.canonical()}]'
    
    def __eq__(self, other) : 
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
