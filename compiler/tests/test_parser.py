from compiler import Lexer, Parser, DirFunc, FunctionEntry
from compiler.dust_ast import *

def test_dir_func_add_function_success():
    input = """
fn f1() {}

fn f2() {}

fn main() {
    f1();
    f2();
}
"""

    expected = DirFunc(
        static_items={},
        functions={
            'f1': FunctionEntry(
                identifier=Identifier('f1'),
                parameters={},
                return_type=None,
                let_statements={}
            ),
            'f2': FunctionEntry(
                identifier=Identifier('f2'),
                parameters={},
                return_type=None,
                let_statements={}
            ),
            'main': FunctionEntry(
                identifier=Identifier('main'),
                parameters={},
                return_type=None,
                let_statements={}
            )
        }
    )

    l = Lexer()
    dir_func1 = DirFunc({}, {})
    p = Parser(l, dir_func1)
    p.test(input)

    assert str(dir_func1) == str(expected)

    p.restart()
