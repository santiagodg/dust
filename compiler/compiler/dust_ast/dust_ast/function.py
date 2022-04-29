from typing import Optional

import copy

from .function_parameter import FunctionParameter
from .primitive_type import PrimitiveType
from .let_statement import LetStatement
from .block_expression import BlockExpression
from .identifier import Identifier

class Function:
    def __init__(
        self, 
        identifier: Identifier, 
        parameters: list[FunctionParameter], 
        return_type: Optional[PrimitiveType], 
        let_statements: list[LetStatement], 
        block: BlockExpression):

        self.__identifier: Identifier = identifier
        self.__parameters: list[FunctionParameter] = parameters
        self.__return_type: Optional[PrimitiveType] = return_type
        self.__let_statements: list[LetStatement] = let_statements
        self.__block: BlockExpression = block
    
    def identifier(self) -> Identifier:
        return copy.deepcopy(self.__identifier)
    
    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'Function:\n'
        identifier_str = self.__identifier.to_string(indent, padding + indent)
        result += f"{space_padding}{space_indent}identifier: {identifier_str}\n"

        if len(self.__parameters) == 0:
            result += f'{space_padding}{space_indent}parameters: []\n'
        else:
            result += f'{space_padding}{space_indent}parameters: [\n'
            
            for parameter in self.__parameters:
                parameter_str: str = parameter.to_string(indent, padding + indent * 2)
                result += f'{space_padding}{space_indent}{space_indent}{parameter_str}\n'
            
            result += f'{space_padding}{space_indent}]\n'
        
        if self.__return_type == None:
            result += f'{space_padding}{space_indent}return_type: None\n'
        else:
            return_type_str: str = self.__return_type.to_string(indent, padding + indent)
            result += f'{space_padding}{space_indent}return_type: {return_type_str}\n'
        
        if len(self.__let_statements) == 0:
            result += f'{space_padding}{space_indent}let_statements: []\n'
        else:
            result += f'{space_padding}{space_indent}let_statements: [\n'

            for let_statement in self.__let_statements:
                let_statement_str: str = let_statement.to_string(indent, padding + indent * 2)
                result += f'{space_padding}{space_indent}{space_indent}{let_statement_str}\n'
            
            result += f'{space_padding}{space_indent}]\n'

        block_str: str = self.__block.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}block: {block_str}'
        return result
    
    def __eq__(self, other): 
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
