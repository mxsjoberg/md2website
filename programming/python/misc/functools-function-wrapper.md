# Functools Function Wrapper

*August 2023* [Python](programming.html#python) [Misc](programming.html#python-misc)

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