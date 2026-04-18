# Matchms 相似性函数参考

本文档提供了有关matchms中可用的所有相似性评分方法的详细信息。

## 概述

Matchms 提供了用于比较质谱的多种相似性函数。使用 `calculate_scores()` 计算参考谱和查询谱集合之间的成对相似性。

```python
from matchms import calculate_scores
from matchms.similarity import CosineGreedy

scores = calculate_scores(references=library_spectra,
                         queries=query_spectra,
                         similarity_function=CosineGreedy())
```

## 基于峰的相似性函数

这些函数根据峰模式（m/z 和强度值）比较质谱。

### CosineGreedy

* *说明**：计算使用快速贪婪匹配算法在两个光谱之间进行余弦相似度。峰在指定的容差内进行匹配，并根据匹配的峰强度计算相似性。

* *何时使用**：
- 大型数据集的快速相似性计算
- 通用光谱匹配
- 当速度优先于数学最佳匹配时

* *参数**：
- `tolerance`（浮点型，默认 = 0.1）：峰匹配的最大 m/z 差异（道尔顿）
- `mz_power`（浮点型，默认 = 0.0）：m/z 加权的指数（0 = 无加权）
- `intensity_power`（浮点型，默认 = 1.0）：强度指数加权

* *示例**：
```python
from matchms.similarity import CosineGreedy

similarity_func = CosineGreedy(tolerance=0.1, mz_power=0.0, intensity_power=1.0)
scores = calculate_scores(references, queries, similarity_func)
```

* *输出**：0.0和1.0之间的相似度得分，加上匹配峰值的数量。

- --

### CosineHungarian

* *描述**：使用计算余弦相似度用于最佳峰值匹配的匈牙利算法。提供数学上最佳的峰值分配，但比 CosineGreedy 慢。

* *何时使用**：
- 需要最佳峰值匹配时
- 高质量参考库比较
- 需要可重复、数学上严格的结果的研究

* *参数**：
- `tolerance`（浮点型，默认=0.1）：峰匹配的最大 m/z 差异
- `mz_power`（浮点型，默认=0.0）：m/z 加权的指数
- `intensity_power`（浮点型，默认=1.0）：强度指数加权

* *示例**：
```python
from matchms.similarity import CosineHungarian

similarity_func = CosineHungarian(tolerance=0.1)
scores = calculate_scores(references, queries, similarity_func)
```

* *输出**：0.0和1.0之间的最佳相似度得分，加上匹配的峰值。

* *注意**：比CosineGreedy慢；用于较小的数据集或当准确性至关重要时。

- --

### ModifiedCosine

* *描述**：通过考虑前体 m/z 差异来扩展余弦相似度。根据前体质量之间的差异应用质量转移后允许峰匹配。用于比较相关化合物（同位素、加合物、类似物）的光谱。

* *何时使用**：
- 比较不同前体质量的光谱
- 识别结构类似物或衍生物
- 交叉电离模式比较
- 当前体质量差异为

* *参数**：
- `tolerance`（浮点型，默认=0.1）：移位后峰匹配的最大 m/z 差异
- `mz_power`（浮点型，默认=0.0）：m/z 加权的指数
- `intensity_power` （浮点，默认=1.0）：强度加权指数

* *示例**：
```python
from matchms.similarity import ModifiedCosine

similarity_func = ModifiedCosine(tolerance=0.1)
scores = calculate_scores(references, queries, similarity_func)
```

* *要求**：两个光谱必须具有有效的前体_mz元数据。

- --

### NeutralLossesCosine

* *描述**：根据中性损失模式而不是片段 m/z 值计算相似性。中性损失是通过从前体 m/z 中减去片段 m/z 得出的。对于识别具有相似碎片模式的化合物特别有用。

* *何时使用**：
- 比较不同前体质量的碎片模式
- 识别具有相似中性损失谱的化合物
- 与常规余弦评分互补
- 代谢物识别和分类

* *参数**：
- `tolerance` (float, default=0.1): 匹配的最大中性损失差
- `mz_power` (float, default=0.0): 损失值加权的指数
- `intensity_power` (float, default=1.0): 强度指数加权

