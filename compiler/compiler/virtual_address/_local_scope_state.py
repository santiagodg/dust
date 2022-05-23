"""Defines _LocalScopeState class and helpers.

Classes
-------
_LocalScopeState
    Manages local scope state.
_LocalScopeStateEnum : Enum
    Enumerates local scope states.
"""

from enum import Enum


class _LocalScopeStateEnum(Enum):
    """Enumerates local scope states."""
    STARTED = 1
    ENDED = 2


class _LocalScopeState:
    """Manages local scope state.

    Methods
    -------
    __init__(self):
        Construct the state initialized to 'ended'.

    start(self):
        Set state to 'started'.

    end(self):
        Set state to 'ended'.

    is_started(self):
        Check if the state is 'started'.

        Returns
        -------
        is_started : bool
            True if the state is 'started'.

    is_ended(self):
        Check if the state is 'ended'.

        Returns
        -------
        is_ended : bool
            True if the state is 'ended'.
    """

    def __init__(self):
        """Construct the state initialized to 'ended'."""
        self.__state: _LocalScopeStateEnum = _LocalScopeStateEnum.ENDED

    def start(self):
        """Set state to 'started'."""
        self.__state = _LocalScopeStateEnum.STARTED

    def end(self):
        """Set state to 'ended'."""
        self.__state = _LocalScopeStateEnum.ENDED

    def is_started(self):
        """Check if the state is 'started'.

        Returns
        -------
        is_started : bool
            True if the state is 'started'.
        """
        return self.__state is _LocalScopeStateEnum.STARTED

    def is_ended(self):
        """Check if the state is 'ended'.

        Returns
        -------
        is_ended : bool
            True if the state is 'ended'.
        """
        return self.__state is _LocalScopeStateEnum.ENDED
