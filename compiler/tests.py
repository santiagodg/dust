import dust_ast
from compiler import Compiler
from lexer import Lexer
from parser import Parser

class TestCase:
    def __init__(self, name: str, input: str, expected: dust_ast.Crate):
        self.name = name
        self.input = input
        self.expected = expected

def run():
    test_cases = [
        TestCase(
            'empty string',
            '',
            dust_ast.Crate([]),
        ),
        TestCase(
            'single static_item',
            'static id1: bool;',
            dust_ast.Crate([
                dust_ast.Item(
                    dust_ast.StaticItem(
                        'id1', 
                        dust_ast.Type(('type', ('primitive_type', 'bool'))),
                    ),
                ),
            ]),
        ),
        TestCase(
            'multiple static_item',
            '''
            static id1: bool;
            static id2: bool;
            ''',
            dust_ast.Crate([
                dust_ast.Item(
                    dust_ast.StaticItem(
                        'id1', 
                        dust_ast.Type(('type', ('primitive_type', 'bool'))),
                    ),
                ),
                dust_ast.Item(
                    dust_ast.StaticItem(
                        'id2', 
                        dust_ast.Type(('type', ('primitive_type', 'bool'))),
                    ),
                ),
            ]),
        ),
        TestCase(
            'single function',
            '''
            fn id1() {}
            ''',
            dust_ast.Crate([
                dust_ast.Item(
                    dust_ast.Function(
                        'id1', 
                        [],
                        None,
                        [],
                        dust_ast.BlockExpression(('block_expression', ('statements', [])))
                    ),
                ),
            ]),
        ),
    ]

    for tc in test_cases:
        l = Lexer()
        p = Parser(l)
        c = Compiler(p)
        result = c.test(tc.input)

        if result == tc.expected:
            print(f'{tc.name}: PASSED')
            continue
        
        print(f'\n{tc.name}: FAILED')
        print(f'expected: {tc.expected.to_string()}')
        print(f'result: {result.to_string()}\n')

if __name__ == '__main__':
    run()
