from .block_expression import BlockExpression

class PredicateLoopExpression:
    def __init__(self, expression, block: BlockExpression):
        self.__expression = expression
        self.__block: BlockExpression = block

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'PredicateLoopExpression:\n'
        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}\n'
        block_str: str = self.__block.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}block: {block_str}'
        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
