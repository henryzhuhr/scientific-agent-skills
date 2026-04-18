---
name: scikit-bio
description: 生物数据工具包。序列分析、比对、系统发育树、多样性指标（α/β、UniFrac）、排序（PCoA）、PERMANOVA、FASTA/Newick I/O，用于微生物组分析。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# scikit-bio

## 概述

scikit-bio 是一个用于处理生物数据的综合 Python 库。将此技能应用于涵盖序列操作、比对、系统发育、微生物生态学和多变量统计的生物信息学分析。

## 何时使用此技能

当用户满足以下条件时应使用此技能：
- 处理生物序列（DNA、RNA、蛋白质）
- 需要读/写生物文件格式（FASTA、FASTQ、GenBank、 Newick、BIOM 等）
- 执行序列比对或搜索基序
- 构建或分析系统发育树
- 计算多样性度量（α/β 多样性、UniFrac 距离）
- 执行排序分析（PCoA、CCA、RDA）
- 运行统计测试生物/生态数据（PERMANOVA、ANOSIM、Mantel）
- 分析微生物组或群落生态数据
- 使用语言模型中的蛋白质嵌入
- 需要操作生物数据表

## 核心功能

### 1. 序列操作

使用DNA、RNA和蛋白质数据的专用类处理生物序列。

* *关键操作：**
- 从FASTA、FASTQ、GenBank、EMBL格式读取/写入序列
- 序列切片、串联和搜索
- 反向补体、转录(DNA→RNA)和翻译（RNA→蛋白质）
- 使用正则表达式查找基序和模式
- 计算距离（基于汉明、k-mer）
- 处理序列质量分数和元数据

* *常见模式：**
```python
import skbio

# Read sequences from file
seq = skbio.DNA.read('input.fasta')

# Sequence operations
rc = seq.reverse_complement()
rna = seq.transcribe()
protein = rna.translate()

# Find motifs
motif_positions = seq.find_with_regex('ATG[ACGT]{3}')

# Check for properties
has_degens = seq.has_degenerates()
seq_no_gaps = seq.degap()
```

* *重要说明：**
- 使用 `DNA`、`RNA`、`Protein` 类进行带验证的语法序列
- 使用 `Sequence` 类进行无字母表的通用序列限制
- 质量分数自动从FASTQ 文件加载到位置元数据中
- 元数据类型：序列级（ID、描述）、位置（每个碱基）、间隔（区域/特征）

### 2. 序列比对

使用动态编程算法执行成对和多序列比对。

* *Key功能：**
- 全局比对（带半全局变体的 Needleman-Wunsch）
- 局部比对（Smith-Waterman）
- 可配置的评分方案（匹配/不匹配、空位罚分、替换矩阵）
- CIGAR 字符串转换
- 多序列比对存储和操作`TabularMSA`

* *常见模式：**
```python
from skbio.alignment import local_pairwise_align_ssw, TabularMSA

# Pairwise alignment
alignment = local_pairwise_align_ssw(seq1, seq2)

# Access aligned sequences
msa = alignment.aligned_sequences

# Read multiple alignment from file
msa = TabularMSA.read('alignment.fasta', constructor=skbio.DNA)

# Calculate consensus
consensus = msa.consensus()
```

* *重要说明：**
- 使用`local_pairwise_align_ssw`进行局部比对（更快，基于SSW）
- 使用`StripedSmithWaterman`进行蛋白质比对
- 推荐用于生物序列的仿射间隙罚分
- 可以在scikit-bio、BioPython和黑云母比对格式之间转换

### 3.系统发育树

构建、操作和分析代表进化关系的系统发育树。

* *关键功能：**
- 从距离矩阵构造树（UPGMA、WPGMA、邻接、GME、BME）
- 树操作（修剪、重新生根、遍历）
- 距离计算（patristic、cophenetic、Robinson-Foulds）
- ASCII 可视化
- 纽维克格式 I/O

* *常见模式：**
```python
from skbio import TreeNode
from skbio.tree import nj

# Read tree from file
tree = TreeNode.read('tree.nwk')

# Construct tree from distance matrix
tree = nj(distance_matrix)

# Tree operations
subtree = tree.shear(['taxon1', 'taxon2', 'taxon3'])
tips = [node for node in tree.tips()]
lca = tree.lowest_common_ancestor(['taxon1', 'taxon2'])

# Calculate distances
patristic_dist = tree.find('taxon1').distance(tree.find('taxon2'))
cophenetic_matrix = tree.cophenetic_matrix()

# Compare trees
rf_distance = tree.robinson_foulds(other_tree)
```

* *重要说明：**
- 使用`nj()`进行邻居连接（经典系统发育方法）
- 使用`upgma()`进行UPGMA（假设分子钟）
- GME和BME具有高度可扩展性对于大树
- 树可以有根或无根；一些指标需要特定的生根

### 4.多样性分析

计算微生物生态和群落分析的α和β多样性指标。

