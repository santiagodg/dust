"""Defines ObjFile interface and concrete classes."""

import json
from msilib.schema import File


class ObjFile():
    """Defines the ObjFile interface.

    Methods
    -------
    constant_table():
        Return constant table.

    globals_table():
        Return the globals table.

    function_directory():
        Return the function directory.

    quadruples():
        Return quadruples.

    filename():
        Return the filename string.
    """

    def __init__(
        self,
        constant_table=None,
        globals_table=None,
        function_directory=None,
        quadruples=None,
        target=None,
        output=None,
    ):
        """Construct an ObjFile.

        Parameters
        ----------
        constant_table - Dict[int, Any]
            A dictionary which with virtual address keys holding
            the value of constants.

            Example:

            {
                41000: 'a',
                42000: 123,
                42001: 77,
            }

        globals_table - dict[str, int]
            Amount of addresses per type.

            Example:

            {
                'bool': 1,
                'char': 2,
                'i32': 4,
                'f64': 6,
            }

        function_directory - Dict[str, Any]
            The function directory for the program.

            Example:

            {
                'function_1': {
                    'parameters': [
                        22000,
                        22001,
                    ],
                    'return_address': 11000,
                    'local_memory': {
                        'bool': 0,
                        'char': 0,
                        'i32': 0,
                        'f64': 0,
                    }
                    'temporary_memory': {
                        'bool': 0,
                        'char': 0,
                        'i32': 1,
                        'f64': 0,
                    },
                }
                'main': {
                    'parameters': [],
                    'local_memory': {
                        'bool': 0,
                        'char': 0,
                        'i32': 0,
                        'f64': 0,
                    }
                    'temporary_memory': {
                        'bool': 0,
                        'char': 0,
                        'i32': 0,
                        'f64': 0,
                    },
                }
            }

        quadruples - List[List[str, Optional[int | str], Optional[int], Optional[int | str]]]
            The list of quadruples.

            Example:

            [
                ['Goto', None, None, 'main'],
                ['=', 42000, None, 12000],
                ['+', 22000, 22001, 32000],
                ['=', 32000, None, 12001],
                ['ERA', 'uno', None, None],
                ['Gosub', 'uno', None, None],
                ['=', 12000, None, 22000],
                ['ERA', dos, None, None],
                ['Parameter', 42001, None, 1],
                ['Parameter', 42002, None, 2],
                ['Gosub', 'dos', None, None],
                ['=', 12001, None, 22001],
            ]

        target - str
            The filename to be compiled.

        output - str
            The filename to output the object file.
        """
        self.__constant_table = constant_table
        self.__globals_table = globals_table
        self.__function_directory = function_directory
        self.__quadruples = quadruples
        self.__target = target
        self.__output = output

    def constant_table(self):
        """Return constant table.

        Returns
        -------
        constant_table - Dict[int, Any]
            A dictionary which with virtual address keys holding
            the value of constants.

            Example:

            {
                41000: 'a',
                42000: 123,
                42001: 77,
            }
        """
        return self.__constant_table

    def globals_table(self):
        """Return the globals table.

        Returns
        -------
        globals_table - dict[str, int]
            Amount of addresses per type.

            Example:

            {
                'bool': 1,
                'char': 2,
                'i32': 4,
                'f64': 6,
            }
        """
        return self.__globals_table

    def function_directory(self):
        """Return the function directory.

        Returns
        -------
        function_directory - Dict[str, Any]
            The function directory for the program.

            Example:

            {
                'function_1': {
                    'parameters': [
                        22000,
                        22001,
                    ],
                    'return_address': 11000,
                    'local_memory': {
                        'bool': 0,
                        'char': 0,
                        'i32': 0,
                        'f64': 0,
                    }
                    'temporary_memory': {
                        'bool': 0,
                        'char': 0,
                        'i32': 1,
                        'f64': 0,
                    },
                }
                'main': {
                    'parameters': [],
                    'local_memory': {
                        'bool': 0,
                        'char': 0,
                        'i32': 0,
                        'f64': 0,
                    }
                    'temporary_memory': {
                        'bool': 0,
                        'char': 0,
                        'i32': 0,
                        'f64': 0,
                    },
                }
            }
        """
        return self.__function_directory

    def quadruples(self):
        """Return quadruples.

        Returns
        -------
        quadruples - List[List[str, Optional[int | str], Optional[int], Optional[int | str]]]
            The list of quadruples.

            Example:

            [
                ['Goto', None, None, 'main'],
                ['=', 42000, None, 12000],
                ['+', 22000, 22001, 32000],
                ['=', 32000, None, 12001],
                ['ERA', 'uno', None, None],
                ['Gosub', 'uno', None, None],
                ['=', 12000, None, 22000],
                ['ERA', dos, None, None],
                ['Parameter', 42001, None, 1],
                ['Parameter', 42002, None, 2],
                ['Gosub', 'dos', None, None],
                ['=', 12001, None, 22001],
            ]
        """
        return self.__quadruples

    def target(self):
        """Return the target filename.

        Returns
        -------
        target - str
            The target filename.
        """
        return self.__target

    def output(self):
        """Return the output filename.

        Returns
        -------
        output - str
            The output filename.
        """
        return self.__output

    def load(self):
        """Load properties from file."""
        with open(self.target(), encoding='utf-8') as file:
            read_data = file.read()
            obj = json.loads(read_data)
            self.__constant_table = obj['constant_table']
            self.__globals_table = obj['globals_table']
            self.__function_directory = obj['function_directory']
            self.__quadruples = obj['quadruples']

    def save(self):
        """Saves properties to file."""
        obj = {}
        obj['constant_table'] = self.constant_table()
        obj['globals_table'] = self.globals_table()
        obj['function_directory'] = self.function_directory()
        obj['quadruples'] = self.quadruples()
        dumped = json.dumps(obj)
        file = None
        try:
            file = open(self.output(), mode='x', encoding='utf-8')
        except FileExistsError:
            file = open(self.output(), mode='w', encoding='utf-8')
        finally:
            file.write(dumped)
            file.close()
