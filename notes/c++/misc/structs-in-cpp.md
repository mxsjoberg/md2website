# Structs in C++

<mark>November 2020</mark>

```cpp
struct my_struct {
    int x;
    int y;
};

// or
typedef struct {
	int x;
	int y;
} my_struct;

struct my_struct A;
struct my_struct B;

// assign values to A
A.x = 2;
A.y = 7;

// assign values to B
B.x = -4;
B.y = 12;

cout << A.x << "," << A.y << endl;
// 2,7
cout << B.x << "," << B.y << endl;
// -4,12
```