* *关键功能：**
- α多样性：丰富度，香农熵，辛普森指数，Faith's PD，Pielou's均匀度
- β多样性： Bray-Curtis、Jaccard、加权/未加权 UniFrac、欧几里德距离
- 系统发育多样性度量（需要树输入）
- 稀疏和子采样
- 与排序和统计测试集成

* *常见模式：**
```python
from skbio.diversity import alpha_diversity, beta_diversity
import skbio

# Alpha diversity
alpha = alpha_diversity('shannon', counts_matrix, ids=sample_ids)
faith_pd = alpha_diversity('faith_pd', counts_matrix, ids=sample_ids,
                          tree=tree, otu_ids=feature_ids)

# Beta diversity
bc_dm = beta_diversity('braycurtis', counts_matrix, ids=sample_ids)
unifrac_dm = beta_diversity('unweighted_unifrac', counts_matrix,
                           ids=sample_ids, tree=tree, otu_ids=feature_ids)

# Get available metrics
from skbio.diversity import get_alpha_diversity_metrics
print(get_alpha_diversity_metrics())
```

* *重要说明：**
- 计数必须是表示丰度的整数，而不是相对频率
- 系统发育指标（Faith's PD、UniFrac）需要树和 OTU ID 映射
- 使用 `partial_beta_diversity()` 计算特定值仅样本对
- Alpha多样性返回Series，beta多样性返回DistanceMatrix

### 5.排序方法

将高维生物数据减少到可视化的低维空间。

* *关键功能：**
- 来自距离矩阵的PCoA（主坐标分析）
- CA用于列联表的（对应分析）
- 具有环境约束的 CCA（典型对应分析）
- 用于线性关系的 RDA（冗余分析）
- 用于特征解释的双标图投影

* *常见模式：**
```python
from skbio.stats.ordination import pcoa, cca

# PCoA from distance matrix
pcoa_results = pcoa(distance_matrix)
pc1 = pcoa_results.samples['PC1']
pc2 = pcoa_results.samples['PC2']

# CCA with environmental variables
cca_results = cca(species_matrix, environmental_matrix)

# Save/load ordination results
pcoa_results.write('ordination.txt')
results = skbio.OrdinationResults.read('ordination.txt')
```

* *重要说明：**
- PCoA 适用于任何距离/相异矩阵
- CCA 揭示群落组成的环境驱动因素
- 排序结果包括特征值、解释的比例和样本/特征坐标
- 结果与绘图库集成（matplotlib、seaborn、plotly）

### 6. 统计测试

执行特定于生态和生物数据的假设检验。

* *关键功能：**
- PERMANOVA：使用距离矩阵测试组差异
- ANOSIM：替代测试对于组差异
- PERMDISP：测试组分散的同质性
- Mantel测试：距离矩阵之间的相关性
- Bioenv：查找与距离相关的环境变量

* *常见模式：**
```python
from skbio.stats.distance import permanova, anosim, mantel

# Test if groups differ significantly
permanova_results = permanova(distance_matrix, grouping, permutations=999)
print(f"p-value: {permanova_results['p-value']}")

# ANOSIM test
anosim_results = anosim(distance_matrix, grouping, permutations=999)

# Mantel test between two distance matrices
mantel_results = mantel(dm1, dm2, method='pearson', permutations=999)
print(f"Correlation: {mantel_results[0]}, p-value: {mantel_results[1]}")
```

* *重要注：**
- 排列检验提供非参数显着性检验
- 使用 999+ 排列获得稳健的 p 值
- PERMANOVA 对色散差异敏感；与 PERMDISP
 配对 - Mantel 测试评估矩阵相关性（例如，地理距离与遗传距离）

### 7. 文件 I/O 和格式转换

通过自动格式检测读取和写入 19 种以上生物文件格式。

* *支持的格式：**
- 序列：FASTA、FASTQ、 GenBank、EMBL、QSeq
- 比对：Clustal、PHYLIP、Stockholm
- 树：Newick
- 表：BIOM（HDF5 和 JSON）
- 距离：分隔方阵
- 分析：BLAST+6/7、GFF3、排序结果
- 元数据：带有验证的 TSV/CSV

* * 常见模式：**
```python
import skbio

# Read with automatic format detection
seq = skbio.DNA.read('file.fasta', format='fasta')
tree = skbio.TreeNode.read('tree.nwk')

# Write to file
seq.write('output.fasta', format='fasta')

# Generator for large files (memory efficient)
for seq in skbio.io.read('large.fasta', format='fasta', constructor=skbio.DNA):
    process(seq)

# Convert formats
seqs = list(skbio.io.read('input.fastq', format='fastq', constructor=skbio.DNA))
skbio.io.write(seqs, format='fasta', into='output.fasta')
```

* * 重要说明：**
- 对大文件使用生成器以避免内存问题
- 可以在以下情况下自动检测格式指定 `into` 参数
- 某些对象可以写入多种格式
- 使用 `verify=False`

### 支持 stdin/stdout 管道### 8. 距离矩阵

