# Hello C++

<mark>November 2020</mark>

```cpp
#include <iostream>

int main() {
    std::cout << "hello c++" << std::endl;

    return 0;
}
```

```cpp
#include <iostream>

int main(int argc, char** argv) {
    // print file name
    std::cout << "Running: " << argv[0] << std::endl;
    // print arguments
    if (argc > 1) {
        std::cout << "Arguments: " << std::endl;
        for (int i = 1; i < argc; i++) {
            std::cout << argv[i] << std::endl;
        }
    }
    return 0;
}
```