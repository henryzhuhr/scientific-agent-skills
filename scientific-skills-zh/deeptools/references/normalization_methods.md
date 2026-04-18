# deepTools 标准化方法

本文档解释了 deepTools 中可用的各种标准化方法以及何时使用每种方法。

## 为什么标准化？

标准化对于：
1 至关重要。 **比较不同测序深度的样本**
2. **考虑库大小差异**
3. **使覆盖率值在实验中可解释**
4. **实现条件之间的公平比较**

在没有标准化的情况下，即使真实的生物信号相同，具有 1 亿个读数的样本似乎也比具有 5000 万个读数的样本具有更高的覆盖率。

- --

## 可用的标准化方法

### 1. RPKM（映射的每千碱基读数）读取）

* *公式：** `(Number of reads) / (Length of region in kb × Total mapped reads in millions)`

* *何时使用：**
- 比较同一样本中的不同基因组区域
- 调整测序深度和区域长度
- RNA-seq基因表达分析

* *适用于：** `bamCoverage`

* *示例：**
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing RPKM
```

* *解释：** RPKM 为 10 表示每百万映射读取中每千碱基特征有 10 个读取。

* *优点：**
- 同时考虑区域长度和库大小
- 在基因组学中广泛使用和理解

* *缺点：**
- 如果总RNA含量不同，则不适合在样品之间进行比较
- 在比较具有非常不同成分的样品时可能会产生误导

- --

### 2. CPM（每百万映射计数）读取）

* *公式：** `(Number of reads) / (Total mapped reads in millions)`

* *也称为：** RPM（每百万读取数）

* *何时使用：**
- 比较不同样本中的相同基因组区域
- 当区域长度恒定或不相关时
- ChIP-seq， ATAC-seq、DNase-seq 分析

* *适用于：** `bamCoverage`、`bamCompare`

* *示例：**
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing CPM
```

* *解释：** CPM 为 5 表示每百万个映射读取中有 5 个读取bin.

* *优点：**
- 简单直观
- 适合比较不同测序深度的样本
- 适合比较固定大小的bins

* *缺点：**
- 不考虑区域长度
- 受高丰度区域（例如，rRNA）的影响RNA-seq)

- --

### 3. BPM（每百万映射读数的 Bins）

* *公式：** `(Number of reads in bin) / (Sum of all reads in bins in millions)`

* *与 CPM 的主要区别：** 仅考虑属于分析 bin 的读数，而不是所有映射读数。

* *何时使用：**
- 类似到 CPM，但当您想要排除分析区域之外的读数时
- 比较特定基因组区域，同时忽略背景

* *可用于：** `bamCoverage`， `bamCompare`

* *示例：**
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing BPM
```

* *解释：** BPM 仅考虑分箱区域中的读取。

* *优点：**
- 专注于分析区域的标准化
- 受读取影响较小未分析区域

* *缺点：**
- 不太常用，可能更难与已发布的数据进行比较

- --

### 4. RPGC（每个基因组内容的读取数）

* *公式：** `(Number of reads × Scaling factor) / Effective genome size`

* *比例因子：** 计算所得实现 1× 基因组覆盖率（每个碱基 1 个读段）

* *何时使用：**
- 想要跨样本的可比较的覆盖率值
- 需要可解释的绝对覆盖率值
- 比较具有非常不同的总读段计数的样本
- 具有尖峰归一化上下文的 ChIP-seq

* * 可用中：** `bamCoverage`、`bamCompare`

* *要求：** `--effectiveGenomeSize` 参数

* *示例：**
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing RPGC \
    --effectiveGenomeSize 2913022398
```

* *解释：** 信号值近似于覆盖深度（例如，2 的值 ≈ 2× 

* *优点：**
- 产生 1× 归一化覆盖度
- 可根据基因组覆盖度进行解释
- 适合比较具有不同测序深度的样本

