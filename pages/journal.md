# Journal

This page contains my day-to-day unstructured and unfiltered notes.

## Machine Learning Compilers

**TVMScript**

[Blitz Course to TensorIR](https://tvm.apache.org/docs/tutorial/tensor_ir_blitz_course.html)

`mm_relu` [[programming](numpy-linear-relu.html)] implemented in `tvm.script` (TensorIR):

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

**General theory**

Instruction selection [[wikipedia](https://en.wikipedia.org/wiki/Instruction_selection)]:

- macro expansion (inefficient)
- graph covering
- output from instruction selection is pseudo-registers (temporaries) then register allocation
