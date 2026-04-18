---
name: primekg
description: 查询精准医学知识图谱（PrimeKG）以获取包括基因、药物、疾病、表型等在内的多尺度生物数据。
license: Unknown
metadata:
    skill-author: K-Dense Inc. (PrimeKG original from Harvard MIMS)
---

# PrimeKG 知识图谱技能

## 概述

PrimeKG 是一个精准医学知识图谱，将 20 多个主要数据库和高质量科学文献集成到一个资源中。它包含超过 100,000 个节点和 400 万条边，涉及 29 种关系类型，包括药物-靶标、疾病-基因和表型-疾病关联。

* *关键功能：**
- 搜索节点（基因、蛋白质、药物、疾病、表型）
- 检索直接邻居（相关实体和临床证据）
- 分析局部疾病背景（相关基因、药物、表型）
- 识别药物疾病路径（潜在的再利用机会）

* *数据访问：**通过`query_primekg.py`进行编程访问。数据存储在 `C:\Users\eamon\Documents\Data\PrimeKG\kg.csv`.

## 何时使用此技能

此技能应在以下情况下使用：

- **基于知识的药物发现：** 识别疾病的靶点和机制。
- **药物再利用：** 寻找可能有新适应症证据的现有药物。
- **表型分析：** 了解症状/表型与疾病和基因的关系。
- **多尺度生物学：** 弥合分子靶标（基因）和临床结果（疾病）之间的差距。
- **网络药理学：** 研究药物-靶标相互作用的更广泛的网络效应。

## 核心工作流程

### 1. 搜索实体

查找基因、药物或疾病的标识符。

```python
from scripts.query_primekg import search_nodes

# Search for Alzheimer's disease nodes
results = search_nodes("Alzheimer", node_type="disease")
# Returns: [{"id": "EFO_0000249", "type": "disease", "name": "Alzheimer's disease", ...}]
```

### 2. 获取邻居（直接关联）

检索所有连接的节点和关系类型。

```python
from scripts.query_primekg import get_neighbors

# Get all neighbors of a specific disease ID
neighbors = get_neighbors("EFO_0000249")
# Returns: List of neighbors like {"neighbor_name": "APOE", "relation": "disease_gene", ...}
```

### 3.分析疾病上下文

A 总结疾病关联的高级函数。

```python
from scripts.query_primekg import get_disease_context

# Comprehensive summary for a disease
context = get_disease_context("Alzheimer's disease")
# Access: context['associated_genes'], context['associated_drugs'], context['phenotypes']
```

## PrimeKG

中的关系类型该图包含多种关键关系类型，包括：
- `protein_protein`：物理 PPI
- `drug_protein`：药物靶点/机制关联
- `disease_gene`：遗传关联
- `drug_disease`：适应症和禁忌症
- `disease_phenotype`：临床体征和症状
- `gwas`：全基因组关联研究证据

## 最佳实践

1. **使用特定 ID：** 使用 `get_neighbors` 时，请确保您拥有 `search_nodes`.
2 中的正确 ID。 **上下文优先：** 在深入研究特定基因或药物之前，使用 `get_disease_context` 进行广泛的概述。
3. **过滤关系：** 在 `get_neighbors` 中使用 `relation_type` 过滤器来关注特定证据（例如，仅 `drug_protein`）。
4. **多尺度整合：** 结合`OpenTargets`获得更深入的遗传证据，或结合`Semantic Scholar`获得最新的文献背景。

## 资源

### 脚本
- `scripts/query_primekg.py`：搜索和查询知识图谱的核心功能。

### 数据Path
- 数据：`/mnt/c/Users/eamon/Documents/Data/PrimeKG/kg.csv`
- 节点总数：~129,000
- 边总数：~4,000,000
- 数据库：基于 CSV，针对 pandas 查询进行了优化。
