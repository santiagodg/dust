class BlockExpression:
    def __init__(self, statements):
        "statements: list[Statement]"
        self.__statements = statements
    
    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'BlockExpression:\n'

        if len(self.__statements) == 0:
            result += f'{space_padding}{space_indent}statements: []'    
        else:
            result += f'{space_padding}{space_indent}statements: [\n'

            for statement in self.__statements:
                statement_str: str = statement.to_string(indent, padding + indent * 2)
                result += f'{space_padding}{space_indent}{space_indent}{statement_str}\n'
            
            result += f'{space_padding}{space_indent}]'

        return result
    
    def __eq__(self, other):
        if other == None:
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
