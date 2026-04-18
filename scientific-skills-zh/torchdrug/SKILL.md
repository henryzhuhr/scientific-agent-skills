---
name: torchdrug
description: PyTorch-分子和蛋白质的原生图神经网络。在构建用于药物发现、蛋白质建模或知识图推理的自定义 GNN 架构时使用。最适合定制模型开发、蛋白质特性预测、逆合成。对于预训练模型和各种特征器，请使用 deepchem；对于基准数据集，请使用 pytdc。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# TorchDrug

## 概述

TorchDrug 是一个基于 PyTorch 的综合机器学习工具箱，用于药物发现和分子科学。将图神经网络、预训练模型和任务定义应用于分子、蛋白质和生物知识图谱，包括分子属性预测、蛋白质建模、知识图谱推理、分子生成、逆合成规划，具有 40 多个精选数据集和 20 多个模型架构。

## 何时使用此技能

在处理：

* *数据时应使用此技能类型：**
- SMILES 字符串或分子结构
- 蛋白质序列或 3D 结构（PDB 文件）
- 化学反应和逆合成
- 生物医学知识图
- 药物发现数据集

* *任务：**
- 预测分子特性（溶解度、毒性、活性）
- 蛋白质功能或结构预测
- 药物靶点结合预测
- 生成新的分子结构
- 规划化学合成路线
- 生物医学知识库中的链接预测
- 根据科学数据训练图神经网络

* * 图书馆和集成：**
- TorchDrug 是主要库
- 通常与 RDKit 一起用于化学信息学
- 与 PyTorch 和 PyTorch Lightning 兼容
- 与 AlphaFold 和 ESM 集成用于蛋白质

## 获取已开始

### 安装

```bash
uv pip install torchdrug
# Or with optional dependencies
uv pip install torchdrug[full]
```

### 快速示例

