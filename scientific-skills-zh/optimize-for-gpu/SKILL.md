---
name: optimize-for-gpu
description: "使用 CuPy、Numba CUDA、Warp、cuDF、cuML、cuGraph、KvikIO、cuCIM、cuxfilter、cuVS、cuSpatial 和 RAFT 对 Python 代码进行 GPU 加速。每当用户提到 GPU/CUDA/NVIDIA 加速，或想要加速 NumPy、pandas、scikit-learn、scikit-image、NetworkX、GeoPandas 或 Faiss 工作负载时使用。涵盖物理模拟、可微渲染、网格光线投射、粒子系统（DEM/SPH/流体）、矢量/相似性搜索、GPUDirect Storage 文件 IO、交互式仪表板、地理空间分析、医学成像和稀疏特征求解器。当您看到 CPU 密集型 Python 代码（循环、大型数组、机器学习管道、图形分析、图像处理）时，即使没有明确请求，也可以使用这些代码，这些代码将受益于 GPU 加速。"
metadata:
  author: K-Dense, Inc.
---

# 使用 NVIDIA 对 Python 进行 GPU 优化

您是一位专家 GPU 优化工程师。您的工作是帮助用户编写新的 GPU 加速代码或将其现有的受 CPU 限制的 Python 代码转换为在 NVIDIA GPU 上运行，以实现显着的加速 — 对于合适的工作负载，速度通常为 10 倍到 1000 倍。

## 此技能何时适用

- 用户想要加速数值/科学 Python 代码
- 用户正在处理大型数组、矩阵或数据帧
- 用户提到 CUDA、GPU、NVIDIA 或并行计算
- 用户拥有 NumPy、pandas、SciPy、scikit-learn、NetworkX 或处理大型数据集的 scipy.sparse.linalg 代码
- 用户需要低级 GPU 原语（稀疏特征解算器、设备内存管理、多 GPU 通信）
- 用户正在进行机器学习（训练、推理、超参数调整、预处理）
- 用户正在进行图形分析（中心性、社区检测、最短路径、PageRank、等）
- 用户正在执行向量搜索、最近邻搜索、相似性搜索或构建 RAG 管道
- 用户拥有可以 GPU 加速的 Faiss、Annoy、ScaNN 或 sklearn 最近邻居代码
- 用户想要 GPU 加速的交互式仪表板、交叉过滤或大型探索性数据分析数据集
- 用户正在使用 GeoPandas 或 shapely 进行地理空间分析（多边形内的点、空间连接、轨迹分析、距离计算）
- 用户正在使用 scikit-image 或 OpenCV
 进行图像处理、计算机视觉或医学成像（过滤、分割、形态、特征检测）- 用户正在使用全幻灯片图像 (WSI)、数字病理学、显微镜学或遥感图像
- 用户正在将大型二进制数据文件加载到 GPU 内存中（numpy.fromfile → cupy 或 Python open() → GPU 数组）
- 用户需要将文件从 S3、HTTP 或 WebHDFS 直接读取到 GPU 内存中
- 用户提到 GPUDirect Storage (GDS)或想要绕过文件的 CPU 内存暂存IO
- 用户正在进行物理模拟（粒子、布料、流体、刚体）或可微分模拟
- 用户需要网格操作（射线投射、最近点查询、有符号距离场）或几何过程GPU 上的 ssing
- 用户正在使用变换和四元数进行机器人学（运动学、动力学、控制）
- 用户具有可以 JIT 编译到 GPU 内核的 Python 模拟循环
- 用户提到 NVIDIA Warp 或想要与 PyTorch/JAX
 集成的可微分 GPU 模拟 - 用户正在进行模拟、信号处理、财务建模、生物信息学、物理或任何计算密集型工作
- 用户想要优化现有代码，GPU 加速是正确的答案

## 决策框架：使用哪个库

根据用户代码的实际用途选择正确的工具。在编写任何 GPU 代码之前，请阅读相应的参考文件。

### CuPy — 用于数组/矩阵运算（NumPy 替换）
* *阅读：** `references/cupy.md`

 当用户的代码主要是：
- NumPy 数组运算（逐元素数学、线性代数、FFT、排序、 
- SciPy 操作（稀疏矩阵、信号处理、图像过滤、特殊函数）
- 链接 NumPy 调用的任何代码 — CuPy 是直接替代品

CuPy 包装了 NVIDIA 的优化库（cuBLAS、cuFFT、cuSOLVER、cuSPARSE、cuRAND），因此标准操作已经调整。大多数 NumPy 代码的工作原理是将 `import numpy as np` 更改为 `import cupy as cp`。

* *最适合：**线性代数、FFT、数组数学、图像处理、信号处理、带有数组操作的蒙特卡罗、任何 NumPy 密集型工作流程。

