# Geniml 实用程序和其他工具

## BBClient：BED 文件缓存

### 概述

BBClient 提供来自远程源的 BED 文件的高效缓存，从而实现更快的重复访问以及与 R 工作流程的集成。

### 何时使用

在以下情况下使用 BBClient：
- 重复从远程数据库访问 BED 文件
- 使用 BEDbase 存储库
- 将基因组数据与 R 管道集成
- 需要本地缓存以提高性能

### Python 用法

```python
from geniml.bbclient import BBClient

# Initialize client
client = BBClient(cache_folder='~/.bedcache')

# Fetch and cache BED file
bed_file = client.load_bed(bed_id='GSM123456')

# Access cached file
regions = client.get_regions('GSM123456')
```

### R集成

```r
library(reticulate)
geniml <- import("geniml.bbclient")

# Initialize client
client <- geniml$BBClient(cache_folder='~/.bedcache')

# Load BED file
bed_file <- client$load_bed(bed_id='GSM123456')
```

### 最佳实践

- 配置具有足够存储空间的缓存目录
- 在分析中使用一致的缓存位置
- 定期清除缓存以删除未使用的文件

- --

## BEDshift：BED 文件随机化

### 概述

BEDshift 提供用于随机化 BED 文件同时保留基因组背景的工具，这对于生成零分布和统计测试至关重要。

### 何时使用

在以下情况下使用 BEDshift：
- 创建用于统计测试的零模型
- 生成控制数据集
- 评估基因组重叠的显着性
- 基准分析方法

### 使用

```python
from geniml.bedshift import bedshift

# Randomize BED file preserving chromosome distribution
randomized = bedshift(
    input_bed='peaks.bed',
    genome='hg38',
    preserve_chrom=True,
    n_iterations=100
)
```

### CLI 使用

```bash
geniml bedshift \
  --input peaks.bed \
  --genome hg38 \
  --preserve-chrom \
  --iterations 100 \
  --output randomized_peaks.bed
```

### 随机化策略

* *保留染色体分布：**
```python
bedshift(input_bed, genome, preserve_chrom=True)
```
维持与原始染色体相同的区域。

* *保留距离分布：**
```python
bedshift(input_bed, genome, preserve_distance=True)
```
维持区域间距离。

* *保留区域大小：**
```python
bedshift(input_bed, genome, preserve_size=True)
```
 保持原始区域长度。

### 最佳实践

- 选择匹配零假设的随机化策略
- 生成稳健统计的多次迭代
- 验证随机输出保持所需的属性
- 记录以下的随机化参数重现性

- --

## 评估：模型评估工具

### 概述

Geniml 提供用于评估嵌入质量和模型性能的评估实用程序。

### 何时使用

在以下情况下使用评估工具：
- 验证经过训练的嵌入
- 比较不同模型
- 评估聚类质量
- 发布模型结果

### 嵌入评估

```python
from geniml.evaluation import evaluate_embeddings

# Evaluate Region2Vec embeddings
metrics = evaluate_embeddings(
    embeddings_file='region2vec_model/embeddings.npy',
    labels_file='metadata.csv',
    metrics=['silhouette', 'davies_bouldin', 'calinski_harabasz']
)

print(f"Silhouette score: {metrics['silhouette']:.3f}")
print(f"Davies-Bouldin index: {metrics['davies_bouldin']:.3f}")
```

### 聚类指标

* *轮廓得分：** 衡量簇内聚力和分离度（-1 到 1，越高越好）

* *Davies-Bouldin 指数：** 簇之间的平均相似度（≥0，越低越好）

* *Calinski-Harabasz分数：** 簇间/簇内分散度比率（越高越好）

### scEmbed 单元格类型注释评估

```python
from geniml.evaluation import evaluate_annotation

# Evaluate cell-type predictions
results = evaluate_annotation(
    predicted=adata.obs['predicted_celltype'],
    true=adata.obs['true_celltype'],
    metrics=['accuracy', 'f1', 'confusion_matrix']
)

print(f"Accuracy: {results['accuracy']:.1%}")
print(f"F1 score: {results['f1']:.3f}")
```

### 最佳实践

- 使用多个互补指标
- 与基线模型进行比较
- 报告保留测试的指标data
- 可视化嵌入 (UMAP/t-SNE)以及指标

- --

## 标记化：区域标记化实用程序

### 概述

