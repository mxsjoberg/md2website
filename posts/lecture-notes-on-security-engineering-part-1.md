# Lecture notes on Security Engineering – Part 1: Introduction

*August 2022*

This is the first post in a series of lecture notes on security engineering, based on the postgraduate-level course with the same name at King's College London. These notes cover most of the topics, but not as deep and without assignments, and are primarily intended as a reference for myself.

- [Computer programs](#computer-programs)
    - [Compilation](#compilation)
    - [Tools](#tools)
- [Computer organisation](#computer-organisation)
    - [CPU](#cpu)
- [Cache memory](#cache-memory)
- [Operating system](#operating-system)
    - [Shell](#shell)
    - [System calls](#system-calls)
    - [Processes](#processes)
    - [Virtual memory](#virtual-memory)
    - [Files](#files)

## <a name="computer-programs" class="anchor"></a> [Computer programs](#computer-programs)

A computer program is a sequence of bits, and organized as 8-bit bytes, where one byte is 8-bits and each byte represent some text character (ASCII standard). Most programs are developed in a high-level programming language, then compiled, or translated, into an object file, which is executed by a process, and finally terminated.

An object file contains application and libraries, such as program code in binary format, relocation information, which are things that need to be fixed once loaded into memory, symbol information as defined by object or imported, and optional debugging information. Interpreted languages are typically translated into an intermediate format.

### <a name="compilation" class="anchor"></a> [Compilation](#compilation)


```c
/* hello.c */
#include <stdio.h>

int main() {
    printf("hello c\n");
    return 0;
}
```

The compilation system generally includes preprocessor, compiler, assembler, and linker, which are used in stages to translate some program into a sequence of machine-language instructions packed into an executable object file. The compilation process is often referred to as simply compilation, or compiler.

The compilation process (note that most program code in this post refer to programs written in the C programming language and using [gcc](https://linux.die.net/man/1/gcc) to compile):

- **preprocessor**, such as [cpp](https://linux.die.net/man/1/cpp), modifies the program according to directives that begin with `#`, in this case `#include <stdio.h>`, and are imported into the program text, resulting in an intermediate file with `.i` suffix, use flag `-E` to see intermediate file

- **compiler**, translates the intermediate file into an assembly program with `.s` suffix, where each line describe one instruction, use flag `-S` to generate assembly program (note that below assembly is generated on 64-bit mac, operand size suffix and special directives for assembler is omitted for clarity)

```x86asm
.section __TEXT
    .globl  _main

_main:
    push    %rbp
    mov     %rsp, %rbp
    sub     $16, %rsp
    mov     $0, -4(%rbp)
    lea     L_.str(%rip), %rdi
    mov     $0, %al
    call    _printf
    xor     %eax, %eax
    add     $16, %rsp
    pop     %rbp
    ret

.section __TEXT
    L_.str: .asciz  "hello c\n"
```

- **assembler**, such as [as](https://linux.die.net/man/1/as), translates assembly program instructions into machine-level instructions, use flag `-c` to compile assembly program, resulting in a relocatable object file with `.o` suffix (this is a binary file)

- **linker**, such as [ld](https://linux.die.net/man/1/ld), merges one or more relocatable object files, which are separate and precompiled `.o`-files that the program is using, such as `printf.o`, resulting in an executable file with no suffix, ready to be loaded into memory and executed by the system

A linker is used to resolve references to external objects, such as variables and functions (e.g. `printf`). Static linking is performed at compile-time and dynamic linking is performed at run-time.

### <a name="tools" class="anchor"></a> [Tools](#tools)

Useful tools for working with programs from a systems perspective:

- [gdp](https://www.sourceware.org/gdb/), GNU debugger
- `objdump` such as `objdump -d <filename>` to display information about object file (disassembler)
    -  `gcc hello.c && objdump -d hello` (alternative to `gcc -S` to see assembly)
- `readelf` to display information about ELF files, which is a standard file format for executable files
- `elfish` to manipulate ELF files
- `hexdump` to display content in binary file
- `/proc/pid/maps` to show memory layout for process

## <a name="computer-organisation" class="anchor"></a> [Computer organisation](#computer-organisation)

A modern computer is organized as an assemble of buses, I/O devices, main memory, and processor:

- buses are collections of electrical conduits that carry bytes between components, usually fixed sized and referred to as words, where the word size is 4 bytes (32 bits) or 8 bytes (64 bits)
- I/O devices are connections to the external world, such as keyboard, mouse, and display, but also disk drives, which is where executable files are stored
    - **controllers** are chip sets in the devices themselves or main circuit board (motherboard)
    - **adapters** are cards plugged into the motherboard

- main memory is a temporary storage device that holds program and data when executed by the processor, physically, it is a collection of dynamic random-access memory (DRAM) chips, and logically, it is a linear array of bytes with its own unique address (array index)
- processor, or central processing unit (CPU), is the engine that interprets and executes the machine-level instructions stored in the main memory

### <a name="cpu" class="anchor"></a> [CPU](#cpu)

The CPU has a word size storage device (register) called program counter (PC) that points at some instruction in main memory. Instructions are executed in a strict sequence, which is to read and interpret the instruction as pointed to by program counter, perform operation (as per the instruction), and then update the counter to point to next instruction (note that each instruction has its own unique address).

An operation, as performed by the CPU, use main memory, register file, which is a small storage device with collection of word-size registers, and the arithmetic logic unit (ALU) to compute new data and address values:

- **load**, copy byte (or word) from main memory into register, overwriting previous content in register
- **store**, copy byte (or word) from register to location in main memory, overwriting previous content in location
- **operate**, copy content of two registers to ALU, perform arithmetic operation on the two words and store result in register, overwriting previous content in register
- **jump**, extract word from instruction and copy that word into counter, overwriting previous value in counter

## <a name="cache-memory" class="anchor"></a> [Cache memory](#cache-memory)

A cache memory is memory devices at different levels of accessibility, or sizes, where smaller sizes are faster. The different levels of cache memory is typically used to make programs run faster.

|    |     |     |
| -- | :-- | :-- |
| L0 | Register | CPU register hold **words** copied from other cache levels |
| L1 | SRAM     | L1 hold cache **lines** copied from L2 |
| L2 | SRAM     | L2 hold cache **lines** copied from L3 |
| L3 | SRAM     | L3 hold cache **lines** copied from main memory |
| L4 | DRAM     | Main memory to hold disk **blocks** from local disks |
| L5 | Local secondary storage | Local disks hold **files** copied from other disks or remote network storage |
| L6 | Remote secondary storage |  |

The different levels of memory is also referred to as [memory hierarchy](https://en.wikipedia.org/wiki/Memory_hierarchy), and is often measured in response time. Each level act as cache memory for the level below, and top-most levels are reserved for information that the processor might need in the near future.

## <a name="operating-systems" class="anchor"></a> [Operating systems](#operating-systems)

An operating system provides services to programs. The services are used via abstractions to make it easier to manipulate low-level devices and protect the hardware.

### <a name="shell" class="anchor"></a> [Shell](#shell)

A shell provides an interface to the operating system via the command-line (or library functions):

- when opened, waiting for commands and read each character as it is typed into some register, which is then stored in memory
- load executable file, such as `./hello` (command to execute program `hello`), which basically copies the code and data in file from disk to main memory
- once loaded, the processor starts to execute the machine-language instructions in the `main` routine, which corresponds to the function `main` in program, copies the data from memory to register, and then from register to display device, which should output the string "hello assembly"

A shell command is a command-line program and `system()` is a library function to execute shell commands in C programs:

- sort files with `ls | sort`

```c
int main() {
    system("ls | sort");
    return 0;
}
```

- copy files with `cp`, such as `cp ~/file /dest` (note that `~` expands into `HOME` environment variable)

For more shell commands, see [List of Unix commands](https://en.wikipedia.org/wiki/List_of_Unix_commands).

### <a name="system-calls" class="anchor"></a> [System calls](#system-calls)

A system call is a function executed by the operating system, such as accessing hard drive and creating processes. System calls use shell commands to implement functions and used by programs to request services from the operating system.

In the C programming language, system commands such as `write`, is wrapped in some other function, such as `printf`.

### <a name="processes" class="anchor"></a> [Processes](#processes)

A process is an abstraction for processor, main memory, or I/O devices, and represent a running program. Its context is the state information the process needs to run. The processor switch between multiple running programs such as shell and some program using context switching, which saves the state of current process and restores the state of some new process. A thread is multiple execution units within a process with access to the same code and global data. 

A **kernel** is a collection of code and data structures that is always in memory. It is used to manage all processes and called using system call instructions, or `syscall`, which transfers control to the kernel when the program need some action done by the operating system, such as read or write to file.

### <a name="virtual-memory" class="anchor"></a> [Virtual memory](#virtual-memory)

A virtual memory is an abstraction for main memory and local disks. It provides each program with a virtual address space to make it seem as programs have exclusive use of memory:

- **program code and data**, code begins at same fixed address for all processes at bottom of the virtual address space, followed by global variables, and is fixed size once process is running
- **heap** expands and contracts its size dynamically at run-time using library functions such as `malloc` and `free`
- **shared libraries**, such as the C standard library, is near the middle of the virtual address space
- **stack** is at top of user-section of the virtual address space and used by compiler to implement function calls, it expands and contracts its size dynamically at run-time so that stack grows with each function call and contracts on return
- **kernel virtual memory** is at top of the virtual memory space and reserved for kernel, programs must call kernel to read or write in this space

### <a name="files" class="anchor"></a> [Files](#files)

A file is an abstraction for I/O devices and provides a uniform view of devices. Most input and output in a system is reading and writing to files.
