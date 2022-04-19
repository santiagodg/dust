from typing import Optional

from .block_expression import BlockExpression

class IfExpression:
    def __init__(self, expression, true_block: BlockExpression, false_block: BlockExpression):
        """
        expression: Expression
        true_block: BlockExpression
        false_block: Optional[BlockExpression]
        """
        
        self.__expression = expression
        self.__true_block: BlockExpression = true_block
        self.__false_block: Optional[BlockExpression] = false_block

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'IfExpression:\n'
        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}\n'
        true_block_str: str = self.__true_block.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}true_block: {true_block_str}\n'

        if self.__false_block == None:
            result += f'{space_padding}{space_indent}false_block: None'
        else:
            false_block_str: str = self.__false_block.to_string(indent, padding + indent)
            result += f'{space_padding}{space_indent}false_block: {false_block_str}'

        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
