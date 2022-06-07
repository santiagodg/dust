# Dust

A less-featured Rust-like language.

# Usage

There are some sample Dust files in the compiler/test_files directory.

## Examples:

Compile a file.

```
cd compiler
py compile.py test_files/final/matrix_multiplication.ds matrix_multiplication.dso
```

Execute object file.

```
py execute.py matrix_multiplication.dso
```
