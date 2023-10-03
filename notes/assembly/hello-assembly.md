# Hello Assembly

<mark>May 2021</mark>

```asm
; program (intel syntax)
section .text
	; start point for execution
    global      start

start:
	; write
    mov         rax, 0x02000004
    ; stdout
    mov         rdi, 1
    ; address of string to output
    mov         rsi, message
    ; bytes
    mov         rdx, 12
    ; invoke to write
    syscall
    ; exit
    mov         rax, 0x02000001
    ; 0
    xor         rdi, rdi
    ; invoke to exit
    syscall

; declare data used in program
section .data

message:
	; db -> raw bytes, text + newline = 11 + 1 = 12, line feed = 0xa = 10 = \n
    db          "hello assembly", 10
```