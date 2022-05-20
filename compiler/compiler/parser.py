import copy
import sys
from typing import Optional

from .ply import yacc

from .lexer import Lexer
from .dir_func import DirFunc
from .semantic_cube import SemanticCube
from .dust_ast import *


class TemporaryVariable:
    def __init__(self, number: int, var_type: Type):
        self.__number = number
        self.__type = var_type

    def number(self) -> int:
        return self.__number

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = f'{type(self).__name__}('
        attr_str = []
        for key, value in vars(self).items():
            prefix = key.replace(f"_{type(self).__name__}", '')
            attr_str += [f'{prefix}={str(value)}']
        result += ','.join(attr_str)
        result += ')'
        return result


class TemporaryVariableGenerator:
    def __init__(self):
        self.__counter = 1
        self.__count = {}

    def next(self, var_type: Type) -> TemporaryVariable:
        new_temporary_variable = TemporaryVariable(self.__counter, var_type)
        self.__counter += 1

        if var_type.canonical() not in self.__count:
            self.__count[var_type.canonical()] = 0
        else:
            self.__count[var_type.canonical()] += 1

        return new_temporary_variable

    def start_counting(self):
        self.__count = {}

    def get_count(self) -> dict[str, int]:
        return copy.deepcopy(self.__count)


class Parser():
    tokens = Lexer().tokens

    precedence = (
        ('right', 'RETURN', 'BREAK'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE', '<', '>', 'LE', 'GE'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('left', 'AS'),
        ('right', 'UMINUS', '!'),
    )

    def p_crate(self, p):
        '''crate : crate item
                 | empty'''

        if len(p) == 2:
            self.__quadruples.append([
                'Goto',
                None,
                None,
                'main',
            ])

            p[0] = Crate([])
        else:
            p[1].add_item(p[2])
            p[0] = p[1]

    def p_item(self, p):
        """item : static_item
                | function"""
        p[0] = Item(p[1])

    def p_static_item(self, p):
        "static_item : STATIC IDENTIFIER static_item_check_id ':' type ';'"
        static_item = StaticItem(p[2], p[5])
        self.__dir_func.add_static_item(static_item)
        p[0] = static_item

    def p_static_item_check_id(self, p):
        "static_item_check_id :"
        if self.__dir_func.exists(p[-1]):
            print(f"Multiple declaration: identifier '{p[-1].identifier()}'")
            sys.exit(1)

    def p_function(self, p):
        """function : FN IDENTIFIER function_point_1 '(' function_parameters ')' function_return_type function_point_2 let_statements function_point_3 block_expression
                    | FN IDENTIFIER function_point_1 '(' function_parameters ')'        empty         function_point_2 let_statements function_point_3 block_expression"""

        temporary_variables_count = self.__temp_var_generator.get_count()
        self.__dir_func.add_temporary_variable_count(
            self.__temp_function_identifier, temporary_variables_count)

        self.__temp_function_identifier = None

        p[0] = Function(p[2], p[5], p[7], p[9], p[11])

    def p_function_point_1(self, p):
        "function_point_1 : "

        if self.__dir_func.exists(p[-1]):
            print(
                f"Multiple declaration: function '{p[-1].identifier()}' in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        self.__temp_function_identifier = p[-1]
        self.__dir_func.add_function_identifier(
            self.__temp_function_identifier)
        self.__dir_func.set_function_start_quadruple_index(
            self.__temp_function_identifier, len(self.__quadruples))

    def p_function_point_2(self, p):
        "function_point_2 :"
        self.__dir_func.add_function_return_type(
            self.__temp_function_identifier, p[-1])

    def p_function_point_3(self, p):
        'function_point_3 :'

        self.__temp_var_generator.start_counting()

    def p_function_parameters_0(self, p):
        """function_parameters : empty
                               | function_param function_parameters_1"""

        if len(p) == 2:
            p[0] = []
        else:
            p[0] = [p[1]] + p[2]

    def p_function_parameters_1(self, p):
        """function_parameters_1 : ',' function_param function_parameters_1
                                 | ','
                                 | empty"""

        if len(p) == 4:
            p[0] = [p[2]] + p[3]
        else:
            p[0] = []

    def p_function_param(self, p):
        "function_param : IDENTIFIER function_param_check_id ':' type"
        function_parameter = FunctionParameter(p[1], p[4])
        self.__dir_func.add_function_parameter(
            self.__temp_function_identifier, function_parameter)
        p[0] = function_parameter

    def p_function_param_check_id(self, p):
        "function_param_check_id :"
        id_exists = self.__dir_func.exists_in_var_tables(
            self.__temp_function_identifier, p[-1])

        if id_exists:
            print(
                f"Multiple declaration: local identifier '{p[-1].identifier()}' in function '{self.__temp_function_identifier.identifier()}' in line {self.lexer.lexer.lineno}")
            sys.exit(1)

    def p_function_return_type(self, p):
        "function_return_type : RIGHT_ARROW primitive_type"
        p[0] = p[2]

    def p_statements(self, p):
        """statements : statements statement
                      | empty"""

        if len(p) == 2:
            p[0] = []
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        "statement : expression ';'"
        p[0] = Statement(p[1])

    def p_let_stataments(self, p):
        """let_statements : let_statements let_statement
                        | empty"""

        if len(p) == 2:
            p[0] = []
        else:
            p[0] = p[1] + [p[2]]

    def p_let_statament(self, p):
        "let_statement : LET IDENTIFIER let_statement_check_id ':' type ';'"
        let_statement = LetStatement(p[2], p[5])
        self.__dir_func.add_function_let_statement(
            self.__temp_function_identifier, let_statement)
        p[0] = let_statement

    def p_let_statement_check_id(self, p):
        "let_statement_check_id :"
        id_exists = self.__dir_func.exists_in_var_tables(
            self.__temp_function_identifier, p[-1])

        if id_exists:
            print(
                f"Multiple declaration: local identifier '{p[-1].identifier()}' in function '{self.__temp_function_identifier.identifier()}' in line {self.lexer.lexer.lineno}")
            sys.exit(1)

    def p_expression(self, p):
        """expression : expression_without_block
                      | expression_with_block"""

        p[0] = Expression(p[1])

    def p_expression_error(self, p):
        """expression : error"""
        print(
            f"Syntax error in expression. Bad subexpression on lines {p.linespan(1)[0]}-{p.linespan(1)[1]}")
        sys.exit(1)

    def p_expression_without_block_not_identifier(self, p):
        """expression_without_block : literal_expression
                                    | operator_expression
                                    | grouped_expression
                                    | array_expression
                                    | index_expression
                                    | call_expression
                                    | continue_expression
                                    | break_expression
                                    | return_expression
                                    | special_function_expression"""

        p[0] = ExpressionWithoutBlock(p[1])

    def p_expression_without_block_identifier(self, p):
        """expression_without_block : IDENTIFIER"""
        typed_identifier = self.__dir_func.get_typed_local_or_static_identifier(
            self.__temp_function_identifier, p[1])

        if typed_identifier == None:
            print(
                f"Use of undeclared identifier '{p[1].identifier()}' in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = ExpressionWithoutBlock(typed_identifier)

    def p_expression_with_block(self, p):
        """expression_with_block : loop_expression
                                 | if_expression"""

        p[0] = ExpressionWithBlock(p[1])

    def p_literal_expression(self, p):
        """literal_expression : CHAR_LITERAL
                              | INTEGER_LITERAL
                              | FLOAT_LITERAL
                              | BOOL_LITERAL"""

        p[0] = LiteralExpression(p[1])

    def p_literal_expression_error(self, p):
        """literal_expression : error"""
        print(
            f"Syntax error in literal expression. Bad literal on lines {p.linespan(1)[0]}-{p.linespan(1)[1]}")

    def p_block_expression(self, p):
        "block_expression : '{' statements '}'"
        p[0] = BlockExpression(p[2])

    def p_operator_expression(self, p):
        """operator_expression : negation_expression
                               | arithmetic_expression
                               | comparison_expression
                               | boolean_expression
                               | type_cast_expression
                               | assignment_expression"""

        p[0] = OperatorExpression(p[1])

    def p_negation_expression(self, p):
        """negation_expression : '-' expression %prec UMINUS
                               | '!' expression"""

        if not p[2].type().is_primitive():
            print(
                f"Cannot apply unary '{p[1]}' operator non-primitive type {p[2].type().canonical()} expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if self.__semantic_cube.search_unary_operation(p[1], p[2].type().type()) == None:
            print(
                f"Cannot apply unary '{p[1]}' operator to type {p[2].type().canonical()} expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = NegationExpression(
            p[1], p[2], self.__semantic_cube, self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_arithmetic_expression(self, p):
        """arithmetic_expression : expression '+' expression
                                 | expression '-' expression
                                 | expression '*' expression
                                 | expression '/' expression
                                 | expression '%' expression"""

        if not p[1].type().is_primitive():
            print(
                f"Cannot apply binary '{p[2]}' operator to non-primitive type {p[1].type().canonical()} left expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if not p[3].type().is_primitive():
            print(
                f"Cannot apply binary '{p[2]}' operator to non-primitive type {p[3].type().canonical()} rigth expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if self.__semantic_cube.search_binary_operation(p[1].type().type(), p[2], p[3].type().type()) == None:
            print(
                f"Cannot apply binary '{p[2]}' operator to type {p[1].type().canonical()} left expression and {p[3].type().canonical()} right expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = ArithmeticExpression(
            p[1], p[2], p[3], self.__semantic_cube, self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_comparison_expression(self, p):
        """comparison_expression : expression EQ expression
                                 | expression NE expression
                                 | expression '>' expression
                                 | expression '<' expression
                                 | expression GE expression
                                 | expression LE expression"""

        if not p[1].type().is_primitive():
            print(
                f"Cannot apply binary '{p[2]}' operator to non-primitive type {p[1].type().canonical()} left expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if not p[3].type().is_primitive():
            print(
                f"Cannot apply binary '{p[2]}' operator to non-primitive type {p[3].type().canonical()} rigth expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if self.__semantic_cube.search_binary_operation(p[1].type().type(), p[2], p[3].type().type()) == None:
            print(
                f"Cannot apply binary '{p[2]}' operator to type {p[1].type().canonical()} left expression and {p[3].type().canonical()} right expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = ComparisonExpression(
            p[1], p[2], p[3], self.__semantic_cube, self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_boolean_expression(self, p):
        """boolean_expression : expression OR expression
                              | expression AND expression"""

        if not p[1].type().is_primitive():
            print(
                f"Cannot apply binary '{p[2]}' operator to non-primitive type {p[1].type().canonical()} left expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if not p[3].type().is_primitive():
            print(
                f"Cannot apply binary '{p[2]}' operator to non-primitive type {p[3].type().canonical()} rigth expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if self.__semantic_cube.search_binary_operation(p[1].type().type(), p[2], p[3].type().type()) == None:
            print(
                f"Cannot apply binary '{p[2]}' operator to type {p[1].type().canonical()} left expression and {p[3].type().canonical()} right expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = BooleanExpression(
            p[1], p[2], p[3], self.__semantic_cube, self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_type_cast_expression(self, p):
        "type_cast_expression : expression AS type"

        if not p[1].type().is_primitive():
            print(
                f"Cannot apply binary '{p[2]}' operator to non-primitive type {p[1].type().canonical()} left expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if self.__semantic_cube.search_binary_operation(p[1].type().type(), p[2], p[3].type()) == None:
            print(
                f"Cannot apply binary '{p[2]}' operator to type {p[1].type().canonical()} left expression and {p[3].canonical()} right expression in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = TypeCastExpression(p[1], p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_assignment_expression(self, p):
        "assignment_expression : expression '=' expression"

        if p[1].type() != p[3].type():
            print(
                f"Cannot assign right expression of type {p[3].type().canonical()} to left expression of type {p[1].type().canonical()} in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = AssignmentExpression(p[1], p[3])
        self.__quadruples += p[0].quadruples()

    def p_grouped_expression(self, p):
        "grouped_expression : '(' expression ')'"
        p[0] = GroupedExpression(p[2])

    def p_array_expression_not_empty(self, p):
        """array_expression : '[' array_elements_literal ']'
                            | '[' array_elements_repeat ']'"""
        p[0] = ArrayExpression(p[2], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_array_expression_empty(self, p):
        "array_expression : '[' empty ']'"
        p[0] = ArrayExpression([], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_array_elements_literal(self, p):
        """array_elements_literal : array_elements_literal ',' expression
                                  | expression"""

        if len(p) == 2:
            self.__temp_array_elements_literal_type = p[1].type()
            p[0] = [p[1]]
        else:
            if p[3].type() != self.__temp_array_elements_literal_type:
                print(
                    f"Cannot add expression of type {p[3].type().canonical()} to literal array expression of type {self.__temp_array_elements_literal_type} in line {self.lexer.lexer.lineno}")
                sys.exit(1)

            p[0] = p[1] + [p[3]]

    def p_array_elements_repeat(self, p):
        "array_elements_repeat : expression ';' INTEGER_LITERAL"
        length = p[3].value()
        result = []

        for _ in range(length):
            result += [copy.deepcopy(p[1])]

        p[0] = result

    def p_index_expression(self, p):
        "index_expression : expression '[' INTEGER_LITERAL ']'"

        if not p[1].type().is_array():
            print(
                f"Cannot perform indexing for expression of type {p[1].type().canonical()} in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if p[3].value() < 0 or p[1].type().type().length() >= p[3].value():
            print(
                f"Index '{p[3].value()}' out of range for array of length {p[1].type().type().length()} in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = IndexExpression(p[1], p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_call_expression(self, p):
        """call_expression : IDENTIFIER call_expression_point_1 '(' call_params ',' ')'
                           | IDENTIFIER call_expression_point_1 '(' call_params empty ')'
                           | IDENTIFIER call_expression_point_1 '(' empty empty ')'"""

        if p[4] == None:
            if not self.__dir_func.function_parameters_match(p[1], []):
                print(
                    f"Function call parameters do not match function parameters definition {self.lexer.lexer.lineno}")
                sys.exit(1)

            p[0] = CallExpression(p[1], [], self.__dir_func)
        else:
            call_params_types: list[Type] = list(
                map(lambda param: param.type(), p[4]))
            if not self.__dir_func.function_parameters_match(p[1], call_params_types):
                print(
                    f"Call parameter types do not match function parameter types in line {self.lexer.lexer.lineno}")
                sys.exit(1)

            p[0] = CallExpression(p[1], p[4], self.__dir_func)

        self.__quadruples.append([
            'Gosub',
            p[1].identifier(),
            None,
            None
        ])

    def p_call_expression_point_1(self, p):
        'call_expression_point_1 :'

        if not self.__dir_func.exists_function(p[-1]):
            print(
                f'Call for undeclared function in line {self.lexer.lexer.lineno}')
            sys.exit(1)

        self.__quadruples.append([
            'ERA',
            p[-1].identifier(),
            None,
            None,
        ])

    def p_call_params(self, p):
        """call_params : call_params ',' expression
                       | expression"""

        if len(p) == 2:
            self.__call_parameter_count = 1

            self.__quadruples.append([
                'Parameter',
                p[1].operand(),
                None,
                self.__call_parameter_count
            ])

            p[0] = [p[1]]
        else:
            self.__call_parameter_count += 1

            self.__quadruples.append([
                'Parameter',
                p[3].operand(),
                None,
                self.__call_parameter_count
            ])

            p[0] = p[1] + [p[3]]

    def p_continue_expression(self, p):
        "continue_expression : CONTINUE"
        p[0] = ContinueExpression()
        self.__quadruples += p[0].quadruples()

    def p_break_expression(self, p):
        "break_expression : BREAK"
        p[0] = BreakExpression()
        self.__quadruples += p[0].quadruples()

    def p_return_expression(self, p):
        "return_expression : RETURN expression"

        function_return_type: Optional[Type] = None
        frt = self.__dir_func.function_entry(
            self.__temp_function_identifier).return_type()
        if frt != None:
            function_return_type = Type(frt)

        if function_return_type == None:
            print(
                f'Returning an expression from a function with no return type is not allowed. Line {self.lexer.lexer.lineno}')
            sys.exit(1)

        if function_return_type != p[2].type():
            print(
                f"Return expression of type {p[2].type().canonical()} does not match function declaration return type {function_return_type.canonical()}")
            sys.exit(1)

        p[0] = ReturnExpression(p[2])

        self.__quadruples.append([
            '=',
            p[2].operand(),
            None,
            self.__temp_function_identifier
        ])
        # self.__quadruples += p[0].quadruples()

    def p_return_expression_empty(self, p):
        "return_expression : RETURN empty"

        function_return_type: Optional[Type] = None
        frt = self.__dir_func.function_entry(
            self.__temp_function_identifier).return_type()
        if frt != None:
            function_return_type = Type(frt)

        if function_return_type != None:
            print(
                f'Returning nothing from a function with return type {function_return_type} is not allowed. Line {self.lexer.lexer.lineno}')
            sys.exit(1)

        p[0] = ReturnExpression(None)

    def p_special_function_expression(self, p):
        """special_function_expression : io_expression
                                       | statistic_expression"""

        p[0] = SpecialFunctionExpression(p[1])

    def p_io_expression(self, p):
        """io_expression : read_expression
                         | write_expression"""

        p[0] = IoExpression(p[1])

    def p_read_expression(self, p):
        """read_expression : READ '(' IDENTIFIER ')'
                           | READ '(' index_expression ')'"""

        if p[3].type() != Type(PrimitiveType('char')):
            print(
                f"Parameter must be of type char in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = ReadExpression(p[3])
        self.__quadruples += p[0].quadruples()

    def p_write_expression(self, p):
        "write_expression : WRITE '(' expression ')'"

        if p[3].type() != Type(PrimitiveType('char')):
            print(
                f"Parameter must be of type char in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = WriteExpression(p[3])
        self.__quadruples += p[0].quadruples()

    def p_write_expression_error(self, p):
        "write_expression : WRITE '(' error ')'"
        print(
            f"Syntax error in write expression. Bad expression on lines {p.linespan(3)[0]}-{p.linespan(3)[1]}")

    def p_statistic_expression(self, p):
        """statistic_expression : plot_expression
                                | scatter_expression
                                | histogram_expression
                                | mean_expression
                                | median_expression
                                | mean_square_error_expression
                                | min_expression
                                | max_expression
                                | standard_deviation_expression
                                | variance_expression
                                | skewness_expression
                                | kurtosis_expression
                                | r_squared_expression
                                | sum_expression"""

        p[0] = StatisticExpression(p[1])

    def p_plot_expression(self, p):
        "plot_expression : PLOT '(' expression ',' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if p[5].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"Second parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = PlotExpression(p[3], p[5])
        self.__quadruples += p[0].quadruples()

    def p_scatter_expression(self, p):
        "scatter_expression : SCATTER '(' expression ',' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if p[5].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"Second parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = ScatterExpression(p[3], p[5])
        self.__quadruples += p[0].quadruples()

    def p_histogram_expression(self, p):
        "histogram_expression : HISTOGRAM '(' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = HistogramExpression(p[3])
        self.__quadruples += p[0].quadruples()

    def p_mean_expression(self, p):
        "mean_expression : MEAN '(' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if p[5].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"Second parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = MeanExpression(p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_median_expression(self, p):
        "median_expression : MEDIAN '(' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = MedianExpression(p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_mean_square_expression(self, p):
        "mean_square_error_expression : MEAN_SQUARE_ERROR '(' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = MeanSquareErrorExpression(p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_min_expression(self, p):
        "min_expression : MIN '(' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = MinExpression(p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_max_expression(self, p):
        "max_expression : MAX '(' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = MaxExpression(p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_standard_deviation_expression(self, p):
        "standard_deviation_expression : STANDARD_DEVIATION '(' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = StandardDeviationExpression(p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_variance_expression(self, p):
        "variance_expression : VARIANCE '(' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = VarianceExpression(p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_skewness_expression(self, p):
        "skewness_expression : SKEWNESS '(' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = SkewnessExpression(p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_kurtosis_expression(self, p):
        "kurtosis_expression : KURTOSIS '(' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = KurtosisExpression(p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_r_squared_expression(self, p):
        "r_squared_expression : R_SQUARED '(' expression ',' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        if p[5].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"Second parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = RSquaredExpression(p[3], p[5], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_sum_expression(self, p):
        "sum_expression : SUM '(' expression ')'"

        if p[3].type().canonical() != Type(ArrayType(Type(PrimitiveType('f64')), IntegerLiteral(3))).canonical():
            print(
                f"First parameter must be of type [f64] in line {self.lexer.lexer.lineno}")
            sys.exit(1)

        p[0] = SumExpression(p[3], self.__temp_var_generator)
        self.__quadruples += p[0].quadruples()

    def p_loop_expression(self, p):
        """loop_expression : infinite_loop_expression
                           | predicate_loop_expression"""

        p[0] = LoopExpression(p[1])

    def p_infinite_loop_expression(self, p):
        "infinite_loop_expression : LOOP infinite_loop_expression_point_1 block_expression infinite_loop_expression_point_2"
        p[0] = InfiniteLoopExpression(p[3])

    def p_infinite_loop_expression_point_1(self, p):
        "infinite_loop_expression_point_1 :"
        self.__infinite_loop_expression_start.append(len(self.__quadruples))

    def p_infinite_loop_expression_point_2(self, p):
        "infinite_loop_expression_point_2 :"

        self.__quadruples += [[
            'Goto',
            None,
            None,
            self.__infinite_loop_expression_start.pop()
        ]]

    def p_predicate_loop_expression(self, p):
        "predicate_loop_expression : WHILE predicate_loop_expression_point_1 expression predicate_loop_expression_point_2 block_expression predicate_loop_expression_point_3"

        if p[3].type() != Type(PrimitiveType('bool')):
            print(f"While condition must evaluate to bool")
            sys.exit(1)

        p[0] = PredicateLoopExpression(p[3], p[5])

    def p_predicate_loop_expression_point_1(self, p):
        "predicate_loop_expression_point_1 :"
        self.__predicate_loop_expression_start.append(len(self.__quadruples))

    def p_predicate_loop_expression_point_2(self, p):
        "predicate_loop_expression_point_2 :"

        self.__predicate_loop_expression_goto_f.append(len(self.__quadruples))

        self.__quadruples += [[
            'GotoF',
            p[-1].operand(),
            None,
            None,
        ]]

    def p_predicate_loop_expression_point_3(self, p):
        "predicate_loop_expression_point_3 :"

        self.__quadruples += [[
            'Goto',
            None,
            None,
            self.__predicate_loop_expression_start.pop()
        ]]

        goto_f = self.__predicate_loop_expression_goto_f.pop()
        self.__quadruples[goto_f][3] = len(self.__quadruples)

    def p_if_expression(self, p):
        """if_expression : IF expression if_expression_point_1 block_expression ELSE if_expression_point_2 block_expression if_expression_point_3
                         | IF expression if_expression_point_1 block_expression empty if_expression_without_else_point_2 empty empty"""

        if p[2].type() != Type(PrimitiveType('bool')):
            print(f"If condition must evaluate to bool")
            sys.exit(1)

        p[0] = IfExpression(p[2], p[4], p[7])

    def p_if_expression_point_1(self, p):
        "if_expression_point_1 :"

        self.__if_expression_goto_f.append(len(self.__quadruples))

        self.__quadruples += [[
            'GotoF',
            p[-1].operand(),
            None,
            None,
        ]]

    def p_if_expression_point_2(self, p):
        "if_expression_point_2 :"

        self.__if_expression_goto_t.append(len(self.__quadruples))

        self.__quadruples += [[
            'Goto',
            None,
            None,
            None,
        ]]

        goto_f = self.__if_expression_goto_f.pop()
        self.__quadruples[goto_f][3] = len(self.__quadruples)

    def p_if_expression_point_3(self, p):
        "if_expression_point_3 :"

        goto_t = self.__if_expression_goto_t.pop()
        self.__quadruples[goto_t][3] = len(self.__quadruples)

    def p_if_expression_without_else_point_2(self, p):
        "if_expression_without_else_point_2 :"

        goto_f = self.__if_expression_goto_f.pop()
        self.__quadruples[goto_f][3] = len(self.__quadruples)

    def p_type(self, p):
        """type : primitive_type
                | array_type"""

        p[0] = Type(p[1])

    def p_primitive_type(self, p):
        """primitive_type : BOOL
                          | I32
                          | F64
                          | CHAR"""

        p[0] = PrimitiveType(p[1])

    def p_array_type(self, p):
        """array_type : '['             primitive_type                 ';' INTEGER_LITERAL ']'
                      | '[' '[' primitive_type ';' INTEGER_LITERAL ']' ';' INTEGER_LITERAL ']'"""

        if len(p) == 6:
            p[0] = ArrayType(Type(p[2]), p[4])
        else:
            p[0] = ArrayType(Type(ArrayType(Type(p[3]), p[5])), p[8])

    def p_empty(self, p):
        'empty :'
        p[0] = None

    def p_error(self, p):
        print("Syntax error in input!")
        print(f"Illegal token {p} at line {self.lexer.lexer.lineno}")
        sys.exit(1)

    def __init__(self, lexer, dir_func: DirFunc, semantic_cube: SemanticCube, quadruples, **kwargs):
        self.lexer = lexer
        self.__dir_func = dir_func
        self.__semantic_cube = semantic_cube
        self.__temp_function_identifier = None
        self.__quadruples = quadruples
        self.__temp_var_generator = TemporaryVariableGenerator()
        self.__infinite_loop_expression_start = []
        self.__predicate_loop_expression_start = []
        self.__predicate_loop_expression_goto_f = []
        self.__if_expression_goto_f = []
        self.__if_expression_goto_t = []
        self.__function_start_temporary_variable_count = None
        self.parser = yacc.yacc(module=self, **kwargs)

    def restart(self):
        self.parser.restart()

    def test(self, data: str) -> Crate:
        """
        Parses an input string and returns the abstract syntax tree.

        Panics if it encounters an error. Writes to stdout an error message
        befor exiting.

        :param data: The input to parse.
        :type data: str
        :return: The abstract syntax tree.
        :rtype: Crate
        """

        return self.parser.parse(data, lexer=self.lexer.lexer)
