# Vectors in C++

*November 2020* [C++](programming.html#c++) [Misc](programming.html#c++-misc)

```cpp
#include <iostream>
#include <vector>

// vector to store integers
vector<int> vec;

// size of vector
std::cout << vec.size() << std::endl;
// 0

// push values to vector
for (int i = 1; i <= 5; i++) {
    vec.push_back(i);
}

// size of vector
std::cout << vec.size() << std::endl;
// 5

// access value
std::cout << vec[0] << std::endl;
// 1
```