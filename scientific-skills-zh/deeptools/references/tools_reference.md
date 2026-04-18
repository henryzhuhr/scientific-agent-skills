# deepTools 完整工具参考

本文档提供了按类别组织的所有 deepTools 命令行实用程序的综合参考。

## BAM 和 bigWig 文件处理工具

### multiBamSummary

跨多个 BAM 文件计算基因组区域的读取覆盖率，输出压缩的 numpy 数组以进行下游关联和 PCA Analysis.

* *模式：**
- **bins**：使用连续等大小窗口进行全基因组分析（默认 10kb）
- **BED 文件**：将分析限制为用户指定的基因组区域

* *关键参数：**
- `--bamfiles, -b`：索引 BAM 文件（空格分隔，必需）
- `--outFileName, -o`：输出覆盖矩阵文件（必需）
- `--BED`：区域规范文件（仅限 BED 文件模式）
- `--binSize`：以基数为单位的窗口大小（默认值：10,000）
- `--labels`：自定义样本标识符
- `--minMappingQuality`：读取包含的质量阈值
- `--numberOfProcessors, -p`：并行处理核心
- `--extendReads`：片段大小扩展
- `--ignoreDuplicates`：删除PCR重复项
- `--outRawCounts`：导出带有坐标列和每个样本计数的制表符分隔文件

* *输出：**用于plotCorrelation和plotPCA

* *常见的压缩numpy数组（.npz）用法：**
```bash
# Genome-wide comparison
multiBamSummary bins --bamfiles sample1.bam sample2.bam -o results.npz

# Peak region comparison
multiBamSummary BED-file --BED peaks.bed --bamfiles sample1.bam sample2.bam -o results.npz
```

- --

### multiBigwigSummary

与multiBamSummary类似，但对bigWig文件而不是BAM文件进行操作。用于比较样本之间的覆盖轨迹。

* *模式：**
- **bins**：全基因组分析
- **BED 文件**：区域特定分析

* *关键参数：** 与 multiBamSummary 类似，但接受 bigWig 文件

- --

### bamCoverage

将 BAM 对齐文件转换为 bigWig 或 bedGraph 格式的标准化覆盖轨道。将覆盖率计算为每个 bin 的读取数。

* *关键参数：**
- `--bam, -b`：输入 BAM 文件（必需）
- `--outFileName, -o`：输出文件名（必需）
- `--outFileFormat, -of`：输出类型（bigwig 或 bedgraph）
- `--normalizeUsing`：归一化方法
  - **RPKM**：每百万映射读取的每千碱基读取数
  - **CPM**：每百万映射读取的计数
  - **BPM**：每百万映射读取的bins
  - **RPGC**：每个基因组内容的读取（需要-- effectiveGenomeSize）
  - **无**：无标准化（默认）
- `--effectiveGenomeSize`：可映射的基因组大小（RPGC 所需）
- `--binSize`：碱基对分辨率（默认：50）
- `--extendReads, -e`：将读数扩展到片段长度（建议用于 ChIP-seq，不适用于 ChIP-seq） RNA-seq)
- `--centerReads`：以片段长度为中心读取以获得更清晰的信号
- `--ignoreDuplicates`：仅对相同读取进行一次计数
- `--minMappingQuality`：过滤低于质量阈值的读取
- `--minFragmentLength / --maxFragmentLength`：片段长度过滤
- `--smoothLength`：用于降噪的窗口平均
- `--MNase`：分析MNase-seq数据以进行核小体定位
- `--Offset`：位置特异性偏移（对于RiboSeq、GROseq有用）
- `--filterRNAstrand`：单独的正向/反向链读数
- `--ignoreForNormalization`：从归一化中排除染色体（例如性染色体）
- `--numberOfProcessors, -p`：并行处理

* *重要说明：**
- 对于RNA-seq：请勿使用--extendReads（将延伸至剪接点）
- 对于 ChIP-seq：使用 --extendReads 进行较小的 bin 大小
- 切勿应用 --ignoreDuplicates GC 偏差校正后 

