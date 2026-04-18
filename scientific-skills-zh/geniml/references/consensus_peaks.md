# 共识峰：宇宙构建

## 概述

Geniml 提供了用于构建基因组“宇宙”的工具——来自 BED 文件集合的共识峰的标准化参考集。这些Universe代表基因组区域，其中分析的数据集显示出显着的覆盖范围重叠，用作标记化和分析的参考词汇表。

## 何时使用

在以下情况下使用共识峰创建：
- 从多个实验构建参考峰集
- 为Region2Vec或BEDspace标记化创建Universe文件
- 跨集合的标准化基因组区域数据集
- 定义具有统计显着性的感兴趣区域

## 工作流程

### 步骤 1：合并 BED 文件

将所有 BED 文件合并到单个组合文件中：

```bash
cat /path/to/bed/files/*.bed > combined_files.bed
```

### 步骤 2：生成覆盖轨迹

创建使用带有平滑窗口的uniwig进行bigWig覆盖跟踪：

```bash
uniwig -m 25 combined_files.bed chrom.sizes coverage/
```

* *参数：**
- `-m 25`：平滑窗口大小（染色质可及性的典型值为25bp）
- `chrom.sizes`：适合您的染色体大小文件基因组
- `coverage/`：bigWig 文件的输出目录

 平滑窗口有助于减少噪声并创建更稳健的峰边界。

### 步骤 3：构建宇宙

使用四种方法之一构建共识峰：

## 宇宙构建方法

### 1.覆盖截止 (CC)

使用固定覆盖阈值的最简单方法：

```bash
geniml universe build cc \
  --coverage-folder coverage/ \
  --output-file universe_cc.bed \
  --cutoff 5 \
  --merge 100 \
  --filter-size 50
```

* *参数：**
- `--cutoff`：覆盖阈值（1 = 并集；文件计数 = 交集）
- `--merge`：合并相邻峰值的距离(bp)
- `--filter-size`：包含的最小峰值大小 (bp)

* *在以下情况下使用：** 基于简单阈值的选择就足够了

### 2. 灵活覆盖截止值 (CCF)

在边界和区域核心的似然截止值附近创建置信区间：

```bash
geniml universe build ccf \
  --coverage-folder coverage/ \
  --output-file universe_ccf.bed \
  --cutoff 5 \
  --confidence 0.95 \
  --merge 100 \
  --filter-size 50
```

* *附加参数：**
- `--confidence`：灵活边界的置信水平 (0-1)

* *使用时间：** 应捕获峰值边界的不确定性

### 3. 最大似然 (ML)

构建考虑区域的概率模型开始/结束位置：

```bash
geniml universe build ml \
  --coverage-folder coverage/ \
  --output-file universe_ml.bed \
  --merge 100 \
  --filter-size 50 \
  --model-type gaussian
```

* *参数：**
- `--model-type`：似然估计分布（高斯、泊松）

* *使用时间：**峰值位置的统计建模很重要

### 4. 隐马尔可夫模型(HMM)

将基因组区域建模为隐藏状态，覆盖范围作为发射：

```bash
geniml universe build hmm \
  --coverage-folder coverage/ \
  --output-file universe_hmm.bed \
  --states 3 \
  --merge 100 \
  --filter-size 50
```

* *参数：**
- `--states`：HMM 隐藏状态的数量（通常为 2-5）

* *何时使用：** 基因组状态的复杂模式应该是capture

## Python API

```python
from geniml.universe import build_universe

# Build using coverage cutoff method
universe = build_universe(
    coverage_folder='coverage/',
    method='cc',
    cutoff=5,
    merge_distance=100,
    min_size=50,
    output_file='universe.bed'
)
```

## 方法比较

|方法|复杂性 |灵活性 |计算成本|最适合|
|--------|------------|------------|--------------------|----------|
|抄送 |低|低|低|快速参考集|
| CCF |中等|中等|中等|边界不确定性|
|机器学习 |高|高|高|统计严谨性|
|嗯|高|高|非常高 |复杂模式 |

## 最佳实践

### 选择方法

1. **从 CC 开始**：快速且可解释的初步探索 
2. **使用 CCF**：当峰边界不确定或有噪声时 
3. **应用 ML**：用于出版质量的统计分析
4. **部署 HMM**：对复杂染色质状态进行建模时

### 参数选择

* *覆盖范围截止：**
- `cutoff = 1`：所有峰的并集（最宽松）
- `cutoff = n_files`：交集（最严格）
- `cutoff = 0.5 * n_files`：中等一致性（典型选择）

* *合并距离：**
- ATAC-seq：100-200bp
- ChIP-seq（窄峰）：50-100bp
- ChIP-seq（宽峰）： 500-1000bp

* *过滤器大小：**
- 最小 30bp，以避免伪影 
- 对于大多数检测来说通常为 50-100bp
- 较大，用于广泛的组蛋白标记

### 质量控制

构建后，评估宇宙质量：

```python
from geniml.evaluation import assess_universe

metrics = assess_universe(
    universe_file='universe.bed',
    coverage_folder='coverage/',
    bed_files='bed_files/'
)

print(f"Number of regions: {metrics['n_regions']}")
print(f"Mean region size: {metrics['mean_size']:.1f}bp")
print(f"Coverage of input peaks: {metrics['coverage']:.1%}")
```

* *关键指标：**
- **区域计数**：应捕获主要特征而不产生过多碎片
- **大小分布**：应匹配预期生物学（例如 ATAC-seq 约为 500bp）
- **输入覆盖率**：表示的原始峰的比例（通常 >80%）

## 输出格式

共识峰保存为包含三个必需列的 BED 文件：

```
chr1    1000    1500
chr1    2000    2800
chr2    500     1000
```

 其他列可能包括置信度分数或状态注释，具体取决于方法。

## 常见工作流程

### 对于 Region2Vec

1. 使用首选方法 
2 构建 Universe。使用 Universe 作为标记化参考
3. 对 BED 文件进行标记 
4. 训练 Region2Vec 模型

### 对于 BEDspace

1. 从所有数据集
2 构建宇宙。在预处理步骤
3中使用universe。使用元数据
4 训练 BEDspace。跨区域和标签查询

### 对于scEmbed

1. 从批量或聚合的 scATAC-seq
2 创建 Universe。用于单元标记化
3. 训练 scEmbed 模型
4. 生成单元嵌入

## 故障排除

* *区域太少：**降低截止阈值或减小滤波器大小

* *区域太多：**提高截止阈值，增加合并距离，或增加滤波器大小

* *噪声边界：**使用CCF或ML方法而不是CC

* *长计算：**从CC 方法可快速获得结果，然后根据需要使用 ML/HMM 进行细化
