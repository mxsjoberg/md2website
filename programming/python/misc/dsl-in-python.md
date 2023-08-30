# DSL in Python

*August 2023* [Python](programming.html#python) [Misc](programming.html#python-misc)

```python
import sys

# Module definition
class Module:
    # Add function
    def add(*args, **kwargs):
        type_ = globals()['__builtins__'].getattr(globals()['__builtins__'], kwargs['type'])
        return sum(map(type_, args))
    # Sub function
    def sub(*args, **kwargs):
        type_ = globals()['__builtins__'].getattr(globals()['__builtins__'], kwargs['type'])
        return float(args[0]) if type_ == 'float' else int(args[0]) - sum(map(type_, args[1:]))

# simple domain-specific language
#   add: sum all arguments
#   sub: subtract tail from head
program = """
Module add 1 2 3 type=float
Module sub 4 1 2 type=float
"""

lines = [line for line in program.splitlines() if line]
# print(lines)
# ['Module add 1 2 3 type=float', 'Module sub 4 1 2 type=float']

def get_args(tokens):
    args = []
    kwargs = {}
    for token in tokens:
        # kwargs
        if '=' in token:
            k, v = token.split('=', 1)
            kwargs[k] = v
        # args
        else:
            args.append(token)
    return args, kwargs

for line in lines:
    tokens = line.split()
    # print(tokens)
    # ['Module', 'add', '1', '2', '3', 'type=float']

    args, kwargs = get_args(tokens[2:])

    # print(args, kwargs)
    # ['1', '2', '3'] {'type': 'float'}

    # print(getattr(sys.modules[__name__], tokens[0]))
    # <class '__main__.Module'>

    # print(getattr(getattr(sys.modules[__name__], tokens[0]), tokens[1]))
    # <function Module.add at 0x1024545e0>

    result = getattr(getattr(sys.modules[__name__], tokens[0]), tokens[1])(*args, **kwargs)
    print(result)
    # 6.0
    # 1.0
```