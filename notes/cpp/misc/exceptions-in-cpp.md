# Exceptions in C++

*November 2020* [C++](programming.html#c++) [Misc](programming.html#c++-misc)

```cpp
#include <iostream>

int main() {
    try {
        throw 0;
    } catch (int error) {
        std::cout << "error: " << error << std::endl;
        // error: 0
    }
}
```