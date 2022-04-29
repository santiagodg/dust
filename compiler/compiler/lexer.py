from .ply import lex

from .dust_ast import Identifier, CharLiteral, IntegerLiteral, FloatLiteral, BooleanLiteral

class Lexer:
    special_function_names = {
        'read': 'READ',
        'write': 'WRITE',
        'plot': 'PLOT',
        'scatter': 'SCATTER',
        'histogram': 'HISTOGRAM',
        'mean': 'MEAN',
        'median': 'MEDIAN',
        'mean_square_error': 'MEAN_SQUARE_ERROR',
        'min': 'MIN',
        'max': 'MAX',
        'standard_deviation': 'STANDARD_DEVIATION',
        'variance': 'VARIANCE',
        'skewness': 'SKEWNESS',
        'kurtosis': 'KURTOSIS',
        'r_squared': 'R_SQUARED',
        'sum': 'SUM',
    }

    reserved = {
        'as': 'AS',
        'bool': 'BOOL',
        'break': 'BREAK',
        'char': 'CHAR',
        'continue': 'CONTINUE',
        'else': 'ELSE',
        'f64': 'F64',
        'fn': 'FN',
        'i32': 'I32',
        'if': 'IF',
        'let': 'LET',
        'loop': 'LOOP',
        'return': 'RETURN',
        'static': 'STATIC',
        'while': 'WHILE',
    } | special_function_names

    tokens = [
        'CHAR_LITERAL',
        'FLOAT_LITERAL',
        'INTEGER_LITERAL',
        'BOOL_LITERAL',
        'EQ',
        'NE',
        'LE',
        'GE',
        'OR',
        'AND',
        'RIGHT_ARROW',
        'IDENTIFIER',
    ] + list(reserved.values())

    literals = [',', ')', '(', ':', ';', ']', '[', '}',
        '{', '=', '-', '!', '+', '*', '/', '%', '>', '<',
    ]

    def t_CHAR_LITERAL(self, t):
        r"'[^'\\\n\t\r]'"
        print(f'Found char literal: {t}')
        t.value = CharLiteral(t.value)

    def t_FLOAT_LITERAL(self, t):
        r'[0-9][0-9]*\.[0-9][0-9]*'
        t.value = FloatLiteral(float(t.value))
        return t
    
    def t_INTEGER_LITERAL(self, t):
        r'[0-9][0-9]*'
        t.value = IntegerLiteral(int(t.value))
        return t

    def t_BOOL_LITERAL(self, t):
        r'(true|false)'

        if t.value == 'true':
            t.value = BooleanLiteral(True)
        else:
            t.value = BooleanLiteral(False)
        
        return t
    
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')

        if t.type == 'IDENTIFIER':
            t.value = Identifier(t.value)

        return t

    t_EQ = r'=='
    t_NE = r'!='
    t_LE = r'<='
    t_GE = r'>='
    t_OR = r'\|\|'
    t_AND = r'&&'
    t_RIGHT_ARROW = r'->'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    t_ignore = " \t"

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
        print(t)
        t.lexer.skip(1)

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    def test(self, data):
        self.lexer.input(data)

        for tok in self.lexer:
            print(tok)
