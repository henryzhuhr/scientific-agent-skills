# 核心概念和技术细节

## 概述

本参考内容涵盖了TorchDrug的基本架构、设计原理和技术实现细节。

## 架构哲学

### 模块化设计

TorchDrug将关注点分成不同的模块：

1. **表示模型** (models.py)：将图编码为嵌入
2. **任务定义** (tasks.py)：定义学习目标和评估
3. **数据处理**（data.py、datasets.py）：图形结构和数据集
4. **核心组件** (core.py)：基类和实用程序

* *优点：**
- 跨任务重用表示形式
- 混合和匹配组件
- 轻松实验和原型设计
- 明确关注点分离

### 可配置系统

All组件继承自`core.Configurable`：
- 序列化到配置字典
- 从配置重建
- 保存并加载完整的管道
- 可重现的实验

## 核心组件

### core.Configurable

所有的基类TorchDrug组件.

* *关键方法：**
- `config_dict()`：序列化到字典
- `load_config_dict(config)`：从字典加载
- `save(file)`：保存到文件
- `load(file)`：从字典加载file

* *示例：**
```python
from torchdrug import core, models

model = models.GIN(input_dim=10, hidden_dims=[256, 256])

# Save configuration
config = model.config_dict()
# {'class': 'GIN', 'input_dim': 10, 'hidden_dims': [256, 256], ...}

# Reconstruct model
model2 = core.Configurable.load_config_dict(config)
```

### core.Registry

Decorator，用于注册模型、任务和datasets.

* *用法：**
```python
from torchdrug import core as core_td

@core_td.register("models.CustomModel")
class CustomModel(nn.Module, core_td.Configurable):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, hidden_dim)

    def forward(self, graph, input, all_loss, metric):
        # Model implementation
        pass
```

* *好处：**
- 模型自动可序列化
- 基于字符串的模型规范
- 轻松模型查找和实例化

## 数据结构

### Graph

代表分子或蛋白质图的核心数据结构。

* *属性：**
- `num_node`：节点数量
- `num_edge`：边数量
- `node_feature`：节点特征张量[num_node，feature_dim] 
- `edge_feature`：边缘特征张量[num_edge， feature_dim]
- `edge_list`：边连通性 [num_edge，2 或 3]
- `num_relation`：边类型数量（对于多关系）

* *方法：**
- `node_mask(mask)`：选择节点子集
- `edge_mask(mask)`：选择边的子集
- `undirected()`：使图无向
- `directed()`：使图有向

* *批处理：**
- 将图批处理为单个断开连接的图
- 自动批处理DataLoader
- 保留每个图的节点/边索引

### 分子（扩展图）

分子专用图。

* *其他属性：**
- `atom_type`：原子序数
- `bond_type`：键类型（单键、双键、三键、芳香键）
- `formal_charge`：原子形式电荷
- `explicit_hs`：显式氢计数

* *方法：**
- `from_smiles(smiles)`：从SMILES创建字符串
- `from_molecule(mol)`：从RDKit分子创建
- `to_smiles()`：转换为SMILES
- `to_molecule()`：转换为RDKit分子
- `ion_to_molecule()`：中和费用

* *示例：**
```python
from torchdrug import data

# From SMILES
mol = data.Molecule.from_smiles("CCO")

# Atom features
print(mol.atom_type)  # [6, 6, 8] (C, C, O)
print(mol.bond_type)  # [1, 1] (single bonds)
```

### 蛋白质（扩展图）

蛋白质专用图。

* *其他属性：**
- `residue_type`：氨基酸类型
- `atom_name`：原子名称（CA、CB等）
- `atom_type`：原子序数
- `residue_number`：残基编号
- `chain_id`：链标识符

* *方法：**
- `from_pdb(pdb_file)`：从PDB文件加载
- `from_sequence(sequence)`：从序列创建
- `to_pdb(pdb_file)`：保存到PDB文件

* *图形构建：**
- 节点通常表示残基（不是原子）
- 边缘可以是顺序的、空间的 (KNN)或基于接触的
- 可配置的边缘构建策略

* *示例：**
```python
from torchdrug import data

# Load protein
protein = data.Protein.from_pdb("1a3x.pdb")

# Build graph with multiple edge types
graph = protein.residue_graph(
    node_position="ca",  # Use Cα positions
    edge_types=["sequential", "radius"]  # Sequential + spatial edges
)
```

### PackedGraph

异构图的高效批处理结构。

* *用途：**
- 不同大小的批量图
- 单GPU内存分配
- 高效并行处理

* *属性：**
- `num_nodes`：每个图的节点计数列表
- `num_edges`：每个图的边计数列表
- `graph_ind`：每个节点的图索引

