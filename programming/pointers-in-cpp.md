# Pointers in C++

*November 2020* [C++](programming.html#c++) [Misc](programming.html#c++-misc)

```cpp
int a = 5;

// memory address of a
std::cout << &a << std::endl;
// 0x7ffee707c75c

// pointer store address of a
int* ptr = &a;

// reference -> output is address
std::cout << ptr << std::endl;
// 0x7ffee707c75c

// dereference -> output is value at address
std::cout << *ptr << std::endl;
// 5

// null pointer
int* np = NULL;

std::cout << np << std::endl;
// 0x0
```