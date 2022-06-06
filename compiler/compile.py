import sys

from compiler import Lexer, Parser, Compiler, DirFunc, SemanticCube, TemporaryVariable
from compiler.virtual_address import VirtualAddressControllerConcrete, VirtualAddressConcrete
from compiler.dust_ast import Identifier, BooleanLiteral, IntegerLiteral, FloatLiteral, CharLiteral
from obj_file import ObjFile


def quadruples_to_dict(quadruples):
    """Convert quadruples to dictionary."""
    result = []
    for quadruple in quadruples:
        subresult = [quadruple[0]]
        for i in range(1, len(quadruple)):
            if quadruple[i] is None:
                subresult.append(None)
                continue
            if isinstance(quadruple[i], TemporaryVariable):
                subresult.append(quadruple[i].virtual_address().addr())
                continue
            if isinstance(quadruple[i], Identifier):
                subresult.append(quadruple[i].operand().addr())
                continue
            if isinstance(quadruple[i], (BooleanLiteral, IntegerLiteral, FloatLiteral, CharLiteral)):
                subresult.append(quadruple[i].operand().addr())
                continue
            if isinstance(quadruple[i], VirtualAddressConcrete):
                subresult.append(quadruple[i].addr())
                continue
            subresult.append(quadruple[i])
        result.append(subresult)
    return result


def main():

    dir_func = DirFunc()
    semantic_cube = SemanticCube()
    quadruples = []
    virtual_address_controller = VirtualAddressControllerConcrete(
        VirtualAddressConcrete.LIMITS)
    constant_table = {}
    l = Lexer(constant_table=constant_table,
              virtual_address_controller=virtual_address_controller)
    p = Parser(l, dir_func, semantic_cube, quadruples, virtual_address_feature_on=True,
               virtual_address_controller=virtual_address_controller, constant_table=constant_table)
    c = Compiler(p, dir_func, semantic_cube)

    if len(sys.argv) != 3:
        print(f'''{sys.argv[0]} must be called with 1 argument:
    {sys.argv[0]} <target> <output>        Compiles the specified file.
    {sys.argv[0]} -                        Reads from stdin the source code to compile.
    {' ' * len(sys.argv[0])}        Outputs to a.dsobj file
    {' ' * len(sys.argv[0])}        To end, enter Ctrl+Z.''')
        return

    source_code = ''
    if sys.argv[1] == '-':
        source_code = sys.stdin.read()
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            source_code = file.read()

    _result = c.test(source_code)
    obj_file_to_save = ObjFile(
        constant_table=constant_table,
        globals_table=dir_func.globals_table(),
        function_directory=dir_func.to_dict(),
        quadruples=quadruples_to_dict(quadruples),
        target=sys.argv[1],
        output=sys.argv[2]
    )
    obj_file_to_save.save()


if __name__ == '__main__':
    main()
