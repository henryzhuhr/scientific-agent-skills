# 分子性质预测

## 概述

分子性质预测涉及从分子的结构预测分子的化学、物理或生物性质。 TorchDrug 为分子图上的分类和回归任务提供全面支持。

## 可用数据集

### 药物发现数据集

* *分类任务：**
- **BACE**（1,513 个分子）：β-分泌酶抑制的二元分类
- **BBBP** （2,039 个分子）：血脑屏障穿透预测
- **HIV** （41,127 个分子）：抑制 HIV 复制的能力
- **Tox21** （7,831 个分子）：跨 12 个目标的毒性预测
- **ToxCast** （8,576 个分子）：毒理学筛选
- **ClinTox**（1,478 个分子）：临床试验毒性
- **SIDER**（1,427 个分子）：药物副作用（27 个系统器官类别）
- **MUV**（93,087 个分子）：虚拟筛选的最大无偏验证

* *回归任务：**
- **ESOL** （1,128 个分子）：水溶性预测
- **FreeSolv** （642 个分子）：水合自由能
- **亲油性** （4,200 个分子）：辛醇/水分配系数
- **SAMPL** （643 个分子）：溶剂化自由能

### 大规模数据集

- **QM7**（7,165 个分子）：量子力学特性
- **QM8**（21,786 个分子）：电子能谱和激发态特性
- **QM9**（133,885 个分子）：几何、能量、电子和热力学特性
- **PCQM4M** （3,803,453 个分子）：大规模量子化学数据集
- **ZINC250k/2M**（250k/2M 分子）：用于生成建模的类药物化合物

## 任务类型

### PropertyPrediction

支持分类和预测的图级属性预测的标准任务回归.

* *关键参数：**
- `model`：图表示模型（GNN）
- `task`：“节点”、“边”或“图”级别预测
- `criterion`：损失函数（“mse”、“bce”、“ce”）
- `metric`：评估指标（“mae”、“rmse”、“auroc”、“auprc”）
- `num_mlp_layer`：用于读出的 MLP 层数

* *示例工作流程：**
```python
import torch
from torchdrug import core, models, tasks, datasets

# Load dataset
dataset = datasets.BBBP("~/molecule-datasets/")

# Define model
model = models.GIN(input_dim=dataset.node_feature_dim,
                   hidden_dims=[256, 256, 256, 256],
                   edge_input_dim=dataset.edge_feature_dim,
                   batch_norm=True, readout="mean")

# Define task
task = tasks.PropertyPrediction(model, task=dataset.tasks,
                                 criterion="bce",
                                 metric=("auprc", "auroc"))
```

### MultipleBinaryClassification

针对多标签场景的专门任务，其中每个分子可以有多个二进制标签（例如，Tox21、SIDER）。

* *主要功能：**
- 优雅地处理丢失的标签
- 计算每个标签的指标并进行平均
- 支持不平衡的加权损失数据集

## 模型选择

#### 任务推荐模型

* *小分子（<1000个分子）：**
- GIN（图同构网络）
- SchNet（用于3D结构）

* *中数据集（1k-100k 分子）：**
- GCN、GAT 或 GIN
- NFP（神经指纹）
- MPNN（消息传递神经网络）

* *大型数据集（> 100k 分子）：**
- 预训练模型微调
- 用于自监督预训练的InfoGraph或MultiviewContrast
- 具有更深架构的GIN

* *可用3D结构：**
- SchNet（连续滤波器卷积）
- GearNet（几何感知关系图）

## 特征工程

### 节点特征

TorchDrug自动提取原子特征：
- 原子类型
- 形式电荷
- 显式/隐式氢
- 杂化
- 芳香度
- 手性

### 边缘特征

键合特征包括：
- 键合类型（单键、双键、三键、芳香键）
- 立体化学
- 共轭
- 环成员资格

### 自定义功能

添加自定义 node/edge features using transforms:
```python
from torchdrug import data, transforms

# Add custom features
transform = transforms.VirtualNode()  # Add virtual node
dataset = datasets.BBBP("~/molecule-datasets/",
                        transform=transform)
```

## Training Workflow

### Basic Pipeline

1. **加载数据集**：选择合适的数据集
2. **Split Data**: Use scaffold split for drug discovery
3. **Define Model**: Select GNN architecture
4. **创建任务**：配置损失和指标
5. **设置优化器**：Adam 通常运行良好
6. **训练**：使用 PyTorch Lightning 或自定义循环

### 数据分割策略

* *随机分割**：标准训练/验证/测试分割
* *支架分割**：通过 Bemis-Murcko 支架对分子进行分组（推荐用于药物发现）
* *分层分割**：保持标签分布splits

### 最佳实践

- 使用支架拆分进行实际药物发现评估
- 对小型数据集应用数据增强（虚拟节点、边缘）
- 监控多个指标（AUROC、AUPRC 用于分类；MAE、RMSE 用于回归）
- 使用基于验证的早期停止性能
- 考虑关键应用的集成方法
- 在对小数据集进行微调之前对大型数据集进行预训练

## 常见问题和解决方案

* *问题：在不平衡数据集上性能较差**
- 解决方案：使用加权损失、焦点损失或过采样/欠采样

* *问题：在小数据集上过度拟合**
- 解决方案：增加正则化、使用更简单的模型、应用数据增强或在较大数据集上预训练

* *问题：内存消耗大**
- 解决方案：减少批量大小、使用梯度累积或实现图形采样

* *问题：慢训练**
  - 解决方案：使用GPU加速，优化多个worker的数据加载，或使用混合精度训练
