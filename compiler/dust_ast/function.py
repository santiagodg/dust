from typing import Optional

from .function_parameter import FunctionParameter
from .dust_type import Type
from .let_statement import LetStatement
from .block_expression import BlockExpression
from .identifier import Identifier

class Function:
    def __init__(
        self, 
        identifier: Identifier, 
        parameters: list[FunctionParameter], 
        return_type: Optional[Type], 
        let_statements: list[LetStatement], 
        block: BlockExpression):

        self.__identifier: Identifier = identifier
        self.__parameters: list[FunctionParameter] = parameters
        self.__return_type: Optional[Type] = return_type
        self.__let_statements: list[LetStatement] = let_statements
        self.__block: BlockExpression = block
    
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