* *缺点：**
- 需要了解有效基因组大小
- 假设均匀覆盖度（不适用于具有峰的 ChIP-seq）

- --

### 5. 无（无标准化）

* *公式：** 原始读取计数

* *何时使用：**
- 初步分析
- 当样本具有相同的库大小时（罕见）
- 当下游工具执行标准化时
- 调试或质量control

* *适用于：**所有工具（通常是默认值）

* *示例：**
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing None
```

* *解释：**每个 bin 的原始读取计数。

* *优点：**
- 不做任何假设
- 适用于查看原始数据
- 计算速度最快

* *缺点：**
- 无法公平比较不同测序深度的样本
- 不适合发表数据

- --

### 6. SES（选择性富集统计）

* *方法：** 信号提取缩放- 比较 ChIP 与对照的更复杂方法

* *何时使用：**
- 使用 bamCompare
- ChIP-seq 分析
- 需要复杂的背景校正
- 简单 readCount 缩放的替代方法

* * 适用于：** `bamCompare`仅

* *示例：**
```bash
bamCompare -b1 chip.bam -b2 input.bam -o output.bw \
    --scaleFactorsMethod SES
```

* *注意：** SES 专为 ChIP-seq 数据设计，对于噪声数据可能比简单的读取计数缩放效果更好。

- --

### 7. readCount (Read Count缩放）

* *方法：**按样本之间总读取计数的比率进行缩放

* *何时使用：**
- `bamCompare`
- 默认为比较中的测序深度差异
- 当您相信总读取计数反映库时size

* *适用于：** `bamCompare`

* *示例：**
```bash
bamCompare -b1 treatment.bam -b2 control.bam -o output.bw \
    --scaleFactorsMethod readCount
```

* *工作原理：**如果sample1有100M读取，sample2有50M读取，则sample2之前会缩放2× 

- --

## 标准化方法选择指南

### 对于ChIP-seq覆盖轨迹

* *推荐：**RPGC或CPM

```bash
bamCoverage --bam chip.bam --outFileName chip.bw \
    --normalizeUsing RPGC \
    --effectiveGenomeSize 2913022398 \
    --extendReads 200 \
    --ignoreDuplicates
```

* *推理：**考虑测序深度差异； RPGC 提供可解释的覆盖值。

- --

### 用于 ChIP-seq 比较（治疗与对照）

* *推荐：** log2 比率与 readCount 或 SES 缩放

```bash
bamCompare -b1 chip.bam -b2 input.bam -o ratio.bw \
    --operation log2 \
    --scaleFactorsMethod readCount \
    --extendReads 200 \
    --ignoreDuplicates
```

 * *推理：** Log2 比率显示富集（正）和耗尽（负）； readCount 根据深度进行调整。

- --

### 对于 RNA-seq 覆盖轨迹

* *推荐：** CPM 或 RPKM

```bash
# Strand-specific forward
bamCoverage --bam rnaseq.bam --outFileName forward.bw \
    --normalizeUsing CPM \
    --filterRNAstrand forward

# For gene-level: RPKM accounts for gene length
bamCoverage --bam rnaseq.bam --outFileName output.bw \
    --normalizeUsing RPKM
```

* *推理：** 用于比较固定宽度 bin 的 CPM；基因的 RPKM（占长度）。

- --

### 对于 ATAC-seq

* *推荐：** RPGC 或 CPM

```bash
bamCoverage --bam atac_shifted.bam --outFileName atac.bw \
    --normalizeUsing RPGC \
    --effectiveGenomeSize 2913022398
```

* *推理：** 与 ChIP-seq 类似； 

- --

### 对于样本相关性分析

* *推荐：** CPM 或 RPGC

```bash
multiBamSummary bins \
    --bamfiles sample1.bam sample2.bam sample3.bam \
    -o readCounts.npz

plotCorrelation -in readCounts.npz \
    --corMethod pearson \
    --whatToShow heatmap \
    -o correlation.png
