# NetworkX 图形生成器

## 经典图形

### 完整图形
```python
# Complete graph (all nodes connected to all others)
G = nx.complete_graph(n=10)

# Complete bipartite graph
G = nx.complete_bipartite_graph(n1=5, n2=7)

# Complete multipartite graph
G = nx.complete_multipartite_graph(3, 4, 5)  # Three partitions
```

### 循环和路径图形
```python
# Cycle graph (nodes arranged in circle)
G = nx.cycle_graph(n=20)

# Path graph (linear chain)
G = nx.path_graph(n=15)

# Circular ladder graph
G = nx.circular_ladder_graph(n=10)
```

### 常规图
```python
# Empty graph (no edges)
G = nx.empty_graph(n=10)

# Null graph (no nodes)
G = nx.null_graph()

# Star graph (one central node connected to all others)
G = nx.star_graph(n=19)  # Creates 20-node star

# Wheel graph (cycle with central hub)
G = nx.wheel_graph(n=10)
```

### 特殊命名图
```python
# Bull graph
G = nx.bull_graph()

# Chvatal graph
G = nx.chvatal_graph()

# Cubical graph
G = nx.cubical_graph()

# Diamond graph
G = nx.diamond_graph()

# Dodecahedral graph
G = nx.dodecahedral_graph()

# Heawood graph
G = nx.heawood_graph()

# House graph
G = nx.house_graph()

# Petersen graph
G = nx.petersen_graph()

# Karate club graph (classic social network)
G = nx.karate_club_graph()
```

## 随机图

### Erdős-Rényi图
```python
# G(n, p) model: n nodes, edge probability p
G = nx.erdos_renyi_graph(n=100, p=0.1, seed=42)

# G(n, m) model: n nodes, exactly m edges
G = nx.gnm_random_graph(n=100, m=500, seed=42)

# Fast version (for large sparse graphs)
G = nx.fast_gnp_random_graph(n=10000, p=0.0001, seed=42)
```

### Watts-Strogatz Small-World
```python
# Small-world network with rewiring
# n nodes, k nearest neighbors, rewiring probability p
G = nx.watts_strogatz_graph(n=100, k=6, p=0.1, seed=42)

# Connected version (guarantees connectivity)
G = nx.connected_watts_strogatz_graph(n=100, k=6, p=0.1, tries=100, seed=42)
```

### Barabási-Albert 优先附件
```python
# Scale-free network (power-law degree distribution)
# n nodes, m edges to attach from new node
G = nx.barabasi_albert_graph(n=100, m=3, seed=42)

# Extended version with parameters
G = nx.extended_barabasi_albert_graph(n=100, m=3, p=0.5, q=0.2, seed=42)
```

### 幂律度序列
```python
# Power law cluster graph
G = nx.powerlaw_cluster_graph(n=100, m=3, p=0.1, seed=42)

# Random power law tree
G = nx.random_powerlaw_tree(n=100, gamma=3, seed=42, tries=1000)
```

### 配置模型
```python
# Graph with specified degree sequence
degree_sequence = [3, 3, 3, 3, 2, 2, 2, 1, 1, 1]
G = nx.configuration_model(degree_sequence, seed=42)

# Remove self-loops and parallel edges
G = nx.Graph(G)
G.remove_edges_from(nx.selfloop_edges(G))
```

### 随机几何图
```python
# Nodes in unit square, edges if distance < radius
G = nx.random_geometric_graph(n=100, radius=0.2, seed=42)

# With positions
pos = nx.get_node_attributes(G, 'pos')
```

### 随机正则图
```python
# Every node has exactly d neighbors
G = nx.random_regular_graph(d=3, n=100, seed=42)
```

### 随机块模型
```python
# Community structure model
sizes = [50, 50, 50]  # Three communities
probs = [[0.25, 0.05, 0.02],  # Within and between community probabilities
         [0.05, 0.35, 0.07],
         [0.02, 0.07, 0.40]]
G = nx.stochastic_block_model(sizes, probs, seed=42)
```

## 点阵图和网格图

### 网格图
```python
# 2D grid
G = nx.grid_2d_graph(m=5, n=7)  # 5x7 grid

# 3D grid
G = nx.grid_graph(dim=[5, 7, 3])  # 5x7x3 grid

# Hexagonal lattice
G = nx.hexagonal_lattice_graph(m=5, n=7)

# Triangular lattice
G = nx.triangular_lattice_graph(m=5, n=7)
```

### 超立方体
```python
# n-dimensional hypercube
G = nx.hypercube_graph(n=4)
```

## 树图

### 随机树
```python
# Random tree with n nodes
G = nx.random_tree(n=100, seed=42)

# Prefix tree (tries)
G = nx.prefix_tree([[0, 1, 2], [0, 1, 3], [0, 4]])
```