Tokenization 使用参考宇宙将基因组区域转换为离散标记，从而实现 word2vec 式训练。

### 何时使用

标记化是以下各项所需的预处理步骤：
- Region2Vec训练
- scEmbed模型训练
- 任何需要离散标记的嵌入方法

### 硬标记化

严格基于重叠标记化：

```python
from geniml.tokenization import hard_tokenization

hard_tokenization(
    src_folder='bed_files/',
    dst_folder='tokenized/',
    universe_file='universe.bed',
    p_value_threshold=1e-9
)
```

* *参数：**
- `p_value_threshold`：重叠的显着性级别（通常为 1e-9 或 1e-6）

### 软标记化

允许部分的概率标记化匹配：

```python
from geniml.tokenization import soft_tokenization

soft_tokenization(
    src_folder='bed_files/',
    dst_folder='tokenized/',
    universe_file='universe.bed',
    overlap_threshold=0.5
)
```

* *参数：**
- `overlap_threshold`：最小重叠分数 (0-1)

### 基于宇宙的标记化

使用自定义将区域映射到宇宙标记参数：

```python
from geniml.tokenization import universe_tokenization

universe_tokenization(
    bed_file='peaks.bed',
    universe_file='universe.bed',
    output_file='tokens.txt',
    method='hard',
    threshold=1e-9
)
```

### 最佳实践

- **宇宙质量**：使用全面、结构良好的宇宙
- **阈值选择**：更严格（较低的p值）以获得更高的置信度
- **验证**：检查标记化覆盖率（标记化的区域百分比）
- **一致性**：在相关分析中使用相同的宇宙和参数

### 标记化覆盖范围

检查区域标记化的效果：

```python
from geniml.tokenization import check_coverage

coverage = check_coverage(
    bed_file='peaks.bed',
    universe_file='universe.bed',
    threshold=1e-9
)

print(f"Tokenization coverage: {coverage:.1%}")
```

目标为> 80％的覆盖率进行可靠的训练。

- --

## Text2BedNN：搜索后端

### 概述

Text2BedNN为以下内容创建基于神经网络的搜索后端使用自然语言或元数据查询基因组区域。

### 何时使用

在以下情况下使用 Text2BedNN：
- 为基因组数据库构建搜索界面
- 对 BED 文件启用自然语言查询
- 创建元数据感知搜索系统
- 部署交互式基因组搜索应用程序

### 工作流程

* *步骤1：准备嵌入**

使用元数据训练BEDspace或Region2Vec模型。

* *步骤2：构建搜索索引**

```python
from geniml.search import build_search_index

build_search_index(
    embeddings_file='bedspace_model/embeddings.npy',
    metadata_file='metadata.csv',
    output_dir='search_backend/'
)
```

* *步骤3：查询索引**

```python
from geniml.search import SearchBackend

backend = SearchBackend.load('search_backend/')

# Natural language query
results = backend.query(
    text="T cell regulatory regions",
    top_k=10
)

# Metadata query
results = backend.query(
    metadata={'cell_type': 'T_cell', 'tissue': 'blood'},
    top_k=10
)
```

### 最佳实践

- 使用丰富的元数据训练嵌入以实现更好的搜索
- 索引大型集合以实现全面覆盖
- 验证已知查询的搜索相关性
- 使用 API 进行部署以进行交互应用程序

- --

## 附加工具

### I/O 实用程序

```python
from geniml.io import read_bed, write_bed, load_universe

# Read BED file
regions = read_bed('peaks.bed')

# Write BED file
write_bed(regions, 'output.bed')

# Load universe
universe = load_universe('universe.bed')
```

### 模型实用程序

```python
from geniml.models import save_model, load_model

# Save trained model
save_model(model, 'my_model/')

# Load model
model = load_model('my_model/')
```

### 通用模式

* *管道工作流程：**
```python
# 1. Build universe
universe = build_universe(coverage_folder='coverage/', method='cc', cutoff=5)

# 2. Tokenize
hard_tokenization(src_folder='beds/', dst_folder='tokens/',
                   universe_file='universe.bed', p_value_threshold=1e-9)

# 3. Train embeddings
region2vec(token_folder='tokens/', save_dir='model/', num_shufflings=1000)

# 4. Evaluate
metrics = evaluate_embeddings(embeddings_file='model/embeddings.npy',
                               labels_file='metadata.csv')
```

这种模块化设计允许灵活组合geniml工具，用于不同的基因组ML工作流程。
