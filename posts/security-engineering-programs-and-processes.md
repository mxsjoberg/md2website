# Security Engineering: Programs and processes

*August 12, 2022*

This is the second post in a series of lecture notes on security engineering.

---

## File permissions

In UNIX-based systems, each process is assigned real UID/GID (user ID, group ID), which is the user initiating or owning the process, effective UID/GID, or EUID, which is used to determine permissions, and saved UID/GID, or SUID, which is used to drop and gain privileges.

A program with the SUID bit set has the effective UID/GID changed to that of the program owner.

File permissions are set using command, such as `-|rwx|r-x|r-x root root <file>`:

- `-` is file type, where `-` is regular file, `d` is directory, and `l` is symbolic link
- `rwx` set read-write-execute permissions for first root (file owner)
- first ``r-x`` set read-execute permission for second root (group owner)
- second ``r-x`` set read-execute permission for all others

The kernel will check EUID when the user is trying to write to file (root is most privileged user), and changing EUID with `chmod 4755 <file>`, which replaces ``rwx`` with ``rws`` (set-UID), makes the file run with the privileges of the file owner instead of the user.

## Address space

An address space is the range of addresses available to some process.

```c
int z;
int w = 10;
int main() {
    int x;
    int y = 42;
    char *p;
    p = malloc(42);
    *p = 42;
}
```

Below are the locations in buffer (address space is based on Linux legacy VM layout where top-most is lower addresses and bottom is higher addresses).

|     |     |
| :-- | --- |
| | **user space** |
| `.text`, program code | |
| `.bss`, uninitialized global data | `z` |
| `.data`, initialized global data | `w` |
| **heap**, growing from lower to higher addresses | `malloc(42)` |
| memory mapped region for large chunks of memory, such as shared libraries (text, data, `printf`) | ... |
| | `x` |
| | `y`  |
| | `*p` |
| | `p` (points to address in heap) |
| **stack**, growing from higher to lower addresses | `*p = 42` (write 42 in address in heap) |
| | **kernel space** |

## Application-level vulnerabilities

Application vulnerabilities are often due to overprivileged programs, such as mobile applications asking for all permissions, programs are read-write but should be read-only, or caused by unexpected inputs or errors:

- **local attack** need an established presence on the host, such as an account or running program controlled by attacker, and would allow executing with elevated privileges of the host
- **remote attack** involves manipulating some application via network-based interaction, it is unauthenticated so no need for authentication or permissions and would allow executing with privileges of the vulnerable application

A typical local attack exploit vulnerabilities in SUID-root programs to obtain root privileges. A malicious input can be injected at startup via command line, environment, or during execution via dynamic-linked objects and files. An unintended interaction with environment can result in the creation of new files, accessing restricted files via the file system, or invoking commands and processes. Local attacks often result in memory corruption (control hijacking, data brainwashing), command injection, and information leaks.

A remote attack is more difficult to perform but more powerful as there no need to require prior access to system.

### Environment attacks

An environment attack can occur when applications invoke external commands to carry out tasks, such as using `system()` to execute some command, `popen()` to open a process, or `execlp()` and `execvp()` to use the `PATH` environment variable to locate applications.

A `PATH` substitution attack use commands without a complete path, where attacker modifies the `PATH` variable to run a script, or the `HOME` variable to control execution of commands, such as accessing files.

### Input argument attacks

An input argument attack can occur when applications are supplied arguments via some input (command-line, web forms). The user-provided input can be used to inject commands such as `./program "; rm -rf /"`, which would call `program` and then delete everything. It is also possible to traverse directories, such as `..`-attack, overflow buffer, and perform format string attacks.

To avoid bad inputs:

- always check size when copied into buffers, use library functions such as `snprintf` to limit size to `n`
- always sanitize user-provided input, such as excluding known bad inputs, defining allowed input, or escaping special characters

### File access attacks

A file access attack can occur when applications create or use files, so always check that file exist and that it is not a symbolic link.

A [race condition](https://en.wikipedia.org/wiki/Race_condition) such as [time-of-check to time-of-use (TOCTTOU)](https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use) can occur when there is conflicting access to shared data and at least one is write.

```c
// access() check real UID and open() check effective UID

/* real UID */
if (access("file", W_OK) == 0) {
    /* symlink("/etc/passwd", "file"); */
    
    /* effective UID */
    if((f = open("file", O_WRONLY)) < 0) {
        /* ... */
    }
    /* potentially writing to "/etc/passwd" */
    write(f, buffer, count);
}
```

### Buffer overflow attacks

A buffer overflow attack can occur when applications try to store more elements in a buffer, which is a set of memory locations, than it can contain. Applications written in Java, Python, and C# are less likely to suffer from buffer overflow attacks as they have built-in overflow detection, but C and C++ do not.

Below is an example program that is vulnerable to a buffer overflow attack, executing this program would result in overflow of `buffer_1` into `buffer_2`.
    
```c
int main() {
    int i;
    char buffer_2[4];
    char buffer_1[6];

    for(i=0; i < 10; i++) {
        buffer_1[i] = 'A';
    }

    return 0;
}
```
