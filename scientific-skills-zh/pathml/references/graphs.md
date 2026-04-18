# 图构建和空间分析

## 概述

PathML 提供了从组织图像构建空间图以表示细胞和组织水平关系的工具。基于图的表示可以实现复杂的空间分析，包括邻域分析、细胞间相互作用研究和图神经网络应用。这些图捕获形态特征和空间拓扑，用于下游计算分析。

## 图类型

PathML支持多种图类型的构建：

### 细胞图
- 节点代表单个细胞
- 边缘代表空间邻近性或生物相互作用
- 节点特征包括形态、标记表达、细胞类型
- 适合单细胞空间分析

### 组织图
- 节点代表组织区域或超像素
- 边缘代表空间邻接
- 节点特征包括组织组成、纹理特征
- 适合组织级空间模式

### 空间转录组学图
- 节点代表空间点或细胞
- 边缘编码空间关系
- 节点特征包括基因表达谱
- 适用于空间组学分析

## 图构建工作流程

### 从分割到图

转换细胞核或单元格分割结果转换为空间图：

```python
from pathml.graph import CellGraph
from pathml.preprocessing import Pipeline, SegmentMIF
import numpy as np

# 1. Perform cell segmentation
pipeline = Pipeline([
    SegmentMIF(
        nuclear_channel='DAPI',
        cytoplasm_channel='CD45',
        model='mesmer'
    )
])
pipeline.run(slide)

# 2. Extract instance segmentation mask
inst_map = slide.masks['cell_segmentation']

# 3. Build cell graph
cell_graph = CellGraph.from_instance_map(
    inst_map,
    image=slide.image,  # Optional: for extracting visual features
    connectivity='delaunay',  # 'knn', 'radius', or 'delaunay'
    k=5,  # For knn: number of neighbors
    radius=50  # For radius: distance threshold in pixels
)

# 4. Access graph components
nodes = cell_graph.nodes  # Node features
edges = cell_graph.edges  # Edge list
adjacency = cell_graph.adjacency_matrix  # Adjacency matrix
```

### 连接方法

* *K-最近邻居 (KNN)：**
```python
# Connect each cell to its k nearest neighbors
graph = CellGraph.from_instance_map(
    inst_map,
    connectivity='knn',
    k=5  # Number of neighbors
)
```
- 每个节点的固定度数
- 捕获局部邻域
- 简单且可解释

* *基于半径：**
```python
# Connect cells within a distance threshold
graph = CellGraph.from_instance_map(
    inst_map,
    connectivity='radius',
    radius=100,  # Maximum distance in pixels
    distance_metric='euclidean'  # or 'manhattan', 'chebyshev'
)
```
-基于密度的可变程度
- 生物动机（交互范围）
- 捕获物理接近度

* *Delaunay三角测量：**
```python
# Connect cells using Delaunay triangulation
graph = CellGraph.from_instance_map(
    inst_map,
    connectivity='delaunay'
)
```
-创建连通图空间位置
- 没有孤立的节点（在凸包中）
- 捕获空间镶嵌

* *基于接触：**
```python
# Connect cells with touching boundaries
graph = CellGraph.from_instance_map(
    inst_map,
    connectivity='contact',
    dilation=2  # Dilate boundaries to capture near-contacts
)
```
-物理细胞与细胞接触
- 最直接的生物学
- 分离细胞的稀疏边缘

## 节点特征

### 形态特征

提取每个细胞的形状和大小特征细胞：

```python
from pathml.graph import extract_morphology_features

# Compute morphological features
morphology_features = extract_morphology_features(
    inst_map,
    features=[
        'area',  # Cell area in pixels
        'perimeter',  # Cell perimeter
        'eccentricity',  # Shape elongation
        'solidity',  # Convexity measure
        'major_axis_length',
        'minor_axis_length',
        'orientation'  # Cell orientation angle
    ]
)

# Add to graph
cell_graph.add_node_features(morphology_features, feature_names=['area', 'perimeter', ...])
```

* *可用形态特征：**
- **面积** - 像素数
- **周长** - 边界长度
- **偏心率** - 0（圆）到1（线）
- **实体度** - 面积/凸包面积
- **圆度** - 4π × 面积/周长²
- **长/短轴** - 拟合椭圆轴的长度
- **方向** - 长轴角度
- **范围** - 面积/边界框区域