* *常见用法：**
```bash
# Basic coverage with RPKM normalization
bamCoverage --bam input.bam --outFileName coverage.bw --normalizeUsing RPKM

# ChIP-seq with extension
bamCoverage --bam chip.bam --outFileName chip_coverage.bw \
    --binSize 10 --extendReads 200 --ignoreDuplicates

# Strand-specific RNA-seq
bamCoverage --bam rnaseq.bam --outFileName forward.bw \
    --filterRNAstrand forward
```

- --

### bamCompare

通过生成 bigWig 或 bedGraph 文件来比较两个 BAM 文件，对测序深度差异进行标准化。在同等大小的箱中处理基因组并执行每个箱的计算。

* *比较方法：**
- **log2**（默认）：样本的Log2比率
- **比率**：直接比率计算
- **减**：文件之间的差异
- **加**：样本总和
- **平均值**：样本之间的平均值
- **倒数比率**：负数比率 < 0
- **第一/第二**：从单个文件输出缩放信号

* *标准化方法：**
- **readCount**（默认）：补偿测序深度
- **SES**：选择性富集统计
- **RPKM**：每千碱基的读取数百万
- **CPM**：每百万计数
- **BPM**：每百万箱
- **RPGC**：每个基因组内容的读取（需要-- effectiveGenomeSize）

  * *关键参数：**
- `--bamfile1, -b1`：第一个BAM文件（必填）
- `--bamfile2, -b2`：第二个 BAM 文件（必填）
- `--outFileName, -o`：输出文件名（必填）
- `--outFileFormat`：bigwig 或 bedgraph
- `--operation`：比较方法（参见上面）
- `--scaleFactorsMethod`：归一化方法（见上文）
- `--binSize`：输出的 Bin 宽度（默认：50bp）
- `--pseudocount`：避免被零除（默认：1）
- `--extendReads`：将读取扩展到片段长度
- `--ignoreDuplicates`：计算相同的读数一次
- `--minMappingQuality`：质量阈值
- `--numberOfProcessors, -p`：并行化

* *通用用法：**
```bash
# Log2 ratio of treatment vs control
bamCompare -b1 treatment.bam -b2 control.bam -o log2ratio.bw

# Subtract control from treatment
bamCompare -b1 treatment.bam -b2 control.bam -o difference.bw \
    --operation subtract --scaleFactorsMethod readCount
```

- --

### CorrectGCBias /computeGCBias

* *computeGCBias:** 识别测序和 PCR 扩增中的 GC 内容偏差。

* * CorrectGCBias:** 更正 BAM 文件中检测到的 GC 偏差computeGCBias.

* *关键参数（computeGCBias）：**
- `--bamfile, -b`：输入BAM文件
- `--effectiveGenomeSize`：可映射基因组大小
- `--genome, -g`：2位格式的参考基因组
- `--fragmentLength, -l`：片段长度（对于单端）
- `--biasPlot`：输出诊断图

* *关键参数（正确的GCBias）：**
- `--bamfile, -b`：输入BAM文件
- `--effectiveGenomeSize`：可映射基因组大小
- `--genome, -g`：2位格式的参考基因组
- `--GCbiasFrequenciesFile`：来自的频率computeGCBias
- `--correctedFile, -o`：输出校正的 BAM

* *重要：** GC 偏差校正后切勿使用 --ignoreDuplicates

- --

### alignmentSieve

通过各种质量指标即时过滤 BAM 文件。对于为特定分析创建过滤的 BAM 文件很有用。

* *关键参数：**
- `--bam, -b`：输入 BAM 文件
- `--outFile, -o`：输出 BAM 文件
- `--minMappingQuality`：最低映射质量
- `--ignoreDuplicates`：删除重复项
- `--minFragmentLength / --maxFragmentLength`：片段长度过滤器
- `--samFlagInclude / --samFlagExclude`：SAM标志过滤
- `--shift`：移位读取（例如，用于ATACseq Tn5校正）
- `--ATACshift`：自动转换ATAC-seq数据

- --

### computeMatrix

计算每个基因组区域的分数并为plotHeatmap和plotProfile准备矩阵。处理 bigWig 乐谱文件和 BED/GTF 区域文件。

* *模式：**
- **参考点**：相对于特定位置（TSS、TES 或中心）的信号分布 
- **尺度区域**：跨区域的信号标准化为统一长度