### Numba CUDA — 用于自定义 GPU 内核
* *阅读：** `references/numba.md`

 当用户需要时使用 Numba：
- 不映射到标准数组操作的自定义算法
- 对 GPU 线程、块和共享内存的细粒度控制
- 具有复杂逻辑的逐元素操作（使用 `@vectorize(target='cuda')`）
- 具有自定义的缩减操作逻辑
- 模板计算或依赖于邻居的计算
- 任何直接需要CUDA 编程模型的东西

Numba 将Python 直接编译到CUDA 内核中。它可以完全控制 GPU 的线程层次结构、共享内存和同步 - 对于无法表示为数组操作的算法至关重要。

* *最适合：** 自定义内核、粒子模拟、模板代码、自定义缩减、需要共享内存的算法、具有复杂的每元素逻辑的任何代码。

### Warp — 用于模拟、空间计算和可微分编程
* *阅读：** `references/warp.md`

 当用户的代码主要是：
- 物理模拟（粒子、布料、流体、刚体、DEM、SPH）
- 几何处理（网格操作、射线投射、带符号距离场、行进） 
- 机器人学（运动学、动力学、变换和四元数控制）
- ML 训练的可微分模拟（与 PyTorch/JAX autograd 集成）
- 任何需要 JIT 编译到 GPU 的 Python 模拟循环
- 使用网格、体积 (NanoVDB)、哈希网格或BVH 查询

Warp JIT 将 `@wp.kernel` Python 函数编译为 CUDA，具有用于空间计算的内置类型（vec3、mat33、quat、transform）和用于几何查询的基元（Mesh、Volume、HashGrid、BVH）。所有内核均可自动微分。

* *最适合：**物理模拟、网格光线投射、粒子系统、可微分渲染、机器人运动学、SDF 操作、将空间数据结构与 GPU 计算相结合的任何工作负载。

* *Warp 与 Numba：** 两者都将 Python 编译为 CUDA，但 Warp 提供更高级别的空间类型（vec3、quat、Mesh、Volume）和自动微分，而 Numba 提供原始数据CUDA 控制（共享内存、块/线程管理、原子）。使用 Warp 进行模拟/几何，Numba 进行通用自定义内核。

### cuDF — 用于数据帧操作（pandas 替换）
* *阅读：** `references/cudf.md`

 当用户的代码主要是：
- pandas DataFrame 操作（过滤、groupby、连接、聚合）
- CSV/Parquet/JSON 读取和处理
- 大型数据集上的 ETL 管道或数据整理
- 适合 GPU 内存的数据集上的任何 pandas 密集型工作流程

cuDF 的 `cudf.pandas` 加速器模式可以在零代码更改的情况下加速现有的 pandas 代码。为了获得最大性能，请使用本机 cuDF API。

* *最适合：**数据整理、ETL、groupby/聚合、联接、数据帧上的字符串处理、表格数据上的时间序列。

### cuML — 用于机器学习（scikit-learn 替换）
* *阅读：** `references/cuml.md`

 使用cuML时用户的代码主要是：
- scikit-learn估计器（分类、回归、聚类、降维）
- ML预处理（缩放、编码、插补、特征提取）
- 超参数调整或交叉验证
- 树模型推理（XGBoost、LightGBM、 sklearn 随机森林（通过 FIL）
- 大型数据集上的 UMAP、t-SNE、HDBSCAN 或 KNN

cuML 的 `cuml.accel` 加速器模式可以在零代码更改的情况下加速现有的 sklearn 代码。为了获得最大性能，请使用本机 cuML API。加速范围从简单线性模型的 2-10 倍到 HDBSCAN 和 KNN 等复杂算法的 60-600 倍。

* *最适合：** 分类、回归、聚类、降维、预处理管道、模型推理、任何 scikit-learn-heavy 工作流程。

### cuGraph — 用于图形分析 (NetworkX替换）
* *阅读：** `references/cugraph.md`

 当用户的代码主要是：
- NetworkX 图算法（中心性、社区检测、最短路径、PageRank）
- 大型网络上的图构建和分析
- 社交网络分析、知识图谱、或推荐系统
- 具有 10K+ 边的网络上的任何图算法

cuGraph 的 `nx-cugraph` 后端可以通过环境变量以零代码更改来加速现有的 NetworkX 代码。为了获得最大性能，请将本机 cuGraph API 与 cuDF DataFrame 结合使用。加速范围从小图的 10 倍到大图（数百万条边）的 500 倍以上。

* *最适合：** PageRank、介数中心性、社区检测（Louvain、Leiden）、BFS/SSSP、连接组件、链接预测、图神经网络采样、任何 NetworkX 密集型工作流程。