### 强度特征

提取标记表达或强度统计：

```python
from pathml.graph import extract_intensity_features

# Extract mean marker intensities per cell
intensity_features = extract_intensity_features(
    inst_map,
    image=multichannel_image,  # Shape: (H, W, C)
    channel_names=['DAPI', 'CD3', 'CD4', 'CD8', 'CD20'],
    statistics=['mean', 'std', 'median', 'max']
)

# Add to graph
cell_graph.add_node_features(
    intensity_features,
    feature_names=['DAPI_mean', 'CD3_mean', ...]
)
```

* *可用统计：**
- **平均值** - 平均强度
- **中位数** - 中值强度
- **std** - 标准偏差
- **max** - 最大强度
- **min** - 最小强度
- **quantile_25/75** - 四分位数

### 纹理特征

计算每个单元的纹理描述符区域：

```python
from pathml.graph import extract_texture_features

# Haralick texture features
texture_features = extract_texture_features(
    inst_map,
    image=grayscale_image,
    features='haralick',  # or 'lbp', 'gabor'
    distance=1,
    angles=[0, np.pi/4, np.pi/2, 3*np.pi/4]
)

cell_graph.add_node_features(texture_features)
```

### 单元类型注释

从分类中添加单元类型标签：

```python
# From ML model predictions
cell_types = hovernet_type_predictions  # Array of cell type IDs

cell_graph.add_node_features(
    cell_types,
    feature_names=['cell_type']
)

# One-hot encode cell types
cell_type_onehot = one_hot_encode(cell_types, num_classes=5)
cell_graph.add_node_features(
    cell_type_onehot,
    feature_names=['type_epithelial', 'type_inflammatory', ...]
)
```

## 边缘特征

### 空间距离

根据空间计算边缘特征关系：

```python
from pathml.graph import compute_edge_distances

# Add pairwise distances as edge features
distances = compute_edge_distances(
    cell_graph,
    metric='euclidean'  # or 'manhattan', 'chebyshev'
)

cell_graph.add_edge_features(distances, feature_names=['distance'])
```

### 交互特征

模型细胞类型之间的生物相互作用：

```python
from pathml.graph import compute_interaction_features

# Cell type co-occurrence along edges
interaction_features = compute_interaction_features(
    cell_graph,
    cell_types=cell_type_labels,
    interaction_type='categorical'  # or 'numerical'
)

cell_graph.add_edge_features(interaction_features)
```

## 图形级特征

整个的聚合特征图：

```python
from pathml.graph import compute_graph_features

# Topological features
graph_features = compute_graph_features(
    cell_graph,
    features=[
        'num_nodes',
        'num_edges',
        'average_degree',
        'clustering_coefficient',
        'average_path_length',
        'diameter'
    ]
)

# Cell composition features
composition = cell_graph.compute_cell_type_composition(
    cell_type_labels,
    normalize=True  # Proportions
)
```

## 空间分析

### 邻域分析

分析细胞邻域和微环境：

```python
from pathml.graph import analyze_neighborhoods

# Characterize neighborhoods around each cell
neighborhoods = analyze_neighborhoods(
    cell_graph,
    cell_types=cell_type_labels,
    radius=100,  # Neighborhood radius
    metrics=['diversity', 'density', 'composition']
)

# Neighborhood diversity (Shannon entropy)
diversity = neighborhoods['diversity']

# Cell type composition in each neighborhood
composition = neighborhoods['composition']  # (n_cells, n_cell_types)
```

### 空间聚类

识别空间簇细胞类型：

```python
from pathml.graph import spatial_clustering
import matplotlib.pyplot as plt

# Detect spatial clusters
clusters = spatial_clustering(
    cell_graph,
    cell_positions,
    method='dbscan',  # or 'kmeans', 'hierarchical'
    eps=50,  # DBSCAN: neighborhood radius
    min_samples=10  # DBSCAN: minimum cluster size
)

# Visualize clusters
plt.scatter(
    cell_positions[:, 0],
    cell_positions[:, 1],
    c=clusters,
    cmap='tab20'
)
plt.title('Spatial Clusters')
plt.show()
```

