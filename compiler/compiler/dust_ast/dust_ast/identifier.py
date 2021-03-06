import copy

from .dust_type import Type


class Identifier:
    def __init__(self, identifier: str):
        self.__identifier: str = identifier
        self.__type = None
        self.__virtual_address = None

    def identifier(self) -> str:
        return copy.deepcopy(self.__identifier)

    def set_type(self, type: Type):
        self.__type = type

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'Identifier:\n'
        result += f"{space_padding}{space_indent}identifier: '{self.__identifier}'"
        return result

    def type(self) -> Type:
        return copy.deepcopy(self.__type)

    def operand(self):
        """
        :rtype: TemporaryVariable | Identifier | BooleanLiteral | IntegerLiteral | FloatLiteral | CharLiteral | None
        """
        if self.__virtual_address is not None:
            return self.__virtual_address
        return self

    def set_virtual_address(self, virtual_address):
        """Set the identifier's virtual address.

        Parameters
        ----------
        virtual_address : VirtualAddress
            The virtual address of this identifier.
        """
        self.__virtual_address = virtual_address

    def __eq__(self, other):
        if not isinstance(other, Identifier):
            return False

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
