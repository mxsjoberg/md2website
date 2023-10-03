# Bubble Sort in C++

*November 2020* [C++](programming.html#c++) [Misc](programming.html#c++-misc)

```cpp
int numbers[] = { 14, 33, 27, 35, 10 };
for (int i = 0; i < sizeof(numbers) / sizeof(int); i++) {
    for (int j = 0; j < sizeof(numbers) / sizeof(int); j++) {
        if (numbers[j] > numbers[j + 1]) {
            int temp = numbers[j];
            // swap
            numbers[j] = numbers[j + 1];
            numbers[j + 1] = temp;
        }
    }
}
// print sorted
for (int i = 0; i < sizeof(numbers) / sizeof(int); i++) {
    std::cout << numbers[i] << std::endl;
}
// 10
// 14
// 27
// 33
// 35
```