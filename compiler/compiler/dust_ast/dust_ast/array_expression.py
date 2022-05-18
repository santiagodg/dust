import copy
from typing import Optional

from .dust_type import Type
from .array_type import ArrayType
from .integer_literal import IntegerLiteral

class ArrayExpression:
    def __init__(self, array_elements, temp_var_generator):
        "array_elements: list[Expression]"
        self.__array_elements = array_elements
        self.__elements_type = self.__array_elements[0].type()
        self.__type = Type(ArrayType(self.__elements_type, IntegerLiteral(len(self.__array_elements))))
        self.__temporary_variable = temp_var_generator.next(self.__type)

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
                result += f'{space_padding}{space_indent}{space_indent}{array_element_str}\n'
            
            result += f'{space_padding}{space_indent}]'
        
        return result
    
    def type(self) -> Optional[Type]:
        return copy.deepcopy(self.__type)
    
    def operand(self):
        """
        :rtype: TemporaryVariable | Identifier | BooleanLiteral | IntegerLiteral | FloatLiteral | CharLiteral | None
        """

        return self.__temporary_variable
    
    def quadruples(self):
        """
        :rtype: List[Tuple[str, str, str, str]]
        """

        return [[
            f'{type(self).__name__} unimplemented', 
            None, 
            None,
            self.__temporary_variable
        ]]

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