* *关键参数：**
- `-R`：BED/GTF 格式的片段文件（必需）
- `-S`：BigWig 乐谱文件（必需）
- `-o`：输出矩阵文件（必需）
- `-b`：距参考点的上游距离
- `-a`：距参考点的下游距离
- `-m`：区域主体长度（仅限比例区域）
- `-bs, --binSize`：平均分数的箱大小
- `--skipZeros`：跳过全零区域
- `--minThreshold / --maxThreshold`：按信号强度过滤
- `--sortRegions`：升序、降序、保留、否
- `--sortUsing`：平均值、中值、最大值、最小值、总和、region_length
- `-p, --numberOfProcessors`：并行处理
- `--averageTypeBins`：统计方法（平均值、中位数、最小值、最大值、总和、标准差）

* *输出选项：**
- `--outFileNameMatrix`：导出制表符分隔数据
- `--outFileSortedRegions`：保存过滤/排序的 BED 文件

* *常见用法：**
```bash
# TSS analysis
computeMatrix reference-point -S signal.bw -R genes.bed \
    -o matrix.gz -b 2000 -a 2000 --referencePoint TSS

# Scaled gene body
computeMatrix scale-regions -S signal.bw -R genes.bed \
    -o matrix.gz -b 1000 -a 1000 -m 3000
```

- --

## 质量控制工具

### plotFingerprint

主要用于 ChIP-seq 实验的质量控制工具。评估抗体富集是否成功。生成累积读取覆盖率配置文件以区分信号和噪声。

* *关键参数：**
- `--bamfiles, -b`：索引 BAM 文件（必需）
- `--plotFile, -plot, -o`：输出图像文件名（必需）
- `--extendReads, -e`：将读取扩展到片段length
- `--ignoreDuplicates`：计算相同的读数一次
- `--minMappingQuality`：映射质量过滤器
- `--centerReads`：片段长度的中心读数
- `--minFragmentLength / --maxFragmentLength`：片段过滤器
- `--outRawCounts`：保存每个 bin 的读取计数
- `--outQualityMetrics`：输出 QC 指标（Jensen-Shannon 距离）
- `--labels`：自定义样本名称
- `--numberOfProcessors, -p`：并行处理

* *解释：**
- 理想对照：直线对角线
- 强ChIP：急剧上升至最高排名（集中读取在几个箱中）
- 弱富集：更平坦的曲线接近对角线

* *常见用法：**
```bash
plotFingerprint -b input.bam chip1.bam chip2.bam \
    --labels Input ChIP1 ChIP2 -o fingerprint.png \
    --extendReads 200 --ignoreDuplicates
```

- --

### plotCoverage

可视化整个基因组的平均读取分布。显示基因组覆盖度并帮助确定测序深度是否足够。

* *关键参数：**
- `--bamfiles, -b`：要分析的 BAM 文件（必需）
- `--plotFile, -o`：输出图文件名（必需）
- `--ignoreDuplicates`：删除 PCR重复项
- `--minMappingQuality`：质量阈值
- `--outRawCounts`：保存基础数据
- `--labels`：样本名称
- `--numberOfSamples`：要采样的位置数（默认值： 1,000,000)

- --

### bamPEFragmentSize

确定双端测序数据的片段长度分布。用于验证文库制备过程中预期片段大小的基本 QC。

* *关键参数：**
- `--bamfiles, -b`：BAM 文件（必需）
- `--histogram, -hist`：输出直方图文件名（必需）
- `--plotTitle, -T`：绘图title
- `--maxFragmentLength`：要考虑的最大长度（默认：1000）
- `--logScale`：使用对数Y轴
- `--outRawFragmentLengths`：保存原始片段长度

- --

### plotCorrelation

分析 multiBamSummary 或 multiBigwigSummary 输出的样本相关性。显示不同样本的相似程度。

* *相关方法：**
- **Pearson**：测量指标差异；对异常值敏感；适用于正态分布数据
- **Spearman**：基于排名；受异常值的影响较小；更适合非正态分布

* *可视化选项：**
- **热图**：具有层次聚类的颜色强度（完全链接）
- **散点图**：具有相关系数的成对散点图

