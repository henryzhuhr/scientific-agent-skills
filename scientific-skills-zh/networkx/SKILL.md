---
name: networkx
description: 用于在 Python 中创建、分析和可视化复杂网络和图形的综合工具包。在处理网络/图形数据结构、分析实体之间的关系、计算图形算法（最短路径、中心性、聚类）、检测社区、生成合成网络或可视化网络拓扑时使用。适用于社交网络、生物网络、交通系统、引文网络以及任何涉及成对关系的领域。
license: 3-clause BSD license
metadata:
    skill-author: K-Dense Inc.
---

# NetworkX

## 概述

NetworkX 是一个用于创建、操作和分析复杂网络和图形的 Python 包。在处理网络或图形数据结构时使用此技能，包括社交网络、生物网络、交通系统、引文网络、知识图或任何涉及实体之间关系的系统。

## 何时使用此技能

当任务涉及以下内容时调用此技能：

- **创建图形**：从数据构建网络结构，添加具有属性的节点和边
- **图形分析**：计算中心性度量，查找最短路径、检测社区、测量聚类
- **图形算法**：运行标准算法，如 Dijkstra、PageRank、最小生成树、最大流量
- **网络生成**：创建用于测试或模拟的合成网络（随机、无标度、小世界模型）
- **图形 I/O**：读取或写入各种格式（边缘列表、GraphML、JSON、CSV、邻接矩阵）
- **可视化**：使用 matplotlib 或交互式库绘制和自定义网络可视化
- **网络比较**：检查同构、计算图度量、分析结构属性

## 核心功能

### 1. 图创建和操作

NetworkX支持四种主要图类型：
- **Graph**：具有单边的无向图
- **DiGraph**：具有单向连接的有向图
- **MultiGraph**：允许节点之间有多个边的无向图
- **MultiDiGraph**：具有多个边的有向图

创建图作者：
```python
import networkx as nx

# Create empty graph
G = nx.Graph()

# Add nodes (can be any hashable type)
G.add_node(1)
G.add_nodes_from([2, 3, 4])
G.add_node("protein_A", type='enzyme', weight=1.5)

# Add edges
G.add_edge(1, 2)
G.add_edges_from([(1, 3), (2, 4)])
G.add_edge(1, 4, weight=0.8, relation='interacts')
```

* *参考**：有关创建、修改、检查和管理图形结构（包括使用属性和子图）的综合指南，请参阅 `references/graph-basics.md`。

### 2. 图形算法

NetworkX 提供了丰富的网络分析算法：

* *最短路径**:
```python
# Find shortest path
path = nx.shortest_path(G, source=1, target=5)
length = nx.shortest_path_length(G, source=1, target=5, weight='weight')
```

* *中心性度量**:
```python
# Degree centrality
degree_cent = nx.degree_centrality(G)

# Betweenness centrality
betweenness = nx.betweenness_centrality(G)

# PageRank
pagerank = nx.pagerank(G)
```

* *社区检测**：
```python
from networkx.algorithms import community

# Detect communities
communities = community.greedy_modularity_communities(G)
```

* *连接**：
```python
# Check connectivity
is_connected = nx.is_connected(G)

# Find connected components
components = list(nx.connected_components(G))
```

* *参考**：有关所有可用算法的详细文档，包括最短路径、中心性度量、聚类、社区检测、流、匹配、树算法和图，请参阅 `references/algorithms.md` traversal.

### 3.图形生成器

创建用于测试、模拟或建模的合成网络：

* *经典图形**：
```python
# Complete graph
G = nx.complete_graph(n=10)

# Cycle graph
G = nx.cycle_graph(n=20)

# Known graphs
G = nx.karate_club_graph()
G = nx.petersen_graph()
```

* *随机网络**：
```python
# Erdős-Rényi random graph
G = nx.erdos_renyi_graph(n=100, p=0.1, seed=42)

# Barabási-Albert scale-free network
G = nx.barabasi_albert_graph(n=100, m=3, seed=42)

# Watts-Strogatz small-world network
G = nx.watts_strogatz_graph(n=100, k=6, p=0.1, seed=42)
```

* *结构化网络**：
```python
# Grid graph
G = nx.grid_2d_graph(m=5, n=7)

# Random tree
G = nx.random_tree(n=100, seed=42)
```

