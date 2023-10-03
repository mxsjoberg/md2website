# Linked List in C

<mark>August 2023</mark>

A linked list implementation in C.

```cpp
#include <stdio.h>
#include <stdlib.h>

// element
struct Element {
    int value;
    struct Element *next;
};

// allocate memory for an element
struct Element *create_element(int value) {
    struct Element *element = (struct Element*)malloc(sizeof(struct Element));
    element->value = value;
    element->next = NULL;
    return element;
}
```

Operations on this linked list are `insert`, `remove`, and `print`.

```cpp
// insert
void ll_insert(struct Element **element, int value) {
    struct Element *new_element = create_element(value);
    // if the list is empty
    if (*element == NULL) {
        *element = new_element;
    }
    // if the list is not empty
    else {
        struct Element *current = *element;
        // iterate until last element
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = new_element;
    }
}
// remove
void ll_remove(struct Element **element, int value) {
    struct Element *current = *element;
    struct Element *previous = NULL;
    // iterate until last element
    while (current != NULL) {
        // if value is found
        if (current->value == value) {
            // if value is first element
            if (previous == NULL) {
                *element = current->next;
            }
            // if value is not first element
            else {
                previous->next = current->next;
            }
            // free memory
            free(current);
            return;
        }
        previous = current;
        current = current->next;
    }
}
// print
void print(struct Element *element) {
    struct Element *current = element;
    // iterate until last element
    while (current != NULL) {
        printf("%d\n", current->value);
        current = current->next;
    }
    printf("NULL\n");
}
```

```cpp
int main() {
    struct Element *ll = NULL;
    
    ll_insert(&ll, 5);
    ll_insert(&ll, 10);
    ll_insert(&ll, 15);
    ll_insert(&ll, 20);
    ll_insert(&ll, 25);
    ll_insert(&ll, 30);
    
    print(ll);
    // 5
    // 10
    // 15
    // 20
    // 25
    // 30
    // NULL

    ll_remove(&ll, 15);
    ll_remove(&ll, 30);

    print(ll);
    // 5
    // 10
    // 20
    // 25
    // NULL
}
```