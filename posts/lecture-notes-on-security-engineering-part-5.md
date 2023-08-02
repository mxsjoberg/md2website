# Lecture notes on Security Engineering – Part 5: Secure system design

*September 2022*

## <a name="1" class="anchor"></a> [Hardware and software solutions](#1)

A system design involves both hardware and software, where software is easy to change, which is good for functionality but bad for security and generally bad for performance, and hardware is hard to change, which is bad for functionality but good for security:

- [AES instruction set](https://en.wikipedia.org/wiki/AES_instruction_set) implements cryptography instructions
- [Intel SGX](https://en.wikipedia.org/wiki/Software_Guard_Extensions) support encrypted computation, such as for cloud computing applications
- hardware primitives, such as [Physical unclonable function](https://en.wikipedia.org/wiki/Physical_unclonable_function), which provides unpredictable and repeatable randomness (fingerprint)

A secure system design favor simplicity, such as fail-safe defaults (key lengths, whitelist better than blacklist) and assume non-expert users, so keep user interface simple and avoid choices. It is preferable to reduce need to trust other parts of system (kernel is assumed to be trusted) and grant least privileges possible, such as restricting flow of sensitive data, secure compartments (operating system), `seccomp` system call isolates process by limiting possible interactions.

Layers of security can be used to further secure systems, such as firewall, encrypting data at rest, using type-safe programming languages, and logging relevant operational information.

### <a name="1.1" class="anchor"></a> [Tainted flow analysis](#1.1)

Trusting unvalidated inputs is the root cause of many attacks, such as a program getting unsafe input, or tainted data, from a user and assuming it is safe, or untainted:

Below is an example vulnerable program, where an input such as `name="%s%s%s"` would crash program and `name="...%n..."` would write to memory.

```c
char *name = fgets( /* ... */, network_fd);
printf(name); /* vulnerable to format string */
```

In tainted flow analysis, such as [Taint checking](https://en.wikipedia.org/wiki/Taint_checking), the goal is to prove that no tainted data is used where untainted data is expected for all possible inputs (`untainted` indicate trusted and `tainted` indicate untrusted):

- legal flow

```c
void f(tainted int);

untainted int a = /* ... */ ;
f(a); /* function expect tainted, and input is untainted, so legal flow */
```

- illegal flow

```c
void f(untainted int);

tainted int a = /* ... */ ;
f(a); /* function assume untainted, and input is tainted, so illegal flow */
```

### <a name="1.2" class="anchor"></a> [Tracking tainted data in programs](#1.2)

Below is an example tainted flow analysis on vulnerable program at each line of execution (`tainted` label can be introduced as type or annotation).
    
```c
void copy(tainted char *src, untainted char *dst, int len) {
    /* tainted: src; untainted: dst; unknown: len */
    untainted int i;
    /* tainted: src; untainted: dst, i; unknown: len */
    for (i = 0; i < len; i++) {
        /* tainted: src; untainted: dst, i; unknown: len */
        dst[i] = src[i]; /* illegal, tainted into untainted */
    }
}
```

## <a name="2" class="anchor"></a> [Preventing buffer overflows](#2)

Buffer overflow attacks can sometimes be prevented using programming languages with boundary checking, such as Java or Python, or contained using virtualization. Here are a few other common methods:

- [StackGuard](https://www.usenix.org/legacy/publications/library/proceedings/sec98/full_papers/cowan/cowan.pdf) is a canary-based method to protect or detect potential danger, where a canary-value is placed on stack, which can be verified to not be corrupted during execution
- non-executable memory, or [NX-bit](https://en.wikipedia.org/wiki/NX_bit), can be used to segregate area in memory used by code and data
- randomized addresses and instructions, such as [ASLR](https://en.wikipedia.org/wiki/Address_space_layout_randomization), which can be used to randomize address space layout (instructions can also be encrypted in memory and decrypted before execution, but substantial overhead)

For further reading, see [Return-oriented programming (ROP)](https://en.wikipedia.org/wiki/Return-oriented_programming).