* *参考**：请参阅`references/generators.md`以全面覆盖所有图生成器，包括经典、随机、格子、二分和专用网络模型以及详细参数和使用case.

### 4. 读写图表

NetworkX 支持多种文件格式和数据源：

* *文件格式**：
```python
# Edge list
G = nx.read_edgelist('graph.edgelist')
nx.write_edgelist(G, 'graph.edgelist')

# GraphML (preserves attributes)
G = nx.read_graphml('graph.graphml')
nx.write_graphml(G, 'graph.graphml')

# GML
G = nx.read_gml('graph.gml')
nx.write_gml(G, 'graph.gml')

# JSON
data = nx.node_link_data(G)
G = nx.node_link_graph(data)
```

* *Pandas集成**：
```python
import pandas as pd

# From DataFrame
df = pd.DataFrame({'source': [1, 2, 3], 'target': [2, 3, 4], 'weight': [0.5, 1.0, 0.75]})
G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr='weight')

# To DataFrame
df = nx.to_pandas_edgelist(G)
```

* *矩阵格式**：
```python
import numpy as np

# Adjacency matrix
A = nx.to_numpy_array(G)
G = nx.from_numpy_array(A)

# Sparse matrix
A = nx.to_scipy_sparse_array(G)
G = nx.from_scipy_sparse_array(A)
```

* *参考**：有关所有 I/O 格式（包括 CSV、SQL 数据库、Cytoscape、DOT）的完整文档，以及针对不同用途的格式选择指南，请参阅 `references/io.md` case.

### 5. 可视化

创建清晰且信息丰富的网络可视化：

* *基本可视化**：
```python
import matplotlib.pyplot as plt

# Simple draw
nx.draw(G, with_labels=True)
plt.show()

# With layout
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos=pos, with_labels=True, node_color='lightblue', node_size=500)
plt.show()
```

* *自定义**：
```python
# Color by degree
node_colors = [G.degree(n) for n in G.nodes()]
nx.draw(G, node_color=node_colors, cmap=plt.cm.viridis)

# Size by centrality
centrality = nx.betweenness_centrality(G)
node_sizes = [3000 * centrality[n] for n in G.nodes()]
nx.draw(G, node_size=node_sizes)

# Edge weights
edge_widths = [3 * G[u][v].get('weight', 1) for u, v in G.edges()]
nx.draw(G, width=edge_widths)
```

* *布局算法**：
```python
# Spring layout (force-directed)
pos = nx.spring_layout(G, seed=42)

# Circular layout
pos = nx.circular_layout(G)

# Kamada-Kawai layout
pos = nx.kamada_kawai_layout(G)

# Spectral layout
pos = nx.spectral_layout(G)
```

* *发布质量**：
```python
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos=pos, node_color='lightblue', node_size=500,
        edge_color='gray', with_labels=True, font_size=10)
plt.title('Network Visualization', fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.savefig('network.png', dpi=300, bbox_inches='tight')
plt.savefig('network.pdf', bbox_inches='tight')  # Vector format
```

* *参考**：有关可视化技术的详细文档，请参阅 `references/visualization.md`，包括布局算法、自定义选项、使用 Plotly 和 PyVis 进行交互式可视化、3D 网络和出版物质量的图形创建。

## 使用网络X

### 安装

确保安装NetworkX：
```python
# Check if installed
import networkx as nx
print(nx.__version__)

# Install if needed (via bash)
# uv pip install networkx
# uv pip install networkx[default]  # With optional dependencies
```

### 通用工作流程模式

大多数 NetworkX 任务遵循以下模式：

1. **创建或加载图表**:
 ```python
 # 从头开始
G = nx.Graph()
 G.add_edges_from([(1, 2), (2, 3), (3, 4)])

 # 或者从文件/数据加载
G = nx.read_edgelist('data.txt')
 ```

2. **检查结构**：
 ```python
 print(f"节点：{G.number_of_nodes()}")
 print(f"边：{G.number_of_edges()}")
 print(f"密度：{nx.密度(G)}")
 print(f"已连接：{nx.is_connected(G)}")
 ```

3. **分析**:
 ```python
 # 计算指标
Degree_cent = nx. Degree_centrality(G)
 avg_clustering = nx.average_clustering(G)

 # 查找路径
path = nx.shortest_path(G, source=1, target=4)

 # 检测社区
Community = Community.greedy_modularity_communities(G)
 ```

