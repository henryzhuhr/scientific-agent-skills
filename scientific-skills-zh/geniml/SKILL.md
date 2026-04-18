---
name: geniml
description: 在处理机器学习任务的基因组区间数据（BED 文件）时应使用此技能。用于训练区域嵌入（Region2Vec、BEDspace）、单细胞 ATAC-seq 分析 (scEmbed)、构建共识峰（宇宙）或任何基于 ML 的基因组区域分析。适用于 BED 文件集合、scATAC-seq 数据、染色质可及性数据集和基于区域的基因组特征学习。
license: BSD-2-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# Geniml：基因组区间机器学习

## 概述

Geniml 是一个 Python 包，用于根据 BED 文件的基因组区间数据构建机器学习模型。它提供了用于学习基因组区域、单细胞和元数据标签嵌入的无监督方法，从而实现相似性搜索、聚类和下游 ML 任务。

## 安装

使用 uv 安装 geniml：

```bash
uv uv pip install geniml
```

对于 ML 依赖项（PyTorch、等）：

```bash
uv uv pip install 'geniml[ml]'
```

来自GitHub的开发版本：

```bash
uv uv pip install git+https://github.com/databio/geniml.git
```

## 核心功能

Geniml提供了五个主要功能，每个功能都在专用参考文件中详细说明：

### 1. Region2Vec：基因组区域嵌入

使用word2vec式学习训练基因组区域的无监督嵌入。

* *用于：** BED文件的降维、区域相似性分析、下游ML的特征向量。

* *工作流程：**
1. 使用 Universe 引用 
2 对 BED 文件进行标记。在 token
3 上训练 Region2Vec 模型。生成区域的嵌入

* *参考：** 请参阅 `references/region2vec.md` 了解详细的工作流程、参数和示例。

### 2. BEDspace：联合区域和元数据嵌入

使用 StarSpace 训练区域集和元数据标签的共享嵌入。

* *用于：** 元数据感知搜索，跨模态查询（区域→标签或标签→区域），基因组内容和实验条件联合分析。

* *工作流程：**
1. 预处理区域和元数据
2. 列车BED空间模型
3. 计算距离
4. 跨区域和标签查询

* *参考：**请参阅`references/bedspace.md`了解详细的工作流程、搜索类型和示例。

### 3. scEmbed：单细胞染色质可及性嵌入

在单细胞ATAC-seq数据上训练Region2Vec模型以进行细胞级嵌入。

* *用于：** scATAC-seq 聚类、细胞类型注释、单细胞降维、与 scanpy 工作流程集成。

  * *工作流程：**
1. 准备 AnnData 和峰值坐标 
2. 预标记单元格
3. 训练 scEmbed 模型
4. 生成单元嵌入
5. 使用 scanpy

* *参考：** 请参阅 `references/scembed.md` 了解详细的工作流程、参数和示例。

### 4. 共识峰：宇宙构建

使用多种统计方法从 BED 文件集合构建参考峰集（宇宙）。

* *用于：** 创建标记化引用，跨数据集标准化区域，定义共识特征统计严谨性。

* *工作流程：**
1. 合并 BED 文件
2. 生成覆盖曲目
3. 使用 CC、CCF、ML 或 HMM 方法构建宇宙

* *方法：**
- **CC（覆盖截止）**：基于简单阈值
- **CCF（灵活覆盖截止）**：边界置信区间
- **ML（最大似然）**：概率建模位置
- **HMM（隐马尔可夫模型）**：复杂状态建模

* *参考：**参见`references/consensus_peaks.md`的方法比较、参数和示例。

### 5.实用工具：支持工具

用于缓存、随机化、评估和分析的附加工具search.

* *可用实用程序：**
- **BBClient**：用于重复访问的 BED 文件缓存
- **BEDshift**：随机化保留基因组上下文
- **评估**：嵌入质量指标（剪影、Davies-Bouldin 等）
- **标记化**：区域标记化实用程序（硬、软、基于宇宙）
- **Text2BedNN**：基因组查询的神经搜索后端

  * *参考：** 有关每个实用程序的详细用法，请参阅 `references/utilities.md`。

## 常见工作流程

### 基本区域嵌入流程

```python
from geniml.tokenization import hard_tokenization
from geniml.region2vec import region2vec
from geniml.evaluation import evaluate_embeddings

# Step 1: Tokenize BED files
hard_tokenization(
    src_folder='bed_files/',
    dst_folder='tokens/',
    universe_file='universe.bed',
    p_value_threshold=1e-9
)

# Step 2: Train Region2Vec
region2vec(
    token_folder='tokens/',
    save_dir='model/',
    num_shufflings=1000,
    embedding_dim=100
)

# Step 3: Evaluate
metrics = evaluate_embeddings(
    embeddings_file='model/embeddings.npy',
    labels_file='metadata.csv'
)
```

### scATAC-seq 分析流程

