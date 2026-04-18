# NetworkX 图算法

## 最短路径

### 单源最短路径
```python
# Dijkstra's algorithm (weighted graphs)
path = nx.shortest_path(G, source=1, target=5, weight='weight')
length = nx.shortest_path_length(G, source=1, target=5, weight='weight')

# All shortest paths from source
paths = nx.single_source_shortest_path(G, source=1)
lengths = nx.single_source_shortest_path_length(G, source=1)

# Bellman-Ford (handles negative weights)
path = nx.bellman_ford_path(G, source=1, target=5, weight='weight')
```

### 所有对最短路径
```python
# All pairs (returns iterator)
for source, paths in nx.all_pairs_shortest_path(G):
    print(f"From {source}: {paths}")

# Floyd-Warshall algorithm
lengths = dict(nx.all_pairs_shortest_path_length(G))
```

### 专用最短路径算法
```python
# A* algorithm (with heuristic)
def heuristic(u, v):
    # Custom heuristic function
    return abs(u - v)

path = nx.astar_path(G, source=1, target=5, heuristic=heuristic, weight='weight')

# Average shortest path length
avg_length = nx.average_shortest_path_length(G)
```

## 连接性

### 连接组件（无向）
```python
# Check if connected
is_connected = nx.is_connected(G)

# Number of components
num_components = nx.number_connected_components(G)

# Get all components (returns iterator of sets)
components = list(nx.connected_components(G))
largest_component = max(components, key=len)

# Get component containing specific node
component = nx.node_connected_component(G, node=1)
```

### 强/弱连接（有向）
```python
# Strong connectivity (mutually reachable)
is_strongly_connected = nx.is_strongly_connected(G)
strong_components = list(nx.strongly_connected_components(G))
largest_scc = max(strong_components, key=len)

# Weak connectivity (ignoring direction)
is_weakly_connected = nx.is_weakly_connected(G)
weak_components = list(nx.weakly_connected_components(G))

# Condensation (DAG of strongly connected components)
condensed = nx.condensation(G)
```

### 剪切和连通性
```python
# Minimum node/edge cut
min_node_cut = nx.minimum_node_cut(G, s=1, t=5)
min_edge_cut = nx.minimum_edge_cut(G, s=1, t=5)

# Node/edge connectivity
node_connectivity = nx.node_connectivity(G)
edge_connectivity = nx.edge_connectivity(G)
```

## 中心性度量

### 度中心性
```python
# Fraction of nodes each node is connected to
degree_cent = nx.degree_centrality(G)

# For directed graphs
in_degree_cent = nx.in_degree_centrality(G)
out_degree_cent = nx.out_degree_centrality(G)
```

### 介数中心性
```python
# Fraction of shortest paths passing through node
betweenness = nx.betweenness_centrality(G, weight='weight')

# Edge betweenness
edge_betweenness = nx.edge_betweenness_centrality(G, weight='weight')

# Approximate for large graphs
approx_betweenness = nx.betweenness_centrality(G, k=100)  # Sample 100 nodes
```

### 紧密度Centrality
```python
# Reciprocal of average shortest path length
closeness = nx.closeness_centrality(G)

# For disconnected graphs
closeness = nx.closeness_centrality(G, wf_improved=True)
```

### 特征向量中心性
```python
# Centrality based on connections to high-centrality nodes
eigenvector = nx.eigenvector_centrality(G, max_iter=1000)

# Katz centrality (variant with attenuation factor)
katz = nx.katz_centrality(G, alpha=0.1, beta=1.0)
```

### PageRank
```python
# Google's PageRank algorithm
pagerank = nx.pagerank(G, alpha=0.85)

# Personalized PageRank
personalization = {node: 1.0 if node in [1, 2] else 0.0 for node in G}
ppr = nx.pagerank(G, personalization=personalization)
```

## 聚类

### 聚类系数
```python
# Clustering coefficient for each node
clustering = nx.clustering(G)

# Average clustering coefficient
avg_clustering = nx.average_clustering(G)

# Weighted clustering
weighted_clustering = nx.clustering(G, weight='weight')
```

### 传递性
```python
# Overall clustering (ratio of triangles to triads)
transitivity = nx.transitivity(G)
```

### 三角形
```python
# Count triangles per node
triangles = nx.triangles(G)

# Total number of triangles
total_triangles = sum(triangles.values()) // 3
```

## 社区检测

### 基于模块化的
```python
from networkx.algorithms import community

# Greedy modularity maximization
communities = community.greedy_modularity_communities(G)

# Compute modularity
modularity = community.modularity(G, communities)
```

### 标签传播
```python
# Fast community detection
communities = community.label_propagation_communities(G)
```

### Girvan-Newman
```python
# Hierarchical community detection via edge betweenness
comp = community.girvan_newman(G)
limited = itertools.takewhile(lambda c: len(c) <= 10, comp)
for communities in limited:
    print(tuple(sorted(c) for c in communities))
```

