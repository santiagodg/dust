"""Define _ScopeTypeCounter."""

from .scope import Scope


class _ScopeTypeCounter:
    """Count how many virtual addresses of each scope and type have been released."""

    def __init__(self):
        """Construct the counter."""
        self.__counter = {}
        for scope in list(Scope):
            self.__counter[scope] = {}
            for primitive_type in ['bool', 'char', 'i32', 'f64', 'pointer']:
                self.__counter[scope][primitive_type] = 0

    def increment(self, scope, addr_type, amount):
        """Increment the specific counter by some amount.

        Parameters
        ----------
        scope : Scope
            The scope of the counter.
        addr_type : PrimitiveType | 'pointer'
            The type of the counter.
        amount : int
            Amount of addresses released.
        """
        if addr_type == 'pointer':
            self.__counter[scope]['pointer'] += amount
            return
        self.__counter[scope][addr_type.canonical()] += amount

    def value(self, scope, addr_type):
        """Return the current value of the specified counter.

        Parameters
        ----------
        scope : Scope
            The scope of the counter.
        addr_type : PrimitiveType | 'pointer'
            The type of the counter.

        Returns
        -------
        value : int
            The current value of the specified counter.
        """
        if addr_type == 'pointer':
            return self.__counter[scope]['pointer']
        return self.__counter[scope][addr_type.canonical()]

    def clear_scope(self, scope):
        """Clear local scope.

        Parameters
        ----------
        scope : Scope
            Scope of the counter to clear.
        """
        self.__counter[scope] = {}
        for primitive_type in ['bool', 'char', 'i32', 'f64', 'pointer']:
            self.__counter[scope][primitive_type] = 0
