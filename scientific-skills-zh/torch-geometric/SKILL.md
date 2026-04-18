---
name: torch-geometric
description: "使用 PyTorch Geometric (PyG)构建图神经网络的指南。每当用户询问图神经网络、GNN、节点分类、链接预测、图分类、消息传递网络、异构图、邻居采样或涉及 torch_geometric / PyG 的任何任务时，请使用此技能。当您看到来自 torch_geometric 的导入，或者用户提到图形卷积（GCN、GAT、GraphSAGE、GIN）、图形数据结构或使用关系/网络数据时也会触发。即使用户只是说“图形学习”或“几何深度学习”，也可以使用此技能。"
---

# PyTorch Geometric (PyG)

PyG 是基于 PyTorch 构建的图神经网络的标准库。它提供了图的数据结构、60+ GNN 层实现、可扩展的小批量训练以及对异构图的支持。

安装：`uv add torch_geometric`（或 `uv pip install torch_geometric`；需要 PyTorch）。可选：`pyg-lib`、`torch-scatter`、`torch-sparse`、`torch-cluster` 用于加速操作。

## 核心概念

### 图形数据：`Data` 和 `HeteroData`

A 图形位于 `Data` 对象中。关键属性：

```python
from torch_geometric.data import Data

data = Data(
    x=node_features,          # [num_nodes, num_node_features]
    edge_index=edge_index,     # [2, num_edges] — COO format, dtype=torch.long
    edge_attr=edge_features,   # [num_edges, num_edge_features]
    y=labels,                  # node-level [num_nodes, *] or graph-level [1, *]
    pos=positions,             # [num_nodes, num_dimensions] (for point clouds/spatial)
)
```

* *`edge_index` 格式至关重要**：它是一个 `[2, num_edges]` 张量，其中 `edge_index[0]` = 源节点，`edge_index[1]` = 目标节点。它不是元组列表。如果将边对作为行，则转置并调用 `.contiguous()`:

```python
# If edges are [[src1, dst1], [src2, dst2], ...] — transpose first:
edge_index = edge_pairs.t().contiguous()
```

 对于无向图，包括两个方向：边 (0,1)需要在 edge_index 中同时使用 `[0,1]` 和 `[1,0]`。

 对于异构图，请使用`HeteroData` — 请参阅下面的异构图部分。

### 数据集

PyG 捆绑了许多自动下载和预处理的标准数据集：

```python
from torch_geometric.datasets import Planetoid, TUDataset

# Single-graph node classification (Cora, Citeseer, Pubmed)
dataset = Planetoid(root='./data', name='Cora')
data = dataset[0]  # single graph with train/val/test masks

# Multi-graph classification (ENZYMES, MUTAG, IMDB-BINARY, etc.)
dataset = TUDataset(root='./data', name='ENZYMES')
# dataset[0], dataset[1], ... are individual graphs
```

 按任务划分的常见数据集：
- **节点分类**：小行星(Cora/Citeseer/Pubmed)、OGB (ogbn-arxiv、ogbn-products、ogbn-mag)
- **图分类**：TU 数据集 (MUTAG、ENZYMES、PROTEINS、IMDB-BINARY)、OGB (ogbg-molhiv)
- **链接预测**：OGB (ogbl-collab、 ogbl-引用2)
- **分子**：QM7、QM9、MoleculeNet
- **点云/网格**：ShapeNet、ModelNet10/40、FAUST

### 变换

变换预处理或增强图形数据，类似于 torchvision变换：

```python
import torch_geometric.transforms as T

# Common transforms
T.NormalizeFeatures()    # Row-normalize node features to sum to 1
T.ToUndirected()         # Add reverse edges to make graph undirected
T.AddSelfLoops()         # Add self-loop edges
T.KNNGraph(k=6)          # Build k-NN graph from point cloud positions
T.RandomJitter(0.01)     # Random noise augmentation on positions
T.Compose([...])         # Chain multiple transforms

# Apply as pre_transform (once, saved to disk) or transform (every access)
dataset = ShapeNet(root='./data', pre_transform=T.KNNGraph(k=6),
                   transform=T.RandomJitter(0.01))
```

## 构建 GNN 模型

