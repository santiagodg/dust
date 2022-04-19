import ply.yacc as yacc

import lexer
from dust_ast import Crate, Item, StaticItem, Function, FunctionParameter, LetStatement, BlockExpression, Type

class Parser():
    tokens = lexer.Lexer().tokens

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
        "static_item : STATIC IDENTIFIER ':' type ';'"
        p[0] = StaticItem(p[2], p[4])
    
    def p_function(self, p):
        """function : FN IDENTIFIER '(' function_parameters ')' function_return_type let_statements block_expression
                    | FN IDENTIFIER '(' function_parameters ')'        empty         let_statements block_expression"""
        p[0] = Function(p[2], p[4], p[6], p[7], p[8])
    
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
        "function_param : IDENTIFIER ':' type"
        p[0] = FunctionParameter('function_param', p[1], p[3])
    
    def p_function_return_type(self, p):
        "function_return_type : RIGHT_ARROW type"
        p[0] = Type(p[2])

    def p_statements(self, p):
        """statements : statements statement
                      | empty"""
        
        if len(p) == 2:
            p[0] = ('statements', [])
        else:
            p[0] = ('statements', p[1][1] + [p[2]])

    def p_statement(self, p):
        "statement : expression ';'"
        p[0] = ('statement', p[1])
    
    def p_let_stataments(self, p):
        """let_statements : let_statements let_statement
                        | empty"""
        
        if len(p) == 2:
            p[0] = []
        else:
            p[0] = p[1] + [p[2]]

    def p_let_statament(self, p):
        "let_statement : LET IDENTIFIER ':' type ';'"
        p[0] = LetStatement('let_statement', p[2], p[4])
    
    def p_expression(self, p):
        """expression : expression_without_block
                      | expression_with_block"""
        
        p[0] = ('expression', p[1])
    
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
        
        p[0] = ('expression_without_block', p[1])
    
    def p_expression_with_block(self, p):
        """expression_with_block : loop_expression
                                 | if_expression"""
        
        p[0] = ('expression_with_block', p[1])
    
    def p_literal_expression(self, p):
        """literal_expression : CHAR_LITERAL
                              | INTEGER_LITERAL
                              | FLOAT_LITERAL
                              | BOOL_LITERAL"""
        
        p[0] = ('literal_expression', p[1])
    
    def p_block_expression(self, p):
        "block_expression : '{' statements '}'"
        p[0] = BlockExpression(('block_expression', p[2]))
    
    def p_operator_expression(self, p):
        """operator_expression : negation_expression
                               | arithmetic_expression
                               | comparison_expression
                               | boolean_expression
                               | type_cast_expression
                               | assignment_expression"""
        
        p[0] = ('operator_expression', p[1])
    
    def p_negation_expression(self, p):
        """negation_expression : '-' expression %prec UMINUS
                               | '!' expression"""
        
        p[0] = ('negation_expression', p[1], p[2])
    
    def p_arithmetic_expression(self, p):
        """arithmetic_expression : expression '+' expression
                                 | expression '-' expression
                                 | expression '*' expression
                                 | expression '/' expression
                                 | expression '%' expression"""
        
        p[0] = ('arithmetic_expression', p[1], p[2], p[3])
    
    def p_comparison_expression(self, p):
        """comparison_expression : expression EQ expression
                                 | expression NE expression
                                 | expression '>' expression
                                 | expression '<' expression
                                 | expression GE expression
                                 | expression LE expression"""
        
        p[0] = ('comparison_expression', p[1], p[2], p[3])
    
    def p_boolean_expression(self, p):
        """boolean_expression : expression OR expression
                              | expression AND expression"""
        
        p[0] = ('boolean_expression', p[1], p[2], p[3])
    
    def p_type_cast_expression(self, p):
        "type_cast_expression : expression AS type"
        p[0] = ('type_cast_expression', p[1], p[3])
    
    def p_assignment_expression(self, p):
        "assignment_expression : expression '=' expression"
        p[0] = ('assignment_expression', p[1], p[3])
    
    def p_grouped_expression(self, p):
        "grouped_expression : '(' expression ')'"
        p[0] = ('grouped_expression', p[2])
    
    def p_array_expression(self, p):
        """array_expression : '[' array_elements_literal ']'
                            | '[' array_elements_repeat ']'
                            | '[' empty ']'"""
        p[0] = ('array_expression', p[2])
    
    def p_array_elements_literal(self, p):
        """array_elements_literal : array_elements_literal ',' expression
                                  | expression"""
        
        if len(p) == 2:
            p[0] = ('array_elements_literal', [p[1]])
        else:
            p[0] = ('array_elements_literal', p[1][1] + [p[3]])
    
    def p_array_elements_repeat(self, p):
        "array_elements_repeat : expression ';' INTEGER_LITERAL"
        p[0] = ('array_elements_repeat', p[1], p[3])
    
    def p_index_expression(self, p):
        "index_expression : expression '[' expression ']'"
        p[0] = ('index_expression', p[1], p[3])
    
    def p_call_expression(self, p):
        """call_expression : IDENTIFIER '(' call_params ',' ')'
                           | IDENTIFIER '(' call_params empty ')'
                           | IDENTIFIER '(' empty ')'"""
        
        p[0] = ('call_expression', p[1], p[3])
    
    def p_call_params(self, p):
        """call_params : call_params ',' expression
                       | expression"""
        
        if len(p) == 2:
            p[0] = ('call_params', [p[1]])
        else:
            p[0] = ('call_params', p[1][1] + [p[3]])
    
    def p_continue_expression(self, p):
        "continue_expression : CONTINUE"
        p[0] = ('continue_expression')
    
    def p_break_expression(self, p):
        "break_expression : BREAK"
        p[0] = ('break_expression')

    def p_return_expression(self, p):
        """return_expression : RETURN expression
                             | RETURN empty"""
        
        p[0] = ('return_expression', p[2])
    
    def p_special_function_expression(self, p):
        """special_function_expression : io_expression
                                       | statistic_expression"""
        
        p[0] = ('special_function_expression', p[1])
    
    def p_io_expression(self, p):
        """io_expression : read_expression
                         | write_expression"""
        
        p[0] = ('io_expression', p[1])
    
    def p_read_expression(self, p):
        """read_expression : READ '(' IDENTIFIER ')'
                           | READ '(' index_expression ')'"""
        
        p[0] = ('read_expression', p[3])

    def p_write_expression(self, p):
        "write_expression : WRITE '(' expression ')'"
        p[0] = ('write_expression', p[3])
    
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
        
        p[0] = ('statistic_expression', p[1])
    
    def p_plot_expression(self, p):
        "plot_expression : PLOT '(' expression ',' expression ')'"
        p[0] = ('plot_expression', p[3], p[5])
    
    def p_scatter_expression(self, p):
        "scatter_expression : SCATTER '(' expression ',' expression ')'"
        p[0] = ('scatter_expression', p[3], p[5])
    
    def p_histogram_expression(self, p):
        "histogram_expression : HISTOGRAM '(' expression ')'"
        p[0] = ('histogram_expression', p[3])
    
    def p_mean_expression(self, p):
        "mean_expression : MEAN '(' expression ')'"
        p[0] = ('mean_expression', p[3])
    
    def p_median_expression(self, p):
        "median_expression : MEDIAN '(' expression ')'"
        p[0] = ('median_expression', p[3])
    
    def p_mean_square_expression(self, p):
        "mean_square_error_expression : MEAN_SQUARE_ERROR '(' expression ')'"
        p[0] = ('mean_square_error_expression', p[3])
    
    def p_min_expression(self, p):
        "min_expression : MIN '(' expression ')'"
        p[0] = ('min_expression', p[3])
    
    def p_max_expression(self, p):
        "max_expression : MAX '(' expression ')'"
        p[0] = ('max_expression', p[3])
    
    def p_standard_deviation_expression(self, p):
        "standard_deviation_expression : STANDARD_DEVIATION '(' expression ')'"
        p[0] = ('standard_deviation_expression', p[3])
    
    def p_variance_expression(self, p):
        "variance_expression : VARIANCE '(' expression ')'"
        p[0] = ('variance_expression', p[3])
    
    def p_skewness_expression(self, p):
        "skewness_expression : SKEWNESS '(' expression ')'"
        p[0] = ('skewness_expression', p[3])
    
    def p_kurtosis_expression(self, p):
        "kurtosis_expression : KURTOSIS '(' expression ')'"
        p[0] = ('kurtosis_expression', p[3])
    
    def p_r_squared_expression(self, p):
        "r_squared_expression : R_SQUARED '(' expression ',' expression ')'"
        p[0] = ('r_squared_expression', p[3], p[5])
    
    def p_sum_expression(self, p):
        "sum_expression : SUM '(' expression ')'"
        p[0] = ('sum_expression', p[3])
    
    def p_loop_expression(self, p):
        """loop_expression : infinite_loop_expression
                           | predicate_loop_expression"""
        
        p[0] = ('loop_expression', p[1])
    
    def p_infinite_loop_expression(self, p):
        "infinite_loop_expression : LOOP block_expression"
        p[0] = ('infinite_loop_expression', p[2])
    
    def p_predicate_loop_expression(self, p):
        "predicate_loop_expression : WHILE expression block_expression"
        p[0] = ('predicate_loop_expression', p[2], p[3])
    
    def p_if_expression(self, p):
        """if_expression : IF expression block_expression empty empty
                         | IF expression block_expression ELSE block_expression"""
        
        p[0] = ('if_expression', p[2], p[3], p[5])
    
    def p_type(self, p):
        """type : primitive_type
                | array_type"""
        
        p[0] = Type(('type', p[1]))
    
    def p_primitive_type(self, p):
        """primitive_type : BOOL
                          | I32
                          | F64
                          | CHAR"""
        
        p[0] = ('primitive_type', p[1])
    
    def p_array_type(self, p):
        """array_type : '['             primitive_type                 ';' INTEGER_LITERAL ']'
                      | '[' '[' primitive_type ';' INTEGER_LITERAL ']' ';' INTEGER_LITERAL ']'"""
        
        if len(p) == 6:
            p[0] = ('array_type', p[2], p[4])
        else:
            p[0] = ('array_type', ('array_type', p[3], p[5]), p[8])

    def p_empty(self, p):
        'empty :'
        p[0] = None
    
    def p_error(self, p):
        print("Syntax error in input!")
        print(p)
    
    def __init__(self, lexer, **kwargs):
        self.lexer = lexer
        self.parser = yacc.yacc(module=self, **kwargs)
    
    def test(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

