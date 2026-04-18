---
name: esm
description: 用于蛋白质语言模型的综合工具包，包括 ESM3（跨序列、结构和功能的生成多模式蛋白质设计）和 ESM C（高效蛋白质嵌入和表示）。在处理蛋白质序列、结构或功能预测时使用此技能；设计新型蛋白质；生成蛋白质嵌入；进行反向折叠；或进行蛋白质工程任务。支持本地模型使用和基于云的 Forge API 以进行可扩展推理。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# ESM：进化规模建模

## 概述

ESM 提供最先进的蛋白质语言模型，用于理解、生成和设计蛋白质。该技能支持使用两个模型系列：用于跨序列、结构和功能的生成蛋白质设计的 ESM3，以及用于高效蛋白质表示学习和嵌入的 ESM C。

## 核心功能

### 1. 使用 ESM3

生成蛋白质序列使用多模式生成模型生成具有所需特性的新型蛋白质序列。

* *当使用：**
- 设计具有特定功能特性的蛋白质
- 完成部分蛋白质序列
- 生成现有蛋白质的变体
- 创建具有所需结构特征的蛋白质

* *基本用法：**

```python
from esm.models.esm3 import ESM3
from esm.sdk.api import ESM3InferenceClient, ESMProtein, GenerationConfig

# Load model locally
model: ESM3InferenceClient = ESM3.from_pretrained("esm3-sm-open-v1").to("cuda")

# Create protein prompt
protein = ESMProtein(sequence="MPRT___KEND")  # '_' represents masked positions

# Generate completion
protein = model.generate(protein, GenerationConfig(track="sequence", num_steps=8))
print(protein.sequence)
```

* *通过Forge进行远程/云使用API：**

```python
from esm.sdk.forge import ESM3ForgeInferenceClient
from esm.sdk.api import ESMProtein, GenerationConfig

# Connect to Forge
model = ESM3ForgeInferenceClient(model="esm3-medium-2024-08", url="https://forge.evolutionaryscale.ai", token="<token>")

# Generate
protein = model.generate(protein, GenerationConfig(track="sequence", num_steps=8))
```

详细的ESM3模型规范、高级生成配置和多模态提示示例请参见`references/esm3-api.md`。

### 2.结构预测和反向折叠

使用ESM3的结构轨迹从序列或反向折叠进行结构预测（序列设计来自结构）。

* *结构预测：**

```python
from esm.sdk.api import ESM3InferenceClient, ESMProtein, GenerationConfig

# Predict structure from sequence
protein = ESMProtein(sequence="MPRTKEINDAGLIVHSP...")
protein_with_structure = model.generate(
    protein,
    GenerationConfig(track="structure", num_steps=protein.sequence.count("_"))
)

# Access predicted structure
coordinates = protein_with_structure.coordinates  # 3D coordinates
pdb_string = protein_with_structure.to_pdb()
```

* *反向折叠（结构序列）：**

```python
# Design sequence for a target structure
protein_with_structure = ESMProtein.from_pdb("target_structure.pdb")
protein_with_structure.sequence = None  # Remove sequence

# Generate sequence that folds to this structure
designed_protein = model.generate(
    protein_with_structure,
    GenerationConfig(track="sequence", num_steps=50, temperature=0.7)
)
```

### 3. 使用 ESM C

进行蛋白质嵌入用于功能预测、分类或相似性分析等下游任务的高质量嵌入。

* *何时使用：**
- 提取用于机器学习的蛋白质表示
- 计算序列相似性
- 用于蛋白质分类的特征提取
- 蛋白质相关任务的迁移学习

* *基本用法：**

```python
from esm.models.esmc import ESMC
from esm.sdk.api import ESMProtein

# Load ESM C model
model = ESMC.from_pretrained("esmc-300m").to("cuda")

# Get embeddings
protein = ESMProtein(sequence="MPRTKEINDAGLIVHSP...")
protein_tensor = model.encode(protein)

# Generate embeddings
embeddings = model.forward(protein_tensor)
```

* *批处理：**

```python
# Encode multiple proteins
proteins = [
    ESMProtein(sequence="MPRTKEIND..."),
    ESMProtein(sequence="AGLIVHSPQ..."),
    ESMProtein(sequence="KTEFLNDGR...")
]

embeddings_list = [model.logits(model.forward(model.encode(p))) for p in proteins]
```

有关ESM C模型详细信息、效率比较和高级嵌入策略，请参阅`references/esm-c-api.md`。

### 4. 功能条件化和注释

使用ESM3的函数轨迹生成具有特定功能注释的蛋白质或根据序列预测功能。

* *功能条件化生成：**

```python
from esm.sdk.api import ESMProtein, FunctionAnnotation, GenerationConfig

# Create protein with desired function
protein = ESMProtein(
    sequence="_" * 200,  # Generate 200 residue protein
    function_annotations=[
        FunctionAnnotation(label="fluorescent_protein", start=50, end=150)
    ]
)

# Generate sequence with specified function
functional_protein = model.generate(
    protein,
    GenerationConfig(track="sequence", num_steps=200)
)
```

### 5. 思想链生成

使用ESM3迭代完善蛋白质设计思想链生成方法。

