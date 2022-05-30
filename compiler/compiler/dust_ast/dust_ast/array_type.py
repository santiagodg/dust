"""Defines the ArrayType class.

Classes
-------
ArrayType:
    Specifies the types contained in the array and its length."""

import copy


class ArrayType:
    def __init__(self, type, length):
        """
        :param type: Type of the elements of the array
        :type type: Type
        :param length: Length of the array
        :type length: IntegerLiteral
        """
        self.__type = type
        self.__length = length
        self.__shape = [self.__length.value()]
        subtype = self.__type.type()
        while isinstance(subtype, ArrayType):
            self.__shape.append(subtype.length().value())
            subtype = subtype.type().type()
        self.__accumulated_magnitudes = []
        self.__accumulated_magnitudes.append(1)
        for local_length in reversed(self.__shape):
            self.__accumulated_magnitudes.append(
                self.__accumulated_magnitudes[-1] * local_length)
        self.__accumulated_magnitudes = list(
            reversed(self.__accumulated_magnitudes))

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'ArrayType:\n'
        type_str: str = self.__type.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}type: {type_str}\n'
        length_str: str = self.__length.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}length: {length_str}'
        return result

    def canonical(self) -> str:
        return f'[{self.__type.canonical()}]'

    def type(self):
        """Return the type of elements inside the array.

        Returns
        -------
        type : Type
            The type of elements inside the array.
        """
        return copy.deepcopy(self.__type)

    def length(self):
        """Return the length of the array.

        Returns
        -------
        length : IntegerLiteral
            The amount of elements that fit in the array.
        """
        return self.__length

    def shape(self):
        """Return shape of array.

        Returns
        -------
        shape: List[int]
            Size of dimensions of the array."""
        return copy.deepcopy(self.__shape)

    def accumulated_magnitudes(self):
        """Return accumulated magnitudes."""
        return copy.deepcopy(self.__accumulated_magnitudes)

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
