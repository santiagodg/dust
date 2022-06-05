from .ply import lex

from .dust_ast import Identifier, CharLiteral, IntegerLiteral, FloatLiteral, BooleanLiteral, Type, PrimitiveType
from .virtual_address import Scope


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
        r"'([^'\\]|\\.)'"
        constant_literal_virtual_address = None
        for virtual_address, value in self.__constant_table.items():
            if value == t.value[1:-1] and isinstance(value, str):
                constant_literal_virtual_address = virtual_address
                break
        if constant_literal_virtual_address is None:
            constant_literal_virtual_address = self.__virtual_address_controller.acquire(
                Scope.CONSTANT, Type(PrimitiveType('char')))
            self.__constant_table[constant_literal_virtual_address.addr(
            )] = t.value[1:-1]
        t.value = CharLiteral(t.value[1:-1], constant_literal_virtual_address)
        return t

    def t_FLOAT_LITERAL(self, t):
        r'[0-9][0-9]*\.[0-9][0-9]*'
        constant_literal_virtual_address = None
        for virtual_address, value in self.__constant_table.items():
            if value == float(t.value) and isinstance(value, float):
                constant_literal_virtual_address = virtual_address
                break
        if constant_literal_virtual_address is None:
            constant_literal_virtual_address = self.__virtual_address_controller.acquire(
                Scope.CONSTANT, Type(PrimitiveType('f64')))
            self.__constant_table[constant_literal_virtual_address.addr()] = float(
                t.value)
        t.value = FloatLiteral(
            float(t.value), constant_literal_virtual_address)
        return t

    def t_INTEGER_LITERAL(self, t):
        r'[0-9][0-9]*'
        constant_literal_virtual_address = None
        for virtual_address, value in self.__constant_table.items():
            if value == int(t.value) and isinstance(value, int):
                constant_literal_virtual_address = virtual_address
                break
        if constant_literal_virtual_address is None:
            constant_literal_virtual_address = self.__virtual_address_controller.acquire(
                Scope.CONSTANT, Type(PrimitiveType('i32')))
            self.__constant_table[constant_literal_virtual_address.addr()] = int(
                t.value)
        t.value = IntegerLiteral(
            int(t.value), constant_literal_virtual_address)
        return t

    def t_BOOL_LITERAL(self, t):
        r'(true|false)'
        t.value = t.value == 'true'
        constant_literal_virtual_address = None
        for virtual_address, value in self.__constant_table.items():
            if value == t.value and isinstance(value, bool):
                constant_literal_virtual_address = virtual_address
                break
        if constant_literal_virtual_address is None:
            constant_literal_virtual_address = self.__virtual_address_controller.acquire(
                Scope.CONSTANT, Type(PrimitiveType('bool')))
            self.__constant_table[constant_literal_virtual_address.addr(
            )] = t.value
        t.value = BooleanLiteral(t.value, constant_literal_virtual_address)
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

    def __init__(self, constant_table={}, virtual_address_controller=None, **kwargs):
        self.__constant_table = constant_table
        self.__virtual_address_controller = virtual_address_controller
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)

        for tok in self.lexer:
            print(tok)