* *用例：**
- DataLoader中的自动
- 自定义批处理策略
- 多图操作

## 模型接口

### 前向函数签名

所有TorchDrug模型均遵循标准化接口：

```python
def forward(self, graph, input, all_loss=None, metric=None):
    """
    Args:
        graph (Graph): Batch of graphs
        input (Tensor): Node input features
        all_loss (Tensor, optional): Accumulator for losses
        metric (dict, optional): Dictionary for metrics

    Returns:
        dict: Output dictionary with representation keys
    """
    # Model computation
    output = self.layers(graph, input)

    return {
        "node_feature": output,
        "graph_feature": graph_pooling(output)
    }
```

* *要点：**
- `graph`：批量图结构
- `input`：节点特征 [num_node，input_dim]
- `all_loss`：累积损失（针对多任务）
- `metric`：共享度量字典
- 返回具有表示类型的字典

### 必需属性

* *所有模型必须定义：**
- `input_dim`：期望输入特征维度
- `output_dim`：输出表示维度

* *用途：**
- 自动维度检查
- 在中构建模型pipelines
- 错误检查和验证

* *示例：**
```python
class CustomModel(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.input_dim = input_dim
        self.output_dim = hidden_dim
        # ... layers ...
```

## 任务接口

### 核心任务方法

所有任务都实现这些方法：

```python
class CustomTask(tasks.Task):
    def preprocess(self, train_set, valid_set, test_set):
        """Dataset-specific preprocessing (optional)"""
        pass

    def predict(self, batch):
        """Generate predictions for a batch"""
        graph, label = batch
        output = self.model(graph, graph.node_feature)
        pred = self.mlp(output["graph_feature"])
        return pred

    def target(self, batch):
        """Extract ground truth labels"""
        graph, label = batch
        return label

    def forward(self, batch):
        """Compute training loss"""
        pred = self.predict(batch)
        target = self.target(batch)
        loss = self.criterion(pred, target)
        return loss

    def evaluate(self, pred, target):
        """Compute evaluation metrics"""
        metrics = {}
        metrics["auroc"] = compute_auroc(pred, target)
        metrics["auprc"] = compute_auprc(pred, target)
        return metrics
```

### 任务组件

* *典型任务结构：**
1. **表示模型**：将图编码为嵌入
2. **读出/预测头**：将嵌入映射到预测
3. **损失函数**：训练目标
4. **指标**：评估措施

* *示例：**
```python
from torchdrug import tasks, models

# Representation model
model = models.GIN(input_dim=10, hidden_dims=[256, 256])

# Task wraps model with prediction head
task = tasks.PropertyPrediction(
    model=model,
    task=["task1", "task2"],  # Multi-task
    criterion="bce",
    metric=["auroc", "auprc"],
    num_mlp_layer=2
)
```

## 训练工作流程

### 标准训练循环

```python
import torch
from torch.utils.data import DataLoader
from torchdrug import core, models, tasks, datasets

# 1. Load dataset
dataset = datasets.BBBP("~/datasets/")
train_set, valid_set, test_set = dataset.split()

# 2. Create data loaders
train_loader = DataLoader(train_set, batch_size=32, shuffle=True)
valid_loader = DataLoader(valid_set, batch_size=32)

# 3. Define model and task
model = models.GIN(input_dim=dataset.node_feature_dim,
                   hidden_dims=[256, 256, 256])
task = tasks.PropertyPrediction(model, task=dataset.tasks,
                                 criterion="bce", metric=["auroc", "auprc"])

# 4. Setup optimizer
optimizer = torch.optim.Adam(task.parameters(), lr=1e-3)

# 5. Training loop
for epoch in range(100):
    # Train
    task.train()
    for batch in train_loader:
        loss = task(batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Validate
    task.eval()
    preds, targets = [], []
    for batch in valid_loader:
        pred = task.predict(batch)
        target = task.target(batch)
        preds.append(pred)
        targets.append(target)

    preds = torch.cat(preds)
    targets = torch.cat(targets)
    metrics = task.evaluate(preds, targets)
    print(f"Epoch {epoch}: {metrics}")
```

### PyTorch 闪电集成

TorchDrug任务与 PyTorch Lightning 兼容：

```python
import pytorch_lightning as pl

class LightningWrapper(pl.LightningModule):
    def __init__(self, task):
        super().__init__()
        self.task = task

    def training_step(self, batch, batch_idx):
        loss = self.task(batch)
        return loss

    def validation_step(self, batch, batch_idx):
        pred = self.task.predict(batch)
        target = self.task.target(batch)
        return {"pred": pred, "target": target}

    def validation_epoch_end(self, outputs):
        preds = torch.cat([o["pred"] for o in outputs])
        targets = torch.cat([o["target"] for o in outputs])
        metrics = self.task.evaluate(preds, targets)
        self.log_dict(metrics)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)
```

