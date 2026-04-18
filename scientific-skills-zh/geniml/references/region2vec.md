# Region2Vec：基因组区域嵌入

## 概述

Region2Vec 从 BED 文件生成基因组区域和区域集的无监督嵌入。它将基因组区域映射到词汇表，通过串联创建句子，并应用 word2vec 训练来学习有意义的表示。

## 何时使用

在处理以下内容时使用 Region2Vec：
- 需要降维的 BED 文件集合
- 基因组区域相似性分析
- 需要区域特征向量的下游 ML 任务
- 跨多个基因组数据集的比较分析

## 工作流程

### 步骤 1：准备数据

在源文件夹中收集 BED 文件。可以选择指定文件列表（默认使用目录中的所有文件）。准备一个 Universe 文件作为标记化的参考词汇。

### 步骤 2：标记化

运行硬标记化，将基因组区域转换为标记：

```python
from geniml.tokenization import hard_tokenization

src_folder = '/path/to/raw/bed/files'
dst_folder = '/path/to/tokenized_files'
universe_file = '/path/to/universe_file.bed'

hard_tokenization(src_folder, dst_folder, universe_file, 1e-9)
```

 最终参数 (1e-9)是标记化重叠重要性的 p 值阈值。

### 步骤 3：训练Region2Vec模型

在标记化文件上执行Region2Vec训练：

```python
from geniml.region2vec import region2vec

region2vec(
    token_folder=dst_folder,
    save_dir='./region2vec_model',
    num_shufflings=1000,
    embedding_dim=100,
    context_len=50,
    window_size=5,
    init_lr=0.025
)
```

## 关键参数

|参数|描述 |典型范围|
|---------|--------------|---------------|
| `init_lr` |初始学习率| 0.01 - 0.05 |
| `window_size` |上下文窗口大小 | 3 - 10 |
| `num_shufflings` |洗牌迭代次数| 500 - 2000 |
| `embedding_dim` |输出嵌入的维度 | 50 - 300 |
| `context_len` |训练的上下文长度| 30 - 100 |

## CLI 用法

```bash
geniml region2vec --token-folder /path/to/tokens \
  --save-dir ./region2vec_model \
  --num-shuffle 1000 \
  --embed-dim 100 \
  --context-len 50 \
  --window-size 5 \
  --init-lr 0.025
```

## 最佳实践

- **参数调整**：经常调整 `init_lr`、`window_size`、`num_shufflings` 和 `embedding_dim`，以获得特定数据集上的最佳性能
- **Universe 文件**：使用涵盖分析中所有感兴趣区域的综合 Universe 文件
- **验证**：在继续之前始终验证标记化输出训练
- **资源**：训练可能是计算密集型的；监控大型数据集的内存使用情况

## 输出

训练后的模型保存可用于以下目的的嵌入：
- 跨基因组区域的相似性搜索
- 聚类区域集
- 下游ML任务的特征向量
- 通过降维进行可视化（t-SNE， UMAP)
