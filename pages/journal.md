-* toc

# Journal

This journal contains my unstructured and unfiltered notes. I might consolidate parts and add to [/notes](/notes.html) or as blog post later.

---

## Runtime implementations

Note on class-based OOP vs prototype-based OOP (instances is an environment):

- class-based OOP: class is blueprint for creating objects (instances)
- prototype-based OOP: object serves as prototype for creating other objects (instances)

In some languages, `module` objects are named environments, e.g. `Math` module with `PI` constant and `sin` function.

**AST interpreter**: interpret AST directly (tree walker)

```
x = 15
x + 10 - 5
```

```
[program, [
    [assign, x, 15],
    [sub,
        [add, x, 10],
        5
    ]
]]
```

AST with type information transformed to simple array:

```
x = y + 15
```

```
{
    type: "assign",
    left: {
        type: "identifier",
        value: "x",
    },
    right: {
        type: "add",
        left: {
            type: "identifier",
            value: "y",
        },
        right: {
            type: "number",
            value: 15,
        },
    },
}
```

```
[
    "assign",
    [
        "identifier",
        "x",
    ],
    [
        "add",
        [
            "identifier",
            "y",
        ],
        [
            "number",
            15,
        ],
    ],
]
```

```
["set", "x", ["+", "y", 10]]
```

Transform to S-expression (no need for parser):

```
(set x (+ y 10))
```

**Bytecode interpreter** (VM): translate AST to bytecode then interpret bytecode

- stack-based VM is stack of operands and operators with result is on top of stack (no registers)

```
push    $15     ; push 15 to stack
set     %0      ; set register 0 to top of stack (15 is popped from stack)
push    %0      ; push register 0 to stack (15 is pushed to stack again)
push    $10     ; push 10 to stack
add             ; add top two elements of stack (15 + 10)
push    $5      ; push 5 to stack
sub             ; subtract top two elements of stack (25 - 5)
```

- register-based VM is virtual registers with result in accumulator register (virtual registers are mapped to real registers via register allocation)

```
mov     r1, $15 ; move 15 to register 1
add     r1, $10 ; add 10 to register 1 (15 + 10)
sub     r1, $5  ; subtract 5 from register 1 (25 - 5)
```

Using `dis` in Python:

```python
import dis

def f(x):
    x = 15
    return x + 10 -5

dis.dis(f)
# 3           0 RESUME                   0

# 4           2 LOAD_CONST               1 (15)
#             4 STORE_FAST               0 (x)

# 5           6 LOAD_FAST                0 (x)
#             8 LOAD_CONST               2 (10)
#            10 BINARY_OP                0 (+)
#            14 LOAD_CONST               3 (5)
#            16 BINARY_OP               10 (-)
#            20 RETURN_VALUE
```

Compilers delegates interpretation via code generation (translate AST to IR or machine code):

- ahead-of-time (AOT) compile to machine code then run
- just-in-time (JIT) generate machine code at runtime (e.g. cached functions for future calls)
- AST transformer (transpiler) translates AST to AST (e.g. translate Python to JavaScript)

Note on terminology: compiler frontend refers to everything before code generation (parsing, type checking, AST transformations). Compiler backend refers to code generation, IR optimizations, and target-specific optimizations. LLVM is a compiler backend (translate AST to LLVM IR instead of bytecode).

Using `clang++ emit_llvm.cpp -S -emit-llvm` in C++ to generate LLVM IR:

```cpp
int main() {
    int x = 15;
    return x + 10 - 5;
}
```

```llvm
define i32 @main() #0 {
    %1 = alloca i32, align 4
    %2 = alloca i32, align 4
    store i32 0, i32* %1, align 4
    store i32 15, i32* %2, align 4
    %3 = load i32, i32* %2, align 4
    %4 = add nsw i32 %3, 10
    %5 = sub nsw i32 %4, 5
    ret i32 %5
}
```

## LLVM/MLIR