### 平衡树木
```python
# Balanced r-ary tree of height h
G = nx.balanced_tree(r=2, h=5)  # Binary tree, height 5

# Full r-ary tree with n nodes
G = nx.full_rary_tree(r=3, n=100)  # Ternary tree
```

### 杠铃和棒棒糖图
```python
# Two complete graphs connected by path
G = nx.barbell_graph(m1=5, m2=3)  # Two K_5 graphs with 3-node path

# Complete graph connected to path
G = nx.lollipop_graph(m=7, n=5)  # K_7 with 5-node path
```

## 社交网络模型

### 空手道俱乐部
```python
# Zachary's karate club (classic social network)
G = nx.karate_club_graph()
```

### 戴维斯南方女子
```python
# Bipartite social network
G = nx.davis_southern_women_graph()
```

### 佛罗伦萨家庭
```python
# Historical marriage and business networks
G = nx.florentine_families_graph()
```

### Les Misérables
```python
# Character co-occurrence network
G = nx.les_miserables_graph()
```

## 有向图生成器

### 随机有向图
```python
# Directed Erdős-Rényi
G = nx.gnp_random_graph(n=100, p=0.1, directed=True, seed=42)

# Scale-free directed
G = nx.scale_free_graph(n=100, seed=42)
```

### DAG（有向无环） Graph)
```python
# Random DAG
G = nx.gnp_random_graph(n=20, p=0.2, directed=True, seed=42)
G = nx.DiGraph([(u, v) for (u, v) in G.edges() if u < v])  # Remove backward edges
```

### 锦标赛图表
```python
# Random tournament (complete directed graph)
G = nx.random_tournament(n=10, seed=42)
```

## 重复发散模型

### 重复发散Graph
```python
# Biological network model (protein interaction networks)
G = nx.duplication_divergence_graph(n=100, p=0.5, seed=42)
```

## 度数序列生成器

### 有效度数序列
```python
# Check if degree sequence is valid (graphical)
sequence = [3, 3, 3, 3, 2, 2, 2, 1, 1, 1]
is_valid = nx.is_graphical(sequence)

# For directed graphs
in_sequence = [2, 2, 2, 1, 1]
out_sequence = [2, 2, 1, 2, 1]
is_valid = nx.is_digraphical(in_sequence, out_sequence)
```

### 从度数创建序列
```python
# Havel-Hakimi algorithm
G = nx.havel_hakimi_graph(degree_sequence)

# Configuration model (allows multi-edges/self-loops)
G = nx.configuration_model(degree_sequence)

# Directed configuration model
G = nx.directed_configuration_model(in_degree_sequence, out_degree_sequence)
```

## 二分图

### 随机二分
```python
# Random bipartite with two node sets
G = nx.bipartite.random_graph(n=50, m=30, p=0.1, seed=42)

# Configuration model for bipartite
G = nx.bipartite.configuration_model(deg1=[3, 3, 2], deg2=[2, 2, 2, 2], seed=42)
```

### 二分生成器
```python
# Complete bipartite
G = nx.complete_bipartite_graph(n1=5, n2=7)

# Gnmk random bipartite (n, m nodes, k edges)
G = nx.bipartite.gnmk_random_graph(n=10, m=8, k=20, seed=42)
```

## 图上的运算符

### 图形操作
```python
# Union
G = nx.union(G1, G2)

# Disjoint union
G = nx.disjoint_union(G1, G2)

# Compose (overlay)
G = nx.compose(G1, G2)

# Complement
G = nx.complement(G1)

# Cartesian product
G = nx.cartesian_product(G1, G2)

# Tensor (Kronecker) product
G = nx.tensor_product(G1, G2)

# Strong product
G = nx.strong_product(G1, G2)
```

## 自定义和播种

### 设置随机种子
始终设置可重复的种子graphs:
```python
G = nx.erdos_renyi_graph(n=100, p=0.1, seed=42)
```

### 转换图形类型
```python
# Convert to specific type
G_directed = G.to_directed()
G_undirected = G.to_undirected()
G_multi = nx.MultiGraph(G)
```

## 性能注意事项

### 快速生成器
对于大型图，请使用优化的生成器：
```python
# Fast ER graph (sparse)
G = nx.fast_gnp_random_graph(n=10000, p=0.0001, seed=42)
```

### 内存效率
一些生成器增量创建图以节省内存。对于非常大的图，请考虑：
- 使用稀疏表示
- 根据需要生成子图
- 使用邻接列表或边列表而不是完整图

## 验证和属性

### 检查生成的图
```python
# Verify properties
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Density: {nx.density(G)}")
print(f"Connected: {nx.is_connected(G)}")

# Degree distribution
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
```