```python
from esm.sdk.api import GenerationConfig

# Multi-step refinement
protein = ESMProtein(sequence="MPRT" + "_" * 100 + "KEND")

# Step 1: Generate initial structure
config = GenerationConfig(track="structure", num_steps=50)
protein = model.generate(protein, config)

# Step 2: Refine sequence based on structure
config = GenerationConfig(track="sequence", num_steps=50, temperature=0.5)
protein = model.generate(protein, config)

# Step 3: Predict function
config = GenerationConfig(track="function", num_steps=20)
protein = model.generate(protein, config)
```

### 6. 使用 Forge API 进行批处理

使用 Forge 的异步执行器高效处理多种蛋白质。

```python
from esm.sdk.forge import ESM3ForgeInferenceClient
import asyncio

client = ESM3ForgeInferenceClient(model="esm3-medium-2024-08", token="<token>")

# Async batch processing
async def batch_generate(proteins_list):
    tasks = [
        client.async_generate(protein, GenerationConfig(track="sequence"))
        for protein in proteins_list
    ]
    return await asyncio.gather(*tasks)

# Execute
proteins = [ESMProtein(sequence=f"MPRT{'_' * 50}KEND") for _ in range(10)]
results = asyncio.run(batch_generate(proteins))
```

 有关详细的 Forge API 文档、身份验证、速率限制和信息，请参阅 `references/forge-api.md`批处理模式。

## 模型选择指南

* *ESM3 模型（生成）：**
- `esm3-sm-open-v1` (1.4B) - 开放权重，本地使用，适合实验
- `esm3-medium-2024-08` (7B) - 质量和速度的最佳平衡（Forge）仅）
- `esm3-large-2024-03` (98B) - 最高质量，速度较慢（仅限 Forge）

* *ESM C 模型（嵌入）：**
- `esmc-300m`（30 层）- 轻量级、快速推理
- `esmc-600m` （36层） - 性能均衡
- `esmc-6b` （80层） - 最大表示质量

* *选择标准：**
- **本地开发/测试：** 使用`esm3-sm-open-v1`或`esmc-300m`
- **生产质量：** 使用`esm3-medium-2024-08` via Forge
- **最大精度：** 使用 `esm3-large-2024-03` 或 `esmc-6b`
- **高吞吐量：** 使用 Forge API 和批处理执行器
- **成本优化：** 使用较小的模型，实施缓存策略

## 安装

* *基本安装：**

```bash
uv pip install esm
```

* *带 Flash Attention（推荐用于更快的推理）：**

```bash
uv pip install esm
uv pip install flash-attn --no-build-isolation
```

* *对于 Forge API 访问：**

```bash
uv pip install esm  # SDK includes Forge client
```

 无需其他依赖项。在 https://forge.evolutionaryscale.ai

## 获取 Forge API 令牌常见工作流程

有关详细示例和完整工作流程，请参阅 `references/workflows.md`，其中包括：
- 具有思想链的新型 GFP 设计
- 蛋白质变体生成和筛选
- 基于结构的序列优化
- 功能预测管道
- 基于嵌入的聚类和分析

## 参考文献

该技能包括全面的参考文档：

- `references/esm3-api.md` - ESM3模型架构、API参考、生成参数和多模态提示
- `references/esm-c-api.md` - ESM C模型细节、嵌入策略和性能优化
- `references/forge-api.md` - Forge平台文档、身份验证、批处理和部署
- `references/workflows.md` - 完整示例和常见工作流程模式

这些参考包含详细的API规范、参数描述和高级使用模式。根据特定任务的需要加载它们。

## 最佳实践

* *对于生成任务：**
- 从较小的模型开始进行原型设计 (`esm3-sm-open-v1`)
- 使用温度参数来控制多样性（0.0 = 确定性，1.0 = 多样性）
- 实施迭代细化复杂设计的思路
- 通过结构预测或湿实验室实验验证生成的序列

* *对于嵌入任务：**
- 尽可能批量处理序列以提高效率
- 缓存嵌入以进行重复分析
- 计算时标准化嵌入相似之处
- 根据下游任务要求使用适当的模型大小

* *用于生产部署：**
- 使用 Forge API 实现可扩展性和最新模型
- 为 API 调用实施错误处理和重试逻辑
- 监控令牌使用情况并实施速率限制
- 考虑将 AWS SageMaker 部署用于专用基础设施

## 资源和文档

- **GitHub 存储库：** https://github.com/evolutionaryscale/esm
- **Forge 平台：** https://forge.evolutionaryscale.ai
- **科学论文：** Hayes 等人，Science (2025) - https://www.science.org/doi/10.1126/science.ads0018
- **博客文章：**
  - ESM3 发布：https://www.evolutionaryscale.ai/blog/esm3-release
  - ESM C 发布：https://www.evolutionaryscale.ai/blog/esm-cambrian
- **社区：** Slack 社区https://bit.ly/3FKwcWd
- **模型权重：** HuggingFace EvolutionaryScale 组织

## 负责任的使用

ESM 专为蛋白质工程、药物发现和科学研究中的有益应用而设计。设计新型蛋白质时遵循负责任的生物设计框架 (https://responsiblebiodesign.ai/)。在实验验证之前考虑蛋白质设计的生物安全性和伦理影响。