### KvikIO — 用于高性能 GPU 文件IO
* *阅读：** `references/kvikio.md`

 当用户的代码主要是：
- 将大型二进制数据文件直接加载到 GPU 内存中
- 将 GPU 数组写入磁盘而不首先复制到主机
- 将数据从远程存储（S3、HTTP、WebHDFS）读取到 GPU 中内存
- 在 GPU 上使用 Zarr 阵列（GDSStore 后端）
- 文件 IO 是存储和 GPU 之间瓶颈的任何管道

KvikIO 提供与 NVIDIA cuFile 的 Python 绑定，从而启用 GPUDirect Storage (GDS) — 数据直接在 NVMe 存储和 GPU 内存之间流动，完全绕过 CPU 内存。当 GDS 不可用时，它会透明地回退到 POSIX IO。它无缝处理主机和设备数据。

* *最适合：**将二进制数据加载到 GPU，将 GPU 数组保存到磁盘，从 S3/HTTP 直接读取到 GPU，GPU 上的 Zarr 数组，替换 `numpy.fromfile()` → `cupy` 模式，任何通过 CPU 内存进行数据暂存是瓶颈的 IO 密集型 GPU 管道。

* *注意：** 对于表格格式（CSV、Parquet、JSON），请使用 cuDF 的内置读取器 - 它们针对这些格式进行了优化。 KvikIO 用于原始二进制数据和远程文件访问。

### cuxfilter — 用于 GPU 加速的交互式仪表板
* *阅读：** `references/cuxfilter.md`

当用户需要时使用 cuxfilter：
- 大型数据集（数百万行）上的交互式交叉过滤仪表板
- 使用相互过滤的链接图表进行探索性数据分析
- 使用散点图、条形图、热图、区域统计图或图形可视化的 GPU 加速可视化
- 来自 Jupyter 的仪表板原型设计具有最少代码的笔记本
- 可视化来自 cuDF、cuML 或 cuGraph 管道的结果

cuxfilter 利用 cuDF 进行 GPU 上的所有数据操作 - 过滤、分组和聚合完全发生在 GPU 上，仅将渲染结果发送到浏览器。它集成了 Bokeh、Datashader（用于数百万个点）、Deck.gl（用于地图）和面板小部件。

* *最适合：**交互式数据探索仪表板、多图表交叉过滤、地理空间可视化、图形可视化、可视化 RAPIDS 管道结果、用户需要交互式探索和过滤大型 GPU 驻留数据集的任何场景。

### cuCIM — 用于图像处理（scikit-image 替换）
* *阅读：** `references/cucim.md`

 使用 cuCIM 当用户的代码主要是：
- scikit-image 操作（过滤、形态学、分割、特征检测、颜色转换）
- 用于深度学习的图像预处理管道（调整大小、归一化、 
- 数字病理学（全玻片图像读取、H&E 染色标准化、细胞计数）
- 显微镜、遥感或医学成像工作流程
- 任何 scikit-image-heavy 管道处理 512x512 或更大的图像

cuCIM 的 `cucim.skimage` 模块镜像scikit-image 的 API 具有 200 多个 GPU 加速函数。它还提供高性能 WSI 读取器 (`CuImage`)，速度比 OpenSlide 快 5-6 倍。所有函数都适用于 CuPy 数组 — 零拷贝，全部在 GPU 上。

* *最适合：** 过滤（高斯、索贝尔、弗朗吉）、形态、阈值、连通分量标记、区域属性、色彩空间转换、图像配准、去噪、全幻灯片图像处理、深度学习预处理管道。

### cuVS — 用于矢量搜索（Faiss/Annoy 替换）
* *阅读：** `references/cuvs.md`

 使用cuVS，当用户的代码主要是：
- 高维向量上的近似最近邻 (ANN)搜索
- RAG、推荐系统或语义检索的相似性搜索
- 用于聚类或可视化的 k-NN 图构建
- 大型上的任何 Faiss、Annoy、ScaNN 或 sklearn 最近邻工作负载嵌入数据集

cuVS 提供 GPU 加速的 ANN 索引类型（CAGRA、IVF-Flat、IVF-PQ、暴力）以及用于从 GPU 构建的索引提供 CPU 服务的 HNSW。它为 Faiss、Milvus 和 Lucene 的 GPU 后端提供支持。对于大多数用例，从 CAGRA 开始 — 它是最快的 GPU 原生算法。

* *最适合：** 嵌入搜索、RAG 检索、推荐系统、图像/文本/音频相似性搜索、k-NN 图构建、10K+ 向量上的任何最近邻工作负载。

### cuSpatial — 用于地理空间分析 (GeoPandas替换）
* *阅读：** `references/cuspatial.md`

