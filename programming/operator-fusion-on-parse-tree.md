# Operator Fusion on Parse Tree

*July 2023* [Python](programming.html#python) [Compilers](programming.html#compilers)

Operator fusion is a technique to combine or rearrange consecutive operations in a parse tree to improve efficiency of code execution. It is a common optimization technique used in compilers.

```python
def simplify_parse_tree(tree):
    if (isinstance(tree, tuple)):
        # first value in tuple, remaining values in tuple
        operator, *operands = tree
        operands = [simplify_parse_tree(operand) for operand in operands]

        if all(isinstance(operand, int) for operand in operands):
            if operator == '+':
                return sum(operands)
            elif operator == '*':
                return eval('*'.join(map(str, operands)))

    return tree
```

```python
# (1 + 2) * (3 + 4)
parse_tree = ('*', ('+', 1, 2), ('+', 3, 4))
print(simplify_parse_tree(parse_tree))
# 21

compiled = compile('(1 + 2) * (3 + 4)', '<string>', 'eval')
print(compiled.co_consts[0])
# 21
```

```python
assert simplify_parse_tree(parse_tree) == compiled.co_consts[0]
```
