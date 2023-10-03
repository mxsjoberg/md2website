# Macros in C

<mark>August 2019</mark>

```cpp
// built-in macros
printf("%s\n", __FILE__);
// filename.c
printf("%s\n", __DATE__);
// Aug 21 2019
printf("%s\n", __TIME__);
// 01:22:18
printf("%d\n", __LINE__);
// 16
printf("%d\n", __STDC__);
// 1
```

```cpp
// stringize error message
#define  error_message(e) \
   printf("Error: " #e "\n")

error_message("This is an error.");
// Error: This is an error.

// if not defined
#if !defined (MESSAGE)
   #define MESSAGE "This is a message."
#endif

printf("%s\n", MESSAGE);
// This is a message.

// parameterized macros
#define square(x) ((x) * (x))
#define MAX(a,b) ((a) > (b) ? (a) : (b))

printf("%d\n", square(2));
// 4
printf("%d\n", MAX(4,5));
// 5
```