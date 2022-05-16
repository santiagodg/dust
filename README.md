# Dust

A less-featured Rust-like language.

# Usage

There are some sample Dust files in the compiler/test_files directory.

## Examples:

Compile a file.

```
cd compiler
python3 main.py test_files/normal.ds
```

Compile from stdin. Enter Ctrl+Z on Windows or Ctrl+D on Mac and Linux to enter EOF and start compilation.

```
cd compiler
python3 main.py -
fn main
let character: char;
{
    character = 'a';
    write(character);
}
```
