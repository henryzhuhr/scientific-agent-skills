# 自定义消息传递层

通过 `MessagePassing` 基类实现自定义 GNN 层的完整参考。

## MessagePassing API

```python
MessagePassing(aggr="add", flow="source_to_target", node_dim=-2)
```

- `aggr`：聚合方案 — `"add"`、`"mean"` 或`"max"`
- `flow`：消息方向 — `"source_to_target"`（默认）或 `"target_to_source"`
- `node_dim`：传播的轴

### 覆盖的方法

- `message(...)`：为每个边缘构造消息。通过 `_j`/`_i` 后缀访问源/目标节点特征。
- `aggregate(inputs, index)`：聚合消息（通常由 `aggr` 参数处理）。
- `update(aggr_out, ...)`：每个节点上的聚合后变换。
- `propagate(edge_index, size=None, **kwargs)`：协调整个管道。从 `forward()`.

 调用此任何传递到 `propagate()` 的张量都可以通过附加 `_i`（目标）或 `_j`（源）在 `message()` 中自动索引。例如，传递 `x=features` 可以让您在消息函数中使用 `x_i` 和 `x_j`。

对于二部图，将 `size=(N, M)` 传递给 `propagate()` 并以元组形式提供特征：`x=(x_src, x_dst)`.

## 示例：GCN 层从头开始

```python
import torch
from torch.nn import Linear, Parameter
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree

class GCNConv(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super().__init__(aggr='add')
        self.lin = Linear(in_channels, out_channels, bias=False)
        self.bias = Parameter(torch.empty(out_channels))
        self.reset_parameters()

    def reset_parameters(self):
        self.lin.reset_parameters()
        self.bias.data.zero_()

    def forward(self, x, edge_index):
        # 1. Add self-loops
        edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))
        # 2. Linear transform
        x = self.lin(x)
        # 3. Compute normalization coefficients
        row, col = edge_index
        deg = degree(col, x.size(0), dtype=x.dtype)
        deg_inv_sqrt = deg.pow(-0.5)
        deg_inv_sqrt[deg_inv_sqrt == float('inf')] = 0
        norm = deg_inv_sqrt[row] * deg_inv_sqrt[col]
        # 4-5. Message passing
        out = self.propagate(edge_index, x=x, norm=norm)
        # 6. Add bias
        return out + self.bias

    def message(self, x_j, norm):
        # x_j: source node features for each edge [num_edges, out_channels]
        # norm: normalization coefficients [num_edges]
        return norm.view(-1, 1) * x_j
```

## 示例：EdgeConv Layer

```python
import torch
from torch.nn import Sequential as Seq, Linear, ReLU
from torch_geometric.nn import MessagePassing

class EdgeConv(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super().__init__(aggr='max')
        self.mlp = Seq(
            Linear(2 * in_channels, out_channels),
            ReLU(),
            Linear(out_channels, out_channels),
        )

    def forward(self, x, edge_index):
        return self.propagate(edge_index, x=x)

    def message(self, x_i, x_j):
        # x_i: target node features [num_edges, in_channels]
        # x_j: source node features [num_edges, in_channels]
        return self.mlp(torch.cat([x_i, x_j - x_i], dim=1))
```

## 示例：Dynamic EdgeConv（重新计算每一层的图形）

```python
from torch_geometric.nn import knn_graph

class DynamicEdgeConv(EdgeConv):
    def __init__(self, in_channels, out_channels, k=6):
        super().__init__(in_channels, out_channels)
        self.k = k

    def forward(self, x, batch=None):
        edge_index = knn_graph(x, self.k, batch, loop=False, flow=self.flow)
        return super().forward(x, edge_index)
```

## 实用程序功能

```python
from torch_geometric.utils import (
    add_self_loops,      # Add self-loop edges
    remove_self_loops,   # Remove self-loop edges
    degree,              # Compute node degrees
    softmax,             # Sparse softmax over neighborhoods
    to_dense_adj,        # Convert edge_index to dense adjacency matrix
    to_undirected,       # Make edge_index undirected
    contains_self_loops, # Check for self-loops
    is_undirected,       # Check if graph is undirected
    scatter,             # Scatter operations (sum, mean, max)
)
```