### 细胞间相互作用分析

细胞类型相互作用的富集或耗尽测试：

```python
from pathml.graph import cell_interaction_analysis

# Test for significant interactions
interaction_results = cell_interaction_analysis(
    cell_graph,
    cell_types=cell_type_labels,
    method='permutation',  # or 'expected'
    n_permutations=1000,
    significance_level=0.05
)

# Interaction scores (positive = attraction, negative = avoidance)
interaction_matrix = interaction_results['scores']

# Visualize with heatmap
import seaborn as sns
sns.heatmap(
    interaction_matrix,
    cmap='RdBu_r',
    center=0,
    xticklabels=cell_type_names,
    yticklabels=cell_type_names
)
plt.title('Cell-Cell Interaction Scores')
plt.show()
```

### 空间统计

计算空间统计和模式：

```python
from pathml.graph import spatial_statistics

# Ripley's K function for spatial point patterns
ripleys_k = spatial_statistics(
    cell_positions,
    cell_types=cell_type_labels,
    statistic='ripleys_k',
    radii=np.linspace(0, 200, 50)
)

# Nearest neighbor distances
nn_distances = spatial_statistics(
    cell_positions,
    statistic='nearest_neighbor',
    by_cell_type=True
)
```

## 与图神经网络集成

### 转换为 PyTorch 几何格式

```python
from pathml.graph import to_pyg
import torch
from torch_geometric.data import Data

# Convert to PyTorch Geometric Data object
pyg_data = cell_graph.to_pyg()

# Access components
x = pyg_data.x  # Node features (n_nodes, n_features)
edge_index = pyg_data.edge_index  # Edge connectivity (2, n_edges)
edge_attr = pyg_data.edge_attr  # Edge features (n_edges, n_edge_features)
y = pyg_data.y  # Graph-level label
pos = pyg_data.pos  # Node positions (n_nodes, 2)

# Use with PyTorch Geometric
from torch_geometric.nn import GCNConv

class GNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

model = GNN(in_channels=pyg_data.num_features, hidden_channels=64, out_channels=5)
output = model(pyg_data)
```

### 多个幻灯片的图形数据集

```python
from pathml.graph import GraphDataset
from torch_geometric.loader import DataLoader

# Create dataset of graphs from multiple slides
graphs = []
for slide in slides:
    # Build graph for each slide
    cell_graph = CellGraph.from_instance_map(slide.inst_map, ...)
    pyg_graph = cell_graph.to_pyg()
    graphs.append(pyg_graph)

# Create DataLoader
loader = DataLoader(graphs, batch_size=32, shuffle=True)

# Train GNN
for batch in loader:
    output = model(batch)
    loss = criterion(output, batch.y)
    loss.backward()
    optimizer.step()
```

## 可视化

### 图形可视化

```python
import matplotlib.pyplot as plt
import networkx as nx

# Convert to NetworkX
nx_graph = cell_graph.to_networkx()

# Draw graph with cell positions as layout
pos = {i: cell_graph.positions[i] for i in range(len(cell_graph.nodes))}

plt.figure(figsize=(12, 12))
nx.draw_networkx(
    nx_graph,
    pos=pos,
    node_color=cell_type_labels,
    node_size=50,
    cmap='tab10',
    with_labels=False,
    alpha=0.8
)
plt.axis('equal')
plt.title('Cell Graph')
plt.show()
```

### 组织图像上的叠加

```python
from pathml.graph import visualize_graph_on_image

# Visualize graph overlaid on tissue
fig, ax = plt.subplots(figsize=(15, 15))
ax.imshow(tissue_image)

# Draw edges
for edge in cell_graph.edges:
    node1, node2 = edge
    pos1 = cell_graph.positions[node1]
    pos2 = cell_graph.positions[node2]
    ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 'b-', alpha=0.3, linewidth=0.5)

# Draw nodes colored by type
for cell_type in np.unique(cell_type_labels):
    mask = cell_type_labels == cell_type
    positions = cell_graph.positions[mask]
    ax.scatter(positions[:, 0], positions[:, 1], label=f'Type {cell_type}', s=20)

ax.legend()
ax.axis('off')
plt.title('Cell Graph on Tissue')
plt.show()
```