4. **可视化**：
 ```python
 pos = nx.spring_layout(G, Seed=42)
 nx.draw(G, pos=pos, with_labels=True)
 plt.show()
 ```

5. **导出结果**:
 ```python
 # 保存 graph
nx.write_graphml(G, 'analyzed_network.graphml')

 # 保存指标
df = pd.DataFrame({
 'node': list(level_cent.keys()),
 'centrality': list( Degree_cent.values())
 })
 df.to_csv('centrality_results.csv', index=False)
 ```

### 重要注意事项

* *浮点精度**：当图形包含浮点数时，由于精度限制，所有结果本质上都是近似值。这可能会影响算法结果，特别是在最小/最大计算中。

* *内存和性能**：每次运行脚本时，图形数据都必须加载到内存中。对于大型网络：
- 使用适当的数据结构（大型稀疏图的稀疏矩阵）
- 考虑仅加载必要的子图
- 使用高效的文件格式（Python对象的pickle，压缩格式）
- 利用非常大的网络的近似算法（例如，中心性中的`k`参数计算）

* *节点和边类型**：
- 节点可以是任何可散列的 Python 对象（数字、字符串、元组、自定义对象）
- 为了清晰起见，使用有意义的标识符
- 删除节点时，所有关联边都会自动删除

* *随机种子**：始终设置随机种子，以实现随机图生成和强制定向中的可再现性布局：
```python
G = nx.erdos_renyi_graph(n=100, p=0.1, seed=42)
pos = nx.spring_layout(G, seed=42)
```

## 快速参考

### 基本操作
```python
# Create
G = nx.Graph()
G.add_edge(1, 2)

# Query
G.number_of_nodes()
G.number_of_edges()
G.degree(1)
list(G.neighbors(1))

# Check
G.has_node(1)
G.has_edge(1, 2)
nx.is_connected(G)

# Modify
G.remove_node(1)
G.remove_edge(1, 2)
G.clear()
```

### 基本算法
```python
# Paths
nx.shortest_path(G, source, target)
nx.all_pairs_shortest_path(G)

# Centrality
nx.degree_centrality(G)
nx.betweenness_centrality(G)
nx.closeness_centrality(G)
nx.pagerank(G)

# Clustering
nx.clustering(G)
nx.average_clustering(G)

# Components
nx.connected_components(G)
nx.strongly_connected_components(G)  # Directed

# Community
community.greedy_modularity_communities(G)
```

### 文件I/O快速参考
```python
# Read
nx.read_edgelist('file.txt')
nx.read_graphml('file.graphml')
nx.read_gml('file.gml')

# Write
nx.write_edgelist(G, 'file.txt')
nx.write_graphml(G, 'file.graphml')
nx.write_gml(G, 'file.gml')

# Pandas
nx.from_pandas_edgelist(df, 'source', 'target')
nx.to_pandas_edgelist(G)
```

## 资源

该技能包括全面的参考文档：

### references/graph-basics.md
有关图类型、创建和修改图、添加节点和边、管理属性、检查结构以及使用的详细指南subgraphs.

### 参考文献/算法.md
完整覆盖NetworkX算法，包括最短路径、中心性度量、连通性、聚类、社区检测、流算法、树算法、匹配、着色、同构和图遍历。

### References/generators.md
有关图生成器的综合文档，包括经典图、随机模型（Erdős-Rényi、Barabási-Albert、Watts-Strogatz）、格子、树、社交网络模型和专用生成器。

### references/io.md
阅读和编写各种格式图形的完整指南：边列表、邻接列表、GraphML、GML、JSON、CSV、Pandas DataFrames、NumPy 数组、SciPy 稀疏矩阵、数据库集成和格式选择指南。

### references/visualization.md
有关可视化技术的大量文档，包括布局算法、自定义节点和边缘外观、标签、使用 Plotly 和 PyVis 进行交互式可视化、3D 网络、二分布局以及创建出版物质量的图形。

## 其他资源

- **官方文档**：https://networkx.org/documentation/latest/
- **教程**：https://networkx.org/documentation/latest/tutorial.html
- **图库**：https://networkx.org/documentation/latest/auto_examples/index.html
- **GitHub**：https://github.com/networkx/networkx
