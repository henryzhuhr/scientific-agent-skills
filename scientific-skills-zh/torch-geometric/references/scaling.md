# 缩放 GNN — 完整参考

在不适合 GPU 内存的大型图上训练 GNN、多 GPU 训练和性能优化的技术。

## 目录
1. 邻居采样（NeighborLoader）
2. 其他采样策略
3. 多GPU/分布式训练
4. torch.compile 支持
5. 性能提示

- --

## 1.邻居采样（NeighborLoader）

大型单图训练的主要方法。递归地对每跳固定数量的邻居进行采样，限制计算图。

```python
from torch_geometric.loader import NeighborLoader

loader = NeighborLoader(
    data,
    num_neighbors=[15, 10],       # Max neighbors per hop (hop 1: 15, hop 2: 10)
    batch_size=1024,               # Number of seed nodes per batch
    input_nodes=data.train_mask,   # Which nodes to sample from
    shuffle=True,
    num_workers=4,                 # Parallel data loading
    replace=False,                 # Sample without replacement
)
```

* *关键参数：**
- `num_neighbors`：每跳最大邻居列表。长度应与 GNN 深度匹配。使用 `-1` 对一跳的所有邻居进行采样。
- `input_nodes`：种子节点 - 可以是掩码、索引张量或异质图的 `('node_type', mask)` 元组。
- `subgraph_type`：`"directional"`（默认）、`"bidirectional"`（添加反向）边），或 `"induced"`（全诱导子图）。
- `disjoint`：如果 `True`，不要融合种子节点之间的邻域（使用更多内存，但可能需要）。

* *训练模式：**
```python
model = GraphSAGE(in_channels, hidden_channels, out_channels, num_layers=2)

for batch in loader:
    batch = batch.to(device)
    out = model(batch.x, batch.edge_index)
    # CRITICAL: only first batch_size nodes are seed nodes
    loss = F.cross_entropy(out[:batch.batch_size], batch.y[:batch.batch_size])
```

* *重要细节：**
- 节点已排序：第一个 `batch.batch_size` 节点是种子节点
- `batch.n_id` 将本地索引映射回原始节点 ID
- 采样 >2-3 跳通常是不可行的（指数邻域增长）
- 保留`len(num_neighbors) == num_gnn_layers`以提高效率

### LinkNeighborLoader（用于链接预测）

围绕监督边缘采样子图：

```python
from torch_geometric.loader import LinkNeighborLoader

loader = LinkNeighborLoader(
    data,
    num_neighbors=[20, 10],
    edge_label_index=train_data.edge_label_index,
    edge_label=train_data.edge_label,
    batch_size=256,
    neg_sampling_ratio=1.0,
    shuffle=True,
)
```

### HGTLoader（类型感知异构）采样）

按类型每跳采样固定数量的节点，遵循 HGT 论文：

```python
from torch_geometric.loader import HGTLoader

loader = HGTLoader(
    data,
    num_samples=[512] * 2,        # Nodes per type per hop
    batch_size=128,
    input_nodes=('paper', data['paper'].train_mask),
)
```

## 2. 其他采样策略

### ClusterLoader (ClusterGCN)

将图划分为簇，在完整子图上进行训练。由于消息在集群内自由流动，因此更适合更深的 GNN：

```python
from torch_geometric.loader import ClusterData, ClusterLoader

cluster_data = ClusterData(data, num_parts=1500)
loader = ClusterLoader(cluster_data, batch_size=20, shuffle=True)

for batch in loader:
    # batch is a full subgraph — no slicing needed
    out = model(batch.x, batch.edge_index)
    loss = F.cross_entropy(out[batch.train_mask], batch.y[batch.train_mask])
```

### GraphSAINTSampler

通过随机游走、节点或具有基于重要性的归一化的边对子图进行采样：

```python
from torch_geometric.loader import GraphSAINTRandomWalkSampler

loader = GraphSAINTRandomWalkSampler(
    data, batch_size=6000, walk_length=2, num_steps=5,
)
```

### ShaDowKHopSampler

提取种子节点周围的 K 跳诱导子图 — 将深度与范围：

```python
from torch_geometric.loader import ShaDowKHopSampler

loader = ShaDowKHopSampler(
    data, depth=2, num_neighbors=5, batch_size=64,
    input_nodes=data.train_mask,
)
```

