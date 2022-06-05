"""Defines the VirtualMachine class.

Classes
-------
VirtualMachine:
    Execute object files.
"""

import sys

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
                            "f64": 0,
                            "pointer": 0,
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
        local_memory = []
        current_era = []
        current_function = ['main']
        ip_stack = []
        input_buffer = ""
        while instruction_pointer < len(obj['quadruples']):
            quadruple = obj['quadruples'][instruction_pointer]
            # print(quadruple)
            if quadruple[0] == 'Goto':
                instruction_pointer = quadruple[3]
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
                if quadruple[2] is not None and quadruple[2] != 0:
                    for i in range(quadruple[2]):
                        value = memory.get(quadruple[1] + i)
                        if quadruple[3] // 10000 == 3 and (quadruple[3] % 10000) // 1000 == 4:
                            memory.put_value_to_pointed(
                                quadruple[3] + i, value)
                        else:
                            memory.put(quadruple[3] + i, value)
                else:
                    value = memory.get(quadruple[1])
                    if quadruple[3] // 10000 == 3 and (quadruple[3] % 10000) // 1000 == 4:
                        memory.put_value_to_pointed(quadruple[3], value)
                    else:
                        memory.put(quadruple[3], value)
                instruction_pointer += 1
                continue
            if quadruple[0] == 'ERA':
                local_memory.append({
                    'bool': [False] * obj['function_directory'][quadruple[1]]['local_memory']['bool'],
                    'char': [''] * obj['function_directory'][quadruple[1]]['local_memory']['char'],
                    'i32': [0] * obj['function_directory'][quadruple[1]]['local_memory']['i32'],
                    'f64': [0] * obj['function_directory'][quadruple[1]]['local_memory']['f64'],
                })
                current_era.append(quadruple[1])
                instruction_pointer += 1
                continue
            if quadruple[0] == 'Parameter':
                address = obj['function_directory'][current_era[-1]
                                                    ]['parameters'][quadruple[3] - 1]
                virtual_address = address % 20000
                offset = virtual_address % 1000
                if virtual_address // 1000 == 0:
                    for i in range(quadruple[2]):
                        value = memory.get(quadruple[1] + i)
                        local_memory[-1]['bool'][offset + i] = value
                if virtual_address // 1000 == 1:
                    for i in range(quadruple[2]):
                        value = memory.get(quadruple[1] + i)
                        local_memory[-1]['char'][offset + i] = value
                if virtual_address // 1000 == 2:
                    for i in range(quadruple[2]):
                        value = memory.get(quadruple[1] + i)
                        local_memory[-1]['i32'][offset + i] = value
                if virtual_address // 1000 == 3:
                    for i in range(quadruple[2]):
                        value = memory.get(quadruple[1] + i)
                        local_memory[-1]['f64'][offset + i] = value
                instruction_pointer += 1
                continue
            if quadruple[0] == 'Gosub':
                temporary_memory = {
                    'bool': [False] * obj['function_directory'][quadruple[1]]['temporary_memory']['bool'],
                    'char': [''] * obj['function_directory'][quadruple[1]]['temporary_memory']['char'],
                    'i32': [0] * obj['function_directory'][quadruple[1]]['temporary_memory']['i32'],
                    'f64': [0] * obj['function_directory'][quadruple[1]]['temporary_memory']['f64'],
                    'pointer': [0] * obj['function_directory'][quadruple[1]]['temporary_memory']['pointer'],
                }
                memory.push_local_scope(
                    local_memory=local_memory.pop(),
                    temporary_memory=temporary_memory,
                )
                ip_stack.append(instruction_pointer + 1)
                instruction_pointer = obj['function_directory'][quadruple[1]
                                                                ]['start_quadruple']
                current_function.append(quadruple[1])
                current_era.pop()
                continue
            if quadruple[0] == 'Return':
                if quadruple[2] != 0:
                    for i in range(quadruple[2]):
                        value = memory.get(quadruple[1] + i)
                        memory.put(quadruple[3] + i, value)
                memory.pop_local_scope()
                instruction_pointer = ip_stack.pop()
                current_function.pop()
                continue
            if quadruple[0] == 'Endfunc':
                memory.pop_local_scope()
                instruction_pointer = ip_stack.pop()
                continue
            if quadruple[0] == 'End':
                return
            if quadruple[0] == 'read':
                while input_buffer == "":
                    input_buffer = input()
                value = input_buffer[0]
                input_buffer = input_buffer[1:]
                if quadruple[3] // 10000 == 3 and (quadruple[3] % 10000) // 1000 == 4:
                    memory.put_value_to_pointed(quadruple[3], value)
                else:
                    memory.put(quadruple[3], value)
                instruction_pointer += 1
                continue
            if quadruple[0] == 'write':
                value = memory.get(quadruple[3])
                if value == '\\n':
                    print()
                elif value == '\\\'':
                    print('\'', end='')
                else:
                    print(value, end='')
                instruction_pointer += 1
                continue
            if quadruple[0] == 'Verify':
                index = memory.get(quadruple[1])
                lower_limit = memory.get(quadruple[2])
                upper_limit = memory.get(quadruple[3])
                if not (lower_limit <= index < upper_limit):
                    print(
                        f'IndexOutOfRange: index={index}, lower_limit={lower_limit}, upper_limit={upper_limit}. Quadruple #{instruction_pointer}: {quadruple}')
                    sys.exit(1)
                instruction_pointer += 1
                continue
            print(f'Failed to execute quadruple: {quadruple}')
            sys.exit(1)
