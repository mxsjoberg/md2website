# DSL in Python

*August 2023* [Python](programming.html#python) [Misc](programming.html#python-misc)

```python
import sys

# Module definition
class Module:
    def add(*args, **kwargs):
        type_ = globals()['__builtins__'].getattr(globals()['__builtins__'], kwargs['type'])
        return sum(map(type_, args))

# simple domain-specific language to add 1, 2, 3 and return result as float
program = "Module add 1 2 3 type=float"

tokens = program.split()
# print(tokens)
# ['Module', 'add', '1', '2', '3', 'type=float']

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

args, kwargs = get_args(tokens[2:])
```

```python
# print(args, kwargs)
# ['1', '2', '3'] {'type': 'float'}

# print(getattr(sys.modules[__name__], tokens[0]))
# <class '__main__.Module'>

# print(getattr(getattr(sys.modules[__name__], tokens[0]), tokens[1]))
# <function Module.add at 0x1024545e0>

result = getattr(getattr(sys.modules[__name__], tokens[0]), tokens[1])(*args, **kwargs)
print(result)
# 6.0
```