from lexer import Lexer
from parser import Parser
from compiler import Compiler

l = Lexer()
p = Parser(l)
c = Compiler(p)
result = c.test("")
print(result.to_string())
