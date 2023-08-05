# Hello C

*November 2020* [C](programming.html#c) [Misc](programming.html#c-misc)

```cpp
#include <stdio.h>

int main(void) {
    printf("Hello C\n");

    return 0;
}
```

```cpp
#include <stdio.h>

int main(int argc, char *argv[]) {
    // print file name
    printf("Running: %s\n", argv[0]);
    // print arguments
    if (argc > 1) {
        printf("%s\n", "Arguments: ");
        
        int i;
        for (i = 1; i < argc; i++) {
            printf("\t%s\n", argv[i]);
        }
    }

    return 0;
}
```