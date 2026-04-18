# 基因组分词器

分词器将基因组区域转换为机器学习应用程序的离散标记，对于训练基因组深度学习模型特别有用。

## Python API

### 创建分词器

从各种来源加载分词器配置：

```python
import gtars

# From BED file
tokenizer = gtars.tokenizers.TreeTokenizer.from_bed_file("regions.bed")

# From configuration file
tokenizer = gtars.tokenizers.TreeTokenizer.from_config("tokenizer_config.yaml")

# From region string
tokenizer = gtars.tokenizers.TreeTokenizer.from_region_string("chr1:1000-2000")
```

### 分词基因组区域

将基因组坐标转换为令牌：

```python
# Tokenize a single region
token = tokenizer.tokenize("chr1", 1000, 2000)

# Tokenize multiple regions
tokens = []
for chrom, start, end in regions:
    token = tokenizer.tokenize(chrom, start, end)
    tokens.append(token)
```

### 令牌属性

访问令牌信息：

```python
# Get token ID
token_id = token.id

# Get genomic coordinates
chrom = token.chromosome
start = token.start
end = token.end

# Get token metadata
metadata = token.metadata
```

## 用例

### 机器学习预处理

Tokenizers对于为 ML 模型准备基因组数据至关重要：

1. **序列建模**：将基因组间隔转换为变压器模型
2的离散标记。 **位置编码**：跨数据集
3 创建一致的位置编码。 **数据增强**：生成用于训练的替代标记

#### 与geniml集成

标记器模块与基因组ML的geniml库无缝集成：

```python
# Tokenize regions for geniml
from gtars.tokenizers import TreeTokenizer
import geniml

tokenizer = TreeTokenizer.from_bed_file("training_regions.bed")
tokens = [tokenizer.tokenize(r.chrom, r.start, r.end) for r in regions]

# Use tokens in geniml models
model = geniml.Model(vocab_size=tokenizer.vocab_size)
```

## 配置格式

Tokenizer配置文件支持YAML格式：

```yaml
# tokenizer_config.yaml
type: tree
resolution: 1000  # Token resolution in base pairs
chromosomes:
  - chr1
  - chr2
  - chr3
options:
  overlap_handling: merge
  gap_threshold: 100
```

## 性能注意事项

- TreeTokenizer 使用高效的数据结构进行快速标记化
- 建议对大型数据集进行批量标记化
- 预加载标记化器可减少重复操作的开销