使用cuSpatial时用户的代码主要是：
- GeoPandas空间操作（点入多边形、空间连接、距离计算）
- 轨迹分析（分组GPS轨迹、计算
- 用于大规模空间连接的空间索引（四叉树）
- 纬度/经度坐标上的半正矢距离计算
- 大型地理空间数据集上的任何 GeoPandas/shapely-heavy 工作流程

cuSpatial 提供 GPU 加速的 `GeoSeries` 和`GeoDataFrame` 类型与 GeoPandas 兼容，加上空间连接、距离和轨迹功能。从 GeoPandas 转换为 `cuspatial.from_geopandas()`.

* *最适合：** 多边形中的点测试、数百万个点/多边形的空间连接、半正矢和欧几里得距离计算、轨迹重建和分析、任何 GeoPandas 重的地理空间工作流程。

### RAFT (pylibraft) — 用于低级 GPU 基元和多 GPU
* *阅读：** `references/raft.md`

 当用户需要时使用 RAFT：
- GPU 加速的稀疏特征值问题（`scipy.sparse.linalg.eigsh` 替换）
- 低级 GPU 设备内存管理（`device_ndarray`）
- 随机图生成（用于基准测试的 R-MAT 模型）
- 多节点多 GPU 通信基础设施（通过 `raft-dask`）
  - 更高级别 RAPIDS 库的构建块

RAFT 提供构建 cuML 和 cuGraph 的基础原语。大多数用户应该首先使用这些更高级别的库 - 当您需要它公开的特定基元（稀疏特征解算器、设备内存、图形生成）或通过 Dask.

 进行多 GPU 通信时，直接使用 RAFT **最适合：** 稀疏特征值分解（谱方法、图形分区）、R-MAT 图形生成、低级设备内存管理、多 GPU Orchestration.

* *注意：**向量搜索算法（k-NN、IVFPQ、CAGRA）已迁移到 cuVS — 不要使用 RAFT 进行向量搜索。

### 组合库

许多实际工作负载受益于同时使用多个库。它们通过 CUDA 阵列接口进行互操作 — CuPy、Numba、Warp、cuDF、cuML、cuGraph、cuVS、cuCIM、cuSpatial、KvikIO、PyTorch、JAX 和其他 GPU 库之间的零拷贝数据共享。

常见组合：
- **cuDF + cuML**：使用 cuDF 加载和预处理数据，使用 cuML 训练/预测 - 完整的 RAPIDS 管道
- **cuDF + cuGraph**：从 cuDF 边缘列表构建图形，使用 cuGraph 运行图形分析
- **cuGraph + cuML**：使用 cuGraph 提取图形特征，输入 cuML ML
- **cuML + cuVS**：使用 cuML 训练嵌入模型，使用 cuVS
 索引和搜索嵌入 - **cuDF + CuPy**：使用 cuDF 加载和过滤数据，然后使用 CuPy
 进行数值分析- **CuPy + cuVS**：使用 CuPy 操作生成嵌入，构建 cuVS 搜索索引 —零复制
- **Warp + PyTorch**：Warp 中的可微分模拟，将梯度反向传播到 PyTorch 训练循环
- **Warp + CuPy**：使用 CuPy 进行数组数学，Warp 进行空间查询（网格、体积） - 通过 CUDA 数组接口进行零复制
- **Warp + JAX**：Warp 内核作为内部的 JAX 原语jitted 函数
- **CuPy + Numba**：使用 CuPy 进行标准操作，使用 Numba 进行自定义内核
- **cuDF + Numba**：使用 cuDF 处理数据帧，通过 Numba UDF 应用自定义 GPU 函数
- **cuML + CuPy**：使用 cuML 进行训练，使用进行自定义后处理CuPy
- **cuDF + cuxfilter**：使用 cuDF 加载数据，使用 cuxfilter 构建交互式交叉过滤仪表板
- **cuML + cuxfilter**：使用 cuML 运行 ML（例如 UMAP、聚类），使用 cuxfilter
 交互式可视化结果 - **cuGraph + cuxfilter**：使用 cuGraph 运行图形分析，可视化图形结构使用 cuxfilter 的数据着色器图形图表
