# NetworkX 图形可视化

## 使用 Matplotlib 进行基本绘图

### 简单可视化
```python
import networkx as nx
import matplotlib.pyplot as plt

# Create and draw graph
G = nx.karate_club_graph()
nx.draw(G)
plt.show()

# Save to file
nx.draw(G)
plt.savefig('graph.png', dpi=300, bbox_inches='tight')
plt.close()
```

### 带标签绘图
```python
# Draw with node labels
nx.draw(G, with_labels=True)
plt.show()

# Custom labels
labels = {i: f"Node {i}" for i in G.nodes()}
nx.draw(G, labels=labels, with_labels=True)
plt.show()
```

## 布局算法

### Spring布局（强制导向）
```python
# Fruchterman-Reingold force-directed algorithm
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos=pos, with_labels=True)
plt.show()

# With parameters
pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
```

### 循环布局
```python
# Arrange nodes in circle
pos = nx.circular_layout(G)
nx.draw(G, pos=pos, with_labels=True)
plt.show()
```

### 随机布局
```python
# Random positioning
pos = nx.random_layout(G, seed=42)
nx.draw(G, pos=pos, with_labels=True)
plt.show()
```

### Shell布局
```python
# Concentric circles
pos = nx.shell_layout(G)
nx.draw(G, pos=pos, with_labels=True)
plt.show()

# With custom shells
shells = [[0, 1, 2], [3, 4, 5, 6], [7, 8, 9]]
pos = nx.shell_layout(G, nlist=shells)
```

### 光谱布局
```python
# Use eigenvectors of graph Laplacian
pos = nx.spectral_layout(G)
nx.draw(G, pos=pos, with_labels=True)
plt.show()
```

### Kamada-Kawai 布局
```python
# Energy-based layout
pos = nx.kamada_kawai_layout(G)
nx.draw(G, pos=pos, with_labels=True)
plt.show()
```

### 平面布局
```python
# For planar graphs only
if nx.is_planar(G):
    pos = nx.planar_layout(G)
    nx.draw(G, pos=pos, with_labels=True)
    plt.show()
```

### 树布局
```python
# For tree graphs
if nx.is_tree(G):
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    nx.draw(G, pos=pos, with_labels=True)
    plt.show()
```

## 自定义节点外观

### 节点颜色
```python
# Single color
nx.draw(G, node_color='red')

# Different colors per node
node_colors = ['red' if G.degree(n) > 5 else 'blue' for n in G.nodes()]
nx.draw(G, node_color=node_colors)

# Color by attribute
colors = [G.nodes[n].get('value', 0) for n in G.nodes()]
nx.draw(G, node_color=colors, cmap=plt.cm.viridis)
plt.colorbar()
plt.show()
```

### 节点尺寸
```python
# Size by degree
node_sizes = [100 * G.degree(n) for n in G.nodes()]
nx.draw(G, node_size=node_sizes)

# Size by centrality
centrality = nx.degree_centrality(G)
node_sizes = [3000 * centrality[n] for n in G.nodes()]
nx.draw(G, node_size=node_sizes)
```

### 节点形状
```python
# Draw nodes separately with different shapes
pos = nx.spring_layout(G)

# Circle nodes
nx.draw_networkx_nodes(G, pos, nodelist=[0, 1, 2],
                       node_shape='o', node_color='red')

# Square nodes
nx.draw_networkx_nodes(G, pos, nodelist=[3, 4, 5],
                       node_shape='s', node_color='blue')

nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
plt.show()
```

### 节点边框
```python
nx.draw(G, pos=pos,
        node_color='lightblue',
        edgecolors='black',  # Node border color
        linewidths=2)        # Node border width
plt.show()
```

## 自定义边缘外观

### 边缘颜色
```python
# Single color
nx.draw(G, edge_color='gray')

# Different colors per edge
edge_colors = ['red' if G[u][v].get('weight', 1) > 0.5 else 'blue'
               for u, v in G.edges()]
nx.draw(G, edge_color=edge_colors)

# Color by weight
edges = G.edges()
weights = [G[u][v].get('weight', 1) for u, v in edges]
nx.draw(G, edge_color=weights, edge_cmap=plt.cm.Reds)
```

