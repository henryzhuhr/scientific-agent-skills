# cuVS 参考

cuVS 是 NVIDIA 用于向量搜索和聚类的 GPU 加速库，是 RAPIDS 生态系统的一部分。它在 GPU 上提供最先进的近似最近邻 (ANN)搜索算法实现，比基于 CPU 的库（如 Faiss（CPU 模式）、Annoy 和 scikit-learn 用于高维向量搜索的 NearestNeighbors）提供数量级的加速。

> **完整文档：** https://docs.rapids.ai/api/cuvs/stable/

## 目录

1. [安装和设置](#installation-and-setup)
2. [何时使用 cuVS](#when-to-use-cuvs)
3. [索引选择指南](#index-selection-guide)
4. [CAGRA — 基于图形的索引](#cagra)
5. [IVF-Flat — 倒排文件索引](#ivf-flat)
6. [IVF-PQ — 压缩倒排文件索引](#ivf-pq)
7. [暴力破解——精确搜索](#brute-force)
8. [HNSW — 从 GPU 索引中搜索 CPU](#hnsw)
9. [距离指标](#distance-metrics)
10. [过滤](#filtering)
11. [多 GPU](#multi-gpu)
12. [内存和性能](#内存和性能)
13. [互操作性](#互操作性)
14. [常见模式](#common-patterns)

- --

## 安装和设置

在所有安装说明、文档字符串、注释和错误中始终使用 `uv add`（切勿使用 `pip install` 或 `conda install`） messages.

```bash
uv add --extra-index-url=https://pypi.nvidia.com cuvs-cu12   # For CUDA 12.x
```

* *平台：**仅限 Linux 和 WSL2（无本机 macOS 或 Windows）。
* *需要：**支持 CUDA 12.x 的 NVIDIA GPU，建议 GPU 使用 CuPy arrays.

Verify:
```python
from cuvs.neighbors import cagra
import cupy as cp

dataset = cp.random.rand(1000, 128, dtype=cp.float32)
index = cagra.build(cagra.IndexParams(), dataset)
print("cuVS working — built CAGRA index")
```

- --

## 何时使用 cuVS

当用户需要以下功能时，cuVS 是正确的工具：
- **高维向量（嵌入）上的最近邻搜索**
- **用于 RAG、推荐系统、图像/文本/音频检索的相似性搜索**
- **用于聚类或可视化管道的 k-NN 图构建**
- **矢量数据库后端** — cuVS 提供搜索功能在 Milvus、Lucene、Kinetica 和 Faiss GPU 中
- **使用 GPU 加速替换 Faiss、Annoy、ScaNN 或 sklearn NearestNeighbors**

cuVS 不是以下的正确工具：
- 一般机器学习（使用 cuML 代替）
- 具有小数据集的低维数据（< ~16 维） （< 10K 向量）
- 仅 CPU 环境，没有可用的 GPU

- --

## 索引选择指南

|索引 |最适合 |构建速度|搜索速度|内存|精度|
|--------|---------|-------------|--------------|--------|----------|
| **卡格拉** |默认选择 - 快速构建和搜索 |快|最快|中等|高|
| **IVF-扁平** |当精确距离很重要时 |中等|快|高（存储完整向量）|非常高|
| **IVF-PQ** | GPU 内存无法容纳的大型数据集 |中等|快|低（压缩）|好|
| **蛮力** |小数据集或地面实况 |不适用 |规模缓慢 |高|准确|
| **新南威尔士州** |来自 GPU 构建索引的 CPU 端服务 |慢|快速（CPU）|中等|高 |

* *从 CAGRA 开始**，除非您有特定原因不这样做。它是最快的 GPU 原生算法，适用于大多数用例。当内存紧张时使用 IVF-PQ，当需要更高的精度时使用 IVF-Flat，对于小数据集或验证则使用暴力破解。

- --

## CAGRA

CAGRA（基于 CUDA 加速图）是针对 GPU 优化的基于图的 ANN 索引。对于大多数工作负载来说，这是最快的选项。

### Build

```python
import cupy as cp
from cuvs.neighbors import cagra

n_samples = 1_000_000
n_features = 128
dataset = cp.random.rand(n_samples, n_features, dtype=cp.float32)

# Default parameters work well for most cases
index_params = cagra.IndexParams(
    metric="sqeuclidean",             # "sqeuclidean", "inner_product", "cosine"
    intermediate_graph_degree=128,     # Higher = better quality, slower build
    graph_degree=64,                   # Final graph degree (lower = less memory)
    build_algo="ivf_pq",              # "ivf_pq", "nn_descent", or "ace"
)

index = cagra.build(index_params, dataset)
```

### 搜索

```python
from cuvs.common import Resources

queries = cp.random.rand(1000, n_features, dtype=cp.float32)

search_params = cagra.SearchParams(
    itopk_size=64,       # Intermediate top-k (higher = more accurate, slower)
    search_width=1,      # Starting nodes per iteration
    max_iterations=0,    # 0 = auto
    algo="auto",         # "auto", "single_cta", "multi_cta", "multi_kernel"
)

resources = Resources()
distances, neighbors = cagra.search(
    search_params, index, queries, k=10, resources=resources
)
resources.sync()

# distances: shape (1000, 10) — squared Euclidean distances
# neighbors: shape (1000, 10) — indices into original dataset
```

### 保存/加载

```python
cagra.save("my_index.cagra", index)
loaded_index = cagra.load("my_index.cagra")
```

### 延长

```python
new_data = cp.random.rand(10_000, n_features, dtype=cp.float32)
extended_index = cagra.extend(cagra.ExtendParams(), index, new_data)
```

### 带压缩（对于大型数据集）

```python
from cuvs.neighbors.cagra import CompressionParams

index_params = cagra.IndexParams(
    compression=CompressionParams(
        pq_bits=8,
        pq_dim=64,
    )
)
index = cagra.build(index_params, dataset)
```

- --

## IVF-Flat

IVF-Flat 将数据集划分为簇（反向文件）并存储完整向量。比 IVF-PQ 精度更高，但占用更多内存。

### Build

```python
from cuvs.neighbors import ivf_flat

build_params = ivf_flat.IndexParams(
    n_lists=1024,                    # Number of clusters (sqrt(n_samples) is a good start)
    metric="sqeuclidean",            # "sqeuclidean", "euclidean", "inner_product", "cosine"
    kmeans_trainset_fraction=0.5,    # Fraction of data used for k-means training
    kmeans_n_iters=20,               # K-means iterations
    add_data_on_build=True,          # Add vectors during build (vs. extend later)
)

index = ivf_flat.build(build_params, dataset)
```

### Search

```python
search_params = ivf_flat.SearchParams(
    n_probes=50,    # Clusters to search (higher = more accurate, slower)
)

distances, neighbors = ivf_flat.search(
    search_params, index, queries, k=10
)
```

### 保存/加载/ Extend

```python
ivf_flat.save("my_index.ivf_flat", index)
loaded_index = ivf_flat.load("my_index.ivf_flat")

# Extend with new data
import numpy as np
new_vectors = cp.random.rand(5000, n_features, dtype=cp.float32)
new_indices = cp.arange(n_samples, n_samples + 5000, dtype=cp.int64)
ivf_flat.extend(index, new_vectors, new_indices)
```

- --

## IVF-PQ

IVF-PQ 使用乘积量化来压缩向量，从而显着减少内存使用量。最适合不适合包含完整向量的 GPU 内存的大型数据集。

### Build

```python
from cuvs.neighbors import ivf_pq

build_params = ivf_pq.IndexParams(
    n_lists=1024,                # Number of clusters
    metric="sqeuclidean",        # "sqeuclidean", "inner_product"
    pq_bits=8,                   # Bits per subquantizer (4 or 8)
    pq_dim=0,                    # PQ dimensions (0 = auto, typically dim/4)
    codebook_kind="subspace",    # "subspace" or "cluster"
    kmeans_n_iters=20,
    add_data_on_build=True,
)

index = ivf_pq.build(build_params, dataset)
```

### Search

```python
search_params = ivf_pq.SearchParams(
    n_probes=50,                     # Clusters to search
    lut_dtype="float32",             # Look-up table precision
    internal_distance_dtype="float32",
)

distances, neighbors = ivf_pq.search(
    search_params, index, queries, k=10
)
```

### 保存/加载/ Extend

```python
ivf_pq.save("my_index.ivf_pq", index)
loaded_index = ivf_pq.load("my_index.ivf_pq")

# Extend
new_vectors = cp.random.rand(5000, n_features, dtype=cp.float32)
new_indices = cp.arange(n_samples, n_samples + 5000, dtype=cp.int64)
ivf_pq.extend(index, new_vectors, new_indices)
```

- --

## Brute Force

Exact k-NN 搜索 — 计算所有距离。用于小型数据集（< 50K 向量）或生成地面实况来评估近似索引。

```python
from cuvs.neighbors import brute_force

# Build (just stores the dataset)
index = brute_force.build(dataset, metric="sqeuclidean")

# Search
distances, neighbors = brute_force.search(index, queries, k=10)

# Save / Load
brute_force.save("bf_index.bin", index)
loaded = brute_force.load("bf_index.bin")
```

- --

## HNSW

cuVS 为 CPU 端搜索提供 HNSW 实现。典型的工作流程是：在GPU上构建CAGRA索引，将其转换为HNSW以供CPU服务。这使您可以在从 CPU 提供服务的同时利用 GPU 速度进行构建（当 GPU 在查询时不可用时很有用）。

```python
from cuvs.neighbors import cagra, hnsw
import numpy as np

# Build CAGRA on GPU
dataset_gpu = cp.random.rand(100_000, 128, dtype=cp.float32)
cagra_index = cagra.build(cagra.IndexParams(), dataset_gpu)

# Convert to HNSW for CPU search
hnsw_index = hnsw.from_cagra(hnsw.IndexParams(), cagra_index)

# Search on CPU with numpy queries
queries_cpu = np.random.rand(100, 128).astype(np.float32)
search_params = hnsw.SearchParams(
    ef=200,           # Search depth (higher = more accurate, slower)
    num_threads=0,    # 0 = auto (uses all available threads)
)
distances, neighbors = hnsw.search(search_params, hnsw_index, queries_cpu, k=10)

# Save / Load
hnsw.save("my_index.hnsw", hnsw_index)
loaded = hnsw.load(hnsw.IndexParams(), "my_index.hnsw", dim=128,
                    dtype=np.float32, metric="sqeuclidean")
```

### 可扩展 HNSW

要在构建后添加向量，请使用`hierarchy="cpu"`:

```python
hnsw_index = hnsw.from_cagra(hnsw.IndexParams(hierarchy="cpu"), cagra_index)

new_data = np.random.rand(5000, 128).astype(np.float32)
hnsw.extend(hnsw.ExtendParams(), hnsw_index, new_data)
```

- --

## 距离度量

|公制|字符串|注释 |
|--------|--------|--------|
|欧几里得平方 | `"sqeuclidean"` |默认。最快 — 避免 sqrt。 |
|欧几里得| `"euclidean"` | L2距离|
|内积| `"inner_product"` |对于归一化嵌入（通过点积的余弦相似度）|
|余弦 | `"cosine"` | CAGRA 和 IVF-Flat 支持 |

 对于与 IVF-PQ 的余弦相似度，将向量归一化为单位长度并使用 `"inner_product"`。

- --

## 过滤

cuVS 支持使用位图或位集预过滤搜索结果，以排除特定向量。

```python
from cuvs.neighbors import brute_force
import cupy as cp

# Bitset filter: exclude specific indices from ALL queries
# 1 = excluded, 0 = included
n_samples = 100_000
bitset = cp.zeros(n_samples, dtype=cp.uint8)
bitset[0:1000] = 1  # Exclude first 1000 vectors

distances, neighbors = brute_force.search(
    index, queries, k=10, prefilter=bitset
)
```

CAGRA还支持通过`cagra.search()`中的`filter`参数进行过滤。

- --

## 多GPU

对于单个GPU来说太大的数据集，请使用多GPU API：

```python
from cuvs.neighbors.mg import cagra as mg_cagra

# Build across all available GPUs
build_params = mg_cagra.IndexParams(
    intermediate_graph_degree=64,
    graph_degree=32,
)
index = mg_cagra.build(build_params, dataset)

# Search across GPUs
search_params = mg_cagra.SearchParams()
distances, neighbors = mg_cagra.search(search_params, index, queries, k=10)
```

多GPU也可通过`cuvs.neighbors.mg`用于IVF-Flat和IVF-PQ。

- --

## 内存和性能

### 支持的数据类型

所有索引类型支持：`float32`， `float16`、`int8`、`uint8`。

 使用 `float16` 可以将内存减半，并且在不需要完整的 float32 精度时可以加快构建和搜索速度（常见于嵌入）。

### 性能提示

1. **使用 CuPy 数组作为输入。** NumPy 数组可以工作，但会触发 CPU 到 GPU 的传输。如果您的向量已经在 GPU 上（来自模型或管道），请直接传递它们。

2. **调整搜索参数，而不仅仅是构建参数。** 最大的精度/速度权衡是在搜索时：
  - CAGRA：增加 `itopk_size`（默认 64）
  - IVF-Flat/IVF-PQ：增加 `n_probes`（默认 20）
  - HNSW：增加`ef`（默认200）

3. **使用 float16 进行嵌入。** 大多数嵌入模型输出 float32，但额外的精度对于相似性搜索很少有影响。转换为 float16 以使吞吐量加倍。

4. **n_lists IVF 索引调整。** `sqrt(n_samples)` 是一个很好的起点。列表太少=搜索速度慢，太多=回忆能力差。

5. **批量查询。** GPU 吞吐量随批量大小而变化。一次搜索 1000 个查询比 1000 个单独搜索要高效得多。

6. **重用资源句柄。** 创建一个 `Resources()` 对象并将其传递给所有构建/搜索调用 - 它管理 CUDA 流和内存。

### Memory Estimates

- **暴力破解：** `n_samples * dim * dtype_size`（完整数据集）
- **IVF-Flat：** 类似于暴力破解 + 集群开销
- **IVF-PQ:** `n_samples * pq_dim * pq_bits / 8`（重度压缩）
- **CAGRA:** `n_samples * (dim * dtype_size + graph_degree * 4)`（数据集 + graph)

- --

## 互操作性

- **CuPy:** 本机输入 — 通过 `__cuda_array_interface__`
- **NumPy:** 接受作为输入（自动传输到 GPU 进行 GPU 索引，直接用于 HNSW）
- **PyTorch / TensorFlow:** 通过接受的张量CUDA 数组接口 — 无需复制
- **cuDF:** 在传递给 cuVS
- **Faiss:** cuVS 为 Faiss GPU 提供支持之前，使用 `.values` 将列转换为 CuPy；对于直接使用，cuVS 提供了更多控制权
- **矢量数据库：** cuVS 集成到 Milvus、Lucene 和 Kinetica

### 端到端 RAG 管道示例

```python
import cupy as cp
from cuvs.neighbors import cagra

# Assume embeddings come from a model (e.g., sentence-transformers on GPU)
document_embeddings = cp.array(embeddings, dtype=cp.float32)  # (n_docs, 768)

# Build index
index_params = cagra.IndexParams(metric="inner_product")
index = cagra.build(index_params, document_embeddings)
cagra.save("doc_index.cagra", index)

# At query time
query_embedding = cp.array(encode("user question"), dtype=cp.float32).reshape(1, -1)
search_params = cagra.SearchParams(itopk_size=128)
distances, neighbors = cagra.search(search_params, index, query_embedding, k=20)

# neighbors[0] contains the indices of the top-20 most similar documents
top_doc_ids = neighbors[0].get()  # Transfer to CPU
```

- --

## 常见模式

### 模式 1：快速 ANN 搜索 (CAGRA)

```python
import cupy as cp
from cuvs.neighbors import cagra

dataset = cp.random.rand(500_000, 128, dtype=cp.float32)
queries = cp.random.rand(1000, 128, dtype=cp.float32)

index = cagra.build(cagra.IndexParams(), dataset)
distances, neighbors = cagra.search(cagra.SearchParams(), index, queries, k=10)
```

### 模式 2：内存高效搜索 (IVF-PQ)

```python
import cupy as cp
from cuvs.neighbors import ivf_pq

dataset = cp.random.rand(10_000_000, 256, dtype=cp.float32)

# PQ compresses vectors — uses ~32x less memory than brute force
params = ivf_pq.IndexParams(n_lists=4096, pq_bits=8, pq_dim=64)
index = ivf_pq.build(params, dataset)

search_params = ivf_pq.SearchParams(n_probes=100)
distances, neighbors = ivf_pq.search(search_params, index, queries, k=10)
```

### 模式 3：GPU 构建、CPU 服务 (CAGRA → HNSW)

```python
import cupy as cp
import numpy as np
from cuvs.neighbors import cagra, hnsw

# Build on GPU (fast)
dataset = cp.random.rand(1_000_000, 128, dtype=cp.float32)
gpu_index = cagra.build(cagra.IndexParams(), dataset)

# Convert to HNSW for CPU serving
cpu_index = hnsw.from_cagra(hnsw.IndexParams(), gpu_index)
hnsw.save("serving_index.hnsw", cpu_index)

# At serving time (no GPU needed)
loaded = hnsw.load(hnsw.IndexParams(), "serving_index.hnsw",
                    dim=128, dtype=np.float32)
queries = np.random.rand(100, 128).astype(np.float32)
distances, neighbors = hnsw.search(
    hnsw.SearchParams(ef=200), loaded, queries, k=10
)
```

### 模式 4：使用暴力验证

```python
from cuvs.neighbors import brute_force, cagra

# Ground truth
bf_index = brute_force.build(dataset)
gt_distances, gt_neighbors = brute_force.search(bf_index, queries, k=10)

# Approximate
cagra_index = cagra.build(cagra.IndexParams(), dataset)
approx_distances, approx_neighbors = cagra.search(
    cagra.SearchParams(), cagra_index, queries, k=10
)

# Compute recall
recall = sum(
    len(set(gt_neighbors[i].get()) & set(approx_neighbors[i].get())) / 10
    for i in range(len(queries))
) / len(queries)
print(f"Recall@10: {recall:.4f}")
```

### 模式 5：余弦相似度Search

```python
import cupy as cp
from cuvs.neighbors import cagra

# Normalize embeddings to unit length
embeddings = cp.random.rand(100_000, 768, dtype=cp.float32)
norms = cp.linalg.norm(embeddings, axis=1, keepdims=True)
embeddings_normalized = embeddings / norms

# Use inner_product on normalized vectors = cosine similarity
index = cagra.build(
    cagra.IndexParams(metric="inner_product"),
    embeddings_normalized,
)

query = cp.random.rand(1, 768, dtype=cp.float32)
query_normalized = query / cp.linalg.norm(query)

distances, neighbors = cagra.search(
    cagra.SearchParams(), index, query_normalized, k=10
)
```

- --

## 超越邻居：聚类、距离和预处理

cuVS 还提供 GPU 加速的聚类、成对距离和量化 — 向量搜索管道中有用的构建块。

### K-Means聚类

```python
import cupy as cp
from cuvs.cluster.kmeans import fit, predict, KMeansParams

X = cp.random.rand(100_000, 128, dtype=cp.float32)

params = KMeansParams(
    n_clusters=256,
    init_method="KMeansPlusPlus",   # or "Random", "Array"
    max_iter=300,
    tol=1e-4,
)
centroids, inertia, n_iter = fit(params, X)
labels, inertia = predict(params, X, centroids)
```

对于大于GPU内存的数据集，使用`streaming_batch_size`传递NumPy数组：

```python
import numpy as np
from cuvs.cluster.kmeans import fit, KMeansParams

X_host = np.random.rand(10_000_000, 128).astype(np.float32)
params = KMeansParams(n_clusters=1000, streaming_batch_size=1_000_000)
centroids, inertia, n_iter = fit(params, X_host)
```

### Pairwise距离

```python
from cuvs.distance import pairwise_distance

# Supports: euclidean, l2, l1, inner_product, cosine, chebyshev,
# canberra, hellinger, jensenshannon, kl_divergence, correlation, minkowski
output = pairwise_distance(X, Y, metric="euclidean")
```

### 量化（预处理）

量化在索引之前压缩向量，减少内存并通常提高搜索吞吐量。

* *标量量化** (float32 → int8):
```python
from cuvs.preprocessing.quantize import scalar

params = scalar.QuantizerParams(quantile=0.99)
quantizer = scalar.train(params, dataset)
transformed = scalar.transform(quantizer, dataset)       # int8
reconstructed = scalar.inverse_transform(quantizer, transformed)
```

* *二进制量化** (float32 → uint8 bitpacked):
```python
from cuvs.preprocessing.quantize import binary

transformed = binary.transform(dataset)  # uint8
# Use with metric="bitwise_hamming"
```

* *产品量化**：
```python
from cuvs.preprocessing.quantize import pq

params = pq.QuantizerParams(pq_bits=8, pq_dim=16)
quantizer = pq.build(params, dataset)
transformed, _ = pq.transform(quantizer, dataset)        # uint8
reconstructed = pq.inverse_transform(quantizer, transformed)
```

### NN-Descent（k-NN 图构建）

构建所有邻居 k-NN 图 - 可用作 UMAP、t-SNE 或基于图的聚类的输入。

```python
import cupy as cp
from cuvs.neighbors import nn_descent

dataset = cp.random.rand(100_000, 128, dtype=cp.float32)

build_params = nn_descent.IndexParams(
    metric="sqeuclidean",
    graph_degree=64,
    intermediate_graph_degree=96,   # >= 1.5 * graph_degree
    max_iterations=20,
)
index = nn_descent.build(build_params, dataset)
graph = index.graph  # (n_samples, graph_degree) — the k-NN graph
```