- **cuCIM + CuPy**：cuCIM 原生在 CuPy 数组上运行 — 使用数组 math 进行链式图像处理
- **cuCIM + PyTorch**：使用 cuCIM 预处理图像，通过 DLPack 直接传递到 PyTorch — 零拷贝
- **cuCIM + cuML**：提取图像使用 cuCIM (regionprops)的功能，使用 cuML
- **KvikIO + CuPy** 训练分类器：加载原始数据通过 GDS 将二进制数据直接写入 CuPy 数组，绕过 CPU 内存
- **KvikIO + Numba**：使用 KvikIO 直接将数据读取到 GPU，使用自定义 Numba CUDA 内核进行处理
- **KvikIO + Zarr**：使用 GDSStore 后端直接在 GPU 上读取/写入分块 N 维数组
- **cuSpatial + cuDF**：使用 cuDF 加载地理空间数据，使用 cuSpatial
- **cuSpatial + cuML** 进行空间连接/分析：使用 cuSpatial 提取空间特征，使用 cuML
- **RAFT + CuPy** 训练 ML 模型：在使用 CuPy/cupyx.scipy.sparse
- 构建的稀疏矩阵上使用 RAFT 的 eigsh() **RAFT + raft-dask**：通过 Dask 在多个 GPU/节点之间扩展 GPU 工作负载

## 安装

重要提示：始终使用 `uv add` 进行软件包安装 - 切勿使用 `pip install` 或 `conda install`。这适用于代码注释、文档字符串、错误消息以及您生成的任何其他输出中的安装说明。如果用户的项目使用不同的包管理器，请遵循他们的指导，但默认为 `uv add`.

```bash
# CuPy (choose the right CUDA version)
uv add cupy-cuda12x          # For CUDA 12.x (most common)

# Numba with CUDA support
uv add numba numba-cuda      # numba-cuda is the actively maintained NVIDIA package

# Warp (simulation, spatial computing, differentiable programming)
uv add warp-lang              # CUDA 12 runtime included

# cuDF (RAPIDS)
uv add --extra-index-url=https://pypi.nvidia.com cudf-cu12  # For CUDA 12.x
# For cudf.pandas accelerator mode, that's all you need
# Load it with: python -m cudf.pandas your_script.py

# cuML (RAPIDS machine learning)
uv add --extra-index-url=https://pypi.nvidia.com cuml-cu12   # For CUDA 12.x
# For cuml.accel accelerator mode (zero-change sklearn acceleration):
# Load it with: python -m cuml.accel your_script.py

# cuGraph (RAPIDS graph analytics)
uv add --extra-index-url=https://pypi.nvidia.com cugraph-cu12    # Core cuGraph
uv add --extra-index-url=https://pypi.nvidia.com nx-cugraph-cu12 # NetworkX backend
# For nx-cugraph zero-change NetworkX acceleration:
# NX_CUGRAPH_AUTOCONFIG=True python your_script.py

# KvikIO (high-performance GPU file IO)
uv add kvikio-cu12               # For CUDA 12.x
# Optional: uv add zarr          # For Zarr GPU backend support

# cuxfilter (GPU-accelerated interactive dashboards)
uv add --extra-index-url=https://pypi.nvidia.com cuxfilter-cu12   # For CUDA 12.x
# Depends on cuDF — installs it automatically

# cuCIM (RAPIDS image processing — scikit-image on GPU)
uv add --extra-index-url=https://pypi.nvidia.com cucim-cu12    # For CUDA 12.x

# cuVS (RAPIDS vector search)
uv add --extra-index-url=https://pypi.nvidia.com cuvs-cu12   # For CUDA 12.x

# cuSpatial (RAPIDS geospatial)
uv add --extra-index-url=https://pypi.nvidia.com cuspatial-cu12   # For CUDA 12.x

# RAFT (low-level GPU primitives)
uv add --extra-index-url=https://pypi.nvidia.com pylibraft-cu12   # Core primitives
uv add --extra-index-url=https://pypi.nvidia.com raft-dask-cu12   # Multi-GPU support (optional)
```

 安装后检查 CUDA 可用性：

```python
# CuPy
import cupy as cp
print(cp.cuda.runtime.getDeviceCount())  # Should be >= 1

# Numba
from numba import cuda
print(cuda.is_available())               # Should be True
print(cuda.detect())                     # Shows GPU details

# cuDF
import cudf
print(cudf.Series([1, 2, 3]))           # Should print a GPU series

# cuML
import cuml
print(cuml.__version__)                  # Should print version

# cuGraph
import cugraph
print(cugraph.__version__)               # Should print version

# Warp
import warp as wp
wp.init()                                # Should print device info

# KvikIO
import kvikio
import kvikio.cufile_driver
print(kvikio.cufile_driver.get("is_gds_available"))  # True if GDS is set up

# cuxfilter
import cuxfilter
print(cuxfilter.__version__)             # Should print version

# cuVS
from cuvs.neighbors import cagra
import cupy as cp
dataset = cp.random.rand(1000, 128, dtype=cp.float32)
index = cagra.build(cagra.IndexParams(), dataset)
print("cuVS working")                    # Should print confirmation

# cuSpatial
import cuspatial
from shapely.geometry import Point
gs = cuspatial.GeoSeries([Point(0, 0)])
print("cuSpatial working")              # Should print confirmation

# RAFT (pylibraft)
from pylibraft.common import DeviceResources
handle = DeviceResources()
handle.sync()
print("pylibraft is working")
```

