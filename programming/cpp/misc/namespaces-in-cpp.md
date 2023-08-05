# Namespaces in C++

*November 2020* [C++](programming.html#c++) [Misc](programming.html#c++-misc)

```cpp
namespace my_namespace {
    void my_function() {
        std::cout << "my_namespace::my_function" << std::endl;
    }
}
```

```cpp
my_namespace::my_function();
// my_namespace::my_function

using namespace my_namespace;
my_function();
// my_namespace::my_function
```