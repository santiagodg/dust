"""Defines GlobalMemory class.

Classes
-------
GlobalMemory:
    Manage global memory.
"""

import copy


class GlobalMemory:
    """Manage global memory.

    Methods
    -------
    get(address):
        Get the value at some address.

    put(address, value):
        Put a value in some address.
    """

    def __init__(self, constant_table, globals_table):
        """Create a GlobalMemory object."""
        counts = {
            'bool': 0,
            'char': 0,
            'i32': 0,
            'f64': 0,
        }
        for virtual_address, _value in constant_table:
            virtual_address = virtual_address % 40000
            if virtual_address // 1000 == 1:
                counts['bool'] += 1
            elif virtual_address // 1000 == 2:
                counts['char'] += 1
            elif virtual_address // 1000 == 3:
                counts['i32'] += 1
            elif virtual_address // 1000 == 2:
                counts['f64'] += 1
        self.__constants = {
            'bool': [False] * counts['bool'],
            'char': [''] * counts['char'],
            'i32': [0] * counts['i32'],
            'f64': [0] * counts['f64'],
        }
        for virtual_address, value in constant_table:
            virtual_address = int(virtual_address) % 40000
            if virtual_address // 1000 == 0:
                self.__constants['bool'][virtual_address % 1000] = value
            if virtual_address // 1000 == 1:
                self.__constants['char'][virtual_address % 1000] = value
            if virtual_address // 1000 == 2:
                self.__constants['i32'][virtual_address % 1000] = value
            if virtual_address // 1000 == 3:
                self.__constants['f64'][virtual_address % 1000] = value
        self.__globals = {}
        for primitive_type, amount in globals_table:
            if primitive_type == 'bool':
                self.__globals['bool'] = [False] * amount
            elif primitive_type == 'char':
                self.__globals['char'] = [''] * amount
            elif primitive_type == 'i32':
                self.__globals['i32'] = [0] * amount
            elif primitive_type == 'f64':
                self.__globals['f64'] = [0] * amount

    def get(self, address):
        """Get the value at some address.

        Parameters
        ----------
        address - int
            The address to look for.
        """
        if address // 10000 == 1:
            virtual_address = address % 10000
            if virtual_address // 1000 == 0:
                return self.__globals['bool'][virtual_address % 1000]
            if virtual_address // 1000 == 1:
                return self.__globals['char'][virtual_address % 1000]
            if virtual_address // 1000 == 2:
                return self.__globals['i32'][virtual_address % 1000]
            if virtual_address // 1000 == 3:
                return self.__globals['f64'][virtual_address % 1000]
        elif address // 10000 == 4:
            virtual_address = address % 40000
            if virtual_address // 1000 == 0:
                return self.__constants['bool'][virtual_address % 1000]
            if virtual_address // 1000 == 1:
                return self.__constants['char'][virtual_address % 1000]
            if virtual_address // 1000 == 2:
                return self.__constants['i32'][virtual_address % 1000]
            if virtual_address // 1000 == 3:
                return self.__constants['f64'][virtual_address % 1000]

    def put(self, address, value):
        """Put a value in some address.

        Parameters
        ----------
        address - int
            The address to save the value in.

        value - Any
            The value to be saved.
        """
        if address // 10000 == 1:
            virtual_address = address % 10000
            if virtual_address // 1000 == 0:
                self.__globals['bool'][virtual_address % 1000] = value
            if virtual_address // 1000 == 1:
                self.__globals['char'][virtual_address % 1000] = value
            if virtual_address // 1000 == 2:
                self.__globals['i32'][virtual_address % 1000] = value
            if virtual_address // 1000 == 3:
                self.__globals['f64'][virtual_address % 1000] = value
        elif address // 10000 == 4:
            virtual_address = address % 40000
            if virtual_address // 1000 == 0:
                self.__constants['bool'][virtual_address % 1000] = value
            if virtual_address // 1000 == 1:
                self.__constants['char'][virtual_address % 1000] = value
            if virtual_address // 1000 == 2:
                self.__constants['i32'][virtual_address % 1000] = value
            if virtual_address // 1000 == 3:
                self.__constants['f64'][virtual_address % 1000] = value