* *关键参数：**
- `--corData, -in`：来自 multiBamSummary/multiBigwigSummary 的输入矩阵（必需）
- `--corMethod`：pearson 或 Spearman（必需）
- `--whatToShow`：热图或散点图（必需）
- `--plotFile, -o`：输出文件名（必填）
- `--skipZeros`：排除零值区域
- `--removeOutliers`：使用中值绝对偏差（MAD）过滤
- `--outFileCorMatrix`：导出相关矩阵
- `--labels`：自定义样本名称
- `--plotTitle`：绘图标题
- `--colorMap`：配色方案（50+选项）
- `--plotNumbers`：在热图上显示相关值

* *常见用法：**
```bash
# Heatmap with Pearson correlation
plotCorrelation -in readCounts.npz --corMethod pearson \
    --whatToShow heatmap -o correlation_heatmap.png --plotNumbers

# Scatterplot with Spearman correlation
plotCorrelation -in readCounts.npz --corMethod spearman \
    --whatToShow scatterplot -o correlation_scatter.png
```

- --

### plotPCA

从multiBamSummary或multiBigwigSummary输出生成主成分分析图。以降维方式显示样本关系。

* *关键参数：**
- `--corData, -in`：来自 multiBamSummary/multiBigwigSummary 的覆盖文件（必需）
- `--plotFile, -o`：输出图像（png、eps、pdf、svg） （必需）
- `--outFileNameData`：导出 PCA 数据（载荷/旋转和特征值）
- `--labels, -l`：自定义样本标签
- `--plotTitle, -T`：绘图标题
- `--plotHeight / --plotWidth`：尺寸以厘米为单位
- `--colors`：自定义符号颜色
- `--markers`：符号形状
- `--transpose`：对转置矩阵执行PCA（行=样本）
- `--ntop`：使用前N变量行（默认：1000）
- `--PCs`：要绘制的组件（默认：1 2）
- `--log2`：分析前对数据进行 Log2 转换
- `--rowCenter`：将每行居中于 0

* *常见用法：**
```bash
plotPCA -in readCounts.npz -o PCA_plot.png \
    -T "PCA of read counts" --transpose
```

- --

## 可视化工具

### plotHeatmap

从computeMatrix输出创建基因组区域热图。生成出版物质量的可视化效果。

* *关键参数：**
- `--matrixFile, -m`：来自computeMatrix的矩阵（必需）
- `--outFileName, -o`：输出图像（png，eps，pdf，svg）（必需）
- `--outFileSortedRegions`：之后保存区域过滤
- `--outFileNameMatrix`：导出矩阵值
- `--interpolationMethod`：自动、最近、双线性、双三次、高斯
  - 默认：最近（≤1000列）、双线性（>1000列）
- `--dpi`：图分辨率

* *聚类：**
- `--kmeans`：k 均值聚类
- `--hclust`：分层聚类（>1000 个区域速度较慢）
- `--silhouette`：计算聚类质量指标

* *Visual定制：**
- `--heatmapHeight / --heatmapWidth`：尺寸 (3-100 cm)
- `--whatToShow`：绘图、热图、颜色条（组合）
- `--alpha`：透明度 (0-1)
- `--colorMap`：50 多种配色方案
- `--colorList`：自定义渐变颜色
- `--zMin / --zMax`：强度范围限制
- `--boxAroundHeatmaps`：是/否（默认值：是)

* *标签：**
- `--xAxisLabel / --yAxisLabel`：轴标签
- `--regionsLabel`：区域集标识符
- `--samplesLabel`：样本名称
- `--refPointLabel`：参考点label
- `--startLabel / --endLabel`：区域边界标签

* *常见用法：**
```bash
# Basic heatmap
plotHeatmap -m matrix.gz -o heatmap.png

# With clustering and custom colors
plotHeatmap -m matrix.gz -o heatmap.png \
    --kmeans 3 --colorMap RdBu --zMin -3 --zMax 3
```

- --

### plotProfile

使用computeMatrix生成显示基因组区域得分的剖面图output.

* *关键参数：**
- `--matrixFile, -m`：来自computeMatrix的矩阵（必需）
- `--outFileName, -o`：输出图像（png、eps、pdf、svg）（必需）
- `--plotType`：线条、填充、se、std、重叠线、热图
- `--colors`：调色板（名称或十六进制代码）
- `--plotHeight / --plotWidth`：尺寸以厘米为单位
- `--yMin / --yMax`：Y 轴range
- `--averageType`：平均值、中位数、最小值、最大值、标准差、总和

