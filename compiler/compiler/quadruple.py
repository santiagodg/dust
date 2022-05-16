from abc import ABC, abstractclass
from typing import Any

class Quadruple:

    @abstractclass
    def __init__(self, dict):
        pass

    @abstractclass
    def __getitem__(self, key: int) -> Any:
        """
        Gets the item at index key.

        # Raises

        - If key is of an inappropriate type, TypeError is raised.
        - If of a value outside the set of indexes for the sequence, IndexError is raised.
        - If key is missing (not in the container), KeyError is raised.

        :param key: index to access
        :type key: int
        """
        pass

    @abstractclass
    def to_dict(self) -> dict:
        pass