```python
from torchdrug import datasets, models, tasks
from torch.utils.data import DataLoader

# Load molecular dataset
dataset = datasets.BBBP("~/molecule-datasets/")
train_set, valid_set, test_set = dataset.split()

# Define GNN model
model = models.GIN(
    input_dim=dataset.node_feature_dim,
    hidden_dims=[256, 256, 256],
    edge_input_dim=dataset.edge_feature_dim,
    batch_norm=True,
    readout="mean"
)

# Create property prediction task
task = tasks.PropertyPrediction(
    model,
    task=dataset.tasks,
    criterion="bce",
    metric=["auroc", "auprc"]
)

# Train with PyTorch
optimizer = torch.optim.Adam(task.parameters(), lr=1e-3)
train_loader = DataLoader(train_set, batch_size=32, shuffle=True)

for epoch in range(100):
    for batch in train_loader:
        loss = task(batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

## 核心功能

### 1.分子特性预测

从分子中预测分子的化学、物理和生物特性

* *用例：**
- 药物相似性和 ADMET 特性
- 毒性筛选
- 量子化学特性
- 结合亲和力预测

* *关键组件：**
- 20+ 分子数据集（BBBP、HIV、 Tox21、QM9 等）
- GNN 模型（GIN、GAT、SchNet）
- 属性预测和多二进制分类任务

* *参考：** 请参阅 `references/molecular_property_prediction.md` 了解：
- 完整数据集目录
- 模型选择指南
- 训练工作流程和最佳实践
- 特征工程详细信息

### 2. 蛋白质建模

使用蛋白质序列、结构和属性。

* *使用案例：**
- 酶功能预测
- 蛋白质稳定性和溶解度
- 亚细胞定位
- 蛋白质-蛋白质相互作用
- 结构预测

* *关键组件：**
- 15+ 蛋白质数据集（EnzymeCommission、GeneOntology、PDBBind、等）
- 序列模型（ESM、ProteinBERT、ProteinLSTM）
- 结构模型（GearNet、SchNet）
- 不同预测级别的多种任务类型

* *参考：** 参见 `references/protein_modeling.md`：
- 特定于蛋白质数据集
- 序列与结构模型
- 预训练策略
- 与AlphaFold和ESM集成

### 3.知识图推理

预测生物知识图中缺失的链接和关系。

* *用例：**
- 药物再利用
- 疾病机制发现
- 基因疾病关联
- 多跳生物医学推理

* *关键组件：**
- 通用KG（FB15k，WN18）和生物医学（Hetionet）
- 嵌入模型（TransE， RotatE, ComplEx)
- KnowledgeGraph完成任务

* *参考：**参见`references/knowledge_graphs.md`了解：
- 知识图数据集（包括具有45k生物医学实体的Hetionet）
- 嵌入模型比较
- 评估指标和协议
- 生物医学应用

### 4.分子生成

生成具有所需特性的新颖分子结构。

* *用例：**
- 从头药物设计
- 先导化合物优化
- 化学空间探索
- 属性引导生成

* *关键组件：**
- 自回归生成
- GCPN（基于策略的生成）
- 图形自回归流程
- 属性优化工作流程

* *参考：**参见`references/molecular_generation.md`了解：
- 生成策略（无条件、条件、基于支架）
- 多目标优化
- 验证和过滤
- 与属性预测集成

### 5.逆合成

预测从目标分子到起始的合成路线Materials.

* *用例：**
- 综合规划
- 路线优化
- 综合可达性评估
- 多步骤规划

* *关键组件：**
- USPTO-50k 反应数据集
- 中心识别（反应）中心预测）
- SynthonCompletion（反应物预测）
- 端到端逆合成流程

* *参考：** 参见`references/retrosynthesis.md`：
- 任务分解（中心ID → Synthon 完成）
- 多步合成规划
- 商业可用性检查
- 与其他逆合成工具集成

### 6.图神经网络模型

针对不同数据类型和任务的GNN架构的综合目录。

* *可用模型：**
- 通用GNN：GCN，GAT，GIN，RGCN， MPNN
- 3D 感知：SchNet、GearNet
- 蛋白质特异性：ESM、ProteinBERT、GearNet
- 知识图：TransE、RotatE、ComplEx、SimplE
- 生成：GraphAutoregressiveFlow

* *参考：**请参阅 `references/models_architectures.md` 了解：
- 详细的模型描述
- 按任务和数据集划分的模型选择指南
- 架构比较
- 实施技巧

### 7. 数据集

40+ 涵盖化学、生物学和知识的精选数据集graphs.

* *类别：**
- 分子特性（药物发现、量子化学）
- 蛋白质特性（功能、结构、相互作用）
- 知识图（一般和生物医学）
- 逆合成反应

* *参考：**参见`references/datasets.md` 用于：
- 包含大小和任务的完整数据集目录
- 数据集选择指南
- 加载和预处理
- 拆分策略（随机、脚手架）

## 常用工作流程

### 工作流程1：分子特性预测

* *场景：** 预测候选药物的血脑屏障渗透性。

* *步骤：**
1. 加载数据集：`datasets.BBBP()`
2. 选择型号：GIN 分子图
3. 定义任务：`PropertyPrediction`，二元分类为
4. 使用支架拆分进行训练以进行实际评估
5. 使用 AUROC 和 AUPRC

 进行评估**导航：** `references/molecular_property_prediction.md` → 数据集选择 → 模型选择 → 训练

### 工作流程 2：蛋白质功能预测

* *场景：** 从序列预测酶功能。

* *步骤：**
1. 加载数据集：`datasets.EnzymeCommission()`
2. 选择模型：ESM（预训练）或GearNet（带结构）
3. 定义任务：`PropertyPrediction`，具有多类分类
4. 微调预训练模型或从头开始训练
5. 使用准确性和每类指标进行评估

* *导航：** `references/protein_modeling.md` → 模型选择（序列与结构）→ 预训练策略

### 工作流程 3：通过知识图进行药物再利用

* *场景：** 在中查找新的疾病治疗方法Hetionet.

* *步骤：**
1. 加载数据集：`datasets.Hetionet()`
2. 选择型号：RotatE 或 ComplEx
3. 定义任务：`KnowledgeGraphCompletion`
4. 使用负采样
5进行训练。查询“Compound-treats-Disease”预测
6. 按合理性和机制过滤

* *导航：** `references/knowledge_graphs.md` → Hetionet 数据集 → 模型选择 → 生物医学应用

### 工作流程 4：从头分子生成

* *场景：** 生成针对目标结合进行优化的类药物分子。

* *步骤：**
1. 根据活动数据 
2 训练属性预测器。选择生成方法：GCPN 用于基于 RL 的优化
3. 结合亲和力、药物相似性、可合成性定义奖励函数
4. 生成具有属性约束的候选
5. 通过药物相似性验证化学和过滤
6. 按多目标评分排序

* *导航：** `references/molecular_generation.md`→条件生成→多目标优化

### 工作流程5：逆合成规划

* *场景：**规划目标分子的合成路线。

* *步骤：**
1. 加载数据集：`datasets.USPTO50k()`
2. 列车中心识别模型（RGCN）
3. 训练合成子完成模型（GIN）
4. 组合成端到端逆合成管道
5. 递归地应用于多步规划
6. 检查构建模块的商业可用性

* *导航：** `references/retrosynthesis.md` → 任务类型 → 多步骤规划

## 集成模式

### 使用 RDKit

在 TorchDrug 分子和RDKit:
```python
from torchdrug import data
from rdkit import Chem