## 匹配和覆盖

### 最大匹配
```python
# Maximum cardinality matching
matching = nx.max_weight_matching(G)

# Check if matching is valid
is_matching = nx.is_matching(G, matching)
is_perfect = nx.is_perfect_matching(G, matching)
```

### 最小顶点/边覆盖
```python
# Minimum set of nodes covering all edges
min_vertex_cover = nx.approximation.min_weighted_vertex_cover(G)

# Minimum edge dominating set
min_edge_dom = nx.approximation.min_edge_dominating_set(G)
```

## 树算法

### 最小跨度树
```python
# Kruskal's or Prim's algorithm
mst = nx.minimum_spanning_tree(G, weight='weight')

# Maximum spanning tree
mst_max = nx.maximum_spanning_tree(G, weight='weight')

# Enumerate all spanning trees
all_spanning = nx.all_spanning_trees(G)
```

### 树属性
```python
# Check if graph is tree
is_tree = nx.is_tree(G)
is_forest = nx.is_forest(G)

# For directed graphs
is_arborescence = nx.is_arborescence(G)
```

## 流量和容量

### 最大流量
```python
# Maximum flow value
flow_value = nx.maximum_flow_value(G, s=1, t=5, capacity='capacity')

# Maximum flow with flow dict
flow_value, flow_dict = nx.maximum_flow(G, s=1, t=5, capacity='capacity')

# Minimum cut
cut_value, partition = nx.minimum_cut(G, s=1, t=5, capacity='capacity')
```

### 成本流程
```python
# Minimum cost flow
flow_dict = nx.min_cost_flow(G, demand='demand', capacity='capacity', weight='weight')
cost = nx.cost_of_flow(G, flow_dict, weight='weight')
```

## 循环

### 查找循环
```python
# Simple cycles (for directed graphs)
cycles = list(nx.simple_cycles(G))

# Cycle basis (for undirected graphs)
basis = nx.cycle_basis(G)

# Check if acyclic
is_dag = nx.is_directed_acyclic_graph(G)
```

### 拓扑排序
```python
# Only for DAGs
try:
    topo_order = list(nx.topological_sort(G))
except nx.NetworkXError:
    print("Graph has cycles")

# All topological sorts
all_topo = nx.all_topological_sorts(G)
```

## 派系

### 查找派系
```python
# All maximal cliques
cliques = list(nx.find_cliques(G))

# Maximum clique (NP-complete, approximate)
max_clique = nx.approximation.max_clique(G)

# Clique number
clique_number = nx.graph_clique_number(G)

# Number of maximal cliques containing each node
clique_counts = nx.node_clique_number(G)
```

## 图着色

### 节点着色
```python
# Greedy coloring
coloring = nx.greedy_color(G, strategy='largest_first')

# Different strategies: 'largest_first', 'smallest_last', 'random_sequential'
coloring = nx.greedy_color(G, strategy='smallest_last')
```

## 同构

### 图同构
```python
# Check if graphs are isomorphic
is_isomorphic = nx.is_isomorphic(G1, G2)

# Get isomorphism mapping
from networkx.algorithms import isomorphism
GM = isomorphism.GraphMatcher(G1, G2)
if GM.is_isomorphic():
    mapping = GM.mapping
```

### 子图同构
```python
# Check if G1 is subgraph isomorphic to G2
is_subgraph_iso = nx.is_isomorphic(G1, G2.subgraph(nodes))
```

## 遍历算法

### 深度优先搜索(DFS)
```python
# DFS edges
dfs_edges = list(nx.dfs_edges(G, source=1))

# DFS tree
dfs_tree = nx.dfs_tree(G, source=1)

# DFS predecessors
dfs_pred = nx.dfs_predecessors(G, source=1)

# Preorder and postorder
preorder = list(nx.dfs_preorder_nodes(G, source=1))
postorder = list(nx.dfs_postorder_nodes(G, source=1))
```

### 广度优先搜索 (BFS)
```python
# BFS edges
bfs_edges = list(nx.bfs_edges(G, source=1))

# BFS tree
bfs_tree = nx.bfs_tree(G, source=1)

# BFS predecessors and successors
bfs_pred = nx.bfs_predecessors(G, source=1)
bfs_succ = nx.bfs_successors(G, source=1)
```

## 效率考虑

### 算法复杂度
- 许多算法都有参数来控制计算time
- 对于大图，考虑近似算法
- 在中心性计算中使用`k`参数对节点进行采样
- 为迭代算法设置`max_iter`

### 内存使用
- 基于迭代器的函数（例如，`nx.simple_cycles()`）节省内存
- 仅在必要时转换为列表
- 对大型结果集使用生成器

### 数值精度
当使用带有浮点数的加权算法时，结果是近似值。考虑：
- 尽可能使用整数权重
- 设置适当的容差参数
- 意识到迭代算法中累积的舍入误差