```

* *注意：** `multiBamSummary` 没有显式标准化，但相关性分析对缩放具有鲁棒性。对于非常不同的文库大小，请考虑首先对 BAM 文件进行标准化，或使用带有 `multiBigwigSummary`.

- --

## 高级标准化注意事项的 CPM 标准化 bigWig 文件

### 尖峰标准化 

对于尖峰对照实验（例如，*Drosophila* 染色质尖峰） ChIP-seq）：

1. 根据插入读数计算缩放因子
2. 使用 `--scaleFactor` 参数应用自定义缩放因子

```bash
# Calculate spike-in factor (example: 0.8)
SCALE_FACTOR=0.8

bamCoverage --bam chip.bam --outFileName chip_spikenorm.bw \
    --scaleFactor ${SCALE_FACTOR} \
    --extendReads 200
```

- --

### 手动缩放因子

您可以应用自定义缩放因子：

```bash
# Apply 2× scaling
bamCoverage --bam input.bam --outFileName output.bw \
    --scaleFactor 2.0
```

- --

### 染色体排除

从归一化计算中排除特定染色体：

```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing RPGC \
    --effectiveGenomeSize 2913022398 \
    --ignoreForNormalization chrX chrY chrM
```

* *何时使用：** 混合性别样本中的性染色体、线粒体 DNA 或染色体

- --

## 常见陷阱

### 1. 对基于 bin 的数据使用 RPKM
* *问题：** RPKM 考虑了区域长度，但所有 bin 的大小相同
* *解决方案：** 使用 CPM 或 RPGC 代替

### 2. 比较未归一化的样本
* *问题：** 2×测序深度的样本似乎有2×信号
* *解决方案：** 比较样本时始终进行归一化

### 3. 有效基因组大小错误
* *问题：** 对 hg38 数据使用 hg19 基因组大小
* *解决方案：** 仔细检查基因组组装并使用正确的大小

### 4. GC 校正后忽略重复项
* *问题：** 会引入偏差
* *解决方案：** 切勿使用`correctGCBias`

### 5. 在没有有效基因组大小的情况下使用 RPGC`--ignoreDuplicates`
* *问题：** 命令失败
* *解决方案：** 始终指定 `--effectiveGenomeSize` 和 RPGC

- --

## 不同的归一化比较

### 样本内比较（不同区域）
* *使用：** RPKM（考虑区域长度）

### 样本间比较（相同区域）
* *使用：** CPM、RPGC 或 BPM（考虑文库大小）

### 治疗与治疗控制
* *使用：** bam与log2比率和readCount/SES缩放比较

### 多样本关联
* *使用：** CPM或RPGC标准化bigWig文件，然后multiBigwigSummary

- --

## 快速参考表

|方法|考虑深度|长度说明 |最适合 |命令|
|--------|--------------------|------------------------|---------|---------|
| RPKM | ✓ | ✓ | RNA-seq 基因 | `--normalizeUsing RPKM` |
|每千次展示费用 | ✓ | ✗ |固定尺寸垃圾箱 | `--normalizeUsing CPM` |
|业务流程管理| ✓ | ✗ |特定地区 | `--normalizeUsing BPM` |
|角色扮演游戏 | ✓ | ✗ |可解释的报道 | `--normalizeUsing RPGC --effectiveGenomeSize X` |
|无 | ✗ | ✗ |原始数据| `--normalizeUsing None` |
|社会服务局 | ✓ | ✗ | ChIP 比较 | `bamCompare --scaleFactorsMethod SES` |
|阅读次数 | ✓ | ✗ | ChIP 比较 | `bamCompare --scaleFactorsMethod readCount` |

- --

## 进一步阅读

有关标准化理论和最佳实践的更多详细信息：
- deepTools 文档：https://deeptools.readthedocs.io/
- ChIP-seq 分析的 ENCODE 指南
- RNA-seq标准化论文（DESeq2、TMM方法）
