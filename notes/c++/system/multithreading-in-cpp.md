# Multithreading in C++

<mark>November 2020</mark>

```cpp
#include <iostream>
#include <pthread.h>

#define NUMBER_OF_THREADS 5

void* print(void* thread_id) {
    long tid;
    tid = (long) thread_id;
    
    std::cout << "hello multithreading, thread: " << tid << std::endl;
    
    // terminate
    pthread_exit(NULL);
};

int main() {
    pthread_t threads[NUMBER_OF_THREADS];

    int rc;
    for (int i = 0; i < NUMBER_OF_THREADS; i++) {
        std::cout << "creating thread: " << i << std::endl;
        
        // create thread
        rc = pthread_create(&threads[i], NULL, print, (void*) i);
        if (rc) {
            std::cout << "unable to create thread: " << rc << std::endl;
            exit(-1);
        }
    }

    // terminate
    pthread_exit(NULL);
    // creating thread: 0
    // creating thread: 1
    // hello multithreading, thread: 0
    // creating thread: 2
    // hello multithreading, thread: 1
    // creating thread: 3
    // hello multithreading, thread: 2
    // creating thread: 4
    // hello multithreading, thread: 3
    // hello multithreading, thread: 4
}
```