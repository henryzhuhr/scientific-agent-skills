# NVIDIA Warp 参考 — GPU 模拟和空间计算

NVIDIA Warp 是一个用于编写高性能模拟和图形代码的 Python 框架。它将用 `@wp.kernel` 修饰的 Python 函数 JIT 编译为在 CPU 或 GPU 上运行的高效 C++/CUDA 代码。 Warp 专为空间计算（物理模拟、机器人、几何处理和可微分编程）而设计，具有丰富的内置类型（向量、矩阵、四元数、变换）和空间基元（网格、体积、哈希网格、BVH）。

 与 Numba CUDA（为您提供原始线程/块控制）或 CuPy（取代 NumPy 操作）不同，Warp 提供了更高级别的编程模型内置支持可微分模拟、空间查询和基于图块的协作操作。

## 目录

1. [安装](#安装)
2. [何时使用 Warp 与其他库](#when-to-use-warp-vs-other-libraries)
3. [内核和启动](#kernels-and-launch)
4. [数组](#arrays)
5. [数据类型](#data-types)
6. [空间计算基元](#spatial-computing-primitives)
7. [基于图块的编程](#基于图块的编程)
8. [可微分性](#可微分性)
9. [流、事件和 CUDA 图](#streams-events-and-cuda-graphs)
10. [随机数生成](#random-number- Generation)
11. [互操作性](#互操作性)
12. [性能优化](#性能优化)
13. [常见模式](#common-patterns)
14. [常见陷阱](#common-pitfalls)

- --

## 安装

```bash
uv add warp-lang              # CUDA 12 runtime (most common)
# uv add warp-lang[examples]  # Includes USD and example dependencies
```

需要 CUDA 驱动程序 >= 525.60.13 (Linux)或 528.33 (Windows)。

验证安装：

```python
import warp as wp
wp.init()
# Prints device info, CUDA version, kernel cache location
```

- --

## 何时使用Warp与其他库

|使用案例|最佳选择|为什么|
|----------|------------|-----|
|物理模拟（粒子、布料、流体）| **扭曲** |内置空间基元，可微分，面向模拟|
|几何处理（网格、射线投射、SDF）| **扭曲** |原生网格/体积/BVH 类型，空间查询 |
| ML 训练的可微分模拟 | **扭曲** |自动前向/后向 AD、PyTorch/JAX 集成 |
|机器人学（运动学、动力学、控制）| **扭曲** |内置变换、四元数、空间向量|
| NumPy 数组数学（FFT、线性代数、排序）| **铜吡啶** |直接 NumPy 替代品，包装 cuBLAS/cuFFT |
|具有原始线程控制的自定义 CUDA 内核 | **努巴** |直接CUDA编程模型，共享内存|
|表格数据的数据整理/ETL | **cuDF** | GPU 上的 pandas API |
| ML 训练（sklearn 风格）| **cuML** | GPU 上的 scikit-learn API |

Warp 和 Numba 均将 Python 编译为 CUDA，但服务于不同的领域：
- **Warp** 凭借其丰富的类型系统（vec3、quat、变换、网格、体积）和自动微分，擅长模拟/空间工作负载
- **Numba** 擅长需要显式的原始 CUDA 编程线程/块控制、共享内存管理以及对任意数据的原子操作

- --

## 内核和启动

### 定义内核

```python
import warp as wp

@wp.kernel
def compute_forces(positions: wp.array(dtype=wp.vec3),
                   velocities: wp.array(dtype=wp.vec3),
                   forces: wp.array(dtype=wp.vec3),
                   dt: float):
    tid = wp.tid()

    pos = positions[tid]
    vel = velocities[tid]

    # Gravity
    force = wp.vec3(0.0, -9.81, 0.0)

    forces[tid] = force
```

### 启动内核

```python
# 1D launch
wp.launch(kernel=compute_forces,
          dim=num_particles,
          inputs=[positions, velocities, forces, 0.01],
          device="cuda")

# 2D launch (e.g., image processing)
wp.launch(kernel=compute_image, dim=(1024, 1024), inputs=[img], device="cuda")

# 3D launch
wp.launch(kernel=compute_field, dim=(nx, ny, nz), inputs=[field], device="cuda")
```

在2D/3D内核内部，检索索引为：

```python
i, j = wp.tid()       # 2D
i, j, k = wp.tid()    # 3D
```

### 用户函数

```python
@wp.func
def spring_force(x0: wp.vec3, x1: wp.vec3, rest_length: float, stiffness: float):
    delta = x1 - x0
    length = wp.length(delta)
    direction = delta / length
    return stiffness * (length - rest_length) * direction
```

可以从内核调用函数，支持

### 用户结构

```python
@wp.struct
class Particle:
    pos: wp.vec3
    vel: wp.vec3
    mass: float
    active: int
```

- --

## 数组

Warp 数组是类型化的、设备感知的容器（1D 到4D):

```python
# Allocate
positions = wp.zeros(n, dtype=wp.vec3, device="cuda")
grid = wp.empty(shape=(nx, ny, nz), dtype=float, device="cuda")

# From NumPy
import numpy as np
data = np.random.rand(1000, 3).astype(np.float32)
wp_data = wp.from_numpy(data, dtype=wp.vec3, device="cuda")

# Back to NumPy (synchronizes GPU automatically)
np_data = wp_data.numpy()

# Array math operators
c = 2.0 * a + b   # Element-wise, GPU-accelerated
c *= 10.0          # In-place
```

内核签名的类型别名：`wp.array2d`、`wp.array3d`、`wp.array4d`.

- --

## 数据类型

### 标量
`bool`、`int8`、`uint8`、`int16`、`uint16`、`int32`（别名：`int`）、`uint32`、`int64`、 `uint64`、`float16`、`float32`（别名：`float`）、`float64`

### 向量
`vec2`、`vec3`、`vec4` — 默认为 float32。每种标量类型的变体：`vec3f`、`vec3d`、`vec3h`、`vec3i` 等。

```python
v = wp.vec3(1.0, 2.0, 3.0)
length = wp.length(v)
normalized = wp.normalize(v)
d = wp.dot(a, b)
c = wp.cross(a, b)
```

### 矩阵
`mat22`、`mat33`、 `mat44` — 行优先。变体：`mat33f`、`mat33d`、`mat33h`.

```python
m = wp.mat33(1.0, 0.0, 0.0,
             0.0, 1.0, 0.0,
             0.0, 0.0, 1.0)
inv = wp.inverse(m)
det = wp.determinant(m)
result = m * v  # Matrix-vector multiply
```

### 四元数
`quat`（i、j、k、w 布局，其中 w 为实数部分）

```python
q = wp.quat_from_axis_angle(wp.vec3(0.0, 1.0, 0.0), 3.14159 / 2.0)
rotated = wp.quat_rotate(q, wp.vec3(1.0, 0.0, 0.0))
q_combined = wp.mul(q1, q2)  # Compose rotations
```

### 变换
`transform` — 7D（位置 vec3 + 四元数）

```python
t = wp.transform(wp.vec3(1.0, 2.0, 3.0), wp.quat_identity())
world_point = wp.transform_point(t, local_point)
world_dir = wp.transform_vector(t, local_dir)
```

### 空间向量和矩阵
`spatial_vector` (6D)、`spatial_matrix` (6x6) — 用于刚体动力学。

- --

## 空间计算基元

### 网格 (`wp.Mesh`)

具有 BVH 的三角形网格，用于快速射线投射和最近点查询：

```python
# Create mesh from vertices and triangle indices
mesh = wp.Mesh(points=vertices,     # wp.array(dtype=wp.vec3)
               indices=triangles)   # wp.array(dtype=int), flattened (v0,v1,v2,...)

# Query in kernel
@wp.kernel
def raycast(mesh_id: wp.uint64, origins: wp.array(dtype=wp.vec3),
            directions: wp.array(dtype=wp.vec3), hits: wp.array(dtype=float)):
    tid = wp.tid()
    query = wp.mesh_query_ray(mesh_id, origins[tid], directions[tid], 1000.0)
    if query.result:
        hits[tid] = query.t  # Hit distance

wp.launch(raycast, dim=n, inputs=[mesh.id, origins, dirs, hits])

# Update vertex positions (topology stays fixed)
mesh.points = new_positions
mesh.refit()  # Rebuild BVH
```

### 哈希网格 (`wp.HashGrid`)

粒子邻居查询的空间哈希（DEM、SPH）：

```python
grid = wp.HashGrid(dim_x=128, dim_y=128, dim_z=128, device="cuda")
grid.build(points=particle_positions, radius=search_radius)

@wp.kernel
def find_neighbors(grid_id: wp.uint64, positions: wp.array(dtype=wp.vec3)):
    tid = wp.tid()
    pos = positions[tid]

    query = wp.hash_grid_query(grid_id, pos, search_radius)
    index = int(0)
    while wp.hash_grid_query_next(query, index):
        neighbor_pos = positions[index]
        dist = wp.length(pos - neighbor_pos)
        if dist < search_radius:
            # Process neighbor
            ...
```

### 体积(`wp.Volume`)

基于 NanoVDB 的稀疏体积网格（SDF、速度场、烟雾）：

```python
# Load from NanoVDB file
volume = wp.Volume.load_from_nvdb("field.nvdb")

# Create from NumPy (dense → sparse)
volume = wp.Volume.load_from_numpy(numpy_3d_array, bg_value=0.0)

# Sample in kernel
@wp.kernel
def sample_sdf(volume_id: wp.uint64, points: wp.array(dtype=wp.vec3),
               distances: wp.array(dtype=float)):
    tid = wp.tid()
    # Trilinear interpolation in world space
    uvw = wp.volume_world_to_index(volume_id, points[tid])
    distances[tid] = wp.volume_sample(volume_id, uvw, wp.Volume.LINEAR)
```

### BVH (`wp.Bvh`)

射线和 AABB 相交的边界体积层次结构查询：

```python
bvh = wp.Bvh(lowers=box_mins, uppers=box_maxs)

# Ray query
query = wp.bvh_query_ray(bvh.id, ray_origin, ray_dir)
# AABB overlap query
query = wp.bvh_query_aabb(bvh.id, aabb_min, aabb_max)
```

### 行进立方体

从 3D 标量场提取等值面：

```python
mc = wp.MarchingCubes(nx=128, ny=128, nz=128, device="cuda")
mc.surface(field=sdf_array, threshold=0.0)

vertices = mc.verts    # wp.array(dtype=wp.vec3)
triangles = mc.indices # wp.array(dtype=int)
```

- --

## 基于图块的编程

Warp 的图块API 使用共享内存和 Tensor Cores：

 实现协作块级操作（类似于 Triton）```python
TILE_M = wp.constant(16)
TILE_N = wp.constant(16)
TILE_K = wp.constant(16)
TILE_THREADS = 64

@wp.kernel
def tile_gemm(A: wp.array2d(dtype=float), B: wp.array2d(dtype=float),
              C: wp.array2d(dtype=float)):
    i, j = wp.tid()

    sum = wp.tile_zeros(shape=(TILE_M, TILE_N), dtype=wp.float32)
    count = int(A.shape[1] / TILE_K)

    for k in range(count):
        a = wp.tile_load(A, shape=(TILE_M, TILE_K), offset=(i * TILE_M, k * TILE_K))
        b = wp.tile_load(B, shape=(TILE_K, TILE_N), offset=(k * TILE_K, j * TILE_N))
        wp.tile_matmul(a, b, sum)

    wp.tile_store(C, sum, offset=(i * TILE_M, j * TILE_N))

wp.launch_tiled(tile_gemm, dim=(M // TILE_M, N // TILE_N),
                inputs=[A, B, C], block_dim=TILE_THREADS)
```

关键图块操作：
- **构造**：`tile_zeros`、`tile_ones`、`tile_load`、`tile_from_thread`
- **数学**：`tile_matmul`、`tile_fft`、 `tile_ifft`、`tile_cholesky`、`tile_cholesky_solve`
- **减少**：`tile_sum`、`tile_min`、`tile_max`、`tile_reduce`
- **IO**：`tile_load`、 `tile_store`、`tile_atomic_add`
- **算术**：`+`、`-`、`*`、`/` 瓷砖上的运算符
- **空间查询**：`tile_bvh_query_aabb`、 `tile_mesh_query_aabb`

SIMT↔Tile桥接：`wp.tile(scalar_value)`根据每个线程的值创建一个tile； `wp.untile(tile)` 提取回每个线程的值。

---

## 可区分性

Warp 自动生成前向和后向（伴随）内核，从而实现基于梯度的优化和 ML 集成：

```python
# Arrays participating in gradients need requires_grad=True
a = wp.zeros(1024, dtype=wp.vec3, device="cuda", requires_grad=True)

# Record forward pass
tape = wp.Tape()
with tape:
    wp.launch(kernel=compute1, inputs=[a, b], device="cuda")
    wp.launch(kernel=compute2, inputs=[c, d], device="cuda")
    wp.launch(kernel=loss_fn, inputs=[d, loss], device="cuda")

# Backward pass
tape.backward(loss)

# Access gradients
grad_a = tape.gradients[a]
```

 主要功能：
- 自动所有内核的伴随代码生成
- `wp.Tape` 记录和重播计算图
- 与 PyTorch autograd 和 JAX 集成 JIT
- 通过 `@wp.func_grad`
- 雅可比计算自定义梯度函数支持

---

##流、事件和CUDA图

```python
# Streams for concurrent execution
stream1 = wp.Stream("cuda:0")
stream2 = wp.Stream("cuda:0")
wp.launch(kernel1, ..., stream=stream1)
wp.launch(kernel2, ..., stream=stream2)

# CUDA Graph capture (eliminates Python launch overhead)
with wp.ScopedCapture() as capture:
    wp.launch(kernel1, ...)
    wp.launch(kernel2, ...)
    wp.launch(kernel3, ...)

# Replay graph many times with near-zero CPU overhead
for _ in range(1000):
    wp.capture_launch(capture.graph)
```

---

##随机数生成

使用PCG（置换同余生成器）—初始化每个线程：

```python
@wp.kernel
def monte_carlo(samples: wp.array(dtype=wp.vec3), seed: int):
    tid = wp.tid()
    rng = wp.rand_init(seed, tid)  # Unique sequence per thread

    x = wp.randf(rng)  # [0, 1)
    y = wp.randf(rng)
    z = wp.randf(rng)
    samples[tid] = wp.vec3(x, y, z)
```

 在启动之间使用不同的种子以避免相关序列。

---

## 互操作性

### NumPy（CPU 上的零复制）
```python
np_array = warp_array.numpy()          # GPU → CPU copy, CPU → zero-copy view
wp_array = wp.from_numpy(np_array, dtype=wp.vec3, device="cuda")
```

### PyTorch（零拷贝、autograd 支持）
```python
torch_tensor = wp.to_torch(warp_array)      # Zero-copy
warp_array = wp.from_torch(torch_tensor)     # Zero-copy
# Gradient arrays are converted between Warp tape and PyTorch autograd
```

### CuPy/Numba（通过 CUDA 数组接口进行零拷贝）
```python
# CuPy arrays can be passed directly to Warp kernels
# Warp arrays expose __cuda_array_interface__
cupy_arr = cp.asarray(warp_array)  # Zero-copy
```

### JAX（通过 CUDA 数组接口进行零拷贝） DLPack)
```python
jax_array = wp.to_jax(warp_array)
warp_array = wp.from_jax(jax_array)
# @warp.jax_experimental.jax_kernel() for JAX primitive integration
```

### DLPack(通用零拷贝)
```python
# Import from any DLPack framework
warp_array = wp.from_dlpack(external_array)
# Export
external = framework.from_dlpack(warp_array)
```

---

##性能优化

### 1.使用CUDA图进行重复启动

如果多次启动相同的内核序列（模拟循环），CUDA图形捕获消除了Python开销：

```python
with wp.ScopedCapture() as capture:
    for _ in range(substeps):
        wp.launch(integrate, ...)
        wp.launch(collide, ...)

for frame in range(num_frames):
    wp.capture_launch(capture.graph)
```

### 2. 最大限度地减少主机设备传输

将数据保留在 GPU 上。在设备上使用 `wp.array`，避免在内部循环中使用 `.numpy()`。

### 3. 使用平铺操作进行缩减，并且基于 GEMM

Tile 的缩减比每线程原子快 50 倍以上。使用 `wp.tile()` + `wp.tile_sum()` + `wp.tile_atomic_add()` 代替 `wp.atomic_add()`.

### 4. 优先选择 float32 而不是 float64

GPU float32 吞吐量比 float64 高 2x-32x.

### 5. 内核缓存

Warp 在运行之间缓存已编译的内核。首次启动编译（可能需要几秒钟）；后续运行以毫秒为单位从缓存中加载。

### 6. 对象生命周期

 在使用 `.id` 时，保持对空间基元（Mesh、HashGrid、Volume、BVH）的 Python 引用处于活动状态。当内核持有 ID 时，Python 对象的垃圾收集会导致未定义的行为。

---

## 常见模式

### 粒子模拟

```python
@wp.kernel
def integrate_particles(positions: wp.array(dtype=wp.vec3),
                        velocities: wp.array(dtype=wp.vec3),
                        forces: wp.array(dtype=wp.vec3),
                        dt: float):
    tid = wp.tid()
    vel = velocities[tid] + forces[tid] * dt
    pos = positions[tid] + vel * dt

    velocities[tid] = vel
    positions[tid] = pos
```

### 网格射线Casting

```python
@wp.kernel
def cast_rays(mesh_id: wp.uint64,
              ray_origins: wp.array(dtype=wp.vec3),
              ray_dirs: wp.array(dtype=wp.vec3),
              hit_points: wp.array(dtype=wp.vec3)):
    tid = wp.tid()
    query = wp.mesh_query_ray(mesh_id, ray_origins[tid], ray_dirs[tid], 1e6)
    if query.result:
        hit_points[tid] = ray_origins[tid] + ray_dirs[tid] * query.t
```

### 使用 PyTorch 进行微分模拟

```python
import torch
import warp as wp

# Warp kernel for simulation
@wp.kernel
def simulate(state: wp.array(dtype=wp.vec3), params: wp.array(dtype=float),
             output: wp.array(dtype=wp.vec3)):
    tid = wp.tid()
    # ... physics computation ...

# PyTorch training loop
optimizer = torch.optim.Adam([torch_params], lr=1e-3)

for epoch in range(100):
    wp_params = wp.from_torch(torch_params)
    tape = wp.Tape()
    with tape:
        wp.launch(simulate, dim=n, inputs=[state, wp_params, output])
        wp.launch(loss_kernel, dim=1, inputs=[output, target, loss])

    tape.backward(loss)
    grad = wp.to_torch(tape.gradients[wp_params])
    torch_params.grad = grad
    optimizer.step()
```

### 带哈希的 SPH 流体Grid

```python
grid = wp.HashGrid(128, 128, 128, device="cuda")

@wp.kernel
def compute_density(grid_id: wp.uint64, positions: wp.array(dtype=wp.vec3),
                    densities: wp.array(dtype=float), radius: float):
    tid = wp.tid()
    pos = positions[tid]
    density = float(0.0)

    query = wp.hash_grid_query(grid_id, pos, radius)
    index = int(0)
    while wp.hash_grid_query_next(query, index):
        dist = wp.length(pos - positions[index])
        if dist < radius:
            # SPH kernel
            q = dist / radius
            density += (1.0 - q) * (1.0 - q) * (1.0 - q)

    densities[tid] = density

# Each timestep:
grid.build(points=positions, radius=h)
wp.launch(compute_density, dim=n, inputs=[grid.id, positions, densities, h])
```

- --

## 常见陷阱

1. **忘记类型注释** — 必须键入所有内核参数。 Warp 从注释推断类型，而不是运行时值。

2. **在内核中使用 Python 数据结构** — 没有列表、字典或集合。使用`wp.array`、`wp.vec3`、`@wp.struct`.

3. **在用户函数中调用 `wp.tid()`** — `wp.tid()` 仅适用于内核。将线程索引作为参数传递给 `@wp.func` 函数。

4. **对象生命周期问题** — 空间基元（Mesh、HashGrid、Volume、BVH）在内核中使用 `.id` 时必须保持活动状态（在 Python 中引用）。让 Python 对象被垃圾收集会导致崩溃。

5. **期望就地操作可微分** - Warp 的自动差异不支持就地数组修改。写入单独的输出数组以进行梯度计算。

6. **不使用 `requires_grad=True`** — 参与梯度计算的数组必须使用 `requires_grad=True`.

7 创建。 **使用错误的设备启动** — 数组和内核启动必须在同一设备上。一致使用`device="cuda"`。

8. **首次启动编译时间** — 首次内核启动会触发 JIT 编译（可能需要几秒钟）。后续运行将使用缓存。不要对第一次运行进行基准测试。

9. **使用元组而不是 Warp 类型** — `(1.0, 2.0, 3.0)` 在内核范围内无效。使用`wp.vec3(1.0, 2.0, 3.0)`.

10. **CPU 上的块大小** — CPU 上的平铺操作使用 `block_dim=1`，这会改变行为。设计独立于块大小的跨设备内核。
