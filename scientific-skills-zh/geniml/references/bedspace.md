# BEDspace：联合区域和元数据嵌入

## 概述

BEDspace 将 StarSpace 模型应用于基因组数据，从而能够在共享低维空间中同时训练区域集及其元数据标签的数值嵌入。这允许跨区域和元数据进行丰富的查询。

## 何时使用

在处理时使用BEDspace：
- 具有关联元数据（细胞类型、组织、条件）的区域集
- 需要元数据感知相似性的搜索任务
- 跨模式查询（例如，“查找与标签X相似的区域”）
- 联合分析基因组内容和实验条件的

## 工作流程

BEDspace由四个顺序操作组成：

### 1.预处理

格式化基因组间隔和元数据用于StarSpace训练：

```bash
geniml bedspace preprocess \
  --input /path/to/regions/ \
  --metadata labels.csv \
  --universe universe.bed \
  --labels "cell_type,tissue" \
  --output preprocessed.txt
```

* *所需文件：**
- **输入文件夹**：目录包含 BED 文件
- **元数据 CSV**：必须包含与 BED 文件名匹配的 `file_name` 列，以及元数据列
- **Universe 文件**：用于标记化的参考 BED 文件
- **标签**：要使用的元数据列的逗号分隔列表

预处理步骤添加 `__label__` 前缀

### 2. 在预处理数据上训练

执行StarSpace模型：

```bash
geniml bedspace train \
  --path-to-starspace /path/to/starspace \
  --input preprocessed.txt \
  --output model/ \
  --dim 100 \
  --epochs 50 \
  --lr 0.05
```

* *关键训练参数：**
- `--dim`：嵌入维度（典型： 50-200)
- `--epochs`：训练周期（典型：20-100）
- `--lr`：学习率（典型：0.01-0.1）

### 3.距离

计算区域集和元数据之间的距离度量标签：

```bash
geniml bedspace distances \
  --input model/ \
  --metadata labels.csv \
  --universe universe.bed \
  --output distances.pkl
```

此步骤创建相似性搜索所需的距离矩阵。

### 4.搜索

跨三个场景检索相似项目：

* *Region-to-Label (r2l)**：查询区域集 → 检索相似的元数据标签
```bash
geniml bedspace search -t r2l -d distances.pkl -q query_regions.bed -n 10
```

* *Label-to-Region (l2r)**：查询元数据标签 → 检索相似的区域集
```bash
geniml bedspace search -t l2r -d distances.pkl -q "T_cell" -n 10
```

* *Region-to-Region (r2r)**：查询区域集→ 检索相似区域集
```bash
geniml bedspace search -t r2r -d distances.pkl -q query_regions.bed -n 10
```

`-n`参数控制返回结果的数量。

## Python API

```python
from geniml.bedspace import BEDSpaceModel

# Load trained model
model = BEDSpaceModel.load('model/')

# Query similar items
results = model.search(
    query="T_cell",
    search_type="l2r",
    top_k=10
)
```

## 最佳实践

- **元数据结构**：确保元数据CSV包含`file_name`列与 BED 文件名完全匹配（无路径）
- **标签选择**：选择捕获感兴趣的生物变异的信息性元数据列
- **宇宙一致性**：在预处理、距离和任何后续分析中使用相同的宇宙文件
- **验证**：在投资训练之前进行预处理和检查输出格式
- **StarSpace 安装**：单独安装 StarSpace因为它是外部依赖项

## 输出解释

搜索结果返回按联合嵌入空间中的相似性排名的项目：
- **r2l**：标识表征您的查询区域的元数据标签
- **l2r**：查找与您的元数据条件匹配的区域集
- **r2r**：发现具有相似特征的区域集基因组内容

## 要求

BEDspace 需要单独安装StarSpace。下载地址：https://github.com/facebookresearch/StarSpace
