# Headers in C

*November 2020* [C](programming.html#c) [Misc](programming.html#c-misc)

```cpp
// program.h
const int number = 10;
```

```cpp
// program.c

#include "program.h"

printf("%d\n", number);
// 10
```