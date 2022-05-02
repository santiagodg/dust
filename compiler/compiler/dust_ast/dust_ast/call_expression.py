from typing import Optional
import copy

from .identifier import Identifier
from .dust_type import Type

class CallExpression:
    def __init__(self, identifier: Identifier, call_params, dir_func):
        """
        identifier: Identifier
        call_params: list[Expression]
        """

        self.__identifier = identifier
        self.__call_params = call_params
        self.__type: Optional[Type] = None

        return_type = dir_func.function_entry(self.__identifier).return_type()
        if return_type != None:
            self.__type = Type(return_type)

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
    
    def type(self) -> Optional[Type]:
        return copy.deepcopy(self.__type)

    def operand(self):
        """
        :rtype: TemporaryVariable | Identifier | BooleanLiteral | IntegerLiteral | FloatLiteral | CharLiteral | None
        """
        
        print(f"{self.__class__.__name__}.operand: Not yet implemented")
        return None

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