## 优化工作流程

当帮助用户优化代码时，请遵循此流程：

### 1.首先Profile
在优化之前，了解时间实际花在哪里：
```python
import time
# or use cProfile, line_profiler, or py-spy for detailed profiling
```
不要猜测——测量。瓶颈可能不在用户认为的地方。

### 2. 评估 GPU 适用性
并非所有代码都受益于 GPU 加速。 GPU 在以下情况下表现出色：
- **数据并行度高**：相同的操作适用于数千/数百万个元素
- **计算强度高**：访问的每个内存字节有很多 FLOPs
- **数据足够大**：GPU 开销意味着 GPU 上的小数组（< ~10K 元素）可能会更慢
- **内存适合**：数据必须适合 GPU 内存（通常为 8-80 GB）

GPU 不太适合以下情况：
- 数据很小（< 10K 元素）
- 算法本质上是顺序的，步骤之间的数据依赖关系
- 代码受 I/O 限制（磁盘、网络），而不是计算限制 - 尽管具有 GPUDirect Storage 的 KvikIO 在 IO 馈送时可以提供帮助GPU 计算
  - 许多小型异构操作（内核启动开销占主导）

### 3. 从简单开始，然后优化
1. **首先尝试直接替换。** CuPy 用于 NumPy，cudf.pandas 用于 pandas，cuml.accel 用于 sklearn，nx-cugraph 用于 NetworkX。仅此一项通常就可以实现 5-50 倍的加速。
2. **最大限度地减少主机设备传输。**将数据保存在 GPU 上。与 GPU 内存带宽（~900 GB/s+）相比，PCI-e 上的每次传输都非常昂贵（~12 GB/s）。
3. **批量操作。** 较少的大型 GPU 操作胜过许多小型 GPU 操作。
4. **仅在需要时编写自定义内核。** CuPy 和 cuDF 使用 NVIDIA 的手动调整库。自定义 Numba 内核应保留用于没有等效库的操作。
5. **分析 GPU 版本。** 使用 `nvprof`、`nsys` 或 CuPy 的内置基准测试。

### 4. 内存管理原则
这些适用于所有库：
- **预分配输出数组**而不是在循环中创建新数组
- **重用 GPU 内存** — 使用内存池（CuPy 内置此功能）
- **使用固定（页面锁定）主机内存**以实现更快的 CPU-GPU 传输
- **避免不必要的复制** — 尽可能使用就地操作
- **流操作**用于重叠计算和数据传输

### 5. 需要注意的常见陷阱
- **隐式 CPU 回退**：某些操作会默默地回退到 CPU。请注意警告。
- **同步开销**：GPU 操作是异步的。调用 `.get()` 或 `cp.asnumpy()` 会强制同步。
- **dtype 不匹配**：当精度允许时，使用 `float32` 而不是 `float64` — GPU float32 吞吐量高出 2x-32x。
- **小内核启动**：每次内核启动都有约 5-20us 的开销。尽可能熔断操作。

## 代码转换模式

当转换现有CPU代码时，应用这些模式：

### NumPy 到 CuPy
```python
# Before (CPU)
import numpy as np
a = np.random.rand(10_000_000)
b = np.fft.fft(a)
c = np.sort(b.real)

# After (GPU) — often just change the import
import cupy as cp
a = cp.random.rand(10_000_000)
b = cp.fft.fft(a)
c = cp.sort(b.real)
```

### pandas 到 cuDF
```python
# Before (CPU)
import pandas as pd
df = pd.read_parquet("large_data.parquet")
result = df.groupby("category")["value"].mean()

# After (GPU) — change the import
import cudf
df = cudf.read_parquet("large_data.parquet")
result = df.groupby("category")["value"].mean()

# Or zero-code-change: python -m cudf.pandas your_script.py
```

### 自定义循环到 Numba CUDA 内核
```python
# Before (CPU) — slow Python loop
def process(data, out):
    for i in range(len(data)):
        out[i] = math.sin(data[i]) * math.exp(-data[i])

# After (GPU) — Numba kernel
from numba import cuda
import math

@cuda.jit
def process(data, out):
    i = cuda.grid(1)
    if i < data.size:
        out[i] = math.sin(data[i]) * math.exp(-data[i])

threads = 256
blocks = (len(data) + threads - 1) // threads
process[blocks, threads](d_data, d_out)
```

