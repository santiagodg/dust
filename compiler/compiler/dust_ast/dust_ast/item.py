from .static_item import StaticItem
from .function import Function

class Item:
    def __init__(self, item: StaticItem | Function):
        self.__item: StaticItem | Function = item

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'Item:\n'
        item_str: str = self.__item.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}item: {item_str}'
        return result
    
    def __eq__(self, other) : 
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
