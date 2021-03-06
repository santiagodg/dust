"""Defines VirtualAddress class.

Classes
-------
VirtualAddress : Specifies the location of a value in virtual memory.
"""

from abc import ABC, abstractmethod

from .scope import Scope


class VirtualAddress(ABC):
    """Specifies the location of a value in virtual memory."""

    @abstractmethod
    def addr(self) -> int:
        """Return the integer address."""

    @abstractmethod
    def scope(self) -> Scope:
        """Return the scope."""

    @abstractmethod
    def type(self):
        """Return the type."""


class VirtualAddressConcrete(VirtualAddress):
    LIMITS = {
        Scope.GLOBAL: {
            "base": 10000,
            "types": {
                "bool": {
                    "base": 0,
                    "max_amount": 1000,
                },
                "char": {
                    "base": 1000,
                    "max_amount": 1000,
                },
                "i32": {
                    "base": 2000,
                    "max_amount": 1000,
                },
                "f64": {
                    "base": 3000,
                    "max_amount": 1000,
                },
            },
        },
        Scope.LOCAL: {
            "base": 20000,
            "types": {
                "bool": {
                    "base": 0,
                    "max_amount": 1000,
                },
                "char": {
                    "base": 1000,
                    "max_amount": 1000,
                },
                "i32": {
                    "base": 2000,
                    "max_amount": 1000,
                },
                "f64": {
                    "base": 3000,
                    "max_amount": 1000,
                },
            },
        },
        Scope.TEMPORARY: {
            "base": 30000,
            "types": {
                "bool": {
                    "base": 0,
                    "max_amount": 1000,
                },
                "char": {
                    "base": 1000,
                    "max_amount": 1000,
                },
                "i32": {
                    "base": 2000,
                    "max_amount": 1000,
                },
                "f64": {
                    "base": 3000,
                    "max_amount": 1000,
                },
                "pointer": {
                    "base": 4000,
                    "max_amount": 1000,
                }
            },
        },
        Scope.CONSTANT: {
            "base": 40000,
            "types": {
                "bool": {
                    "base": 0,
                    "max_amount": 1000,
                },
                "char": {
                    "base": 1000,
                    "max_amount": 1000,
                },
                "i32": {
                    "base": 2000,
                    "max_amount": 1000,
                },
                "f64": {
                    "base": 3000,
                    "max_amount": 1000,
                },
            },
        },
    }

    def __init__(self, scope, addr_type, offset):
        """Construct a virtual address.

        Parameters
        ----------
        scope: Scope
            The scope of this virtual address.
        addr_type: PrimitiveType | 'pointer'
            The type of the virtual address.
        offset: int
            The offset of this virtual address from the base memory address of its section.
        """
        self.__scope = scope
        self.__addr_type = addr_type
        self.__offset = offset
        if addr_type == 'pointer':
            self.__addr: int = self.LIMITS[self.__scope]['base'] + \
                self.LIMITS[self.__scope]['types']['pointer']['base'] + \
                self.__offset
            return
        self.__addr: int = self.LIMITS[self.__scope]['base'] + \
            self.LIMITS[self.__scope]['types'][self.__addr_type.canonical(
            )]['base'] + self.__offset

    def addr(self) -> int:
        return self.__addr

    def scope(self) -> Scope:
        return self.__scope

    def type(self):
        return self.__addr_type