[MLIR](https://mlir.llvm.org/)

LLVM CPU-focused backend used by `clang` and `rustc` [[Code generation](https://rustc-dev-guide.rust-lang.org/backend/codegen.html)]:

- LLVM input is LLVM IR [[AST to TAC to LLVM](ast-to-tac-to-llvm.html)] (LLVM IR is basically annotated assembly)

MLIR have IR at different abstraction levels (dialects):

- Tensor operators [[TOSA](https://mlir.llvm.org/docs/Dialects/TOSA/)]
- linear algebra [[linalg](https://mlir.llvm.org/docs/Dialects/Linalg/)]
- low-level control flow [[cf](https://mlir.llvm.org/docs/Dialects/ControlFlowDialect/)]

In MLIR, multiple lowering passes incrementally translate higher-level IRs to lower-level IRs until reaching LLVM IR (or machine code).

- optimization can be applied at different levels
- higher-level dialects mainly useful to make it easier to write "optimization passes" (IR-rewriting modules, same as lowerings)

**polyhedral optimizations**

A polyhedral optimization is a loop transformation that maps a loop nest to another loop nest (nested loops). The name "polyhedral" comes from the fact that the loop nest can be represented as a polyhedron in the iteration space.

- MLIR `linalg` dialect can be used for tiling optimizations (data locality, cache utilization)

**MLIR operations**

In MLIR, `@` is used to denote a function (operation) and `%` is used to denote a variable (value). All values are typed. `func` is dialect for function abstractions [[func](https://mlir.llvm.org/docs/Dialects/Func/)].

```llvm
func.func @main(%arg0: i32) -> i32 {
    %0 = math.ctlz %arg0 : i32
    func.return %0 : i32
}
```

In the expression `math.ctlz`, `math` is a dialect [[math](https://mlir.llvm.org/docs/Dialects/MathOps/)] and `ctlz` is an operation to count leading zeros [[math.ctlz](https://mlir.llvm.org/docs/Dialects/MathOps/#mathctlz-mathcountleadingzerosop)]-

- `%arg0` is the integer argument to count leading zeroes on and `%0` is the result
- set of operations within braces is called "region"
- multiple dialects can be used in a single program (progressively lowered to backend target)

## Machine Learning Compilers

**pyopencl**

Testing on Macbook Pro (2019):

```bash
>>> import pyopencl
>>> from pyopencl.tools import get_test_platforms_and_devices
>>> get_test_platforms_and_devices()
[(<pyopencl.Platform 'Apple' at 0x7fff0000>, [<pyopencl.Device 'Intel(R) Core(TM) i9-9880H CPU @ 2.30GHz' on 'Apple' at 0xffffffff>, <pyopencl.Device 'Intel(R) UHD Graphics 630' on 'Apple' at 0x1024500>, <pyopencl.Device 'AMD Radeon Pro 5500M Compute Engine' on 'Apple' at 0x1021e00>])]
```

OpenCL via `pyopencl` seems to work fine on Macbook using AMD [[Sobel Filter using OpenCL in Python](sobel-filter-using-opencl-in-python.html)].

**CUDA**

CUDA kernel to add two arrays:

```cpp
__global__ void add(float* a, float* b, float* result, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < size) {
        result[idx] = a[idx] + b[idx];
    }
}
```

**TVMScript**

<mark>Ignore TVM. Too many dependencies and not easy to build. Development efforts will likely move elsewhere.</mark>

<mark>Not even the Google Colab tutorial work.</mark>

[Blitz Course to TensorIR](https://tvm.apache.org/docs/tutorial/tensor_ir_blitz_course.html) (not working?)

`mm_relu` [[Numpy Linear Relu](numpy-linear-relu.html)] implemented in `tvm.script` (TensorIR):

```python
# IRModule
@tmv.script.ir_module
class MyModule:
    # primitive tensor function
    @T.prim_func
    def mm_relu(A: T.Buffer((128, 128), "float32"), B: T.Buffer((128, 128), "float32"), C: T.Buffer((128, 128), "float32")):
        T.func_attr({ "global_symbol": "mm_relu", "tir.noalias": True })
        # intermediate tensor
        Y = T.alloc_buffer((128, 128), dtype="float32")
        # matmul
        for i, j, k in T.grid(128, 128, 128):
            # computational unit
            with T.block("Y"):
                # vi = T.axis.spatial(128, i)
                # vj = T.axis.spatial(128, j)
                # vk = T.axis.reduce(128, k)
                vi, vj, vk = T.axis.remap("SSR", [i, j, k])
                with T.init():
                    Y[vi, vj] = T.float32(0)
                Y[vi, vj] = Y[vi, vj] + A[vi, vk] * B[vk, vj]
        # relu
        for i, j in T.grid(128, 128):
            # computational unit
            with T.block("C"):
                # vi = T.axis.spatial(128, i)
                # vj = T.axis.spatial(128, j)
                vi, vj = T.axis.remap("SS", [i, j])
                C[vi, vj] = T.max(Y[vi, vj], T.float32(0))
```

- `IRModule` is a collection of `prim_func`s
- `T.Buffer` is a tensor with shape and data type arguments
- `T.alloc_buffer` allocates tensor
- `T.grid` iterates over tensor indices (nested iterators)
- `T.block` defines a computation block (basic unit of computation in TensorIR)

**Tensor Functions**

Linear transformation followed relu can be combined:

```python
# input tensor: (1, 3072)
# output tensor: (1, 200)
def linear_relu(x, w, out):
    for i in range(1):
        for j in range(200):
            out[i, j] = 0
            for k in range(3072):
                # linear                
                out[i, j] += x[i, k] * w[j, k]
            # relu
            out[i, j] = max(out[i, j], 0)
```

Primitive Tensor Functions:

```python
def add(a, b, c):
    for i in range(128):
        c[i] = a[i] + b[i]
```

```cpp
void add(float* a, float* b, float* c) {
    for (int i = 0; i < 128; i++) {
        c[i] = a[i] + b[i];
    }
}
```

- linear, add, relu, softmax
- implemented in low-level languages (C/C++) or assembly
    - can be hardware-specific to utilize parallelism

Primitive tensor function in `tvm.script` (tensor program abstraction):

```python
@T.prim_func
def main(A: T.Buffer[128, "float32"], B: T.Buffer[128, "float32"], C: T.Buffer[128, "float32"]):
    for i in range(128):
        with T.block("C"):
            vi = T.axis.spatial(128, i)
            C[vi] = A[vi] + B[vi]
```

**Deep Learning compiler stack**

[dl_compiler_stack.png](https://d3i71xaburhd42.cloudfront.net/69046519775ca6ac40c7d577887149525df2ee5d/10-Figure2-1.png)

[The Deep Learning Compiler: A Comprehensive Survey](https://arxiv.org/pdf/2002.03794.pdf)

[Machine Learning Compilation (MLC)](https://mlc.ai/index.html)

[MLC notes and videos](https://mlc.ai/summer22/schedule)

MLC front-end:

- "DL frontend": parsing models (ONNX, pytorch, tensorflow)
    - [Protocol Buffers](https://protobuf.dev/)
- graph optimization
    - constant folding, operator fusion, pruning (dead code elimination)
    - [Graph Transform Tool](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/tools/graph_transforms/README.md)
    - [Computational Graph Optimization](https://mlc.ai/chapter_graph_optimization/index.html)

MLC back-end:

- kernel selection
    - pick best kernel for each operation (kernel refers to hardware-specific implementation of an operation)
    - [cuDNN](https://developer.nvidia.com/cudnn)
    - quantized kernels (computing on lower-precision data types)
- auto-tuning
    - find best kernel/ kernel parameters (GA, RL)
    - [GA tuner](https://github.com/apache/tvm/blob/main/python/tvm/autotvm/tuner/ga_tuner.py)
- code generation
    - machine code or device-specific GPU instructions (LLVM, XLA, WASM, WebGPU)
    - [Compiling Machine Learning to WASM and WebGPU with Apache TVM](https://tvm.apache.org/2020/05/14/compiling-machine-learning-to-webassembly-and-webgpu)
- "DL backend": runtime environment and hardware-specific details (CUDA, OpenCL)

## Misc

**Abstract interpretation** [[wikipedia](https://en.wikipedia.org/wiki/Abstract_interpretation)]: generalized answers to questions without precise answers

- e.g. answering `yes` or `no` to "is this program correct?"
- or, answering "what is the value of this variable?" without running the program

```python
import ast
import inspect

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

# abstract interpretation analysis
def abstract_analysis(func):
    if any(isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult) for node in ast.walk(ast.parse(inspect.getsource(func)))):
        return "function involves multiplication"
    return "function do not involve multiplication"

result = abstract_analysis(factorial)
print(result)
# function involves multiplication
```

**Kolmogorov complexity** [[wikipedia](https://en.wikipedia.org/wiki/Kolmogorov_complexity)]: length of shortest program that outputs some string

- `abababababababababababababababab` generated by `print("ab" * 16)`
- `4c1j5b2p0cv4w1x8rx2y39umgw5q85s7` generated by `print("".join(random.choices(string.ascii_lowercase + string.digits, k=32)))`
    - or `print("4c1j5b2p0cv4w1x8rx2y39umgw5q85s7")`

**Instruction selection** [[wikipedia](https://en.wikipedia.org/wiki/Instruction_selection)]:

- macro expansion (inefficient)
- graph covering
- output from instruction selection is pseudo-registers (temporaries) then register allocation