* *示例**：
```python
from matchms.similarity import NeutralLossesCosine
from matchms.filtering import add_losses

# First add losses to spectra
spectra_with_losses = [add_losses(s) for s in spectra]

similarity_func = NeutralLossesCosine(tolerance=0.1)
scores = calculate_scores(references_with_losses, queries_with_losses, similarity_func)
```

* *要求**：
- 两个光谱必须具有有效的前体_mz元数据
- 在评分之前使用`add_losses()`滤波器计算中性损失

- --

## 结构相似性函数

这些函数比较分子结构而不是光谱峰。

### FingerprintSimilarity

* *描述**：计算源自化学结构（SMILES或InChI）的分子指纹之间的相似性。支持多种指纹类型和相似性指标。

* *何时使用**：
- 无光谱数据的结构相似性
- 结合结构和光谱相似性
- 光谱匹配前预过滤候选
- 结构-活性关系研究

* *参数**：
- `fingerprint_type` (str, default="daylight")：指纹类型
  - `"daylight"`：日光指纹
  - `"morgan1"`、`"morgan2"`、`"morgan3"`：半径为1、2或3的摩根指纹
- `similarity_measure` (str, default="jaccard")：相似度度量
  - `"jaccard"`：杰卡德索引（交集/并集）
  - `"dice"`：骰子系数（2 * 交集/（size1 + size2））
  - `"cosine"`：余弦相似性

* *示例**：
```python
from matchms.similarity import FingerprintSimilarity
from matchms.filtering import add_fingerprint

# Add fingerprints to spectra
spectra_with_fps = [add_fingerprint(s, fingerprint_type="morgan2", nbits=2048)
                    for s in spectra]

similarity_func = FingerprintSimilarity(similarity_measure="jaccard")
scores = calculate_scores(references_with_fps, queries_with_fps, similarity_func)
```

* *要求**：
- Spectra 必须具有有效的 SMILES 或 InChI 元数据
- 使用 `add_fingerprint()` 过滤器计算指纹
- 要求rdkit 库

- --

## 基于元数据的相似性函数

这些函数比较元数据字段而不是光谱或结构数据。

### MetadataMatch

* *描述**：比较光谱之间用户定义的元数据字段。支持分类数据的精确匹配和数值数据的基于公差的匹配。

* *何时使用**：
- 按实验条件（碰撞能量、保留时间）过滤
- 仪器特定匹配
- 将元数据约束与光谱相似性相结合
- 基于自定义元数据过滤

* *参数**：
- `field` (str)：要比较的元数据字段名称
- `matching_type` (str, default="exact")：匹配方法
  - `"exact"`：精确字符串/值匹配
  - `"difference"`：数值的绝对差值
  - `"relative_difference"`：数值的相对差值
- `tolerance`（浮点型，可选）：数值匹配的最大差值

* *示例（精确）匹配）**：
```python
from matchms.similarity import MetadataMatch

# Match by instrument type
similarity_func = MetadataMatch(field="instrument_type", matching_type="exact")
scores = calculate_scores(references, queries, similarity_func)
```

* *示例（数字匹配）**：
```python
# Match retention time within 0.5 minutes
similarity_func = MetadataMatch(field="retention_time",
                                matching_type="difference",
                                tolerance=0.5)
scores = calculate_scores(references, queries, similarity_func)
```

* *输出**：返回1.0（匹配）或0.0（不匹配）以进行精确匹配。对于数值匹配，根据差异返回相似度分数。

- --

### PrecursorMzMatch

* *说明**：基于前体 m/z 值的二进制匹配。根据前体质量是否在指定容差范围内匹配，返回 True/False。

* *何时使用**：
- 按前体质量预过滤谱库
- 基于质量的快速候选选择
- 与其他相似性度量相结合
- 同量异位化合物识别

* *参数**：
- `tolerance`（浮点型，默认=0.1）：匹配的最大m/z差值
- `tolerance_type`（str，默认=“道尔顿”）：公差单位
  - `"Dalton"`：绝对质量差异
  - `"ppm"`：百万分之一（相对）

* *示例**：
```python
from matchms.similarity import PrecursorMzMatch

# Match precursor within 0.1 Da
similarity_func = PrecursorMzMatch(tolerance=0.1, tolerance_type="Dalton")
scores = calculate_scores(references, queries, similarity_func)

# Match precursor within 10 ppm
similarity_func = PrecursorMzMatch(tolerance=10, tolerance_type="ppm")
scores = calculate_scores(references, queries, similarity_func)
```

