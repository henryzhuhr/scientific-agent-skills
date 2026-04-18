# PyDESeq2 API 参考

本文档提供了 PyDESeq2 类、方法和实用程序的全面 API 参考。

## 核心类

### DeseqDataSet

差异表达分析的主类，处理从归一化到对数倍变化拟合的数据处理。

* *用途：**实现分散和记录 RNA-seq 计数数据的折叠变化（LFC）估计。

* *初始化参数：**
- `counts`：包含非负整数读取计数的形状（样本×基因）的 pandas 数据帧
- `metadata`：带有样本注释的形状（样本×变量）的 pandas 数据帧
- `design`：str，指定统计模型的 Wilkinson 公式（例如“~condition”、“~group + condition”） 
- `refit_cooks`：bool，去除 Cook 距离异常值后是否重新拟合参数（默认：True） 
- `n_cpus`：int，用于并行处理的 CPU 数量（可选）
- `quiet`：bool，抑制进度消息（默认值：False）

* *关键方法：**

#### `deseq2()`
运行完整的DESeq2管道进行归一化和色散/LFC拟合。

* *步骤执行：**
1. 计算归一化因子（尺寸因子）
2. 拟合 Genewise 分散体
3. 拟合离散趋势曲线
4. 计算色散先验
5. 拟合 MAP（最大后验）离散度 
6. 适合原木折叠变化
7. 计算异常值检测的库克距离
8. 如果 `refit_cooks=True`

  * *返回：** None（就地修改对象）

#### `to_picklable_anndata()`
将 DeseqDataSet 转换为可以用 pickle 保存的 AnnData 对象。

 * *返回：** AnnData 对象包含：
- `X`：计数数据矩阵
- `obs`：样本级元数据 (1D)
- `var`：基因级元数据 (1D)
- `varm`：基因级多维数据（例如，LFC估计）

* *用法：**
```python
import pickle
with open("result_adata.pkl", "wb") as f:
    pickle.dump(dds.to_picklable_anndata(), f)
```

* *属性（运行deseq2()后）：**
- `layers`：包含各种矩阵（归一化计数等）的字典 
- `varm`：包含基因级结果的字典（对数倍数变化、离散度、等）
- `obsm`：包含样本级别信息的字典
- `uns`：包含全局参数的字典

- --

### DeseqStats

用于执行统计测试和计算差异表达的p值的类。

* *用途：**使用 Wald 测试和可选的 LFC 收缩促进 PyDESeq2 统计测试。

* *初始化参数：**
- `dds`：已使用 `deseq2()`
- `contrast` 处理的 DeseqDataSet 对象：列表或无，指定对比度测试
  - 格式：`[variable, test_level, reference_level]`
  - 示例：`["condition", "treated", "control"]` 测试与对照进行处理
  - 如果无，则使用设计公式中的最后一个系数
- `alpha`：浮点数，独立过滤的显着性阈值（默认值：0.05）
- `cooks_filter`：bool，是否根据Cook距离过滤异常值（默认：True） 
- `independent_filter`：bool，是否进行独立过滤（默认：True） 
- `n_cpus`：int，并行处理的CPU数量（可选）
- `quiet`：bool，抑制进度消息（默认值：False）

* *关键方法：**

#### `summary()`
运行 Wald 测试并计算 p 值和调整的 p 值。

* *执行的步骤：**
1. 对指定的对比度
2 运行 Wald 统计检验。可选库克距离过滤
3. 可选独立滤波去除低功耗测试
4. 多重测试校正（Benjamini-Hochberg 程序）

* *返回：** 无（结果存储在 `results_df` 属性中）

* *结果数据帧列：**
- `baseMean`：所有样本的平均标准化计数
- `log2FoldChange`：条件之间的log2倍数变化
- `lfcSE`：log2倍数变化的标准误差
- `stat`：Wald检验statistic
- `pvalue`：原始 p 值
- `padj`：调整后的 p 值（FDR 校正）

#### `lfc_shrink(coeff=None)`
使用 apeGLM 方法应用收缩来记录倍数变化。

* *用途：** 减少LFC 估计中的噪声，以实现更好的可视化和排名，特别是对于计数较低或变异性较高的基因。

* *参数：**
- `coeff`：str 或 None，要收缩的系数名称（如果 None，则使用对比度中的系数）

* *重要：** 收缩仅适用于可视化/排名目的。统计测试结果（p 值，调整后的 p 值）保持不变。

* *返回：**无（使用缩小的 LFC 更新 `results_df`）

* *属性：**
- `results_df`：包含测试结果的 pandas DataFrame（在之后可用） `summary()`)

- --

## 实用函数

### `pydeseq2.utils.load_example_data(modality="single-factor")`

加载用于测试和教程的合成示例数据集。

* *参数：**
- `modality`：str，或者“单因素”或“多因素”

* *返回：**（counts_df，metadata_df）的元组
- `counts_df`：带有合成计数数据的pandas DataFrame
- `metadata_df`：带有样本的pandas DataFrame注释

- --

## 预处理模块

`pydeseq2.preprocessing`模块提供数据准备的实用工具。

* *常用操作：**
- 基于最小读取计数的基因过滤
- 基于元数据标准的样本过滤
- 数据转换和归一化

- --

## 推理类

### Inference
抽象基类，定义DESeq2相关推理方法的接口。

### DefaultInference
使用 scipy、sklearn 和 numpy 推理方法的默认实现。

* *目的：** 提供数学实现：
- GLM（广义线性模型）拟合
- 色散估计
- 趋势曲线拟合
- 统计测试

- --

## 数据结构要求

### 计数矩阵
- **形状：**（样本×基因）
- **类型：** pandas DataFrame
- **值：** 非负整数（原始读取计数）
- **索引：**样本标识符（必须匹配元数据索引）
- **列：** 基因标识符

### 元数据
- **形状：**（样本×变量）
- **类型：** pandas DataFrame
- **索引：** 样本标识符（必须匹配计数矩阵索引）
- **列：** 实验因素（例如“条件”、“批次”、“组”）
- **值：** 设计公式中使用的分类或连续变量

### 重要说明
- 样本顺序必须在计数和元数据之间匹配
- 应在分析之前处理元数据中的缺失值
- 基因名称应该是唯一的
- 计数文件经常需要换位：`counts_df = counts_df.T`

- --

## 通用工作流程模式

```python
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# 1. Initialize dataset
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True
)

# 2. Fit dispersions and LFCs
dds.deseq2()

# 3. Perform statistical testing
ds = DeseqStats(
    dds,
    contrast=["condition", "treated", "control"],
    alpha=0.05
)
ds.summary()

# 4. Optional: Shrink LFCs for visualization
ds.lfc_shrink()

# 5. Access results
results = ds.results_df
```

- --

## 版本兼容性

PyDESeq2旨在匹配默认设置DESeq2 v1.34.0。可能存在一些差异，因为它是 Python 中的从头开始重新实现。

* *测试使用：**
- Python 3.10-3.11
- anndata 0.8.0+
- numpy 1.23.0+
- pandas 1.4.3+
- scikit-learn 1.1.1+
- scipy 1.11.0+
