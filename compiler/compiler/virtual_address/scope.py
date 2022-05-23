"""Define the Scope class."""

from enum import Enum

class Scope(Enum):
    """Enumerate the scopes of a virtual address."""

    GLOBAL = 1
    LOCAL = 2
    TEMPORARY = 3
    CONSTANT = 4
