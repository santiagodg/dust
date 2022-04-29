import copy
import sys

from .ply import yacc

from .lexer import Lexer
from .dust_ast import *

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
            raise SyntaxError
    
    def p_function(self, p):
        """function : FN IDENTIFIER function_check_id '(' function_parameters ')' function_return_type function_add_return_type let_statements block_expression
                    | FN IDENTIFIER function_check_id '(' function_parameters ')'        empty         function_add_return_type let_statements block_expression"""
        
        self.__temp_function_identifier = None
        p[0] = Function(p[2], p[5], p[7], p[9], p[10])
    
    def p_function_add_return_type(self, p):
        "function_add_return_type :"
        self.__dir_func.add_function_return_type(self.__temp_function_identifier, p[-1])
    
    def p_function_check_id(self, p):
        "function_check_id : "

        if self.__dir_func.exists(p[-1]):
            print(f"Multiple declaration: function '{p[-1].identifier()}' in line {self.lexer.lexer.lineno}")
            sys.exit(1)
        
        self.__temp_function_identifier = p[-1]
        self.__dir_func.add_function_identifier(self.__temp_function_identifier)
    
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
        self.__dir_func.add_function_parameter(self.__temp_function_identifier, function_parameter)
        p[0] = function_parameter
    
    def p_function_param_check_id(self, p):
        "function_param_check_id :"
        id_exists = self.__dir_func.exists_in_var_tables(self.__temp_function_identifier, p[-1])

        if id_exists:
            print(f"Multiple declaration: local identifier '{p[-1].identifier()}' in function '{self.__temp_function_identifier.identifier()}' in line {self.lexer.lexer.lineno}")
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
        self.__dir_func.add_function_let_statement(self.__temp_function_identifier, let_statement)
        p[0] = let_statement
    
    def p_let_statement_check_id(self, p):
        "let_statement_check_id :"
        id_exists = self.__dir_func.exists_in_var_tables(self.__temp_function_identifier, p[-1])

        if id_exists:
            print(f"Multiple declaration: local identifier '{p[-1].identifier()}' in function '{self.__temp_function_identifier.identifier()}' in line {self.lexer.lexer.lineno}")
            sys.exit(1)
    
    def p_expression(self, p):
        """expression : expression_without_block
                      | expression_with_block"""
        
        p[0] = Expression(p[1])
    
    def p_expression_error(self, p):
        """expression : error"""
        print(f"Syntax error in expression. Bad subexpression on lines {p.linespan(1)[0]}-{p.linespan(1)[1]}")
    
    def p_expression_without_block(self, p):
        """expression_without_block : literal_expression
                                    | IDENTIFIER
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
        print(f"Syntax error in literal expression. Bad literal on lines {p.linespan(1)[0]}-{p.linespan(1)[1]}")
    
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
        
        p[0] = NegationExpression(p[1], p[2])
    
    def p_arithmetic_expression(self, p):
        """arithmetic_expression : expression '+' expression
                                 | expression '-' expression
                                 | expression '*' expression
                                 | expression '/' expression
                                 | expression '%' expression"""
        
        p[0] = ArithmeticExpression(p[1], p[2], p[3])
    
    def p_comparison_expression(self, p):
        """comparison_expression : expression EQ expression
                                 | expression NE expression
                                 | expression '>' expression
                                 | expression '<' expression
                                 | expression GE expression
                                 | expression LE expression"""
        
        p[0] = ComparisonExpression(p[1], p[2], p[3])
    
    def p_boolean_expression(self, p):
        """boolean_expression : expression OR expression
                              | expression AND expression"""
        
        p[0] = BooleanExpression(p[1], p[2], p[3])
    
    def p_type_cast_expression(self, p):
        "type_cast_expression : expression AS type"
        p[0] = TypeCastExpression(p[1], p[3])
    
    def p_assignment_expression(self, p):
        "assignment_expression : expression '=' expression"
        p[0] = AssignmentExpression(p[1], p[3])
    
    def p_grouped_expression(self, p):
        "grouped_expression : '(' expression ')'"
        p[0] = GroupedExpression(p[2])
    
    def p_array_expression_not_empty(self, p):
        """array_expression : '[' array_elements_literal ']'
                            | '[' array_elements_repeat ']'"""
        p[0] = ArrayExpression(p[2])
    
    def p_array_expression_empty(self, p):
        "array_expression : '[' empty ']'"
        p[0] = ArrayExpression([])
    
    def p_array_elements_literal(self, p):
        """array_elements_literal : array_elements_literal ',' expression
                                  | expression"""
        
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
    
    def p_array_elements_repeat(self, p):
        "array_elements_repeat : expression ';' INTEGER_LITERAL"
        length = p[3].value()
        result = []

        for _ in range(length):
            result += [copy.deepcopy(p[1])]
        
        p[0] = result
    
    def p_index_expression(self, p):
        "index_expression : expression '[' expression ']'"
        p[0] = IndexExpression(p[1], p[3])
    
    def p_call_expression(self, p):
        """call_expression : IDENTIFIER '(' call_params ',' ')'
                           | IDENTIFIER '(' call_params empty ')'"""
        
        p[0] = CallExpression(p[1], p[3])
    
    def p_call_expression_empty(self, p):
        "call_expression : IDENTIFIER '(' empty ')'"
        p[0] = CallExpression(p[1], [])
    
    def p_call_params(self, p):
        """call_params : call_params ',' expression
                       | expression"""
        
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
    
    def p_continue_expression(self, p):
        "continue_expression : CONTINUE"
        p[0] = ContinueExpression()
    
    def p_break_expression(self, p):
        "break_expression : BREAK"
        p[0] = BreakExpression()

    def p_return_expression(self, p):
        "return_expression : RETURN expression"
        p[0] = ReturnExpression(p[2])

    def p_return_expression_empty(self, p):
        "return_expression : RETURN empty"
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
        
        p[0] = ReadExpression(p[3])

    def p_write_expression(self, p):
        "write_expression : WRITE '(' expression ')'"
        p[0] = WriteExpression(p[3])
    
    def p_write_expression_error(self, p):
        "write_expression : WRITE '(' error ')'"
        print(f"Syntax error in write expression. Bad expression on lines {p.linespan(3)[0]}-{p.linespan(3)[1]}")
    
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
        p[0] = PlotExpression(p[3], p[5])
    
    def p_scatter_expression(self, p):
        "scatter_expression : SCATTER '(' expression ',' expression ')'"
        p[0] = ScatterExpression(p[3], p[5])
    
    def p_histogram_expression(self, p):
        "histogram_expression : HISTOGRAM '(' expression ')'"
        p[0] = HistogramExpression(p[3])
    
    def p_mean_expression(self, p):
        "mean_expression : MEAN '(' expression ')'"
        p[0] = MeanExpression(p[3])
    
    def p_median_expression(self, p):
        "median_expression : MEDIAN '(' expression ')'"
        p[0] = MedianExpression(p[3])
    
    def p_mean_square_expression(self, p):
        "mean_square_error_expression : MEAN_SQUARE_ERROR '(' expression ')'"
        p[0] = MeanSquareErrorExpression(p[3])
    
    def p_min_expression(self, p):
        "min_expression : MIN '(' expression ')'"
        p[0] = MinExpression(p[3])
    
    def p_max_expression(self, p):
        "max_expression : MAX '(' expression ')'"
        p[0] = MaxExpression(p[3])
    
    def p_standard_deviation_expression(self, p):
        "standard_deviation_expression : STANDARD_DEVIATION '(' expression ')'"
        p[0] = StandardDeviationExpression(p[3])
    
    def p_variance_expression(self, p):
        "variance_expression : VARIANCE '(' expression ')'"
        p[0] = VarianceExpression(p[3])
    
    def p_skewness_expression(self, p):
        "skewness_expression : SKEWNESS '(' expression ')'"
        p[0] = SkewnessExpression(p[3])
    
    def p_kurtosis_expression(self, p):
        "kurtosis_expression : KURTOSIS '(' expression ')'"
        p[0] = KurtosisExpression(p[3])
    
    def p_r_squared_expression(self, p):
        "r_squared_expression : R_SQUARED '(' expression ',' expression ')'"
        p[0] = RSquaredExpression(p[3], p[5])
    
    def p_sum_expression(self, p):
        "sum_expression : SUM '(' expression ')'"
        p[0] = SumExpression(p[3])
    
    def p_loop_expression(self, p):
        """loop_expression : infinite_loop_expression
                           | predicate_loop_expression"""
        
        p[0] = LoopExpression(p[1])
    
    def p_infinite_loop_expression(self, p):
        "infinite_loop_expression : LOOP block_expression"
        p[0] = InfiniteLoopExpression(p[2])
    
    def p_predicate_loop_expression(self, p):
        "predicate_loop_expression : WHILE expression block_expression"
        p[0] = PredicateLoopExpression(p[2], p[3])
    
    def p_if_expression(self, p):
        """if_expression : IF expression block_expression ELSE block_expression"""
        p[0] = IfExpression(p[2], p[3], p[5])
    
    def p_if_expression_without_else(self, p):
        """if_expression : IF expression block_expression"""
        p[0] = IfExpression(p[2], p[3], None)

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
    
    def __init__(self, lexer, dir_func, **kwargs):
        self.lexer = lexer
        self.__dir_func = dir_func
        self.__temp_function_identifier = None
        self.parser = yacc.yacc(module=self, **kwargs)
    
    def test(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)