### 快速入门：使用内置层

构建 GNN 的最快方法 - 来自 `torch_geometric.nn`:

 的堆栈转换层```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class GCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        return x
```

**重要**：PyG 转换层不包含激活函数 - 在每层之后自行应用它们。这是为了灵活性而设计的。

### 选择Conv Layer

根据您的任务和图形结构选择：

|层|最适合 |关键思想|
|--------|---------|----------|
| `GCNConv` |同质、半监督节点分类 |受光谱启发、度归一化聚合 |
| `GATConv` / `GATv2Conv` |当邻居重要性不同时 |注意力加权消息|
| `SAGEConv` |大图，归纳设置|采样友好、可学习的聚合|
| `GINConv` |图分类，最大化表现力 |与WL测试一样强大|
| `TransformerConv` |丰富的边缘特征，复杂的交互 |具有边缘特征的多头注意力|
| `EdgeConv` |点云、动态图|边缘特征 (x_i, x_j - x_i) |
| 上的 MLP `RGCNConv` |具有多种关系类型的异构 |特定于关系的权重矩阵 |
| `HGTConv` |异构图|特定于类型的注意力|

所有转换层至少接受`(x, edge_index)`。许多人还接受 `edge_attr` 作为边缘特征。

### 延迟初始化

 使用 `-1` 作为输入通道，让 PyG 自动推断尺寸 - 对于异构模型特别有用：

```python
conv = SAGEConv((-1, -1), 64)  # Input dims inferred on first forward pass
# Initialize lazy modules:
with torch.no_grad():
    out = model(data.x, data.edge_index)
```

### 高级模型 API

 对于常见架构中，PyG 提供了现成的模型类：

```python
from torch_geometric.nn import GraphSAGE, GCN, GAT, GIN

model = GraphSAGE(
    in_channels=dataset.num_features,
    hidden_channels=64,
    out_channels=dataset.num_classes,
    num_layers=2,
)
```

### 通过 MessagePassing 自定义层 

 来实现新颖的 GNN 层，子类 `MessagePassing`。框架为：

1、`propagate()`编排消息传递
2。 `message()` 定义沿每条边流动的信息（phi 函数）
3。 `aggregate()` 在每个节点组合消息（总和/平均值/最大值）
4。 `update()` 转换聚合结果（gamma 函数）

```python
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree

class MyConv(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super().__init__(aggr='add')  # "add", "mean", or "max"
        self.lin = torch.nn.Linear(in_channels, out_channels)

    def forward(self, x, edge_index):
        # Pre-processing before message passing
        x = self.lin(x)
        # Start message passing
        return self.propagate(edge_index, x=x)

    def message(self, x_j):
        # x_j: features of source nodes for each edge [num_edges, features]
        # The _j suffix auto-indexes source nodes, _i indexes target nodes
        return x_j
```

**`_i` / `_j` 约定**：传递给 `propagate()` 的任何张量都可以通过附加 `_i` （目标/中心节点）或`message()` 签名中的 `_j`（源/邻居节点）。因此，如果您传递 `x=...` 进行传播，则可以在 message()中访问 `x_i` 和 `x_j`。

阅读 `references/message_passing.md` 以获取完整的 GCN 和 EdgeConv 实现示例。

## 任务特定模式

### 节点分类

```python
# Full-batch training on a single graph (e.g., Cora)
model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()

# Evaluation
model.eval()
pred = model(data.x, data.edge_index).argmax(dim=1)
acc = (pred[data.test_mask] == data.y[data.test_mask]).float().mean()
```

###图分类

多个图——使用`DataLoader`进行小批处理和全局池化以获得图级表示：

```python
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv, global_mean_pool

loader = DataLoader(dataset, batch_size=32, shuffle=True)

class GraphClassifier(torch.nn.Module):
    def __init__(self, in_ch, hidden_ch, out_ch):
        super().__init__()
        self.conv1 = GCNConv(in_ch, hidden_ch)
        self.conv2 = GCNConv(hidden_ch, hidden_ch)
        self.lin = torch.nn.Linear(hidden_ch, out_ch)

    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index).relu()
        x = global_mean_pool(x, batch)  # [num_graphs_in_batch, hidden_ch]
        return self.lin(x)

# Training loop
for data in loader:
    out = model(data.x, data.edge_index, data.batch)
    loss = F.cross_entropy(out, data.y)
```

