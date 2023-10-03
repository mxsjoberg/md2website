# Exceptions in C++

<mark>November 2020</mark>

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