使用统计方法创建和操作距离/相异矩阵。

* *关键功能：**
- 存储对称 (DistanceMatrix)或非对称 (DissimilarityMatrix)数据
- 基于 ID 的索引和切片
- 与多样性、排序和统计测试集成
- 读/写分隔文本格式

* *常见模式：**
```python
from skbio import DistanceMatrix
import numpy as np

# Create from array
data = np.array([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
dm = DistanceMatrix(data, ids=['A', 'B', 'C'])

# Access distances
dist_ab = dm['A', 'B']
row_a = dm['A']

# Read from file
dm = DistanceMatrix.read('distances.txt')

# Use in downstream analyses
pcoa_results = pcoa(dm)
permanova_results = permanova(dm, grouping)
```

* *重要说明：**
- 距离矩阵强制对称性和零对角线
- 相异矩阵允许不对称值
- ID 支持与元数据和生物知识集成
- 兼容 pandas、numpy 和 scikit-learn

### 9. 生物表

使用微生物组研究中常见的特征表（OTU/ASV 表）。

* *关键功能：**
- BIOM 格式 I/O（HDF5 和 JSON）
- 与集成pandas、polars、AnnData、numpy
- 数据增强技术（phylomix、mixup、组合方法）
- 样本/特征过滤和归一化
- 元数据集成

* *常见模式：**
```python
from skbio import Table

# Read BIOM table
table = Table.read('table.biom')

# Access data
sample_ids = table.ids(axis='sample')
feature_ids = table.ids(axis='observation')
counts = table.matrix_data

# Filter
filtered = table.filter(sample_ids_to_keep, axis='sample')

# Convert to/from pandas
df = table.to_dataframe()
table = Table.from_dataframe(df)
```

* *重要说明：**
- BIOM 表是 QIIME 2 工作流程中的标准
- 行通常表示样本，列表示特征（OTU/ASV）
- 支持稀疏和密集表示
- 输出格式可配置 (pandas/polars/numpy)

### 10. 蛋白质嵌入

使用蛋白质语言模型嵌入进行下游分析。

* *关键功能：**
- 存储来自蛋白质语言模型的嵌入（ESM、ProtTrans 等）
- 将嵌入转换为距离矩阵
- 生成排序对象以进行可视化
- 导出到 numpy/pandas 以用于 ML 工作流程

* *常见模式：**
```python
from skbio.embedding import ProteinEmbedding, ProteinVector

# Create embedding from array
embedding = ProteinEmbedding(embedding_array, sequence_ids)

# Convert to distance matrix for analysis
dm = embedding.to_distances(metric='euclidean')

# PCoA visualization of embedding space
pcoa_results = embedding.to_ordination(metric='euclidean', method='pcoa')

# Export for machine learning
array = embedding.to_array()
df = embedding.to_dataframe()
```

* *重要说明：**
- Embeddings 将蛋白质语言模型与传统生物信息学联系起来
- 与scikit-bio 的距离/排序/统计生态系统兼容
- SequenceEmbedding 和 ProteinEmbedding 提供专门的功能
- 用于序列聚类、分类和可视化

## 最佳实践

### 安装
```bash
uv pip install scikit-bio
```

### 性能注意事项
- 使用大型序列文件的生成器以最大程度地减少内存使用
- 对于大规模系统发育树，更喜欢 GME 或NJ
 上的 BME - Beta 多样性计算可以与 `partial_beta_diversity()`
 并行 - BIOM 格式 (HDF5)对于大型表而言比 JSON 更高效

### 与生态系统集成
- 序列通过标准格式与 Biopython 进行互操作
- 表与pandas、polars 和 AnnData
- 与 scikit-learn 兼容的距离矩阵
- 使用 matplotlib/seaborn/plotly 可视化的排序结果
- 与 QIIME 2 工件（BIOM、树、距离矩阵）无缝协作 

### 通用工作流程
1. **微生物组多样性分析**：读取BIOM表→计算α/β多样性→排序（PCoA）→统计测试（PERMANOVA）
2. **系统发育分析**：读取序列→对齐→构建距离矩阵→构建树→计算系统发育距离
3. **序列处理**：读取 FASTQ → 质量过滤器 → 修剪/清理 → 查找图案 → 翻译 → 写入 FASTA
4. **比较基因组学**：读取序列→配对比对→计算距离→构建树→分析进化枝

## 参考文档

有关详细的 API 信息、参数规范和高级使用示例，请参阅 `references/api_reference.md`，其中包含以下内容的综合文档：
- 所有功能的完整方法签名和参数
- 复杂工作流程的扩展代码示例
- 常见问题故障排除
- 性能优化技巧
- 与其他库的集成模式

## 其他资源

- 官方文档：https://scikit.bio/docs/latest/
- GitHub 存储库：https://github.com/scikit-bio/scikit-bio
- 论坛支持：https://forum.qiime2.org（scikit-bio 是 QIIME 2 生态系统的一部分）
