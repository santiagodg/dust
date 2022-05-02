from .dust_ast import *
from .parser import TemporaryVariable

def pretty_print_quadruples(quadruples):
    result = ''
    for quadruple in quadruples:
        result += f'({quadruple[0]}, '

        for i in range(1, 3):
            if quadruple[i] == '':
                result += ', '
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
        
        if quadruple[3] == '':
            result += ''
        elif isinstance(quadruple[3], TemporaryVariable):
            result += f't{quadruple[3].number()}'
        elif isinstance(quadruple[3], Identifier):
            result += f'{quadruple[3].identifier()}'
        elif isinstance(quadruple[3], (BooleanLiteral, IntegerLiteral, FloatLiteral, CharLiteral)):
            result += f'{quadruple[3].value()}'
        
        result += ')\n'
    
    print(result)
            
        