## 3.多GPU/分布式训练

### 分布式数据并行（DDP）

标准PyTorch DDP与PyG配合使用。每个GPU获得种子节点的分区：

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel
import torch.multiprocessing as mp

def run(rank, world_size, dataset):
    # Initialize process group
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12345'
    dist.init_process_group('nccl', rank=rank, world_size=world_size)

    data = dataset[0]

    # Split training nodes across GPUs
    train_idx = data.train_mask.nonzero().view(-1)
    train_idx = train_idx.split(train_idx.size(0) // world_size)[rank]

    loader = NeighborLoader(
        data,
        input_nodes=train_idx,
        num_neighbors=[25, 10],
        batch_size=1024,
        num_workers=4,
        shuffle=True,
    )

    # Wrap model in DDP
    model = GraphSAGE(...).to(rank)
    model = DistributedDataParallel(model, device_ids=[rank])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(10):
        model.train()
        for batch in loader:
            batch = batch.to(rank)
            optimizer.zero_grad()
            out = model(batch.x, batch.edge_index)[:batch.batch_size]
            loss = F.cross_entropy(out, batch.y[:batch.batch_size])
            loss.backward()
            optimizer.step()

        # Synchronize before evaluation
        dist.barrier()

        if rank == 0:
            # Evaluate on rank 0 only
            ...

    dist.destroy_process_group()

# Launch
if __name__ == '__main__':
    dataset = Reddit('./data/Reddit')
    world_size = torch.cuda.device_count()
    mp.spawn(run, args=(world_size, dataset), nprocs=world_size, join=True)
```

* *要点：**
- 在`mp.spawn()`之前初始化数据集——数据自动移动到共享内存
- 每个等级使用种子节点的子集创建自己的NeighborLoader
- 调用`dist.barrier()` 在评估之前进行同步
- 仅为了简单起见而在排名 0 上评估
- 使用 `dist.destroy_process_group()`

### PyTorch Lightning 集成

PyG 提供 Lightning 包装器，以实现最小化样板：

```python
from torch_geometric.data import LightningNodeData

datamodule = LightningNodeData(
    data,
    input_train_nodes=data.train_mask,
    input_val_nodes=data.val_mask,
    input_test_nodes=data.test_mask,
    loader='neighbor',
    num_neighbors=[25, 10],
    batch_size=1024,
)

# Use with any Lightning Trainer
trainer = L.Trainer(devices=4, accelerator='gpu', strategy='ddp')
trainer.fit(model, datamodule)
```

还可用：`LightningLinkData`用于链接预测，`LightningDataset`用于图形级任务。

## 4. torch.compile支持

PyG支持`torch.compile`以加快速度执行：

```python
model = GCN(...)
model = torch.compile(model)

# Works with standard training loops
out = model(data.x, data.edge_index)
```

* *工作原理：**
- 大多数GNN层（GCNConv、SAGEConv、GATConv等）
- 标准训练/推理管道
- CPU和CUDA后端

* *限制：**
- 动态形状（每个批次的图形大小不同）可能会触发重新编译
- 某些专用层或自定义MessagePassing子类可能无法编译
- 如果批次图形大小变化很大，请使用`torch.compile(model, dynamic=True)`

## 5.性能提示

- **num_workers**：在数据加载器中设置 `num_workers=4`（或更多）以实现 CPU 端并行性
- **pin_memory**：在加载器中使用 `pin_memory=True` 以实现更快的 CPU 到 GPU 传输
- **稀疏张量**：使用 `torch_sparse` 中的 `SparseTensor` 而不是`edge_index` 可在某些层上更快地传递消息
- **分析**：使用 `torch_geometric.profile` 测量各个层的时间和内存
- **混合精度**：标准 PyTorch AMP 与 PyG 配合使用：
 ```python
 from torch.amp import autocast, GradScaler
缩放器= GradScaler（）
与自动转换（'cuda'）：
输出=模型（batch.x，batch.edge_index）
损失= F.cross_entropy（out [：batch.batch_size]，batch.y [：batch.batch_size]）
 scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
 ```
- **减少采样**：每跳邻居更少=更快但噪音更大。从 `[15, 10]` 开始，用于 2 层 GNN。
  - **避免不必要的计算**：使用 NeighborLoader，只有第一个 `batch_size` 输出很重要 - 不要在仅采样的节点上计算指标。