* *聚类：**
- `--kmeans`：k 均值聚类
- `--hclust`：层次聚类
- `--silhouette`：集群质量指标

* *标签：**
- `--plotTitle`：主标题
- `--regionsLabel`：区域集标识符
- `--samplesLabel`：样本名称
- `--startLabel / --endLabel`：区域边界标签（比例区域）模式）

* *输出选项：**
- `--outFileNameData`：将数据导出为制表符分隔值
- `--outFileSortedRegions`：将过滤/排序区域保存为 BED

* *常见用法：**
```bash
# Line plot
plotProfile -m matrix.gz -o profile.png --plotType lines

# With standard error shading
plotProfile -m matrix.gz -o profile.png --plotType se \
    --colors blue red green
```

- --

### plotEnrichment

计算并可视化跨基因组区域的信号富集。测量与区域组重叠的比对百分比。对于 FRiP（峰中的片段）分数很有用。

* *关键参数：**
- `--bamfiles, -b`：索引 BAM 文件（必需）
- `--BED`：BED/GTF 格式的区域文件（必需）
- `--plotFile, -o`：输出可视化（png、pdf、eps、svg）
- `--labels, -l`：自定义样本标识符
- `--outRawCounts`：导出数值数据
- `--perSample`：按样本而不是特征分组（默认）
- `--regionLabels`：自定义区域名称

* *读取处理：**
- `--minFragmentLength / --maxFragmentLength`：片段过滤器
- `--minMappingQuality`：质量阈值
- `--samFlagInclude / --samFlagExclude`：SAM标志过滤器
- `--ignoreDuplicates`：删除重复项
- `--centerReads`：中心读取以获得更清晰的信号

* *常见用法：**
```bash
plotEnrichment -b Input.bam H3K4me3.bam \
    --BED peaks_up.bed peaks_down.bed \
    --regionLabels "Up regulated" "Down regulated" \
    -o enrichment.png
```

- --

## 其他工具

### computeMatrixOperations

高级矩阵操作工具，用于组合computeMatrix中的矩阵或对矩阵进行子集化。支持复杂的多样本、多区域分析。

* *操作：**
- `cbind`：按列组合矩阵
- `rbind`：按行组合矩阵
- `subset`：提取特定样本或区域
- `filterStrand`：仅保留特定链上的区域
- `filterValues`：应用信号强度过滤器
- `sort`：按各种标准对区域进行排序
- `dataRange`：报告最小值/最大值值

* *常用用法：**
```bash
# Combine matrices
computeMatrixOperations cbind -m matrix1.gz matrix2.gz -o combined.gz

# Extract specific samples
computeMatrixOperations subset -m matrix.gz --samples 0 2 -o subset.gz
```

- --

### estimateReadFiltering

无需实际过滤即可预测各种过滤参数的影响。在运行完整分析之前帮助优化过滤策略。

* *关键参数：**
- `--bamfiles, -b`：要分析的 BAM 文件
- `--sampleSize`：要采样的读取数（默认值：100,000）
- `--binSize`：Bin 大小分析
- `--distanceBetweenBins`：采样箱之间的间距

* *要测试的过滤选项：**
- `--minMappingQuality`：测试质量阈值
- `--ignoreDuplicates`：评估重复影响
- `--minFragmentLength / --maxFragmentLength`：测试片段过滤器

- --

## 跨工具的通用参数

许多deepTools命令共享这些过滤和性能选项：

* *读取过滤：**
- `--ignoreDuplicates`：删除PCR重复项
- `--minMappingQuality`：按比对置信度过滤
- `--samFlagInclude / --samFlagExclude`：SAM格式过滤
- `--minFragmentLength / --maxFragmentLength`：片段长度界限

* *性能：**
- `--numberOfProcessors, -p`：启用并行处理
- `--region`：处理特定基因组区域（字符：开始-结束）

* *读取处理：**
- `--extendReads`：延伸至片段长度
- `--centerReads`：以片段中点为中心
- `--ignoreDuplicates`：仅计数唯一读取
