"""Defines VirtualAddressController interface and concrete implementation.

Classes
-------
VirtualAddressControllerInterface : extends ABC
    Primary interface to acquire virtual addresses.

VirtualAddressControllerConcrete : implements VirtualAddressController
    Implements VirtualAddressControllerInterface.
"""

from abc import ABC, abstractmethod
import sys

from .virtual_address import VirtualAddress, VirtualAddressConcrete
from ._scope_type_counter import _ScopeTypeCounter
from .scope import Scope
from ._local_scope_state import _LocalScopeState


class VirtualAddressControllerInterface(ABC):
    """Primary interface to acquire virtual addresses.

    Methods
    -------
    start_local_scope(self):
        Start a scope with new local and temporary addresses.

        Panics
        ------
        If this method is called twice without ending the local scope in between.

    end_local_scope(self):
        End the current local scope.

        Panics
        ------
        If this method is called twice without starting the local scope in between.

    acquire(self, scope, addr_type, size):
        Acquire a virtual address with specified scope and type.

        Parameters
        ----------
        scope : Scope
            The scope of the virtual address.

        addr_type : Type
            The type of the virtual address.

        size : int, default = 1
            The amount of addresses to acquire.
    """

    @abstractmethod
    def start_local_scope(self):
        """Start a scope with new local and temporary addresses.

        Panics
        ------
        If this method is called twice without ending the local scope in between.
        """

    @abstractmethod
    def end_local_scope(self):
        """End the current local scope.

        Panics
        ------
        If this method is called twice without starting the local scope in between.
        """

    @abstractmethod
    def acquire(self, scope, addr_type) -> VirtualAddress:
        """Acquire a virtual address with specified scope and type.

        Parameters
        ----------
        scope : Scope
            The scope of the virtual address.

        addr_type : Type
            The type of the virtual address.
        """


# class GenericScopeVirtualAddressSubcontroller:
#     def __init__(self, class_name, virtual_address_class, base_address, max_size):
#         self.__class_name = class_name
#         self.__virtual_address_class = virtual_address_class
#         self.__base_address = base_address
#         self.__max_size = max_size
#         self.__type_counter = _TypeCounter()

#     def acquire(self, addr_type, size=1) -> VirtualAddress:
#         subcontroller_address = self.__type_counter.value(addr_type)
#         if subcontroller_address + size > self.__max_size:
#             print(
#                 f'Error: {self.class_name}.acquire(): ran out of addresses to release')
#         if address + size > self.__max_size:
#         self.__type_counter.increment(addr_type, size)
#         return self.__virtual_address_class(address)


# class GlobalVirtualAddressController:
#     def __init__(self, max_size_per_type, base_address):
#         self.__max_size_per_type = max_size_per_type
#         self.__base_address = base_address
#         self.__type_counter = _TypeCounter()

#     def acquire(self, addr_type, size=1):
#         type_address = self.__type_counter.value()
#         if type_address + size > self.__max_size_per_type[addr_type]:
#             print(
#                 f'Error: GlobalVirtualAddressController.acquire(): ran out of {addr_type} addresses to release.')
#             sys.exit(1)
#         self.__type_counter.increment(addr_type, size)
#         virtual_address_number = type_address + self.__base_address
#         return VirtualAddressConcrete(virtual_address_number)


# class _VirtualAddressSubcontrollerFactory:
#     def create(self, scope):
#         subcontroller = None
#         if scope is Scope.GLOBAL:
#             subcontroller = GlobalVirtualAddressController()
#         elif scope is Scope.LOCAL:
#             subcontroller = LocalVirtualAddressController()
#         elif scope is Scope.TEMPORARY:
#             subcontroller = TemporaryVirtualAddressController()
#         elif scope is Scope.CONSTANT:
#             subcontroller = ConstantVirtualAddressController()
#         else:
#             print(
#                 f'Error: _VirtualAddressSubcontrollerFactory.create(): scope not supported: {scope}')
#             sys.exit(1)
#         return subcontroller


class VirtualAddressControllerConcrete(VirtualAddressControllerInterface):
    """Implements VirtualAddressControllerInterface."""

    def __init__(self, limits):
        """
        Example
        -------

        limits : VirtualAddressConcrete.LIMITS
        """
        self.__limits = limits
        self.__counter = _ScopeTypeCounter()
        self.__state = _LocalScopeState()

    def start_local_scope(self):
        """Start a scope with new local and temporary addresses.

        Panics
        ------
        If this method is called twice without ending the local scope in between.
        """
        if self.__state.is_started():
            print(
                'Error: VirtualAddressControllerConcrete.start_local_scope(): cannot be started unless ended first.')
            sys.exit(1)
        self.__state.start()
        self.__counter.clear_scope(Scope.LOCAL)
        self.__counter.clear_scope(Scope.TEMPORARY)

    def end_local_scope(self):
        """End the current local scope.

        Panics
        ------
        If this method is called twice without starting the local scope in between.
        """
        if self.__state.is_ended():
            print(
                'Error: VirtualAddressControllerConcrete.end_local_scope(): cannot be ended unless started first.')
            sys.exit(1)
        self.__state.end()

    def acquire(self, scope, addr_type) -> VirtualAddress:
        size: int = 1
        subtype = addr_type
        while subtype.is_array():
            array_type = subtype.type()
            size *= array_type.length().value()
            subtype = array_type.type()
        primitive_type = subtype.type()
        offset = self.__counter.value(scope, primitive_type)
        if offset + size > self.__limits[scope]['types'][primitive_type.canonical()]['max_amount']:
            print(
                f'Error: VirtualAddressControllerConcrete.acquire(): ran out of addresses to release for scope {scope} and type {addr_type}.')
            sys.exit(1)
        self.__counter.increment(scope, primitive_type, size)
        return VirtualAddressConcrete(scope, primitive_type, offset)