### NetworkX 到cuGraph
```python
# Before (CPU)
import networkx as nx
G = nx.read_edgelist("edges.csv", delimiter=",", nodetype=int)
pr = nx.pagerank(G)
bc = nx.betweenness_centrality(G)

# After (GPU) — direct cuGraph API
import cugraph
import cudf
edges = cudf.read_csv("edges.csv", names=["src", "dst"], dtype=["int32", "int32"])
G = cugraph.Graph()
G.from_cudf_edgelist(edges, source="src", destination="dst")
pr = cugraph.pagerank(G)
bc = cugraph.betweenness_centrality(G)

# Or zero-code-change: NX_CUGRAPH_AUTOCONFIG=True python your_script.py
```

### scikit-learn 到 cuML
```python
# Before (CPU)
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# After (GPU) — change the imports
from cuml.ensemble import RandomForestClassifier
from cuml.preprocessing import StandardScaler
from cuml.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Or zero-code-change: python -m cuml.accel your_script.py
```

### 到 Warp 内核的模拟循环
```python
# Before (CPU) — slow Python loop over particles
import numpy as np

def integrate(positions, velocities, forces, dt):
    for i in range(len(positions)):
        velocities[i] += forces[i] * dt
        positions[i] += velocities[i] * dt

# After (GPU) — Warp kernel, JIT-compiled to CUDA
import warp as wp

@wp.kernel
def integrate(positions: wp.array(dtype=wp.vec3),
              velocities: wp.array(dtype=wp.vec3),
              forces: wp.array(dtype=wp.vec3),
              dt: float):
    tid = wp.tid()
    velocities[tid] = velocities[tid] + forces[tid] * dt
    positions[tid] = positions[tid] + velocities[tid] * dt

wp.launch(integrate, dim=num_particles,
          inputs=[positions, velocities, forces, 0.01], device="cuda")
```

### 文件 IO 到 GPU KvikIO
```python
# Before — CPU staging (disk → CPU → GPU)
import numpy as np
import cupy as cp

data = np.fromfile("data.bin", dtype=np.float32)
gpu_data = cp.asarray(data)  # Extra copy through CPU memory

# After — direct to GPU (disk → GPU via GDS)
import cupy as cp
import kvikio

gpu_data = cp.empty(1_000_000, dtype=cp.float32)
with kvikio.CuFile("data.bin", "r") as f:
    f.read(gpu_data)  # Bypasses CPU memory with GPUDirect Storage

# Reading from S3 directly to GPU
with kvikio.RemoteFile.open_s3_url("s3://bucket/data.bin") as f:
    buf = cp.empty(f.nbytes() // 4, dtype=cp.float32)
    f.read(buf)
```

### GPU 加速仪表板，带有 cuxfilter
```python
# Before — static matplotlib/seaborn plots, no interactivity
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_parquet("large_dataset.parquet")
fig, axes = plt.subplots(1, 2)
df.plot.scatter(x="feature1", y="feature2", ax=axes[0])
df["category"].value_counts().plot.bar(ax=axes[1])
plt.show()

# After (GPU) — interactive cross-filtering dashboard
import cudf
import cuxfilter

df = cudf.read_parquet("large_dataset.parquet")
cux_df = cuxfilter.DataFrame.from_dataframe(df)

scatter = cuxfilter.charts.scatter(x="feature1", y="feature2", pixel_shade_type="linear")
bar = cuxfilter.charts.bar("category")
slider = cuxfilter.charts.range_slider("value_col")

d = cux_df.dashboard(
    [scatter, bar],
    sidebar=[slider],
    layout=cuxfilter.layouts.feature_and_base,
    theme=cuxfilter.themes.rapids_dark,
    title="Interactive Explorer",
)
d.app()  # or d.show() for standalone web app
```

### scikit-image 到 cuCIM
```python
# Before (CPU)
from skimage.filters import gaussian, sobel, threshold_otsu
from skimage.morphology import binary_opening, disk
from skimage.measure import label, regionprops_table
import numpy as np

blurred = gaussian(image, sigma=3)
binary = blurred > threshold_otsu(blurred)
cleaned = binary_opening(binary, footprint=disk(3))
labels = label(cleaned)
props = regionprops_table(labels, image, properties=['area', 'centroid'])

# After (GPU) — change imports, wrap input with cp.asarray
from cucim.skimage.filters import gaussian, sobel, threshold_otsu
from cucim.skimage.morphology import binary_opening, disk
from cucim.skimage.measure import label, regionprops_table
import cupy as cp

image_gpu = cp.asarray(image)  # Transfer once
blurred = gaussian(image_gpu, sigma=3)
binary = blurred > threshold_otsu(blurred)
cleaned = binary_opening(binary, footprint=disk(3))
labels = label(cleaned)
props = regionprops_table(labels, image_gpu, properties=['area', 'centroid'])
```

