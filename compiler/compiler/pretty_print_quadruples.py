from .dust_ast import *
from .parser import TemporaryVariable


def pretty_print_quadruples(quadruples):
    super_result = []
    for index, quadruple in enumerate(quadruples):
        result = f'{str(index).zfill(3)}. ({quadruple[0]}, '

        for i in range(1, 3):
            if quadruple[i] == None:
                result += 'None, '
                continue

            if isinstance(quadruple[i], TemporaryVariable):
                result += f't{quadruple[i].number()}, '
                continue

            if isinstance(quadruple[i], Identifier):
                result += f'{quadruple[i].identifier()}, '
                continue

            if isinstance(quadruple[i], (BooleanLiteral, IntegerLiteral, FloatLiteral, CharLiteral)):
                result += f'{quadruple[i].value()}, '
                continue

            result += f'{str(quadruple[i])}, '

        if quadruple[3] == None:
            result += 'None'
        elif isinstance(quadruple[3], TemporaryVariable):
            result += f't{quadruple[3].number()}'
        elif isinstance(quadruple[3], Identifier):
            result += f'{quadruple[3].identifier()}'
        elif isinstance(quadruple[3], (BooleanLiteral, IntegerLiteral, FloatLiteral, CharLiteral)):
            result += f'{quadruple[3].value()}'
        else:
            result += str(quadruple[3])

        result += ')'

        super_result.append(result)

    print('\n'.join(super_result))


def pretty_print_quadruples_with_addresses(quadruples):
    super_result = []
    for index, quadruple in enumerate(quadruples):
        result = f'{str(index).zfill(3)}. ({quadruple[0]}, '
        for i in range(1, 3):
            if quadruple[i] is None:
                result += 'None, '
                continue
            if isinstance(quadruple[i], TemporaryVariable):
                result += f'{quadruple[i].virtual_address()}, '
                continue
            if isinstance(quadruple[i], Identifier):
                result += f'{quadruple[i].operand()}, '
                continue
            if isinstance(quadruple[i], (BooleanLiteral, IntegerLiteral, FloatLiteral, CharLiteral)):
                result += f'{quadruple[i].operand()}, '
                continue
            result += f'{str(quadruple[i])}, '
        if quadruple[3] is None:
            result += 'None'
        elif isinstance(quadruple[3], TemporaryVariable):
            result += f'{quadruple[3].virtual_address()}'
        elif isinstance(quadruple[3], Identifier):
            result += f'{quadruple[3].operand()}'
        elif isinstance(quadruple[3], (BooleanLiteral, IntegerLiteral, FloatLiteral, CharLiteral)):
            result += f'{quadruple[3].operand()}'
        else:
            result += str(quadruple[3])
        result += ')'
        super_result.append(result)
    print('\n'.join(super_result))