## 完整工作流程示例

```python
from pathml.core import SlideData, CODEXSlide
from pathml.preprocessing import Pipeline, CollapseRunsCODEX, SegmentMIF
from pathml.graph import CellGraph, extract_morphology_features, extract_intensity_features
import matplotlib.pyplot as plt

# 1. Load and preprocess slide
slide = CODEXSlide('path/to/codex', stain='IF')

pipeline = Pipeline([
    CollapseRunsCODEX(z_slice=2),
    SegmentMIF(
        nuclear_channel='DAPI',
        cytoplasm_channel='CD45',
        model='mesmer'
    )
])
pipeline.run(slide)

# 2. Build cell graph
inst_map = slide.masks['cell_segmentation']
cell_graph = CellGraph.from_instance_map(
    inst_map,
    image=slide.image,
    connectivity='knn',
    k=6
)

# 3. Extract features
# Morphological features
morph_features = extract_morphology_features(
    inst_map,
    features=['area', 'perimeter', 'eccentricity', 'solidity']
)
cell_graph.add_node_features(morph_features)

# Intensity features (marker expression)
intensity_features = extract_intensity_features(
    inst_map,
    image=slide.image,
    channel_names=['DAPI', 'CD3', 'CD4', 'CD8', 'CD20'],
    statistics=['mean', 'std']
)
cell_graph.add_node_features(intensity_features)

# 4. Spatial analysis
from pathml.graph import analyze_neighborhoods

neighborhoods = analyze_neighborhoods(
    cell_graph,
    cell_types=cell_type_predictions,
    radius=100,
    metrics=['diversity', 'composition']
)

# 5. Export for GNN
pyg_data = cell_graph.to_pyg()

# 6. Visualize
plt.figure(figsize=(15, 15))
plt.imshow(slide.image)

# Overlay graph
nx_graph = cell_graph.to_networkx()
pos = {i: cell_graph.positions[i] for i in range(cell_graph.num_nodes)}
nx.draw_networkx(
    nx_graph,
    pos=pos,
    node_color=cell_type_predictions,
    cmap='tab10',
    node_size=30,
    with_labels=False
)
plt.axis('off')
plt.title('Cell Graph with Spatial Neighborhood')
plt.show()
```

## 性能注意事项

* *大组织部分：**
- 逐块构建图，然后合并
- 使用稀疏邻接矩阵
- 利用GPU进行特征提取

* *内存效率：**
- 仅存储必要的边缘特征
- 使用int32/float32而不是int64/float64
- 批量处理多个幻灯片

* *计算效率：**
- 跨单元并行特征提取
- 使用 KNN 进行更快的邻居查询
- 缓存计算的特征

## 最佳实践

1. **选择适当的连接：** KNN 用于统一分析，半径用于物理交互，接触用于直接细胞间通信

2. **标准化特征：**缩放形态和强度特征以实现 GNN 兼容性

3. **处理边缘效应：**排除边界单元或使用组织掩模来定义有效区域

4. **验证图的构造：**在大规模处理之前可视化小区域上的图

5. **组合多种特征类型：**形态+强度+纹理提供丰富的表示

6. **考虑组织背景：**组织类型影响适当的图形参数（连通性、半径）

## 常见问题和解决方案

* *问题：边缘太多/太少**
- 调整k（KNN）或半径（基于半径）参数
- 验证生物相关性的像素到微米转换

* *问题：大图的内存错误**
- 单独处理图块并合并图
- 使用稀疏矩阵表示
- 将边缘特征减少到基本特征

* *问题：组织边界处缺少细胞**
- 应用边缘校正参数
- 使用组织掩模排除无效区域

* *问题：特征尺度不一致**
- 标准化特征：`(x - mean) / std`
- 对异常值使用稳健缩放

## 其他资源

- **PathML 图形 API：** https://pathml.readthedocs.io/en/latest/api_graph_reference.html
- **PyTorch 几何：** https://pytorch-geometric.readthedocs.io/
- **NetworkX：** https://networkx.org/
- **空间统计：** Baddeley 等人，“空间点模式：R 的方法和应用”
