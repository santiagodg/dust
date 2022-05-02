from compiler import Lexer, Parser, Compiler, DirFunc, SemanticCube

l = Lexer()
dir_func = DirFunc()
semantic_cube = SemanticCube()
p = Parser(l, dir_func, semantic_cube)
c = Compiler(p, dir_func, semantic_cube)

result = c.test(
"""
static global_1: bool;

fn main()
let local_1: i32;
let local_2: i32;
let local_char: char;
{
    global_1 = true;
    local_1 = 2;
    local_2 = 3;
    local_char = 'a';

    if global_1 {
        local_1 = local_1 + local_2;
    } else {
        local_1 = local_1 - local_2;
    };

    write(local_char);
}
""")

print()
print(result)
print()
print(dir_func)
