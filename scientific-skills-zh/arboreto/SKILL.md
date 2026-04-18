---
name: arboreto
description: 使用可扩展算法（GRNBoost2、GENIE3）从基因表达数据推断基因调控网络 (GRN)。在分析转录组学数据（批量 RNA-seq、单细胞 RNA-seq）时使用，以识别转录因子-靶基因关系和调控相互作用。支持大规模数据集的分布式计算。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# Arboreto

## 概述

Arboreto 是一个计算库，用于使用从单机扩展到多节点集群的并行算法从基因表达数据推断基因调控网络 (GRN)。

* *核心功能**：根据观察（细胞、样本、 

## 快速入门

安装arboreto：
```bash
uv pip install arboreto
```

基本GRN推理：
```python
import pandas as pd
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load expression data (genes as columns)
    expression_matrix = pd.read_csv('expression_data.tsv', sep='\t')

    # Infer regulatory network
    network = grnboost2(expression_data=expression_matrix)

    # Save results (TF, target, importance)
    network.to_csv('network.tsv', sep='\t', index=False, header=False)
```

* *关键**：始终使用`if __name__ == '__main__':`防护，因为Dask 催生新流程。

## 核心功能

### 1. 基本 GRN 推理

对于标准 GRN 推理工作流程，包括：
- 输入数据准备（Pandas DataFrame 或 NumPy 数组）
- 使用 GRNBoost2 或 GRNBoost2 运行推理GENIE3
- 通过转录因子过滤
- 输出格式和解释

* *参见**：`references/basic_inference.md`

* *使用可立即运行的脚本**：`scripts/basic_grn_inference.py` 用于标准推理任务：
```bash
python scripts/basic_grn_inference.py expression_data.tsv output_network.tsv --tf-file tfs.txt --seed 777
```

### 2.算法选择

Arboreto 提供两种算法：

* *GRNBoost2（推荐）**：
- 基于快速梯度提升推理
- 针对大型数据集（10k+ 观测值）进行优化
- 大多数分析的默认选择

* *GENIE3**：
- 基于随机森林的推理
- 原始多元回归方法
- 用于比较或验证

Quick对比：
```python
from arboreto.algo import grnboost2, genie3

# Fast, recommended
network_grnboost = grnboost2(expression_data=matrix)

# Classic algorithm
network_genie3 = genie3(expression_data=matrix)
```

* *详细的算法对比、参数和选型指导**：`references/algorithms.md`

### 3.分布式计算

从本地多核到集群环境的规模推理：

* *本地（默认）** - 自动使用所有可用核心：
```python
network = grnboost2(expression_data=matrix)
```

 * *自定义本地客户端** - 控制资源：
```python
from distributed import LocalCluster, Client

local_cluster = LocalCluster(n_workers=10, memory_limit='8GB')
client = Client(local_cluster)

network = grnboost2(expression_data=matrix, client_or_address=client)

client.close()
local_cluster.close()
```

 * *集群计算** - 连接到远程 Dask调度程序：
```python
from distributed import Client

client = Client('tcp://scheduler:8786')
network = grnboost2(expression_data=matrix, client_or_address=client)
```

* *用于集群设置、性能优化和大规模工作流程**：`references/distributed_computing.md`

## 安装

```bash
uv pip install arboreto
```

* *依赖项**：scipy、scikit-learn、numpy、pandas、 dask，分布式

## 常见用例

### 单细胞RNA-seq分析
```python
import pandas as pd
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load single-cell expression matrix (cells x genes)
    sc_data = pd.read_csv('scrna_counts.tsv', sep='\t')

    # Infer cell-type-specific regulatory network
    network = grnboost2(expression_data=sc_data, seed=42)

    # Filter high-confidence links
    high_confidence = network[network['importance'] > 0.5]
    high_confidence.to_csv('grn_high_confidence.tsv', sep='\t', index=False)
```

### 带TF过滤的批量RNA-seq
```python
from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load data
    expression_data = pd.read_csv('rnaseq_tpm.tsv', sep='\t')
    tf_names = load_tf_names('human_tfs.txt')

    # Infer with TF restriction
    network = grnboost2(
        expression_data=expression_data,
        tf_names=tf_names,
        seed=123
    )

    network.to_csv('tf_target_network.tsv', sep='\t', index=False)
```

### 比较分析（多重条件）
```python
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Infer networks for different conditions
    conditions = ['control', 'treatment_24h', 'treatment_48h']

    for condition in conditions:
        data = pd.read_csv(f'{condition}_expression.tsv', sep='\t')
        network = grnboost2(expression_data=data, seed=42)
        network.to_csv(f'{condition}_network.tsv', sep='\t', index=False)
```

## 输出解释

Arboreto 返回带有监管链接的 DataFrame：

|专栏 |描述|
|--------|-------------|
| `TF` |转录因子（调节因子）|
| `target` |目的基因|
| `importance` |监管重要性得分（越高=更强）|

* *过滤策略**：
- 每个目标基因的前 N 个链接
- 重要性阈值（例如，> 0.5）
- 统计显着性测试（排列测试）

## 与 pySCENIC 集成

Arboreto 是单细胞调控网络 SCENIC 管道的核心组件分析：

```python
# Step 1: Use arboreto for GRN inference
from arboreto.algo import grnboost2
network = grnboost2(expression_data=sc_data, tf_names=tf_list)

# Step 2: Use pySCENIC for regulon identification and activity scoring
# (See pySCENIC documentation for downstream analysis)
```

## 再现性

始终设置可再现结果的种子：
```python
network = grnboost2(expression_data=matrix, seed=777)
```

运行多个种子进行稳健性分析：
```python
from distributed import LocalCluster, Client

if __name__ == '__main__':
    client = Client(LocalCluster())

    seeds = [42, 123, 777]
    networks = []

    for seed in seeds:
        net = grnboost2(expression_data=matrix, client_or_address=client, seed=seed)
        networks.append(net)

    # Combine networks and filter consensus links
    consensus = analyze_consensus(networks)
```

## 故障排除

* *内存错误**：通过过滤低方差基因或使用分布式计算来减少数据集大小

* *性能缓慢**：使用GRNBoost2而不是GENIE3，启用分布式客户端，过滤TF列表

* *Dask错误**：确保脚本中存在`if __name__ == '__main__':`防护

* *空结果**：检查数据格式（基因作为列），验证 TF 名称与基因名称匹配
