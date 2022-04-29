import copy
from typing import Optional, Tuple

from .dust_ast import Function, Identifier, StaticItem, FunctionParameter, PrimitiveType, LetStatement, Type

class DirFuncError:
    def __init__(self, type: str, message: str):
        self.__type = type
        self.__message = message
    
    def type(self) -> str:
        return copy.deepcopy(self.__type)
    
    def message(self) -> str:
        return copy.deepcopy(self.__message)

class Variable:
    def __init__(self, identifier: Identifier, type: Type):
        self.__identifier = identifier
        self.__type = type

    def identifier(self) -> Identifier:
        return copy.deepcopy(self.__identifier)
    
    def type(self) -> Identifier:
        return copy.deepcopy(self.__type)
    
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

class FunctionEntry:
    def __init__(
            self,
            identifier: Identifier,
            parameters: dict[str, list[FunctionParameter]] = {},
            return_type: Optional[PrimitiveType] = None,
            let_statements: dict[str, LetStatement] = {}):

        self.__identifier = identifier
        self.__parameters = parameters
        self.__return_type = return_type
        self.__let_statements = let_statements
    
    def exists_identifier(self, variable_identifier: Identifier) -> bool:
        return variable_identifier.identifier() in self.__parameters.keys() ^ self.__let_statements.keys()
    
    def add_parameter(self, parameter: FunctionParameter):
        self.__parameters[parameter.identifier().identifier()] = parameter

    def add_let_statement(self, let_statement: LetStatement):
        self.__let_statements[let_statement.identifier().identifier()] = let_statement
    
    def set_return_type(self, return_type: PrimitiveType):
        self.__return_type = return_type
    
    def return_type(self) -> PrimitiveType:
        return copy.deepcopy(self.__return_type)
    
    def identifier(self) -> Identifier:
        return copy.deepcopy(self.__identifier)
    
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

class DirFunc:
    def __init__(self, static_items: dict[str, StaticItem] = {}, functions: dict[str, FunctionEntry] = {}):
        self.__static_items = static_items
        self.__functions = functions

    def add_static_item(self, static_item: StaticItem) -> Optional[DirFuncError]:
        identifier_str = static_item.identifier().identifier()

        if identifier_str in self.__static_items.keys() ^ self.__functions.keys():
            return DirFuncError(
                type='MultipleDeclaration', 
                message=f"Multiple declaration for '{identifier_str}' identifier"
            )

        self.__static_items[identifier_str] = copy.deepcopy(static_item)
        return None
    
    def add_function_identifier(self, identifier: Identifier):
        # print(f"Called DirFunc.add_function_identifier with identifier {identifier}")
        self.__functions[identifier.identifier()] = FunctionEntry(identifier)
    
    def add_function_parameter(self, function_identifier: Identifier, function_parameter: FunctionParameter):
        self.__functions[function_identifier.identifier()].add_parameter(function_parameter)
    
    def add_function_return_type(self, function_identifier: Identifier, return_type: PrimitiveType):
        self.__functions[function_identifier.identifier()].set_return_type(return_type)
    
    def add_function_let_statement(self, function_identifier: Identifier, let_statement: LetStatement):
        self.__functions[function_identifier.identifier()].add_let_statement(let_statement)
    
    def exists_in_var_tables(
            self, 
            function_identifier: Identifier, 
            variable_identifier: Identifier) -> bool:

        if function_identifier.identifier() not in self.__functions:
            return False
        
        function_entry = self.__functions[function_identifier.identifier()]

        return function_entry.exists_identifier(variable_identifier)

    def search_static_item(self, identifier: Identifier) -> Optional[StaticItem]:
        return None

    def exists(self, identifier: Identifier) -> bool:
        # print(self.__functions.keys() ^ self.__static_items.keys())
        return identifier.identifier() in (self.__functions.keys() ^ self.__static_items.keys())

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
    
    def __eq__(self, other):
        if not isinstance(other, DirFunc):
            return False

        return self.__dict__ == other.__dict__
