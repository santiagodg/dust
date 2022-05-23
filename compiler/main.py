import sys

from compiler import Lexer, Parser, Compiler, DirFunc, SemanticCube, pretty_print_quadruples_with_addresses
from compiler.virtual_address import VirtualAddressControllerConcrete, VirtualAddressConcrete


def main():

    l = Lexer()
    dir_func = DirFunc()
    semantic_cube = SemanticCube()
    quadruples = []
    virtual_address_controller = VirtualAddressControllerConcrete(
        VirtualAddressConcrete.LIMITS)
    p = Parser(l, dir_func, semantic_cube, quadruples, virtual_address_feature_on=True,
               virtual_address_controller=virtual_address_controller)
    c = Compiler(p, dir_func, semantic_cube)

    if len(sys.argv) != 2:
        print(f'''{sys.argv[0]} must be called with 1 argument:
    {sys.argv[0]} <filename>        Compiles the specified file.
    {sys.argv[0]} -                 Reads from stdin the source code to compile.
    {' ' * len(sys.argv[0])}                   To end, enter Ctrl+Z.''')
        return

    source_code = ''
    if sys.argv[1] == '-':
        source_code = sys.stdin.read()
    else:
        with open(sys.argv[1], 'r') as file:
            source_code = file.read()

    result = c.test(source_code)

    # print()
    # print(result)
    # print()
    # print(dir_func)

    print()
    pretty_print_quadruples_with_addresses(quadruples)


if __name__ == '__main__':
    main()