PyG的`DataLoader`通过创建块对角邻接矩阵来批量处理多个图。 `batch` 张量将每个节点映射到其图索引。池化操作（`global_mean_pool`、`global_max_pool`、`global_add_pool`）使用它来聚合每个图。

###链接预测

将边分割为训练/验证/测试，使用负采样：

```python
from torch_geometric.transforms import RandomLinkSplit

transform = RandomLinkSplit(
    num_val=0.1,
    num_test=0.1,
    is_undirected=True,
    add_negative_train_samples=False,
)
train_data, val_data, test_data = transform(data)

# Encode nodes, then score edges
z = model.encode(train_data.x, train_data.edge_index)
# Positive edges
pos_score = (z[train_data.edge_label_index[0]] * z[train_data.edge_label_index[1]]).sum(dim=1)
```

Read `references/link_prediction.md` 提供完整的链接预测指南：GAE/VGAE 自动编码器、完整训练循环、用于大图的 LinkNeighborLoader、异构链接预测和评估指标。

## 缩放到大图

对于不适合 GPU 内存的图，通过 `NeighborLoader`:

 使用邻居采样```python
from torch_geometric.loader import NeighborLoader

train_loader = NeighborLoader(
    data,
    num_neighbors=[15, 10],     # Sample 15 neighbors in hop 1, 10 in hop 2
    batch_size=128,              # Number of seed nodes per batch
    input_nodes=data.train_mask, # Which nodes to sample from
    shuffle=True,
)

for batch in train_loader:
    batch = batch.to(device)
    out = model(batch.x, batch.edge_index)
    # Only use first batch_size nodes for loss (these are the seed nodes)
    loss = F.cross_entropy(out[:batch.batch_size], batch.y[:batch.batch_size])
```

* *有关 NeighborLoader 的要点**：
- `num_neighbors` 列表长度应与 GNN 深度（消息传递层数）匹配 
- 种子节点始终是输出中的第一个 `batch.batch_size` 节点
- `batch.n_id` 将重新标记的索引映射回到原始节点ID
- 适用于`Data`和`HeteroData`
- 对于链路预测，使用`LinkNeighborLoader`代替
- 采样超过2-3跳通常是不可行的（指数爆炸）

其他可扩展性选项： `ClusterLoader`（集群GCN）、`GraphSAINTSampler`、`ShaDowKHopSampler`。对于多 GPU 训练、DDP、PyTorch Lightning 集成和 `torch.compile` 支持，请阅读 `references/scaling.md`.

## 异构图

对于具有多个节点和边缘类型的图（社交网络、知识图、推荐）：

```python
from torch_geometric.data import HeteroData

data = HeteroData()

# Node features — indexed by node type string
data['user'].x = torch.randn(1000, 64)
data['movie'].x = torch.randn(500, 128)

# Edge indices — indexed by (src_type, edge_type, dst_type) triplet
data['user', 'rates', 'movie'].edge_index = torch.randint(0, 500, (2, 3000))
data['user', 'follows', 'user'].edge_index = torch.randint(0, 1000, (2, 5000))

# Access convenience dicts
data.x_dict        # {'user': tensor, 'movie': tensor}
data.edge_index_dict  # {('user','rates','movie'): tensor, ...}
data.metadata()    # ([node_types], [edge_types])
```

### 三种方式构建异构 GNN

* *1。使用 `to_hetero()` 自动转换** — 编写同类模型，自动转换：

```python
from torch_geometric.nn import SAGEConv, to_hetero

class GNN(torch.nn.Module):
    def __init__(self, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

model = GNN(64, dataset.num_classes)
model = to_hetero(model, data.metadata(), aggr='sum')

# Now accepts dicts:
out = model(data.x_dict, data.edge_index_dict)
```

 将 `(-1, -1)` 用于双向输入通道（源、目标可能不同）。惰性初始化处理剩下的事情。

* *2。 `HeteroConv` 包装器** — 每个边缘类型的不同转换：