### 边宽度
```python
# Width by weight
edge_widths = [3 * G[u][v].get('weight', 1) for u, v in G.edges()]
nx.draw(G, width=edge_widths)

# Width by betweenness
edge_betweenness = nx.edge_betweenness_centrality(G)
edge_widths = [5 * edge_betweenness[(u, v)] for u, v in G.edges()]
nx.draw(G, width=edge_widths)
```

### 边样式
```python
# Dashed edges
nx.draw(G, style='dashed')

# Different styles per edge
pos = nx.spring_layout(G)
strong_edges = [(u, v) for u, v in G.edges() if G[u][v].get('weight', 0) > 0.5]
weak_edges = [(u, v) for u, v in G.edges() if G[u][v].get('weight', 0) <= 0.5]

nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=strong_edges, style='solid', width=2)
nx.draw_networkx_edges(G, pos, edgelist=weak_edges, style='dashed', width=1)
plt.show()
```

### 有向图（箭头）
```python
# Draw directed graph with arrows
G_directed = nx.DiGraph([(1, 2), (2, 3), (3, 1)])
pos = nx.spring_layout(G_directed)

nx.draw(G_directed, pos=pos, with_labels=True,
        arrows=True,
        arrowsize=20,
        arrowstyle='->',
        connectionstyle='arc3,rad=0.1')
plt.show()
```

## 标签和注释

### 节点标签
```python
pos = nx.spring_layout(G)

# Custom labels
labels = {n: f"N{n}" for n in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=12, font_color='white')

# Font customization
nx.draw_networkx_labels(G, pos,
                       font_size=10,
                       font_family='serif',
                       font_weight='bold')
```

### 边缘标签
```python
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)

# Edge labels from attributes
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()

# Custom edge labels
edge_labels = {(u, v): f"{u}-{v}" for u, v in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
```

## 高级绘图技术

### 组合绘图函数
```python
# Full control by separating components
pos = nx.spring_layout(G, seed=42)

# Draw edges
nx.draw_networkx_edges(G, pos, alpha=0.3, width=1)

# Draw nodes
nx.draw_networkx_nodes(G, pos,
                       node_color='lightblue',
                       node_size=500,
                       edgecolors='black')

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10)

# Remove axis
plt.axis('off')
plt.tight_layout()
plt.show()
```

### 子图突出显示
```python
pos = nx.spring_layout(G)

# Identify subgraph to highlight
subgraph_nodes = [1, 2, 3, 4]
subgraph = G.subgraph(subgraph_nodes)

# Draw main graph
nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=300)
nx.draw_networkx_edges(G, pos, alpha=0.2)

# Highlight subgraph
nx.draw_networkx_nodes(subgraph, pos, node_color='red', node_size=500)
nx.draw_networkx_edges(subgraph, pos, edge_color='red', width=2)

nx.draw_networkx_labels(G, pos)
plt.axis('off')
plt.show()
```

### 社区着色
```python
from networkx.algorithms import community

# Detect communities
communities = community.greedy_modularity_communities(G)

# Assign colors
color_map = {}
colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
for i, comm in enumerate(communities):
    for node in comm:
        color_map[node] = colors[i % len(colors)]

node_colors = [color_map[n] for n in G.nodes()]

pos = nx.spring_layout(G)
nx.draw(G, pos=pos, node_color=node_colors, with_labels=True)
plt.show()
```

## 创建出版物质量人物

### 高分辨率导出
```python
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)

nx.draw(G, pos=pos,
        node_color='lightblue',
        node_size=500,
        edge_color='gray',
        width=1,
        with_labels=True,
        font_size=10)

plt.title('Graph Visualization', fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.savefig('publication_graph.png', dpi=300, bbox_inches='tight')
plt.savefig('publication_graph.pdf', bbox_inches='tight')  # Vector format
plt.close()
```

### 多面板人物
```python
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Different layouts
layouts = [nx.circular_layout(G), nx.spring_layout(G), nx.spectral_layout(G)]
titles = ['Circular', 'Spring', 'Spectral']

for ax, pos, title in zip(axes, layouts, titles):
    nx.draw(G, pos=pos, ax=ax, with_labels=True, node_color='lightblue')
    ax.set_title(title)
    ax.axis('off')

plt.tight_layout()
plt.savefig('layouts_comparison.png', dpi=300)
plt.close()
```

