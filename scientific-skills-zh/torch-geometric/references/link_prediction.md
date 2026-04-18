# 链接预测 — 完整参考

链接预测是预测图中缺失或未来的边的任务。常见应用：社交网络好友建议、知识图谱补全、药物-靶点交互。

## 边缘分割

使用 `RandomLinkSplit` 将边缘分割为训练/验证/测试，同时保持图结构：

```python
import torch_geometric.transforms as T

transform = T.RandomLinkSplit(
    num_val=0.1,              # 10% of edges for validation
    num_test=0.1,             # 10% of edges for test
    is_undirected=True,       # Set True for undirected graphs
    add_negative_train_samples=False,  # Generate negatives on-the-fly during training
    neg_sampling_ratio=1.0,   # 1 negative per positive edge
)
train_data, val_data, test_data = transform(data)
```

 分割后，每个分割包含：
- `edge_index`：消息传递边缘（仅训练边缘 - 无数据泄漏）
- `edge_label_index`：监督边缘 `[2, num_supervision_edges]` - 要预测的边缘
- `edge_label`：二进制标签 - 1 表示正（真实）边缘，0 表示负（假）边缘

对于使用 `add_negative_train_samples=False` 的训练分割，只有正边缘在`edge_label_index` 和负样本在训练期间进行采样。验证/测试分割始终包括正边沿和负边沿。

## 编码器-解码器模式

标准方法：
1. **编码** — 使用 GNN 从消息传递边 
2 生成节点嵌入。 **解码** — 使用节点嵌入对候选边进行评分

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class LinkEncoder(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

def decode(z, edge_label_index):
    """Dot-product decoder: score = z_src . z_dst for each edge."""
    src, dst = edge_label_index
    return (z[src] * z[dst]).sum(dim=1)
```

## 批量训练循环

```python
from torch_geometric.utils import negative_sampling

model = LinkEncoder(data.num_features, 128, 64)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

def train(train_data):
    model.train()
    optimizer.zero_grad()

    # Encode using message-passing edges only
    z = model(train_data.x, train_data.edge_index)

    # Sample negative edges for this batch
    neg_edge_index = negative_sampling(
        edge_index=train_data.edge_index,
        num_nodes=train_data.num_nodes,
        num_neg_samples=train_data.edge_label_index.size(1),
    )

    # Combine positive and negative supervision edges
    edge_label_index = torch.cat([train_data.edge_label_index, neg_edge_index], dim=1)
    edge_label = torch.cat([
        torch.ones(train_data.edge_label_index.size(1)),
        torch.zeros(neg_edge_index.size(1)),
    ])

    # Decode and compute loss
    pred = decode(z, edge_label_index)
    loss = F.binary_cross_entropy_with_logits(pred, edge_label)
    loss.backward()
    optimizer.step()
    return loss.item()

@torch.no_grad()
def test(data_split):
    model.eval()
    z = model(data_split.x, data_split.edge_index)
    pred = decode(z, data_split.edge_label_index).sigmoid()
    # AUC is the standard metric for link prediction
    from sklearn.metrics import roc_auc_score
    return roc_auc_score(data_split.edge_label.cpu(), pred.cpu())
```

## 图自动编码器（GAE / VGAE）

PyG 提供 `GAE` 和`VGAE` 用于无监督链接预测：

```python
from torch_geometric.nn import GAE, VGAE, GCNConv

class Encoder(torch.nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, 2 * out_channels)
        self.conv2 = GCNConv(2 * out_channels, out_channels)
        # For VGAE, also define conv_mu and conv_logstd

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        return self.conv2(x, edge_index)

# GAE wraps your encoder and provides train/test methods
model = GAE(Encoder(data.num_features, 64))
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

def train():
    model.train()
    optimizer.zero_grad()
    z = model.encode(train_data.x, train_data.edge_index)
    loss = model.recon_loss(z, train_data.edge_label_index)
    # For VGAE, add KL divergence:
    # loss = loss + (1 / data.num_nodes) * model.kl_loss()
    loss.backward()
    optimizer.step()
    return loss.item()

@torch.no_grad()
def test(data_split):
    model.eval()
    z = model.encode(data_split.x, data_split.edge_index)
    return model.test(z, data_split.edge_label_index[0],  # positive edges
                         data_split.edge_label_index[1])   # negative edges
```

 对于 VGAE，编码器必须返回 `mu` 和 `logstd`，而不是单个嵌入。使用 VGAE 特定的编码器模式：

```python
class VariationalEncoder(torch.nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, 2 * out_channels)
        self.conv_mu = GCNConv(2 * out_channels, out_channels)
        self.conv_logstd = GCNConv(2 * out_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        return self.conv_mu(x, edge_index), self.conv_logstd(x, edge_index)

model = VGAE(VariationalEncoder(data.num_features, 64))
```

## 使用 LinkNeighborLoader

进行小批量链接预测对于大型图，请使用 `LinkNeighborLoader` — 它对监督边缘周围的子图进行采样：

```python
from torch_geometric.loader import LinkNeighborLoader

train_loader = LinkNeighborLoader(
    data=train_data,
    num_neighbors=[20, 10],         # Sample neighbors per hop
    edge_label_index=train_data.edge_label_index,
    edge_label=train_data.edge_label,
    batch_size=128,                  # Number of supervision edges per batch
    neg_sampling_ratio=1.0,          # 1 negative per positive
    shuffle=True,
)

for batch in train_loader:
    # batch.edge_label_index: supervision edges (pos + neg)
    # batch.edge_label: 1 for positive, 0 for negative
    # batch.edge_index: message-passing edges (from neighbor sampling)
    z = model(batch.x, batch.edge_index)
    pred = decode(z, batch.edge_label_index)
    loss = F.binary_cross_entropy_with_logits(pred, batch.edge_label)
```

## 异构链接预测

对于异构图（例如用户项目推荐）：

```python
transform = T.RandomLinkSplit(
    num_val=0.1,
    num_test=0.1,
    neg_sampling_ratio=1.0,
    add_negative_train_samples=False,
    edge_types=('user', 'rates', 'movie'),              # Which edge type to predict
    rev_edge_types=('movie', 'rev_rates', 'user'),       # Its reverse
)
train_data, val_data, test_data = transform(data)

# Supervision edges are in:
# train_data['user', 'rates', 'movie'].edge_label_index
# train_data['user', 'rates', 'movie'].edge_label
```

## 评估指标

- **AUC-ROC**：标准指标 — ROC 曲线下的面积
- **平均精度 (AP)**：精确回忆曲线下的面积
- **Hits@K**：排名前 K 的正边缘分数（用于知识图中）
- **MRR**：正的平均倒数排名Edges

```python
from sklearn.metrics import roc_auc_score, average_precision_score

auc = roc_auc_score(edge_label.cpu(), pred.cpu())
ap = average_precision_score(edge_label.cpu(), pred.cpu())
```

## 常见陷阱

1. **数据泄漏**：训练期间切勿在消息传递图中包含验证/测试边。 `RandomLinkSplit` 正确处理了这个问题 - train_data 中的 `edge_index` 仅包含训练边。
2. **负样本质量**：使用随机负样本是标准做法，但可能太容易了。对于更难的负例，请从 2 跳邻居中采样。
3. **无向图**：在`RandomLinkSplit`中设置`is_undirected=True` - 否则它将独立处理每个方向并泄漏信息。
4. **解码**：点积最简单，但并不总是最好的。考虑使用 MLP 解码器或 DistMult 来实现异构/知识图。