```python
from torch_geometric.nn import HeteroConv, GCNConv, SAGEConv, GATConv

conv = HeteroConv({
    ('paper', 'cites', 'paper'): GCNConv(-1, 64),
    ('author', 'writes', 'paper'): SAGEConv((-1, -1), 64),
    ('paper', 'rev_writes', 'author'): GATConv((-1, -1), 64, add_self_loops=False),
}, aggr='sum')
```

* *3。原生异构运算符**如`HGTConv`：

```python
from torch_geometric.nn import HGTConv
conv = HGTConv(hidden_channels, hidden_channels, data.metadata(), num_heads=4)
```

* *对于异构图很重要**：
- 使用`T.ToUndirected()`为双向消息流添加反向边缘类型
- 在二分转换层中禁用`add_self_loops`（不同源/目标类型） — 使用跳过连接代替： `conv(x, edge_index) + lin(x)`
- 对于 HeteroData 上的 NeighborLoader，将 `input_nodes` 指定为 `('node_type', mask)` 元组
- `num_neighbors` 可以是由边缘类型键入的字典，以进行细粒度控制

Read `references/heterogeneous.md` 的完整示例，包括训练循环和 NeighborLoader 在异构图上的使用。

## 自定义数据集

用于将您自己的数据加载到 PyG 中：

- **快速（无需类）**：直接创建 `Data` 对象并将列表传递给 `DataLoader`
  - **可重用（适合 RAM）**：子类 `InMemoryDataset` — 覆盖 `raw_file_names`、`processed_file_names`、`download()`、 `process()`
- **大型（磁盘支持）**：子类 `Dataset` — 也覆盖 `len()` 和 `get()`
- **从 CSV**：使用 pandas 加载节点/边缘表，构建到连续索引的映射，组装成 `Data` 或`HeteroData`
- **来自NetworkX**：`from_networkx(G)`直接转换NetworkX图
- **来自scipy稀疏**：`from_scipy_sparse_matrix(adj)`提取edge_index

阅读`references/custom_datasets.md`以获取包含所有模式的完整示例，CSV加载

## 可解释性

PyG 提供 `torch_geometric.explain` 用于解释 GNN 预测：

```python
from torch_geometric.explain import Explainer, GNNExplainer

explainer = Explainer(
    model=model,
    algorithm=GNNExplainer(epochs=200),
    explanation_type='model',
    node_mask_type='attributes',
    edge_mask_type='object',
    model_config=dict(
        mode='multiclass_classification',
        task_level='node',
        return_type='log_probs',
    ),
)

explanation = explainer(data.x, data.edge_index, index=10)
explanation.visualize_graph()           # Important subgraph
explanation.visualize_feature_importance(top_k=10)  # Feature importance
```

 可用算法：`GNNExplainer`（基于优化）、`PGExplainer`（参数、经过训练）、`CaptumExplainer`（通过 Captum 基于梯度）、`AttentionExplainer`（注意力权重）。适用于同构图和异构图。

阅读 `references/explainability.md` 了解所有算法、异构解释、评估指标和 PGExplainer 训练。

## 常见陷阱

1. **edge_index shape**：必须是`[2, num_edges]`，而不是`[num_edges, 2]`。如果需要的话转置。
2. **忘记激活**：Conv 层不包括 ReLU 等 - 手动添加它们。
3. **异二分中的自循环**：当源节点和目标节点类型不同时，不要使用 `add_self_loops=True`。请改用跳过连接。
4. **NeighborLoader 切片**：只有第一个 `batch.batch_size` 节点是您的种子节点。相应地对预测和标签进行切片。
5. **无向图**：如果您的图是无向的，请在 `edge_index` 中包含两个方向的边，或使用 `T.ToUndirected()`.
6. **延迟初始化**：具有 `-1` 输入通道的模型在训练初始化参数之前需要使用 `torch.no_grad()` 进行一次前向传递。
7. **图任务的全局池化**：使用`global_mean_pool(x, batch)`（不是手动重塑）将节点特征聚合到图级别。
8. **num_neighbors 对齐**：保持 `len(num_neighbors)` 等于 GNN 层数。跳数多于层浪费的计算量；更少意味着浪费模型容量。
