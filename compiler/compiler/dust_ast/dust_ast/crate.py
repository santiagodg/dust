from .item import Item

class Crate:
    def __init__(self, items: list[Item]):
        self.__items: list[Item] = items
    
    def add_item(self, item: Item):
        self.__items.append(item)
    
    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'Crate:\n'

        if len(self.__items) == 0:
            result += f'{space_padding}{space_indent}items: []'
        else:
            result += f'{space_padding}{space_indent}items: [\n'

            for item in self.__items:
                item_str: str = item.to_string(indent, padding + indent * 2)
                result += f'{space_padding}{space_indent}{space_indent}{item_str}\n'
            
            result += f'{space_padding}{space_indent}]'
        
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