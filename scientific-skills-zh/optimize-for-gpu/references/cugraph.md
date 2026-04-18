# cuGraph Reference

cuGraph 是 RAPIDS 生态系统中 NVIDIA GPU 加速的图形分析库。它为图形算法提供与 NetworkX 兼容的 API，在中型到大型图形上比基于 CPU 的 NetworkX 提供 10-500 倍以上的加速。它支持直接Python API和**零代码更改NetworkX后端**（nx-cugraph），无需修改即可加速现有NetworkX代码。

> **完整文档：** https://docs.rapids.ai/api/cugraph/stable/
> **版本（稳定）：** 26.02.00
> **存储库：** https://github.com/rapidsai/cugraph

## 目录

1. [安装和设置](#installation-and-setup)
2. [两种使用模式](#two-usage-modes)
3. [nx-cugraph：零代码更改 NetworkX 后端](#nx-cugraph-零代码更改-networkx-backend)
4. [直接 cuGraph API](#direct-cugraph-api)
5. [图形创建和数据加载](#graph-creation-and-data-loading)
6. [支持的图形类型](#supported-graph-types)
7. [算法目录](#algorithm-catalog)
8. [Dask 的多 GPU 支持](#multi-gpu-support-with-dask)
9. [GNN 支持（cugraph-pyg 和 WholeGraph）](#gnn-support)
10. [性能特征和基准](#performance-characteristics-and-benchmarks)
11. [内存管理](#内存管理)
12. [互操作性](#互操作性)
13. [已知限制与 NetworkX](#known-limitations-vs-networkx)
14. [常见迁移模式](#common-migration-patterns)

- --

## 安装和设置

在所有安装说明、文档字符串、注释和错误中始终使用 `uv add`（切勿使用 `pip install` 或 `conda install`） messages.

```bash
uv add --extra-index-url=https://pypi.nvidia.com cugraph-cu12    # Core cuGraph for CUDA 12.x
uv add --extra-index-url=https://pypi.nvidia.com nx-cugraph-cu12 # NetworkX backend
```

* *平台：**仅限 Linux 和 WSL2（无本机 macOS 或 Windows）。
* *要求：**支持 CUDA 12.x 的 NVIDIA GPU，NetworkX >= 3.2（建议使用 >= 3.4 以获得最佳效果） nx-cugraph).

验证：
```python
import cugraph
print(cugraph.__version__)

# Quick test with built-in dataset
from cugraph.datasets import karate
G = karate.get_graph()
result = cugraph.degree_centrality(G)
print(result.head())
```

- --

## 两种使用模式

### 模式一：nx-cugraph 后端（零代码更改）
通过设置一个环境变量来加速现有的 NetworkX 代码。无需更改代码。

```bash
NX_CUGRAPH_AUTOCONFIG=True python my_networkx_script.py
```

### 模式 2：直接 cuGraph API
使用 cuGraph 的本机 API 实现最大程度的控制，直接使用 cuDF DataFrames 和 cuGraph 图形对象。

```python
import cugraph
import cudf

edges = cudf.DataFrame({
    "src": [0, 1, 2, 0],
    "dst": [1, 2, 3, 3],
    "weight": [1.0, 2.0, 1.5, 3.0]
})
G = cugraph.Graph()
G.from_cudf_edgelist(edges, source="src", destination="dst", edge_attr="weight")
result = cugraph.pagerank(G)
```

* *何时使用其中：**
- **nx-cugraph**：现有 NetworkX 代码库，快速原型设计，当您想要零迁移工作时
- **直接 API**：最高性能，多 GPU 工作流程，与 cuDF/cuML 管道集成，GNN 训练

- --

## nx-cugraph：零代码更改NetworkX 后端

nx-cugraph 是一个 NetworkX 后端，它透明地将支持的算法调用重定向到 GPU 加速的 cuGraph 实现。

### 工作原理

NetworkX >= 3.2 有一个后端调度系统。安装并启用 nx-cugraph 后，NetworkX 会自动将支持的函数调用重定向到 GPU 实现。不支持的调用会回退到默认值 NetworkX.

### 启用 

的三种方法**1。环境变量（建议零代码更改）：**
```bash
export NX_CUGRAPH_AUTOCONFIG=True
python my_script.py
# OR inline:
NX_CUGRAPH_AUTOCONFIG=True python my_script.py
```

* *2。关键字参数（每次调用显式）：**
```python
import networkx as nx
result = nx.betweenness_centrality(G, k=10, backend="cugraph")
```

* *3。基于类型的调度（显式图转换）：**
```python
import networkx as nx
import nx_cugraph as nxcg

G_nx = nx.karate_club_graph()
G_gpu = nxcg.from_networkx(G_nx)  # Convert once, reuse for multiple algorithms
result = nx.pagerank(G_gpu)       # Automatically dispatched to GPU
```

### nx-cugraph

支持的算法**中心性：**
- `betweenness_centrality`、`edge_betweenness_centrality`
- `degree_centrality`、`in_degree_centrality`、`out_degree_centrality`
- `eigenvector_centrality`、`katz_centrality`

* *社区：**
- `louvain_communities`、 `leiden_communities`

* *组件：**
- `connected_components`、`is_connected`、`number_connected_components`
- `node_connected_component`
- `weakly_connected_components`、`is_weakly_connected`、 `number_weakly_connected_components`

* *集群：**
- `average_clustering`、`clustering`、`transitivity`、`triangles`

* *核心：**
- `core_number`、 `k_truss`

* *链接分析：**
- `pagerank`、`hits`

* *链接预测：**
- `jaccard_coefficient`

* *最短路径（23+功能）：**
- `shortest_path`、`shortest_path_length`
- `has_path`、`all_pairs_shortest_path`、`all_pairs_shortest_path_length`
- `dijkstra_path`、`dijkstra_path_length`、 `all_pairs_dijkstra`、`all_pairs_dijkstra_path_length`
- `bellman_ford_path`、`bellman_ford_path_length`、`all_pairs_bellman_ford_path_length`
- `single_source_shortest_path`、`single_source_shortest_path_length`
- `single_source_dijkstra`、 `single_source_dijkstra_path`、`single_source_dijkstra_path_length`
- `single_source_bellman_ford`、`single_source_bellman_ford_path`、`single_source_bellman_ford_path_length`
- `single_target_shortest_path_length`

* *遍历：**
- `bfs_edges`、 `bfs_layers`、`bfs_predecessors`、`bfs_successors`、`bfs_tree`
- `generic_bfs_edges`、`descendants_at_distance`

* *DAG：**
- `ancestors`、 `descendants`

* *二分：**
- `betweenness_centrality`（二分），`biadjacency_matrix`
- `complete_bipartite_graph`，`from_biadjacency_matrix`

* *树：**
- `is_arborescence`、`is_branching`、`is_forest`、`is_tree`

* *运算符：**
- `complement`、`reverse`

* *互惠：**
- `overall_reciprocity`、`reciprocity`

* *隔离：**
- `is_isolate`、`isolates`、`number_of_isolates`

* *最低共同祖先：**
- `lowest_common_ancestor`

* *布局：**
- `forceatlas2_layout`

* *图形生成器：**还支持直接在 GPU 上创建图形的各种生成器。

- --

## 直接 cuGraph API

### 快速示例

```python
import cugraph
import cudf

# Load edges from cuDF DataFrame
edges = cudf.DataFrame({
    "source": [0, 1, 2, 3, 0, 2],
    "destination": [1, 2, 3, 4, 4, 1],
    "weight": [1.0, 2.0, 1.0, 3.0, 0.5, 1.5]
})

G = cugraph.Graph(directed=True)
G.from_cudf_edgelist(edges, source="source", destination="destination", edge_attr="weight")

# Run algorithms
pr = cugraph.pagerank(G)
bc = cugraph.betweenness_centrality(G)
components = cugraph.weakly_connected_components(G)
```

- --

## 图形创建和数据加载

### 来自cuDF DataFrame（主要方法）
```python
import cudf, cugraph

df = cudf.DataFrame({"src": [0, 1, 2], "dst": [1, 2, 3], "wt": [1.0, 2.0, 3.0]})

# Unweighted
G = cugraph.Graph()
G.from_cudf_edgelist(df, source="src", destination="dst")

# Weighted
G = cugraph.Graph()
G.from_cudf_edgelist(df, source="src", destination="dst", edge_attr="wt")

# Directed
G = cugraph.Graph(directed=True)
G.from_cudf_edgelist(df, source="src", destination="dst")
```

### 来自Pandas DataFrame
```python
import pandas as pd, cugraph

df = pd.DataFrame({"src": [0, 1, 2], "dst": [1, 2, 3]})
G = cugraph.Graph()
G.from_pandas_edgelist(df, source="src", destination="dst")
```

### 来自 cuDF 邻接列表
```python
G = cugraph.Graph()
G.from_cudf_adjlist(offsets, indices, values)  # CSR format
```

### 来自 NumPy 数组
```python
import numpy as np
adj_matrix = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
G = cugraph.Graph()
G.from_numpy_array(adj_matrix)
```

### 来自 Pandas 邻接Matrix
```python
G = cugraph.Graph()
G.from_pandas_adjacency(adj_df)
```

### 来自Dask-cuDF（多GPU）
```python
G = cugraph.Graph()
G.from_dask_cudf_edgelist(dask_cudf_df, source="src", destination="dst")
```

### 来自内置数据集
```python
from cugraph.datasets import karate, dolphins, polbooks, netscience
G = karate.get_graph()
```

### 对称化（无向图）
```python
# Ensure all edges are bidirectional
sym_df = cugraph.symmetrize_df(df, "src", "dst")

# Or symmetrize a graph directly
sym_df = cugraph.symmetrize(source_col, dest_col, weight_col)
```

### 顶点重新编号
cuGraph 内部将顶点重新编号为从 0 开始的连续整数。使用 `unrenumber()` 映射回原始值ID：
```python
result = cugraph.pagerank(G)
result = G.unrenumber(result, "vertex")  # Map internal IDs back to original
```

- --

## 支持的图形类型

|图表类型| cuGraph 类 |注释 |
|---|---|---|
| **无指导** | `cugraph.Graph()` |默认;边是双向的|
| **导演** | `cugraph.Graph(directed=True)` |有向边；一些算法需要有向/无向|
| **加权** |将`edge_attr`设置为`from_cudf_edgelist` | SSSP、PageRank、Louvain 等使用的边权重 |
| **多图** | `cugraph.MultiGraph()` |相同顶点对之间的多条边|
| **双方** |通过具有二分结构的标准图支持 |没有专门的班级； `cugraph.bipartite` |

 中的算法**重要：** cuGraph 使用 CSR（压缩稀疏行）内部表示。图在创建后是不可变的——调用 `from_cudf_edgelist()` 后您无法动态添加/删除单个边。要修改图，请从新的 DataFrame 重建它。

- --

## 算法目录

### Centrality

|算法|单 GPU |多 GPU | NetworkX 等效 |
|---|---|---|---|
|介数中心性 | `cugraph.betweenness_centrality(G)` | `cugraph.dask.centrality.betweenness_centrality()` | `nx.betweenness_centrality()` |
|边缘介数| `cugraph.edge_betweenness_centrality(G)` | `cugraph.dask.centrality.edge_betweenness_centrality()` | `nx.edge_betweenness_centrality()` |
|度中心度 | `cugraph.degree_centrality(G)` | --| `nx.degree_centrality()` |
|特征向量中心性| `cugraph.eigenvector_centrality(G)` | `cugraph.dask.centrality.eigenvector_centrality()` | `nx.eigenvector_centrality()` |
|卡茨中心性| `cugraph.katz_centrality(G)` | `cugraph.dask.centrality.katz_centrality()` | `nx.katz_centrality()` |

### 社区检测

|算法|单 GPU |多 GPU | NetworkX 等效 |
|---|---|---|---|
|鲁汶 | `cugraph.louvain(G, max_level=, max_iter=, resolution=)` | `cugraph.dask.community.louvain.louvain()` | `nx.community.louvain_communities()` |
|莱顿 | `cugraph.leiden(G, max_iter=, resolution=)` | `cugraph.dask.community.leiden.leiden()` | `nx.community.leiden_communities()` |
|心电图| `cugraph.ecg(G, min_weight=)` | `cugraph.dask.community.ecg.ecg()` | -- |
|光谱平衡切割 | `cugraph.spectralBalancedCutClustering(G, num_clusters)` | --| -- |
|频谱模块化 | `cugraph.spectralModularityMaximizationClustering(G, num_clusters)` | --| -- |
|三角形计数| `cugraph.triangle_count(G)` | `cugraph.dask.community.triangle_count()` | `nx.triangles()` |
| K 型桁架 | `cugraph.k_truss(G, k)` 或 `cugraph.ktruss_subgraph(G, k)` | `cugraph.dask.community.ktruss_subgraph()` | `nx.k_truss()` |
|自我网 | `cugraph.ego_graph(G, n, radius=)` | `cugraph.dask.community.egonet()` | `nx.ego_graph()` |
|诱导子图| `cugraph.induced_subgraph(G, vertices)` | `cugraph.dask.community.induced_subgraph()` | `G.subgraph(vertices)` |

* *聚类分析：**
- `cugraph.analyzeClustering_edge_cut(G, n_clusters, clustering)`
- `cugraph.analyzeClustering_modularity(G, n_clusters, clustering)`
- `cugraph.analyzeClustering_ratio_cut(G, n_clusters, clustering)`

### 遍历

|算法|单 GPU |多 GPU | NetworkX 等效 |
|---|---|---|---|
| BFS | `cugraph.bfs(G, start=, depth_limit=)` | `cugraph.dask.traversal.bfs.bfs()` | `nx.bfs_edges()` |
| BFS 边缘 | `cugraph.bfs_edges(G, source)` | --| `nx.bfs_edges()` |
| SSSP | `cugraph.sssp(G, source=)` | `cugraph.dask.traversal.sssp.sssp()` | `nx.single_source_dijkstra()` |
|最短路径| `cugraph.shortest_path(G, source=)` | --| `nx.shortest_path()` |
|最短路径长度| `cugraph.shortest_path_length(G, source, target=)` | --| `nx.shortest_path_length()` |
|过滤器无法访问 | `cugraph.filter_unreachable(df)` | --| -- |

### 链接分析

|算法|单 GPU |多 GPU | NetworkX 等效 |
|---|---|---|---|
|网页排名 | `cugraph.pagerank(G, alpha=)` | `cugraph.dask.link_analysis.pagerank()` | `nx.pagerank()` |
|点击 | `cugraph.hits(G, max_iter=, tol=)` | `cugraph.dask.link_analysis.hits()` | `nx.hits()` |

### 链接预测/相似度

|算法|单 GPU |多 GPU | NetworkX 等效 |
|---|---|---|---|
|杰卡德| `cugraph.jaccard(G, vertex_pair=)` | --| `nx.jaccard_coefficient()` |
|余弦相似度| `cugraph.cosine(G, vertex_pair=)` | --| -- |
|重叠| `cugraph.overlap(G, vertex_pair=)` | `cugraph.dask.link_prediction.overlap()` | -- |
|索伦森| `cugraph.sorensen(G, vertex_pair=)` | `cugraph.dask.link_prediction.sorensen()` | -- |

* *NetworkX 兼容包装器：** `cugraph.jaccard_coefficient(G, ebunch)`、`cugraph.overlap_coefficient(G, ebunch)`、`cugraph.sorensen_coefficient(G, ebunch)`

### 组件

|算法|单 GPU |多 GPU | NetworkX 等效 |
|---|---|---|---|
|连接组件| `cugraph.connected_components(G)` | --| `nx.connected_components()` |
|弱连接| `cugraph.weakly_connected_components(G)` | `cugraph.dask.components.weakly_connected_components()` | `nx.weakly_connected_components()` |
|强关联 | `cugraph.strongly_connected_components(G)` | --| `nx.strongly_connected_components()` |

### 内核

|算法|单 GPU |多 GPU | NetworkX 等效 |
|---|---|---|---|
|核心数| `cugraph.core_number(G, degree_type=)` | `cugraph.dask.cores.core_number()` | `nx.core_number()` |
| K-核心| `cugraph.k_core(G, k=, core_number=)` | `cugraph.dask.cores.k_core()` | `nx.k_core()` |

### 采样

|算法|单 GPU |多 GPU |注释 |
|---|---|---|---|
|有偏随机游走 | `cugraph.biased_random_walks(G, start_vertices)` | `cugraph.dask.sampling.biased_random_walks()` |加权/偏置遍历|
|均匀随机游走 | --| `cugraph.dask.sampling.uniform_random_walks()` |具有最大路径长度的填充结果|
|随机游走 | --| `cugraph.dask.sampling.random_walks()` |一般随机游走|
| Node2Vec | --| `cugraph.dask.sampling.node2vec_random_walks()` | Node2Vec采样框架|
|同质邻域样本 | `cugraph.homogeneous_neighbor_sample(G, start_vertices, fanout)` | --|每跳可配置扇出|
|异质邻居样本 | `cugraph.heterogeneous_neighbor_sample(G, ...)` | --|多类型节点/边图 |

### 布局

|算法|单 GPU |多 GPU | NetworkX 等效 |
|---|---|---|---|
|原力阿特拉斯 2 | `cugraph.force_atlas2(G)` | --| `nx.forceatlas2_layout()`（来自nx-cugraph）|

### Tree

|算法|单 GPU |多 GPU | NetworkX 等效 |
|---|---|---|---|
|最小生成树| `cugraph.minimum_spanning_tree(G)` | --| `nx.minimum_spanning_tree()` |
|最大生成树| `cugraph.maximum_spanning_tree(G)` | --| `nx.maximum_spanning_tree()` |

### 线性赋值

|算法|单 GPU |多GPU |
|---|---|---|
|匈牙利语 | `cugraph.hungarian(G, workers, cost)` | -- |

### 实用工具

|功能|用途 |
|---|---|
| `cugraph.symmetrize(src, dst, val)` |使边双向（对于无向图）|
| `cugraph.symmetrize_df(df, src, dst)` |对称数据帧 |
| `cugraph.symmetrize_ddf(ddf, src, dst)` |对称 Dask 数据帧 |
| `cugraph.NumberMap` |将外部顶点 ID 映射到连续的内部 ID |
| `G.unrenumber(df, col)` |将内部顶点 ID 映射回原始 |

- --

## Dask 的多 GPU 支持

cuGraph 通过 Dask 支持多 GPU 计算，用于超出单 GPU 内存或需要更快处理的图形。

### 设置
```python
from dask.distributed import Client
from dask_cuda import LocalCUDACluster
import cugraph
import cugraph.dask as dask_cugraph
import dask_cudf

# Initialize multi-GPU cluster
cluster = LocalCUDACluster()
client = Client(cluster)

# Load distributed edge list
ddf = dask_cudf.read_csv("large_graph.csv", names=["src", "dst", "weight"])

# Create distributed graph
G = cugraph.Graph(directed=True)
G.from_dask_cudf_edgelist(ddf, source="src", destination="dst", edge_attr="weight")

# Run multi-GPU algorithms
pr = dask_cugraph.pagerank(G)
components = dask_cugraph.weakly_connected_components(G)
```

### 支持多 GPU 的算法

以下算法具有基于 Dask 的多 GPU 实现：
- **中心性：** Betweenness、Edge Betweenness、Eigenvector、Katz
- **社区：** Louvain、Leiden、ECG、K-Truss、Triangle Counting、EgoNet、Induced Subgraph
- **组件：**弱连接组件
- **核心：**核心数、K-Core
- **链接分析：** PageRank、HITS
- **链接预测：**重叠、Sorensen
- **采样：** 随机游走、偏置随机游走、均匀随机游走、Node2Vec、邻域采样
- **遍历：** BFS、SSSP
- **实用程序：** 重新编号、对称、路径提取、两跳邻居、RMAT 生成器

- --

## GNN 支持

### cugraph-pyg（PyTorch 几何）集成）

从版本 25.06 开始，**cugraph-pyg 是推荐的 GNN 框架集成**（cuGraph-DGL 已被删除）。

cugraph-pyg 提供 PyG 核心接口的本机 GPU 加速实现：

- **GraphStore**：使用 cuGraph 的 CSR 表示的 GPU 加速图形存储
- **FeatureStore**：用于节点/边缘特征的 GPU 驻留特征存储
- **采样器/加载器**：具有可配置扇出的 GPU 加速邻域采样

```bash
uv add --extra-index-url=https://pypi.nvidia.com cugraph-pyg-cu12
```

* *关键功能：**
- 异构图采样（多个节点/边缘类型）
- 多 GPU 分布式采样
- 与 PyG 的 `NeighborLoader` 和训练循环直接集成
- GPU 加速的中心性、社区检测和 PyG 内的其他分析工作流程

* *存储库：** https://github.com/rapidsai/cugraph-gnn

### WholeGraph（GNN 的分布式 GPU 内存）

WholeGraph 通过其 **WholeMemory** 抽象为大规模 GNN 训练提供分布式 GPU 内存管理。

```bash
uv add --extra-index-url=https://pypi.nvidia.com pylibwholegraph-cu12
```

* *Core概念：**

- **WholeMemory**：分布在多个 GPU 上的 GPU 内存的统一视图。即使数据在物理上是分布式的，每个 GPU 也可以通过单个抽象来查看整个内存空间。
- **WholeMemory Communicator**：定义一组协作的 GPU，每个 GPU 有一个进程。
- **WholeMemory Tensor**：与 PyTorch 张量类似，但是分布式的；支持跨 GPU 划分第一维的 1D 和 2D 数据。
- **WholeMemory Embedding**：具有内置缓存策略和稀疏优化器（SGD、Adam、RMSProp、AdaGrad）的 2D 张量变体。

* *内存模式：**
|模式|描述 |使用案例 |
|---|---|---|
| **连续** |通过硬件点对点的单一连续地址空间 | NVLink 系统 (DGX) |
| **分块** |具有直接多指针访问的每 GPU 块 |带有一些 NVLink 的多 GPU |
| **分布式** |远程访问所需的显式通信 |多节点集群 |

* *存储位置：**主机内存（固定）或设备/GPU 内存。

* *图形存储：** CSR 格式，将 ROW_INDEX 和 COL_INDEX 作为 WholeMemory 张量，用于高效的分布式图形管理。

* *缓存策略：**设备缓存主机内存、本地缓存全局内存 - 对于处理大于 GPU 的图形至关重要内存.

* *目标硬件：** DGX A100/H100 服务器等 NVLink 系统可实现最佳性能。

### cuGraph-DGL（已弃用）

* *cuGraph-DGL 自 25.06 版起已删除。**用户应迁移到 cugraph-pyg。 cuGraph 团队不打算在 DGL 生态系统中进行进一步的工作。

- --

## 性能特征和基准

### nx-cugraph 基准（NetworkX 后端）

* *硬件：** Intel Xeon w9-3495X（56 核）、NVIDIA RTX 3090 (24GB)、251 GB RAM、CUDA 12.8

* *测试数据集：**

|数据集 |节点|边缘 |类型 |
|---|---|---|---|
|网络科学| 1,461 | 1,461 5,484 | 5,484小|
|亚马逊0302 | 262,111 | 262,111 1,234,877 | 1,234,877中号|
| cit-专利 | 3,774,768 | 3,774,768 16,518,948 |大号|
| soc-LiveJournal1 | 4,847,571 | 4,847,571 68,993,773 | 68,993,773非常大 |

* *加速（GPU 与 CPU NetworkX）：**

|算法|中图|大图|超大图|
|---|---|---|---|
| `betweenness_centrality` (k=100) | 〜20x | ~520x | ~300x |
| `katz_centrality` | 〜100x | ~5,000x | ~24,768x |
| `average_clustering` | 〜50x | 〜1,000x | ~2,828x |
| `transitivity` | 〜50x | 〜1,000x | ~2,832x |
| `louvain_communities` | 〜30x | 〜273x | ~200x |
| `pagerank` | 〜2x | 〜50x | ~188x |
| `eigenvector_centrality` | 〜7x | 〜100x | ~376x |
| `k_truss` | 〜8x | 〜200x | ~540x |

* *关键发现：** 加速随着图形大小的增加而显着增加。小图（< 5K 边）可能会因 GPU 初始化而产生开销，从而影响加速。对于具有 > 100K 边的图，大多数算法预计会提高 10-500 倍以上。

* *具体示例：** cit-Patents 上的介数中心性（370 万个节点，1650 万条边）：
- CPU NetworkX：7 分 41 秒
- nx-cugraph GPU： 5.32 秒（~86 倍加速）

### 一般性能指南

- **小图（< 10K 边）：** GPU 开销可能占主导地位； NetworkX CPU 可能更快
- **中型图形（100K-1M 边）：** 典型加速 10-100 倍
- **大型图形（1M-100M 边）：** 典型加速 100-1000x+ 
- **非常大的图形（> 100M 边）：**使用多GPU；单个 GPU 内存可能不足
- **首次调用开销：** 初始 GPU 内核编译和图形传输增加约 1-3 秒；对同一图的后续调用要快得多

- --

## 内存管理

### GPU内存注意事项

- cuGraph将CSR格式的图存储在GPU内存上
- 内存使用量约为：`(num_edges * 2 * 4 bytes) + (num_vertices * 4 bytes)`用于未加权，加上`(num_edges * 8 bytes)`用于加权（float64）权重）
- 具有 100M 边的图大约需要约 1.6 GB 未加权或约 2.4 GB 加权
- 算法工作内存各不相同；一些算法（如介数中心性）需要额外的 O(V)或 O(E)临时空间

### 大图策略

1. **对于超过单 GPU 内存 
2 的图形，通过 Dask 使用多 GPU**。 **对需要分布式特征/图形存储的 GNN 工作负载使用 WholeGraph**
3. **使用 `rmm`** (RAPIDS Memory Manager)进行细粒度 GPU 内存控制：
 ```python
 import rmm
 rmm.reinitialize(pool_allocator=True, initial_pool_size=2**30) # 1 GB pool
 ``
4. **使用 `nvidia-smi` 或 `rmm.get_memory_info()`
5 监控内存**。 **明确删除中间结果**：`del result; import gc; gc.collect()`

- --

## 互操作性

### 使用cuDF
cuGraph本机消费并生成cuDF DataFrame。算法结果以带有顶点/边列的 cuDF DataFrames 返回。

```python
import cudf, cugraph
# Create graph from cuDF
edges = cudf.read_csv("edges.csv")
G = cugraph.Graph()
G.from_cudf_edgelist(edges, source="src", destination="dst")

# Results come back as cuDF DataFrames
pr = cugraph.pagerank(G)  # cuDF DataFrame with 'vertex' and 'pagerank' columns
```

### 使用 cuML
Pipe 图形分析结果转换为 cuML 用于下游 ML：
```python
import cuml
# Use graph embeddings (e.g., from Node2Vec) as features for cuML
# Or use community labels as features for classification
louvain_result = cugraph.louvain(G)
# Feed partition labels into cuML models
```

### 使用 CuPy / SciPy
```python
# cuGraph can work with CuPy and SciPy sparse matrices as input data
import cupy, scipy
```

### 使用NetworkX
```python
import networkx as nx
import cugraph

# NetworkX -> cuGraph
G_nx = nx.karate_club_graph()
G_cu = cugraph.from_networkx(G_nx)  # Not yet available in all versions

# Or use nx-cugraph backend for transparent acceleration
```

### 使用 PyTorch Geometric
```python
# Via cugraph-pyg (see GNN Support section)
from cugraph_pyg.data import CuGraphStore
from cugraph_pyg.loader import CuGraphNeighborLoader
```

### 使用 Pandas
```python
import pandas as pd
df = pd.DataFrame({"src": [0, 1, 2], "dst": [1, 2, 3]})
G = cugraph.Graph()
G.from_pandas_edgelist(df, source="src", destination="dst")
```

- --

## 已知限制 vs网络X

1. **不可变图：** 创建图后无法添加/删除单个边。必须从 DataFrame.
2 重建。 **图对象上没有节点/边属性：** cuGraph 仅存储结构。节点/边属性必须单独维护（例如，在 cuDF DataFrame 中）。 nx-cugraph后端透明地处理属性映射。
3. **顶点类型：** 顶点必须是整数（或者将在内部重新编号为整数）。字符串顶点 ID 自动重新编号。
4. **并非所有 NetworkX 算法都受支持：** 检查 nx-cugraph 支持的算法列表。不受支持的调用会回退到 CPU NetworkX.
5. **数值精度：** 由于并行降序，GPU 浮点结果可能与 CPU 结果略有不同。
6. **没有动态图：** cuGraph 专为静态图分析而设计，而不是流/动态图更新。
7. **强连接组件：** 仅单 GPU（无多 GPU Dask 变体）。
8. **谱聚类：** 仅限单 GPU。
9. **最小/最大生成树：** 仅限单 GPU。
10. **Force Atlas 2 布局：** 仅单 GPU。
11. **兼容性文档：** cuGraph 与 NetworkX 的官方兼容性文档在 26.02 版本中被列为“即将推出”。

- --

## 常见迁移模式

### NetworkX 到 nx-cugraph（零）努力）
```python
# Before (CPU):
import networkx as nx
G = nx.from_pandas_edgelist(df, "src", "dst")
pr = nx.pagerank(G)

# After (GPU, no code changes):
# Just set: NX_CUGRAPH_AUTOCONFIG=True
# Same code runs on GPU automatically
```

### NetworkX 到直接 cuGraph API
```python
# Before (NetworkX):
import networkx as nx
G = nx.from_pandas_edgelist(df, "src", "dst")
pr = nx.pagerank(G, alpha=0.85)
bc = nx.betweenness_centrality(G, k=100)
communities = nx.community.louvain_communities(G, resolution=1.0)

# After (cuGraph):
import cudf, cugraph
edges = cudf.from_pandas(df)
G = cugraph.Graph()
G.from_cudf_edgelist(edges, source="src", destination="dst")
pr = cugraph.pagerank(G, alpha=0.85)
bc = cugraph.betweenness_centrality(G)
parts, modularity = cugraph.louvain(G, resolution=1.0)
```

### Pandas 到 cuDF + cuGraph Pipeline
```python
# Before:
import pandas as pd
import networkx as nx
df = pd.read_csv("edges.csv")
G = nx.from_pandas_edgelist(df, "source", "target", "weight")
result = nx.pagerank(G)

# After:
import cudf
import cugraph
df = cudf.read_csv("edges.csv")
G = cugraph.Graph()
G.from_cudf_edgelist(df, source="source", destination="target", edge_attr="weight")
result = cugraph.pagerank(G)
```

### 将多GPU添加到现有cuGraph代码
```python
# Before (single-GPU):
import cugraph
G = cugraph.Graph()
G.from_cudf_edgelist(edges, source="src", destination="dst")
result = cugraph.pagerank(G)

# After (multi-GPU):
from dask.distributed import Client
from dask_cuda import LocalCUDACluster
import cugraph, cugraph.dask as dcg
import dask_cudf

cluster = LocalCUDACluster()
client = Client(cluster)

ddf = dask_cudf.from_cudf(edges, npartitions=len(cluster.workers))
G = cugraph.Graph()
G.from_dask_cudf_edgelist(ddf, source="src", destination="dst")
result = dcg.pagerank(G)
result_local = result.compute()  # Collect to single GPU
```
