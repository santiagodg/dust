from .identifier import Identifier

class CallExpression:
    def __init__(self, identifier: Identifier, call_params):
        """
        identifier: Identifier
        call_params: list[Expression]
        """

        self.__identifier = identifier
        self.__call_params = call_params

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'CallExpression:\n'
        identifier_str: str = self.__identifier.to_string(indent, padding + indent)
        result += f"{space_padding}{space_indent}identifier: {identifier_str}\n"

        if len(self.__call_params) == 0:
            result += f'{space_padding}{space_indent}call_params: []'
        else:
            result += f'{space_padding}{space_indent}call_params: [\n'

            for call_param in self.__call_params:
                call_param_str: str = call_param.to_string(indent, padding + indent * 2)
                result += f'{space_padding}{space_indent}{space_indent}{call_param_str}\n'
            
            result += f'{space_padding}{space_indent}]'

        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