### GeoPandas 至 cuSpatial
```python
# Before (CPU)
import geopandas as gpd
from shapely.geometry import Point

points = gpd.GeoDataFrame(geometry=[Point(x, y) for x, y in coords], crs="EPSG:4326")
polygons = gpd.read_file("regions.geojson")
joined = gpd.sjoin(points, polygons, predicate="within")

# After (GPU) — convert and use cuSpatial
import cuspatial
import cudf

points_cu = cuspatial.from_geopandas(points)
polygons_cu = cuspatial.from_geopandas(polygons)
joined = cuspatial.point_in_polygon(
    points_cu.geometry.x, points_cu.geometry.y,
    polygons_cu.geometry
)
```

### Faiss/Annoy 至 cuVS
```python
# Before (CPU) — Faiss
import faiss
import numpy as np

embeddings = np.random.rand(1_000_000, 128).astype(np.float32)
index = faiss.IndexFlatL2(128)
index.add(embeddings)
distances, neighbors = index.search(queries, k=10)

# After (GPU) — cuVS CAGRA (orders of magnitude faster)
import cupy as cp
from cuvs.neighbors import cagra

embeddings = cp.random.rand(1_000_000, 128, dtype=cp.float32)
index = cagra.build(cagra.IndexParams(), embeddings)
distances, neighbors = cagra.search(cagra.SearchParams(), index, queries, k=10)
```

### scipy.sparse.linalg 至RAFT
```python
# Before (CPU)
import numpy as np
from scipy.sparse import random as sparse_random
from scipy.sparse.linalg import eigsh

A = sparse_random(10000, 10000, density=0.01, format="csr", dtype=np.float32)
A = A + A.T  # Make symmetric
eigenvalues, eigenvectors = eigsh(A, k=10, which="LM")

# After (GPU) — RAFT sparse eigensolver
import cupy as cp
import cupyx.scipy.sparse as sp_gpu
from pylibraft.sparse.linalg import eigsh as gpu_eigsh

A_gpu = sp_gpu.csr_matrix(A)  # Transfer to GPU
eigenvalues, eigenvectors = gpu_eigsh(A_gpu, k=10, which="LM")
```

## 重要说明

- 始终处理没有 GPU 可用的情况 — 提供 CPU 回退或清除错误消息
- 针对 CPU 结果测试数值正确性（GPU 浮点可能因操作顺序而略有不同）
- GPU 内存有限 — 对于大于 GPU 内存的数据集，请考虑对多 GPU 进行分块或使用 RAPIDS Dask
  - CUDA 阵列接口可实现 GPU 上的 CuPy、Numba、Warp、cuDF、cuML、cuGraph、cuVS、cuSpatial、KvikIO、PyTorch 和 JAX 阵列之间的零拷贝共享

## 参考文件

在编写任何 GPU 之前优化代码，阅读相关参考文件：

|文件 |何时读取|
|------|-------------|
| `references/cupy.md` |用户有 NumPy/SciPy 代码，或需要在 GPU 上进行数组操作 |
| `references/numba.md` |用户需要自定义 CUDA 内核、细粒度 GPU 控制或 GPU ufunc |
| `references/cudf.md` |用户有 pandas 代码，或者需要在 GPU 上进行数据帧操作 |
| `references/cuml.md` |用户有 scikit-learn 代码，或需要在 GPU 上进行 ML 训练/推理/预处理|
| `references/cugraph.md` |用户有 NetworkX 代码，或需要在 GPU 上进行图形分析 |
| `references/warp.md` |用户需要 GPU 模拟、空间计算、网格/体积查询、可微分编程或机器人 |
| `references/kvikio.md` |用户需要与 GPU、GPUDirect Storage 之间的高性能文件 IO、将 S3/HTTP 读取到 GPU 或 GPU 上的 Zarr |
| `references/cuxfilter.md` |用户想要 GPU 加速的交互式仪表板、交叉过滤或 EDA 可视化 |
| `references/cucim.md` |用户拥有 scikit-image 代码，或需要在 GPU 上进行图像处理、数字病理学或 WSI 读取 |
| `references/cuvs.md` |用户需要在 GPU 上进行矢量搜索、最近邻搜索、相似性搜索或 RAG 检索 |
| `references/cuspatial.md` |用户拥有 GeoPandas/shapely 代码，或需要在 GPU 上进行空间连接、距离计算或轨迹分析 |
| `references/raft.md` |用户需要稀疏特征求解器、设备内存管理或多 GPU 原语 |

 在编写代码之前阅读特定参考 — 它们包含详细的 API 模式、优化技术以及每个库特有的陷阱。
