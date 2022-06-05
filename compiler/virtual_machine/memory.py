"""Defines Memory class.

Classes
-------
Memory:
    Manage memory.
"""


class Memory:
    """Manage memory.

    Methods
    -------
    get(address):
        Get the value at some address.

    put(address, value):
        Put a value in some address.
    """

    def __init__(self, global_count, local_count, temporary_count, constant_table):
        self.__globals = {
            'bool': [False] * global_count['bool'],
            'char': [''] * global_count['char'],
            'i32': [0] * global_count['i32'],
            'f64': [0] * global_count['f64'],
        }
        self.__locals_stack = []
        self.__locals_top = {
            'bool': [False] * local_count['bool'],
            'char': [''] * local_count['char'],
            'i32': [0] * local_count['i32'],
            'f64': [0] * local_count['f64'],
        }
        self.__temporaries_stack = []
        self.__temporaries_top = {
            'bool': [False] * temporary_count['bool'],
            'char': [''] * temporary_count['char'],
            'i32': [0] * temporary_count['i32'],
            'f64': [0] * temporary_count['f64'],
            'pointer': [0] * temporary_count['pointer'],
        }
        constant_count = {
            'bool': 0,
            'char': 0,
            'i32': 0,
            'f64': 0,
        }
        for virtual_address, _value in constant_table.items():
            virtual_address = int(virtual_address) % 40000
            if virtual_address // 1000 == 0:
                constant_count['bool'] += 1
            elif virtual_address // 1000 == 1:
                constant_count['char'] += 1
            elif virtual_address // 1000 == 2:
                constant_count['i32'] += 1
            elif virtual_address // 1000 == 3:
                constant_count['f64'] += 1
        self.__constants = {
            'bool': [False] * constant_count['bool'],
            'char': [''] * constant_count['char'],
            'i32': [0] * constant_count['i32'],
            'f64': [0] * constant_count['f64'],
        }
        for virtual_address, value in constant_table.items():
            virtual_address = int(virtual_address) % 40000
            if virtual_address // 1000 == 0:
                self.__constants['bool'][virtual_address % 1000] = value
            if virtual_address // 1000 == 1:
                self.__constants['char'][virtual_address % 1000] = value
            if virtual_address // 1000 == 2:
                self.__constants['i32'][virtual_address % 1000] = value
            if virtual_address // 1000 == 3:
                self.__constants['f64'][virtual_address % 1000] = value

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
        elif address // 10000 == 2:
            virtual_address = address % 20000
            if virtual_address // 1000 == 0:
                return self.__locals_top['bool'][virtual_address % 1000]
            if virtual_address // 1000 == 1:
                return_value = self.__locals_top['char'][virtual_address % 1000]
                return return_value
            if virtual_address // 1000 == 2:
                return self.__locals_top['i32'][virtual_address % 1000]
            if virtual_address // 1000 == 3:
                return self.__locals_top['f64'][virtual_address % 1000]
        elif address // 10000 == 3:
            virtual_address = address % 30000
            if virtual_address // 1000 == 0:
                return self.__temporaries_top['bool'][virtual_address % 1000]
            if virtual_address // 1000 == 1:
                return_value = self.__temporaries_top['char'][virtual_address % 1000]
                return return_value
            if virtual_address // 1000 == 2:
                return self.__temporaries_top['i32'][virtual_address % 1000]
            if virtual_address // 1000 == 3:
                return self.__temporaries_top['f64'][virtual_address % 1000]
            if virtual_address // 1000 == 4:
                pointer_address = self.__temporaries_top['pointer'][virtual_address % 1000]
                return_value = self.get(pointer_address)
                return return_value
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
        elif address // 10000 == 2:
            virtual_address = address % 20000
            if virtual_address // 1000 == 0:
                self.__locals_top['bool'][virtual_address % 1000] = value
            if virtual_address // 1000 == 1:
                self.__locals_top['char'][virtual_address % 1000] = value
            if virtual_address // 1000 == 2:
                self.__locals_top['i32'][virtual_address % 1000] = value
            if virtual_address // 1000 == 3:
                self.__locals_top['f64'][virtual_address % 1000] = value
        elif address // 10000 == 3:
            virtual_address = address % 30000
            if virtual_address // 1000 == 0:
                self.__temporaries_top['bool'][virtual_address % 1000] = value
            if virtual_address // 1000 == 1:
                self.__temporaries_top['char'][virtual_address % 1000] = value
            if virtual_address // 1000 == 2:
                self.__temporaries_top['i32'][virtual_address % 1000] = value
            if virtual_address // 1000 == 3:
                self.__temporaries_top['f64'][virtual_address % 1000] = value
            if virtual_address // 1000 == 4:
                self.__temporaries_top['pointer'][virtual_address %
                                                  1000] = value
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

    def put_value_to_pointed(self, address, value):
        pointed_address = self.__temporaries_top['pointer'][address % 1000]
        self.put(pointed_address, value)

    def push_local_scope(self, local_memory, temporary_memory):
        """Start a local scope with new local_memory and temporary_memory.

        Saves previous scope in a stack.

        Parameters
        ----------
        local_memory - Dict[str, int]
            Must have 'bool', 'char', 'i32', and 'f64' keys.
            Values must be an array of memory for each type.

        temporary_memory - Dict[str, int]
            Must have 'bool', 'char', 'i32', and 'f64' keys.
            Values must be an array of memory for each type.
        """
        self.__locals_stack.append(self.__locals_top)
        self.__locals_top = local_memory
        self.__temporaries_stack.append(self.__temporaries_top)
        self.__temporaries_top = temporary_memory

    def pop_local_scope(self):
        """Pop the local scope."""
        self.__locals_top = self.__locals_stack.pop()
        self.__temporaries_top = self.__temporaries_stack.pop()
