from compiler import Lexer, Parser, Compiler, DirFunc, SemanticCube, pretty_print_quadruples

l = Lexer()
dir_func = DirFunc()
semantic_cube = SemanticCube()
quadruples = []
p = Parser(l, dir_func, semantic_cube, quadruples)
c = Compiler(p, dir_func, semantic_cube)

result = c.test(
"""
static global_1: bool;

fn main()
let local_1: i32;
let local_2: i32;
let local_char: char;
let local_arr: [f64; 2];
{
    global_1 = true;
    local_1 = 2;
    local_2 = 3;
    local_char = 'a';
    local_arr = [4.4; 2];

    if global_1 {
        local_1 = local_1 + local_2;
    } else {
        local_1 = local_1 - local_2;
    };

    write(local_char);
}
""")

# print()
# print(result)
# print()
# print(dir_func)

print()
pretty_print_quadruples(quadruples)
