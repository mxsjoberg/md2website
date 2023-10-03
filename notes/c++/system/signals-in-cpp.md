# Signals in C++

<mark>November 2020</mark>

```cpp
#include <iostream>
#include <csignal>
#include <unistd.h>

// signal handler
void terminate(int s) {
   std::cout << "interrupt signal: " << s << std::endl;
   exit(s);  
}

int main() {
    // register signal
    signal(SIGINT, terminate);  
    // keyboard interrupt
    while(1) {
        std::cout << "working hard..." << std::endl;
        sleep(5);
    }
    // run then ctrl+c -> interrupt signal: 2
}
```