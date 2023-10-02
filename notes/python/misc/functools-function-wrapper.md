# Functools Function Wrapper

*August 2023* [Python](programming.html#python) [Misc](programming.html#python-misc)

Function wrappers are used to modify the behavior of a function or method. The `wraps` decorator copies over the function name, docstring, and arguments list to the wrapper function. This is particularly useful for debugging and logging.

```python
from functools import wraps

def logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"call to {func.__name__}, args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@logging
def power(base, exp): return base ** exp

power(2, 3)
# call to power, args: (2, 3), kwargs: {}
```