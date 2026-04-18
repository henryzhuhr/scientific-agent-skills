# 使用 Arboreto

## 进行基本 GRN 推断## 输入数据要求

Arboreto 需要两种格式之一的基因表达数据：

### Pandas DataFrame（推荐）
- **行**：观察结果（细胞、样本、条件）
- **列**：基因（以基因名称作为列）标题）
- **格式**：数值表达式值

示例：
```python
import pandas as pd

# Load expression matrix with genes as columns
expression_matrix = pd.read_csv('expression_data.tsv', sep='\t')
# Columns: ['gene1', 'gene2', 'gene3', ...]
# Rows: observation data
```

### NumPy Array
- **形状**：（观察值，基因）
- **要求**：单独提供基因名称列表匹配列顺序

示例：
```python
import numpy as np

expression_matrix = np.genfromtxt('expression_data.tsv', delimiter='\t', skip_header=1)
with open('expression_data.tsv') as f:
    gene_names = [gene.strip() for gene in f.readline().split('\t')]

assert expression_matrix.shape[1] == len(gene_names)
```

## 转录因子(TF)

可选地提供转录因子名称列表以限制调控推断：

```python
from arboreto.utils import load_tf_names

# Load from file (one TF per line)
tf_names = load_tf_names('transcription_factors.txt')

# Or define directly
tf_names = ['TF1', 'TF2', 'TF3']
```

如果未提供，则所有基因都被认为是潜在的ulators.

## 基本推理工作流程

### 使用 Pandas DataFrame

```python
import pandas as pd
from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load expression data
    expression_matrix = pd.read_csv('expression_data.tsv', sep='\t')

    # Load transcription factors (optional)
    tf_names = load_tf_names('tf_list.txt')

    # Run GRN inference
    network = grnboost2(
        expression_data=expression_matrix,
        tf_names=tf_names  # Optional
    )

    # Save results
    network.to_csv('network_output.tsv', sep='\t', index=False, header=False)
```

* *关键**：需要 `if __name__ == '__main__':` 防护，因为 Dask 在内部生成新进程。

### 使用 NumPy阵列

```python
import numpy as np
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load expression matrix
    expression_matrix = np.genfromtxt('expression_data.tsv', delimiter='\t', skip_header=1)

    # Extract gene names from header
    with open('expression_data.tsv') as f:
        gene_names = [gene.strip() for gene in f.readline().split('\t')]

    # Verify dimensions match
    assert expression_matrix.shape[1] == len(gene_names)

    # Run inference with explicit gene names
    network = grnboost2(
        expression_data=expression_matrix,
        gene_names=gene_names,
        tf_names=tf_names
    )

    network.to_csv('network_output.tsv', sep='\t', index=False, header=False)
```

## 输出格式

Arboreto 返回包含三列的 Pandas DataFrame：

|专栏 |描述|
|--------|-------------|
| `TF` |转录因子（调节因子）基因名称|
| `target` |目标基因名称|
| `importance` |监管重要性得分（越高=监管越强）|

示例输出：
```
TF1    gene5    0.856
TF2    gene12   0.743
TF1    gene8    0.621
```

## 设置随机种子

为了获得可重现的结果，请提供种子参数：

```python
network = grnboost2(
    expression_data=expression_matrix,
    tf_names=tf_names,
    seed=777
)
```

## 算法选择

大多数情况使用`grnboost2()`（更快，处理大数据集）：
```python
from arboreto.algo import grnboost2
network = grnboost2(expression_data=expression_matrix)
```

使用`genie3()`进行比较或特定要求：
```python
from arboreto.algo import genie3
network = genie3(expression_data=expression_matrix)
```

详细算法参见`references/algorithms.md`比较.