* *输出**：1.0（匹配）或0.0（不匹配）

* *要求**：两个光谱都必须具有有效的前体_mz元数据.

- --

### ParentMassMatch

* *描述**：基于父质量（中性质量）值的二进制匹配。与 PrecursorMzMatch 类似，但使用计算的母体质量而不是前体 m/z。

* *何时使用**：
- 比较不同电离模式的光谱
- 与加合物无关的匹配
- 基于中性质量的库搜索

* *参数**：
- `tolerance`（float，默认=0.1）：匹配的最大质量差
- `tolerance_type`（str，默认=“Dalton”）：公差单位（“Dalton”或“ppm”）

* *示例**：
```python
from matchms.similarity import ParentMassMatch

similarity_func = ParentMassMatch(tolerance=0.1, tolerance_type="Dalton")
scores = calculate_scores(references, queries, similarity_func)
```

* *输出**： 1.0（匹配）或0.0（不匹配）

* *要求**：两个谱图都必须具有有效的parent_mass元数据。

- --

## 组合多个相似性函数

组合多个相似性度量以进行稳健的化合物识别：

```python
from matchms import calculate_scores
from matchms.similarity import CosineGreedy, ModifiedCosine, FingerprintSimilarity

# Calculate multiple similarity scores
cosine_scores = calculate_scores(refs, queries, CosineGreedy())
modified_cosine_scores = calculate_scores(refs, queries, ModifiedCosine())
fingerprint_scores = calculate_scores(refs, queries, FingerprintSimilarity())

# Combine scores with weights
for i, query in enumerate(queries):
    for j, ref in enumerate(refs):
        combined_score = (0.5 * cosine_scores.scores[j, i] +
                         0.3 * modified_cosine_scores.scores[j, i] +
                         0.2 * fingerprint_scores.scores[j, i])
```

## 访问分数结果

`Scores`对象提供多种方法来访问结果：

```python
# Get best matches for a query
best_matches = scores.scores_by_query(query_spectrum, sort=True)[:10]

# Get scores as numpy array
score_array = scores.scores

# Get scores as pandas DataFrame
import pandas as pd
df = scores.to_dataframe()

# Filter by threshold
high_scores = [(i, j, score) for i, j, score in scores.to_list() if score > 0.7]

# Save scores
scores.to_json("scores.json")
scores.to_pickle("scores.pkl")
```

## 性能注意事项

* *快速方法**（大型数据集）：
- CosineGreedy
- PrecursorMzMatch
- ParentMassMatch

* *慢方法**（较小的数据集或高精度）：
- CosineHungarian
- ModifiedCosine（比 CosineGreedy 慢）
- NeutralLossesCosine
- FingerprintSimilarity（需要指纹计算）

* *建议**：对于大规模库搜索，使用 PrecursorMzMatch 预过滤候选，然后应用 CosineGreedy 或 ModifiedCosine 过滤结果。

## 常见相似度工作流程

### 标准库匹配
```python
from matchms.similarity import CosineGreedy

scores = calculate_scores(library_spectra, query_spectra,
                         CosineGreedy(tolerance=0.1))
```

### 多指标匹配
```python
from matchms.similarity import CosineGreedy, ModifiedCosine, FingerprintSimilarity

# Spectral similarity
cosine = calculate_scores(refs, queries, CosineGreedy())
modified = calculate_scores(refs, queries, ModifiedCosine())

# Structural similarity
fingerprint = calculate_scores(refs, queries, FingerprintSimilarity())
```

### 前体过滤匹配
```python
from matchms.similarity import PrecursorMzMatch, CosineGreedy

# First filter by precursor mass
mass_filter = calculate_scores(refs, queries, PrecursorMzMatch(tolerance=0.1))

# Then calculate cosine only for matching precursors
cosine_scores = calculate_scores(refs, queries, CosineGreedy())
```

## 进一步阅读

For详细的API文档、参数说明、数学公式请参见：
https://matchms.readthedocs.io/en/latest/api/matchms.similarity.html
