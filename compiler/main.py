import lexer
import parser

l = lexer.Lexer()
l.build()

p = parser.Parser()
p.build(l.lexer)

result = p.test("fn main() { }")
print(result)