## 交互式可视化库

### Plotly （交互式）
```python
import plotly.graph_objects as go

# Create positions
pos = nx.spring_layout(G)

# Edge trace
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

# Node trace
node_x = [pos[node][0] for node in G.nodes()]
node_y = [pos[node][1] for node in G.nodes()]

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=10,
        colorbar=dict(thickness=15, title='Node Connections'),
        line_width=2))

# Color by degree
node_adjacencies = [len(list(G.neighbors(node))) for node in G.nodes()]
node_trace.marker.color = node_adjacencies

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0, l=0, r=0, t=0)))

fig.show()
```

### PyVis（交互式 HTML）
```python
from pyvis.network import Network

# Create network
net = Network(notebook=True, height='750px', width='100%')

# Add nodes and edges from NetworkX
net.from_nx(G)

# Customize
net.show_buttons(filter_=['physics'])

# Save
net.show('graph.html')
```

### Graphviz（通过 pydot）
```python
# Requires graphviz and pydot
from networkx.drawing.nx_pydot import graphviz_layout

pos = graphviz_layout(G, prog='neato')  # neato, dot, fdp, sfdp, circo, twopi
nx.draw(G, pos=pos, with_labels=True)
plt.show()

# Export to graphviz
nx.drawing.nx_pydot.write_dot(G, 'graph.dot')
```

## 二分图可视化

### 两套布局
```python
from networkx.algorithms import bipartite

# Create bipartite graph
B = nx.Graph()
B.add_nodes_from([1, 2, 3, 4], bipartite=0)
B.add_nodes_from(['a', 'b', 'c', 'd', 'e'], bipartite=1)
B.add_edges_from([(1, 'a'), (1, 'b'), (2, 'b'), (2, 'c'), (3, 'd'), (4, 'e')])

# Layout with two columns
pos = {}
top_nodes = [n for n, d in B.nodes(data=True) if d['bipartite'] == 0]
bottom_nodes = [n for n, d in B.nodes(data=True) if d['bipartite'] == 1]

pos.update({node: (0, i) for i, node in enumerate(top_nodes)})
pos.update({node: (1, i) for i, node in enumerate(bottom_nodes)})

nx.draw(B, pos=pos, with_labels=True,
        node_color=['lightblue' if B.nodes[n]['bipartite'] == 0 else 'lightgreen'
                   for n in B.nodes()])
plt.show()
```

## 3D 可视化

### 3D 网络图
```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 3D spring layout
pos = nx.spring_layout(G, dim=3, seed=42)

# Extract coordinates
node_xyz = np.array([pos[v] for v in G.nodes()])
edge_xyz = np.array([(pos[u], pos[v]) for u, v in G.edges()])

# Create figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot edges
for vizedge in edge_xyz:
    ax.plot(*vizedge.T, color='gray', alpha=0.5)

# Plot nodes
ax.scatter(*node_xyz.T, s=100, c='lightblue', edgecolors='black')

# Labels
for i, (x, y, z) in enumerate(node_xyz):
    ax.text(x, y, z, str(i))

ax.set_axis_off()
plt.show()
```

## 最佳实践

### 性能
- 对于大型图（>1000个节点），使用更简单的布局（圆形、随机）
- 使用`alpha`参数使密集边缘更加可见
- 考虑对非常大的网络进行下采样或显示子图

### 美学
- 使用一致的配色方案
- 有意义地缩放节点大小（例如，按程度或重要性）
- 保持标签可读（调整字体大小和位置）
- 有效使用空白（调整图形大小）

### 再现性
- 始终为布局设置随机种子： `nx.spring_layout(G, seed=42)`
- 保存布局位置以确保多个绘图之间的一致性
- 图例或标题中的文档颜色/大小映射

### 文件格式
- 用于光栅图像（Web、演示文稿）的 PNG 
- 用于矢量图形（出版物、可扩展）
- 用于 Web 和交互式应用程序的 SVG
- 用于交互式可视化的 HTML
