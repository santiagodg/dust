"""Defines the VirtualMachine class.

Classes
-------
VirtualMachine:
    Execute object files.
"""

from .memory import Memory


class VirtualMachine:
    """Execute object files.

    Methods
    -------
    execute(obj):
        Execute an object.
    """

    def execute(self, obj):
        """Execute an object.

        Parameters
        ----------
        obj - dict
            The object to be executed.

            Example:

            {
                "constant_table": {
                    "41000": "h"
                },
                "globals_table": {
                    "bool": 0,
                    "char": 0,
                    "i32": 0,
                    "f64": 0
                },
                "function_directory": {
                    "main": {
                        "parameters": [],
                        "return_address": null,
                        "local_memory": {
                            "bool": 0,
                            "char": 0,
                            "i32": 0,
                            "f64": 0
                        },
                        "temporary_memory": {
                            "bool": 0,
                            "char": 0,
                            "i32": 0,
                            "f64": 0
                        }
                    }
                },
                "quadruples": [
                    [
                        "Goto",
                        null,
                        null,
                        "main"
                    ],
                    [
                        "write",
                        null,
                        null,
                        41000
                    ]
                ]
            }
        """
        instruction_pointer = 0
        memory = Memory(
            global_count=obj['globals_table'],
            local_count=obj['function_directory']['main']['local_memory'],
            temporary_count=obj['function_directory']['main']['temporary_memory'],
            constant_table=obj['constant_table'],
        )
        local_memory = {}
        current_era = None
        current_function = ['main']
        ip_stack = []
        while instruction_pointer < len(obj['quadruples']):
            quadruple = obj['quadruples'][instruction_pointer]
            if quadruple[0] == 'Goto':
                instruction_pointer = obj['function_directory'][quadruple[3]
                                                                ]['start_quadruple']
                continue
            if quadruple[0] == 'GotoF':
                value = memory.get(quadruple[1])
                if not value:
                    instruction_pointer = int(quadruple[3])
                else:
                    instruction_pointer += 1
                continue
            if quadruple[0] == 'GotoT':
                value = memory.get(quadruple[1])
                if value:
                    instruction_pointer = int(quadruple[3])
                else:
                    instruction_pointer += 1
                continue
            if quadruple[0] == '-':
                value = memory.get(quadruple[1])
                result = -value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '!':
                value = memory.get(quadruple[1])
                result = not value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '+':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value + right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '-':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value - right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '*':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value * right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '/':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = None
                if isinstance(left_value, int):
                    result = left_value // right_value
                else:
                    result = left_value / right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '%':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value % right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '==':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value == right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '!=':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value != right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '>':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value > right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '<':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value < right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '>=':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value >= right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '<=':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value <= right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '||':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value or right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '&&':
                left_value = memory.get(quadruple[1])
                right_value = memory.get(quadruple[2])
                result = left_value and right_value
                memory.put(quadruple[3], result)
                instruction_pointer += 1
                continue
            if quadruple[0] == '=':
                value = memory.get(quadruple[1])
                memory.put(quadruple[3], value)
                instruction_pointer += 1
                continue
            if quadruple[0] == 'ERA':
                local_memory = {
                    'bool': [False] * obj['function_directory'][quadruple[1]]['local_memory']['bool'],
                    'char': [''] * obj['function_directory'][quadruple[1]]['local_memory']['char'],
                    'i32': [0] * obj['function_directory'][quadruple[1]]['local_memory']['i32'],
                    'f64': [0] * obj['function_directory'][quadruple[1]]['local_memory']['f64'],
                }
                current_era = quadruple[1]
                instruction_pointer += 1
                continue
            if quadruple[0] == 'Parameter':
                value = memory.get(quadruple[1])
                address = obj['function_directory'][current_era]['parameters'][quadruple[3] - 1]
                virtual_address = address % 20000
                offset = virtual_address % 1000
                if virtual_address // 1000 == 0:
                    local_memory['bool'][offset] = value
                if virtual_address // 1000 == 1:
                    local_memory['char'][offset] = value
                if virtual_address // 1000 == 2:
                    local_memory['i32'][offset] = value
                if virtual_address // 1000 == 3:
                    local_memory['f64'][offset] = value
                instruction_pointer += 1
                continue
            if quadruple[0] == 'Gosub':
                temporary_memory = {
                    'bool': [False] * obj['function_directory'][quadruple[1]]['temporary_memory']['bool'],
                    'char': [''] * obj['function_directory'][quadruple[1]]['temporary_memory']['char'],
                    'i32': [0] * obj['function_directory'][quadruple[1]]['temporary_memory']['i32'],
                    'f64': [0] * obj['function_directory'][quadruple[1]]['temporary_memory']['f64'],
                }
                memory.push_local_scope(
                    local_memory=local_memory,
                    temporary_memory=temporary_memory,
                )
                local_memory = {}
                ip_stack.append(instruction_pointer + 1)
                instruction_pointer = obj['function_directory'][quadruple[1]
                                                                ]['start_quadruple']
                current_function.append(quadruple[1])
                continue
            if quadruple[0] == 'Return':
                value = memory.get(quadruple[1])
                memory.put(quadruple[3], value)
                memory.pop_local_scope()
                instruction_pointer = ip_stack.pop()
                current_function.pop()
                continue
            if quadruple[0] == 'Endfunc':
                if current_function[-1] == 'main':
                    return
                memory.pop_local_scope()
                instruction_pointer = ip_stack.pop()
                continue
            if quadruple[0] == 'write':
                value = memory.get(quadruple[3])
                if value == '\\n':
                    print()
                else:
                    print(value, end='')
                instruction_pointer += 1
                continue
            print(f'Failed to execute quadruple: {quadruple}')
