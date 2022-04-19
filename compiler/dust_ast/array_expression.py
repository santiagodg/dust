class ArrayExpression:
    def __init__(self, array_elements):
        self.__array_elements = array_elements

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ArrayExpression:\n'
        
        if len(self.__array_elements) == 0:
            result += f'{space_padding}{space_indent}array_elements: []'
        else:
            result += f'{space_padding}{space_indent}array_elements: [\n'

            for array_element in self.__array_elements:
                array_element_str: str = array_element.to_string(indent, padding + indent * 2)
                result += f'{space_padding}{space_indent}{space_indent}{array_element}\n'
            
            result += f'{space_padding}{space_indent}]'
        
        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