```python
import scanpy as sc
from geniml.scembed import ScEmbed
from geniml.io import tokenize_cells

# Step 1: Load data
adata = sc.read_h5ad('scatac_data.h5ad')

# Step 2: Tokenize cells
tokenize_cells(
    adata='scatac_data.h5ad',
    universe_file='universe.bed',
    output='tokens.parquet'
)

# Step 3: Train scEmbed
model = ScEmbed(embedding_dim=100)
model.train(dataset='tokens.parquet', epochs=100)

# Step 4: Generate embeddings
embeddings = model.encode(adata)
adata.obsm['scembed_X'] = embeddings

# Step 5: Cluster with scanpy
sc.pp.neighbors(adata, use_rep='scembed_X')
sc.tl.leiden(adata)
sc.tl.umap(adata)
```

### Universe构建和评估

```bash
# Generate coverage
cat bed_files/*.bed > combined.bed
uniwig -m 25 combined.bed chrom.sizes coverage/

# Build universe with coverage cutoff
geniml universe build cc \
  --coverage-folder coverage/ \
  --output-file universe.bed \
  --cutoff 5 \
  --merge 100 \
  --filter-size 50

# Evaluate universe quality
geniml universe evaluate \
  --universe universe.bed \
  --coverage-folder coverage/ \
  --bed-folder bed_files/
```

## CLI参考

Geniml提供主要操作的命令行界面：

```bash
# Region2Vec training
geniml region2vec --token-folder tokens/ --save-dir model/ --num-shuffle 1000

# BEDspace preprocessing
geniml bedspace preprocess --input regions/ --metadata labels.csv --universe universe.bed

# BEDspace training
geniml bedspace train --input preprocessed.txt --output model/ --dim 100

# BEDspace search
geniml bedspace search -t r2l -d distances.pkl -q query.bed -n 10

# Universe building
geniml universe build cc --coverage-folder coverage/ --output universe.bed --cutoff 5

# BEDshift randomization
geniml bedshift --input peaks.bed --genome hg38 --preserve-chrom --iterations 100
```

## 何时使用哪个工具

* *使用Region2Vec当：**
- 处理大量基因组数据（ChIP-seq、ATAC-seq等）
- 需要无元数据的无监督嵌入
- 跨实验比较区域集
- 为下游监督学习构建特征

* *在以下情况下使用BEDspace：**
- 可用元数据标签（细胞类型、组织、条件）
- 需要通过元数据查询区域，反之亦然
- 想要区域和标签的联合嵌入空间
- 构建可搜索的基因组数据库

* *在以下情况下使用 scEmbed：**
- 分析单细胞 ATAC-seq 数据
- 通过以下方式对细胞进行聚类染色质可及性
- 注释来自scATAC-seq的细胞类型
- 需要与scanpy集成

* *在以下情况下使用Universe Building：**
- 需要参考峰集进行标记化
- 将多个实验组合成共识
- 想要统计上严格的区域定义
- 为项目构建标准参考

* *在以下情况下使用实用程序：**
- 需要缓存远程 BED 文件 (BBClient)
- 生成统计空模型 (BEDshift)
- 评估嵌入质量 (Evaluation)
- 构建搜索界面(Text2BedNN)

## 最佳实践

### 一般准则

- **宇宙质量至关重要**：投入时间构建全面、结构良好的宇宙
- **标记化验证**：训练前检查覆盖率（> 80% 理想）
- **参数调整**：尝试嵌入维度、学习率、和训练时期
- **评估**：始终使用多个指标和可视化来验证嵌入
- **文档**：记录参数和随机种子以实现可重复性

### 性能注意事项

- **预分词**：对于 scEmbed，始终对单元进行预分词以加快训练
- **内存管理**：大型数据集可能需要批处理或下采样
- **计算资源**：ML/HMM Universe 方法属于计算密集型
- **模型缓存**：使用 BBClient 避免重复下载

### 集成模式

- **使用 scanpy**：scEmbed 嵌入无缝集成为 `adata.obsm` 条目
- **使用 BEDbase**：使用 BBClient 访问远程 BED 存储库
- **使用 Hugging Face**：导出经过训练的模型以实现共享和可重复性
- **使用 R**：使用网状用于 R 集成（请参阅实用程序参考）

## 相关项目

Geniml 是 BEDbase 生态系统的一部分：

- **BEDbase**：基因组区域的统一平台
- **BEDboss**：BED 文件的处理管道
- **Gtars**：基因组工具和实用程序
- **BBClient**：BEDbase 存储库的客户端

## 其他资源

- **文档**：https://docs.bedbase.org/geniml/
- **GitHub**：https://github.com/databio/geniml
- **预训练模型**：在 Hugging Face 上可用（databio）组织）
- **出版物**：在文档中引用方法细节

## 故障排除

* *“标记化覆盖率太低”：**
- 检查Universe质量和完整性
- 调整p值阈值（尝试1e-6而不是1e-9）
- 确保Universe匹配基因组组装

* *“训练不收敛”：**
- 调整学习率（尝试0.01-0.05范围）
- 增加训练时期
- 检查数据质量和预处理

* *“内存不足错误”：**
- 减少批量大小scEmbed
- 以块的形式处理数据
- 对单单元数据使用预标记化

* *“未找到 StarSpace”(BEDspace)：**
  - 单独安装 StarSpace：https://github.com/facebookresearch/StarSpace
  - 正确设置 `--path-to-starspace` 参数

有关详细的故障排除和特定于方法的问题，请查阅相应的参考文件。
