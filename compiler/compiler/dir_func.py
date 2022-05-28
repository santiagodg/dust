"""Save function information.

# Exported classes

DirFunc: Function directory holding static variables and function information.

DirFuncError: Error type returned by DirFunc class.

FunctionEntry: Holds information of a function.
"""

import copy
from typing import Optional
import sys

from .dust_ast import Identifier, StaticItem, FunctionParameter, PrimitiveType, LetStatement, Type


class DirFuncError:
    """Error type returned by DirFunc class.

    # Methods

    type(): Get the type of error.

    message(): Get the error message.
    """

    def __init__(self, error_type: str, message: str):
        """Construct a DirFuncError with type and message.

        :param error_type: The type of error.
        :type error_type: str
        :param message: Error message.
        :type message: str
        """
        self.__type = error_type
        self.__message = message

    def type(self) -> str:
        return copy.deepcopy(self.__type)

    def message(self) -> str:
        return copy.deepcopy(self.__message)


class FunctionEntry:
    def __init__(
        self,
        identifier: Identifier,
        parameters: dict[str, FunctionParameter] = {},
        return_type: Optional[PrimitiveType] = None,
        let_statements: dict[str, LetStatement] = {},
        temporary_variables_count: dict[str, int] = {},
        start_quadruple_index: int = -1,
        return_virtual_address=None,
        local_variable_count: dict[str, int] = {},
    ):

        self.__identifier = identifier
        self.__parameters = copy.deepcopy(parameters)
        self.__return_type = return_type
        self.__let_statements = let_statements
        self.__temporary_variables_count = temporary_variables_count
        self.__start_quadruple_index = start_quadruple_index
        self.__return_virtual_address = return_virtual_address
        self.__local_variable_count = copy.deepcopy(local_variable_count)

    def exists_identifier(self, variable_identifier: Identifier) -> bool:
        return variable_identifier.identifier() in self.__parameters.keys() ^ self.__let_statements.keys()

    def add_parameter(self, parameter: FunctionParameter):
        self.__parameters[parameter.identifier().identifier()
                          ] = copy.deepcopy(parameter)

    def parameters(self):
        return copy.deepcopy(self.__parameters)

    def add_let_statement(self, let_statement: LetStatement):
        self.__let_statements[let_statement.identifier(
        ).identifier()] = let_statement

    def set_return_type(self, return_type: PrimitiveType):
        self.__return_type = return_type

    def return_type(self) -> Optional[PrimitiveType]:
        return copy.deepcopy(self.__return_type)

    def identifier(self) -> Identifier:
        return copy.deepcopy(self.__identifier)

    def parameter_type_list(self) -> list[Type]:
        return copy.deepcopy(list(map(lambda parameter: parameter.type(), list(self.__parameters.values()))))

    def get_typed_local_identifier(self, identifier: Identifier) -> Optional[Identifier]:
        if identifier.identifier() in self.__parameters:
            return copy.deepcopy(self.__parameters[identifier.identifier()].identifier())

        if identifier.identifier() in self.__let_statements:
            return copy.deepcopy(self.__let_statements[identifier.identifier()].identifier())

        return None

    def get_temporary_variable_count(self) -> dict[str, int]:
        return copy.deepcopy(self.__temporary_variables_count)

    def set_temporary_variable_count(self, count: dict[str, int]):
        self.__temporary_variables_count = copy.deepcopy(count)

    def get_start_quadruple_index(self) -> int:
        return self.__start_quadruple_index

    def set_start_quadruple_index(self, index: int):
        self.__start_quadruple_index = index

    def return_virtual_address(self):
        return self.__return_virtual_address

    def set_return_virtual_address(self, virtual_address):
        self.__return_virtual_address = virtual_address

    def get_local_variable_count(self):
        """Get local variable count.

        Returns
        -------
        local_variable_count - Dict[str, int]
            A dictionary containing the amount of local variables used
            in a function for each primitive data type.

            Example
            -------
            {
                'bool': 3,
                'char': 55,
                'i32': 12,
                'f64': 15,
            }
        """
        return copy.deepcopy(self.__local_variable_count)

    def set_local_variable_count(self, count):
        """Set local variable count.

        Parameters
        ----------
        count - Dict[str, int]
            A dictionary containing the amount of local variables used
            in a function for each primitive data type.

            Example
            -------
            {
                'bool': 3,
                'char': 55,
                'i32': 12,
                'f64': 15,
            }
        """
        self.__local_variable_count = copy.deepcopy(count)

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
    def __init__(
        self,
        static_items: dict[str, StaticItem] = {},
        functions: dict[str, FunctionEntry] = {},
    ):

        self.__static_items = static_items
        self.__functions = functions

    def add_static_item(self, static_item: StaticItem) -> Optional[DirFuncError]:
        identifier_str = static_item.identifier().identifier()

        if identifier_str in self.__static_items.keys() ^ self.__functions.keys():
            return DirFuncError(
                error_type='MultipleDeclaration',
                message=f"Multiple declaration for '{identifier_str}' identifier"
            )

        self.__static_items[identifier_str] = copy.deepcopy(static_item)
        return None

    def add_function_identifier(self, identifier: Identifier):
        self.__functions[identifier.identifier()] = FunctionEntry(identifier)

    def add_function_parameter(self, function_identifier: Identifier, function_parameter: FunctionParameter):
        self.__functions[function_identifier.identifier()].add_parameter(
            function_parameter)

    def add_function_return_type(self, function_identifier: Identifier, return_type: PrimitiveType):
        self.__functions[function_identifier.identifier()
                         ].set_return_type(return_type)

    def add_function_let_statement(self, function_identifier: Identifier, let_statement: LetStatement):
        self.__functions[function_identifier.identifier()].add_let_statement(
            let_statement)

    def exists_in_var_tables(
            self,
            function_identifier: Identifier,
            variable_identifier: Identifier) -> bool:

        if function_identifier.identifier() not in self.__functions:
            return False

        function_entry = self.__functions[function_identifier.identifier()]

        return function_entry.exists_identifier(variable_identifier)

    def exists(self, identifier: Identifier) -> bool:
        return identifier.identifier() in (self.__functions.keys() ^ self.__static_items.keys())

    def exists_function(self, identifier: Identifier) -> bool:
        return identifier.identifier() in self.__functions.keys()

    def get_typed_local_or_static_identifier(self, function_identifier: Identifier, identifier: Identifier) -> Optional[Identifier]:
        """
        Returns a typed local or static identifier.

        :param function_identifier: The function identifier of the current scope.
        :type function_identifier: Identifier
        :param identifier: The identifier without type. The returned identifier will match this name if it is found.
        :type identifier: Identifier
        :return: A type local or static identifier if found. Returning a typed local identifier is preferred, otherwise a typed static identifier is returned.
        :rtype: Optional[Type]
        """

        if identifier.identifier() in self.__static_items.keys():
            return copy.deepcopy(self.__static_items[identifier.identifier()].identifier())

        if function_identifier.identifier() in self.__functions:
            function_entry = self.__functions[function_identifier.identifier()]

            if function_entry.exists_identifier(identifier):
                return function_entry.get_typed_local_identifier(identifier)

        return None

    def function_parameters_match(self, function_identifier: Identifier, parameter_types: list[Type]) -> bool:
        for p1, p2 in zip(parameter_types, self.__functions[function_identifier.identifier()].parameter_type_list()):
            if p1 != p2:
                return False

        return True

    def function_entry(self, function_identifier: Identifier) -> FunctionEntry:
        return copy.deepcopy(self.__functions[function_identifier.identifier()])

    def set_function_entry(self, function_identifier: Identifier, function_entry: FunctionEntry):
        self.__functions[function_identifier.identifier()] = function_entry

    def add_temporary_variable_count(self, function_identifier: Identifier, count: dict[str, int]):
        if function_identifier.identifier() not in self.__functions:
            print(
                f'DirFunc.add_temporary_variable_count(function_identifier={function_identifier}, count={count}): function_identifier does not have a corresponding function registered.')
            sys.exit(1)

        self.__functions[function_identifier.identifier(
        )].set_temporary_variable_count(count)

    def set_function_start_quadruple_index(self, function_identifier: Identifier, index: int):
        if function_identifier.identifier() not in self.__functions:
            print(
                f'DirFunc.set_function_start_quadruple_index(function_identifier={function_identifier}, index={index}): function_identifier does not have a corresponding function registered.')
            sys.exit(1)

        self.__functions[function_identifier.identifier(
        )].set_start_quadruple_index(index)

    def globals_table(self):
        result = {
            'bool': 0,
            'char': 0,
            'i32': 0,
            'f64': 0,
        }
        for _static_item_name, static_item in self.__static_items.items():
            size: int = 1
            subtype = static_item.type()
            while subtype.is_array():
                array_type = subtype.type()
                size *= array_type.length().value()
                subtype = array_type.type()
            primitive_type = subtype.type()
            result[primitive_type.canonical()] += size
        for _function_name, function_entry in self.__functions.items():
            return_type = function_entry.return_type()
            if return_type is None:
                continue
            result[return_type.canonical()] += 1
        return result

    def to_dict(self):
        result = {}
        for function_name, function_entry in self.__functions.items():
            result[function_name] = {}
            result[function_name]['parameters'] = []
            for _parameter_name, parameter in function_entry.parameters().items():
                result[function_name]['parameters'].append(
                    parameter.identifier().operand().addr())
            return_virtual_address = function_entry.return_virtual_address()
            if return_virtual_address is None:
                result[function_name]['return_address'] = None
            else:
                result[function_name]['return_address'] = return_virtual_address.addr()
            result[function_name]['local_memory'] = function_entry.get_local_variable_count()
            result[function_name]['temporary_memory'] = function_entry.get_temporary_variable_count()
            result[function_name]['start_quadruple'] = function_entry.get_start_quadruple_index()
        return result

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