# SMILES → TorchDrug molecule
smiles = "CCO"
mol = data.Molecule.from_smiles(smiles)

# TorchDrug → RDKit
rdkit_mol = mol.to_molecule()

# RDKit → TorchDrug
rdkit_mol = Chem.MolFromSmiles(smiles)
mol = data.Molecule.from_molecule(rdkit_mol)
```

### 使用 AlphaFold/ESM

使用预测结构：
```python
from torchdrug import data

# Load AlphaFold predicted structure
protein = data.Protein.from_pdb("AF-P12345-F1-model_v4.pdb")

# Build graph with spatial edges
graph = protein.residue_graph(
    node_position="ca",
    edge_types=["sequential", "radius"],
    radius_cutoff=10.0
)
```

### 使用 PyTorch Lightning

Wrap 闪电任务培训：
```python
import pytorch_lightning as pl

class LightningTask(pl.LightningModule):
    def __init__(self, torchdrug_task):
        super().__init__()
        self.task = torchdrug_task

    def training_step(self, batch, batch_idx):
        return self.task(batch)

    def validation_step(self, batch, batch_idx):
        pred = self.task.predict(batch)
        target = self.task.target(batch)
        return {"pred": pred, "target": target}

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)
```

## 技术细节

深入了解TorchDrug的架构：

* *核心概念：**参见`references/core_concepts.md`了解：
- 架构哲学（模块化，可配置）
- 数据结构（图、分子、蛋白质、PackedGraph）
- 模型接口和前向函数签名
- 任务接口（预测、目标、前向、评估）
- 训练工作流程和最佳实践
- 损失函数和指标
- 常见陷阱和调试

## 快速参考作弊Sheet

* *选择数据集：**
- 分子属性→`references/datasets.md`→分子部分
- 蛋白质任务→`references/datasets.md`→蛋白质部分
- 知识图→`references/datasets.md`→知识图部分

* *选择型号：**
- 分子 → `references/models_architectures.md` → GNN 部分 → GIN/GAT/SchNet
- 蛋白质（序列）→ `references/models_architectures.md` → 蛋白质部分 → ESM
- 蛋白质（结构）→ `references/models_architectures.md` → 蛋白质部分 → GearNet
- 知识图谱 → `references/models_architectures.md` → KG 部分 → RotatE/ComplEx

* *常见任务：**
- 属性预测 → `references/molecular_property_prediction.md` 或 `references/protein_modeling.md`
- 生成 → `references/molecular_generation.md`
- 逆合成 → `references/retrosynthesis.md`
- KG推理 → `references/knowledge_graphs.md`

* *了解架构：**
- 数据结构 → `references/core_concepts.md` → 数据结构
- 模型设计 → `references/core_concepts.md` → 模型接口
- 任务设计 → `references/core_concepts.md` → 任务界面

## 常见问题故障排除

* *问题：尺寸不匹配错误**
→ 检查 `model.input_dim` 是否匹配 `dataset.node_feature_dim`
→ 参见 `references/core_concepts.md` → 基本属性

* *问题：分子任务表现不佳**
→使用支架分割，而不是随机
→尝试GIN而不是GCN
→参见`references/molecular_property_prediction.md`→最佳实践

* *问题：蛋白质模型不学习**
→使用预训练用于序列任务的 ESM
→ 检查结构模型的边缘构造
→ 参见 `references/protein_modeling.md` → 训练工作流程

* *问题：大图的内存错误**
→ 减少批量大小
→ 使用梯度累积
→ 参见`references/core_concepts.md` → 内存效率

* *问题：生成的分子无效**
→ 添加有效性约束
→ 使用 RDKit 验证进行后处理
→ 参见 `references/molecular_generation.md` → 验证和过滤

## 资源

* *官方文档：** https://torchdrug.ai/docs/
* *GitHub：** https://github.com/DeepGraphLearning/torchdrug
* *论文：** TorchDrug：强大而灵活的药物发现机器学习平台

## 摘要

导航到相应的根据您的任务参考文件：

1. **分子性质预测** → `molecular_property_prediction.md`
2. **蛋白质建模** → `protein_modeling.md`
3. **知识图** → `knowledge_graphs.md`
4. **分子生成** → `molecular_generation.md`
5. **逆合成** → `retrosynthesis.md`
6. **型号选择** → `models_architectures.md`
7. **数据集选择** → `datasets.md`
8. **技术细节** → `core_concepts.md`

Each 参考通过示例、最佳实践和常见用例全面覆盖其领域。
