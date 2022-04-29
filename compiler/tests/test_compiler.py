from compiler import Lexer, Parser, Compiler, DirFunc
from compiler.dust_ast import *

def test_compiler_empty_crate():
    l = Lexer()
    dir_func = DirFunc()
    p = Parser(l, dir_func)
    c = Compiler(p)

    result = c.test("")
    expected = Crate([])

    assert result == expected

    p.restart()

def test_compiler_1():
    l = Lexer()
    dir_func = DirFunc()
    p = Parser(l, dir_func)
    c = Compiler(p)

    result = c.test("""
static global_bool: bool;
static global_i32: i32;
static global_f64: f64;
static global_char: char;

fn sum_two_f64(local_f64_1: f64, local_f64_2: f64) -> f64 {
    return local_f64_1 + local_f64_2;
}

fn main()
let local_f64_main_1: f64;
let local_f64_main_2: f64;
{
    local_f64_main_1 = 1.0;
    local_f64_main_2 = 2.0;

    if sum_two_f64(local_f64_main_1, local_f64_main_2) == 3.0 {

    };
}
""")

    expected = Crate([
        Item(StaticItem(Identifier('global_bool'), Type(PrimitiveType('bool')))), # static global_bool: bool;
        Item(StaticItem(Identifier('global_i32'), Type(PrimitiveType('i32')))), # static global_i32: i32;
        Item(StaticItem(Identifier('global_f64'), Type(PrimitiveType('f64')))), # static global_f64: f64;
        Item(StaticItem(Identifier('global_char'), Type(PrimitiveType('char')))), # static global_char: char;
        Item(Function( # fn sum_two_f64(local_f64_1: f64, local_f64_2: f64) -> f64 {
            Identifier('sum_two_f64'),
            [
                FunctionParameter(Identifier('local_f64_1'), Type(PrimitiveType('f64'))),
                FunctionParameter(Identifier('local_f64_2'), Type(PrimitiveType('f64'))),
            ],
            PrimitiveType('f64'),
            [],
            BlockExpression([
                Statement(Expression(ExpressionWithoutBlock(ReturnExpression( # return local_f64_1 + local_f64_2;
                    Expression(ExpressionWithoutBlock(OperatorExpression(ArithmeticExpression(
                        Expression(ExpressionWithoutBlock(Identifier('local_f64_1'))),
                        '+',
                        Expression(ExpressionWithoutBlock(Identifier('local_f64_2'))),
                    )))))
                ))),
            ])
        )),
        Item(Function( # fn main()
            Identifier('main'),
            [],
            None,
            [
                LetStatement(Identifier('local_f64_main_1'), Type(PrimitiveType('f64'))), # let local_f64_main_1: f64;
                LetStatement(Identifier('local_f64_main_2'), Type(PrimitiveType('f64'))), # let local_f64_main_2: f64;
            ],
            BlockExpression([
                Statement(Expression(ExpressionWithoutBlock(OperatorExpression(AssignmentExpression( # local_f64_main_1 = 1.0;
                    Expression(ExpressionWithoutBlock(Identifier('local_f64_main_1'))),
                    Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(1.0))))
                ))))),
                Statement(Expression(ExpressionWithoutBlock(OperatorExpression(AssignmentExpression( # local_f64_main_2 = 2.0;
                    Expression(ExpressionWithoutBlock(Identifier('local_f64_main_2'))),
                    Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(2.0))))
                ))))),
                Statement(Expression(ExpressionWithBlock(IfExpression( # if sum_two_f64(local_f64_main_1, local_f64_main_2) == 3.0 {
                    Expression(ExpressionWithoutBlock(OperatorExpression(ComparisonExpression(
                        Expression(ExpressionWithoutBlock(CallExpression(
                            Identifier('sum_two_f64'),
                            [
                                Expression(ExpressionWithoutBlock(Identifier('local_f64_main_1'))),
                                Expression(ExpressionWithoutBlock(Identifier('local_f64_main_2'))),
                            ]
                        ))),
                        '==',
                        Expression(ExpressionWithoutBlock(LiteralExpression(FloatLiteral(3.0)))),
                    )))),
                    BlockExpression([]),
                    None
                ))))
            ])
        ))
    ])

    assert result.to_string() == expected.to_string()

    p.restart()
