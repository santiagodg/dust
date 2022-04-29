from compiler import Lexer, Parser, Compiler, DirFunc

l = Lexer()
dir_func = DirFunc()
p = Parser(l, dir_func)
c = Compiler(p)

result = c.test(
"""
static global_1: bool;

fn main()
let local_1: i32;
let local_2: i32;
{
    global_1 = true;
    local_1 = 2;
    local_2 = 3;

    if id1 {
        local_1 = local_1 + local_2;
    } else {
        local_1 = local_1 - local_2;
    };

    write(local_2);
}
""")

print(result.to_string())
print(dir_func)