## 损失函数

### 内置标准

* *分类：**
- `"bce"`：二元交叉熵
- `"ce"`：交叉熵（多类）

* *回归：**
- `"mse"`：均方误差
- `"mae"`：平均绝对误差

  * *知识图：**
- `"bce"`：三元组的二元分类
- `"ce"`：交叉熵排名损失
- `"margin"`：基于保证金的排名

### 自定义损失

```python
class CustomTask(tasks.Task):
    def forward(self, batch):
        pred = self.predict(batch)
        target = self.target(batch)

        # Custom loss computation
        loss = custom_loss_function(pred, target)

        return loss
```

## 指标

### 通用指标

* *分类：**
- **AUROC**：ROC 曲线下面积
- **AUPRC**：精确率-召回率曲线下面积
- **准确度**：总体准确率
- **F1**：精确度和召回率的调和平均值

* *回归：**
- **MAE**：平均绝对误差
- **RMSE**：均方根误差
- **R²**：确定系数
- **皮尔逊**：皮尔逊相关性

* *排名（知识图）：**
- **MR**：平均排名
- **MRR**：平均倒数排名
- **Hits@K**：顶部百分比 K

### 多任务指标

对于多标签或多任务：
- 每个任务计算的指标
- 跨任务的宏观平均
- 可以按任务重要性加权

## 数据转换

### 分子转换

```python
from torchdrug import transforms

# Add virtual node connected to all atoms
transform1 = transforms.VirtualNode()

# Add virtual edges
transform2 = transforms.VirtualEdge()

# Compose transforms
transform = transforms.Compose([transform1, transform2])

dataset = datasets.BBBP("~/datasets/", transform=transform)
```

### 蛋白质转换

```python
# Add edges based on spatial proximity
transform = transforms.TruncateProtein(max_length=500)

dataset = datasets.Fold("~/datasets/", transform=transform)
```

## 最佳实践

### 内存效率

1. **梯度累积**：适用于大型型号
2. **混合精度**：FP16 训练
3. **批量大小调整**：平衡速度和内存
4. **数据加载**：I/O

### 的多个工作线程再现性

1. **设置种子**：PyTorch、NumPy、Python random
2. **确定性操作**：`torch.use_deterministic_algorithms(True)`
3. **保存配置**：使用`core.Configurable`
4. **版本控制**：跟踪TorchDrug版本

### 调试

1. **检查尺寸**：验证 `input_dim` 和 `output_dim`
2. **验证批次**：打印批次统计信息
3. **监视梯度**：观察消失/爆炸
4. **过拟合小批量**：保证模型容量

### 性能优化

1. **GPU利用率**：使用`nvidia-smi`
2进行监控。 **配置文件代码**：使用 PyTorch 分析器
3. **优化数据加载**：预取，引脚存储器
4. **编译模型**：如果可能，请使用 TorchScript

## 高级主题

### 多任务学习

在多个相关任务上训练单个模型：
```python
task = tasks.PropertyPrediction(
    model,
    task=["task1", "task2", "task3"],
    criterion="bce",
    metric=["auroc"],
    task_weight=[1.0, 1.0, 2.0]  # Weight task 3 more
)
```

### 迁移学习

1. 在大型数据集 
2 上进行预训练。对目标数据集
3进行微调。可选择冻结早期层

### 自监督预训练

使用预训练任务：
- `AttributeMasking`：掩模节点特征
- `EdgePrediction`：预测边缘存在
- `ContextPrediction`：对比学习

### 自定义层

使用自定义GNN层扩展TorchDrug：
```python
from torchdrug import layers

class CustomConv(layers.MessagePassingBase):
    def message(self, graph, input):
        # Custom message function
        pass

    def aggregate(self, graph, message):
        # Custom aggregation
        pass

    def combine(self, input, update):
        # Custom combination
        pass
```

## 常见陷阱

1. **忘记 `input_dim` 和 `output_dim`**：模型不会组成 
2. **未正确批处理**：对可变大小的图使用 PackedGraph
3. **数据泄漏**：小心脚手架分割和预训练
4. **忽略边缘特征**：键/空间信息可能很重要
5. **错误的评估指标**：将指标与任务匹配（AUROC 表示不平衡）
6. **正则化不足**：使用dropout、权重衰减、提前停止
7. **不验证化学**：生成的分子必须是有效的
8. **过度拟合小数据集**：使用预训练或更简单的模型
