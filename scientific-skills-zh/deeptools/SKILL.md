---
name: deeptools
description: NGS 分析工具包。 BAM 到 bigWig 的转换、QC（相关性、PCA、指纹）、热图/概况（TSS、峰值），用于 ChIP-seq、RNA-seq、ATAC-seq 可视化。
license: BSD license
metadata:
    skill-author: K-Dense Inc.
---

# deepTools：NGS 数据分析工具包

## 概述

deepTools 是一套全面的 Python 命令行工具，专为处理和分析高通量测序数据而设计。使用 deepTools 执行质量控制、标准化数据、比较样本，并为 ChIP-seq、RNA-seq、ATAC-seq、MNase-seq 和其他 NGS 实验生成发表质量的可视化效果。

* *核心功能：**
- 将 BAM 比对转换为标准化覆盖轨迹 (bigWig/bedGraph)
- 质量控制评估（指纹、 
- 样本比较和相关性分析
- 围绕基因组特征生成热图和剖面图
- 富集分析和峰区域可视化

## 何时使用此技能

此技能应在以下情况下使用：

- **文件转换**：“将 BAM 转换为 bigWig”、“生成覆盖轨迹”、 “标准化 ChIP-seq 数据”
- **质量控制**：“检查 ChIP 质量”、“比较重复”、“评估测序深度”、“QC 分析”
- **可视化**：“围绕 TSS 创建热图”、“绘制 ChIP 信号”、“可视化富集”、“生成剖面图”
- **样品比较**：“比较处理与控制”、“关联样本”、“PCA 分析”
- **分析工作流程**：“分析 ChIP-seq 数据”、“RNA-seq 覆盖范围”、“ATAC-seq 分析”、“完整工作流程”
- **处理特定文件类型**：基因组背景下的 BAM 文件、bigWig 文件、BED 区域文件

## 快速开始

对于deepTools的新用户，从文件验证和常见工作流程开始：

### 1.验证输入文件

在运行任何分析之前，使用验证脚本验证BAM、bigWig和BED文件：

```bash
python scripts/validate_files.py --bam sample1.bam sample2.bam --bed regions.bed
```

这将检查文件是否存在， BAM索引，以及格式正确性。

### 2.生成工作流程模板

对于标准分析，使用工作流程生成器创建自定义脚本：

```bash
# List available workflows
python scripts/workflow_generator.py --list

# Generate ChIP-seq QC workflow
python scripts/workflow_generator.py chipseq_qc -o qc_workflow.sh \
    --input-bam Input.bam --chip-bams "ChIP1.bam ChIP2.bam" \
    --genome-size 2913022398

# Make executable and run
chmod +x qc_workflow.sh
./qc_workflow.sh
```

### 3. 最常见操作

有关常用命令和参数，请参阅 `assets/quick_reference.md`。

## 安装

```bash
uv pip install deeptools
```

## 核心工作流程

deepTools 工作流程通常遵循以下模式：**QC → 标准化 → 比较/可视化**

### ChIP-seq 质量控制工作流程

当用户请求 ChIP-seq QC 或质量评估时：

1. **使用 `scripts/workflow_generator.py chipseq_qc`
2 生成工作流程脚本**。 **关键 QC 步骤**：
 - 样本相关性 (multiBamSummary +plotCorrelation)
  - PCA 分析 (plotPCA)
  - 覆盖率评估 (plotCoverage)
  - 片段大小验证 (bamPEFragmentSize)
  - ChIP 富集强度(plotFingerprint)

* *解释结果：**
- **相关性**：重复应以高相关性聚集在一起 (>0.9)
- **指纹**：强 ChIP 显示急剧上升；平坦对角线表示富集度较差
- **覆盖率**：评估测序深度是否足以进行分析

`references/workflows.md` →“ChIP-seq 质量控制工作流程”中的完整工作流程详细信息

### ChIP-seq 完整分析工作流程

用于从 BAM 到可视化：

1. **使用标准化 (bamCoverage)
2 生成覆盖轨道**。 **创建比较轨道**（bamCompare for log2 比率）
3. **围绕特征 (computeMatrix)
4 计算信号矩阵**。 **生成可视化**（plotHeatmap、plotProfile）
5. **峰处的富集分析**（plotEnrichment）

使用`scripts/workflow_generator.py chipseq_analysis`生成模板。

`references/workflows.md`中完整的命令序列→“ChIP-seq分析工作流程”

### RNA-seq覆盖工作流程

用于链特异性RNA-seq覆盖轨道：

 使用 bamCoverage 与 `--filterRNAstrand` 分离正向和反向股线。

* *重要：**切勿使用 `--extendReads` 进行 RNA-seq（会延伸到剪接连接处）。

 使用归一化：CPM 用于固定箱，RPKM 用于基因水平分析。

 可用模板：`scripts/workflow_generator.py rnaseq_coverage`

 `references/workflows.md` 中的详细信息→“RNA-seq 覆盖率”工作流程“

### ATAC-seq 分析工作流程

ATAC-seq 需要 Tn5 偏移校正：

1. **使用对齐筛和 `--ATACshift`
2 进行移位读取**。 **使用 bamCoverage
3 生成覆盖率**。 **分析片段大小**（预计核小体阶梯模式）
4. **在峰值处可视化**（如果可用）

模板：`scripts/workflow_generator.py atacseq`

`references/workflows.md` 中的完整工作流程→“ATAC-seq 工作流程”

## 工具类别和常见任务

### BAM/bigWig 处理

* *将 BAM 转换为标准化覆盖率：**
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing RPGC --effectiveGenomeSize 2913022398 \
    --binSize 10 --numberOfProcessors 8
```

* *比较两个样本（log2比率）：**
```bash
bamCompare -b1 treatment.bam -b2 control.bam -o ratio.bw \
    --operation log2 --scaleFactorsMethod readCount
```

* *关键工具：** bamCoverage、bamCompare、multiBamSummary、multiBigwigSummary、 CorrectGCBias、比对筛

完整参考：`references/tools_reference.md` →“BAM 和 bigWig 文件处理工具”

### 质量控制

* *检查 ChIP 富集：**
```bash
plotFingerprint -b input.bam chip.bam -o fingerprint.png \
    --extendReads 200 --ignoreDuplicates
```

* *样品相关性：**
```bash
multiBamSummary bins --bamfiles *.bam -o counts.npz
plotCorrelation -in counts.npz --corMethod pearson \
    --whatToShow heatmap -o correlation.png
```

* *关键工具：**plotFingerprint、plotCoverage、plotCorrelation、plotPCA、bamPEFragmentSize

完整参考：`references/tools_reference.md`→“质量控制工具”

### 可视化

* *创建TSS 周围的热图：**
```bash
# Compute matrix
computeMatrix reference-point -S signal.bw -R genes.bed \
    -b 3000 -a 3000 --referencePoint TSS -o matrix.gz

# Generate heatmap
plotHeatmap -m matrix.gz -o heatmap.png \
    --colorMap RdBu --kmeans 3
```

* *创建剖面图：**
```bash
plotProfile -m matrix.gz -o profile.png \
    --plotType lines --colors blue red
```

* *关键工具：**computeMatrix、plotHeatmap、plotProfile、plotEnrichment

 完整参考：`references/tools_reference.md` →“可视化”工具“

## 标准化方法

选择正确的标准化对于有效比较至关重要。请咨询`references/normalization_methods.md`以获得全面指导。

* *快速选型指南：**

- **ChIP-seq 覆盖率**：使用 RPGC 或 CPM
- **ChIP-seq 比较**：使用 bamCompare 与 log2 和 readCount
- **RNA-seq bins**：使用 CPM
- **RNA-seq 基因**：使用 RPKM（考虑基因长度）
- **ATAC-seq**：使用 RPGC或 CPM

* *标准化方法：**
- **RPGC**：1× 基因组覆盖率（需要 -- effectiveGenomeSize）
- **CPM**：每百万个映射读取的计数 
- **RPKM**：每百万每 kb 的读取数（占区域长度）
- **BPM**：每百万个的 bins百万
- **无**：原始计数（不建议进行比较）

完整解释：`references/normalization_methods.md`

## 有效基因组大小

RPGC标准化需要有效的基因组大小。常用值：

|有机体 |组装|尺寸|用法 |
|----------|---------|-----|--------|
|人类 | GRCh38/hg38 | 2,913,022,398 | 2,913,022,398 `--effectiveGenomeSize 2913022398` |
|鼠标| GRCm38/mm10 | 2,652,783,500 | `--effectiveGenomeSize 2652783500` |
|斑马鱼 | GRCz11 | 1,368,780,147 | 1,368,780,147 `--effectiveGenomeSize 1368780147` |
| *果蝇* | DM6 | 142,573,017 | 142,573,017 `--effectiveGenomeSize 142573017` |
| *C。线虫* | ce10/ce11 | 100,286,401 | `--effectiveGenomeSize 100286401` |

 具有特定读取长度值的完整表：`references/effective_genome_sizes.md`

## 跨工具的通用参数

许多 deepTools 命令共享这些选项：

* *性能：**
- `--numberOfProcessors, -p`：启用并行处理（始终使用可用内核）
- `--region`：处理特定区域进行测试（例如，`chr1:1-1000000`）

* *读取过滤：**
- `--ignoreDuplicates`：删除 PCR 重复项（建议大多数人使用）分析）
- `--minMappingQuality`：按比对质量过滤（例如，`--minMappingQuality 10`）
- `--minFragmentLength` / `--maxFragmentLength`：片段长度范围
- `--samFlagInclude` / `--samFlagExclude`：SAM标记过滤

* *读取处理：**
- `--extendReads`：延伸至片段长度（ChIP-seq：是，RNA-seq：否）
- `--centerReads`：以片段中点为中心以获得更清晰的信号

## 最佳实践

### 文件验证
* *始终首先验证文件** 使用 `scripts/validate_files.py` 检查：
- 文件存在和可读性
- 存在 BAM 索引（.bai 文件）
- BED 格式正确性
- 文件大小合理

### 分析策略

1. **从 QC 开始**：在继续 
2 之前运行相关性、覆盖率和指纹分析。 **小区域测试**：使用`--region chr1:1-10000000`进行参数测试
3. **文档命令**：保存完整的命令行以实现重现性
4. **使用一致的标准化**：在比较中的样本中应用相同的方法
5. **验证基因组组装**：确保 BAM 和 BED 文件使用匹配的基因组构建 

### ChIP-seq Specific

- **始终为 ChIP-seq 扩展读取**：`--extendReads 200`
- **删除重复**：在大多数情况下使用 `--ignoreDuplicates`
- **首先检查富集**：在详细分析之前运行plotFingerprint
- **GC 校正**：仅在检测到显着偏差时适用； GC 校正后切勿使用 `--ignoreDuplicates`

### RNA-seq Specific

- **切勿为 RNA-seq 延伸读取**（将跨越剪接点）
- **链特异性**：对链状文库使用 `--filterRNAstrand forward/reverse`
- **标准化**：CPM bins，基因的 RPKM

### ATAC-seq Specific

- **应用 Tn5 校正**：使用对齐筛与 `--ATACshift`
- **片段过滤**：设置适当的最小/最大片段长度
- **检查核小体模式**：片段大小图应显示阶梯模式

### 性能优化

1. **使用多个处理器**：`--numberOfProcessors 8`（或可用内核）
2. **增加 bin 大小**以加快处理速度并缩小文件
3. **针对内存有限的系统单独处理染色体**
4. **使用alignmentSieve 预过滤BAM 文件**以创建可重复使用的过滤文件
5. **在 bedGraph 上使用 bigWig**：压缩且处理速度更快

## 故障排除

### 常见问题

* *BAM 索引缺失：**
```bash
samtools index input.bam
```

* *内存不足：**
 使用 `--region` 单独处理染色体：
```bash
bamCoverage --bam input.bam -o chr1.bw --region chr1
```

* *慢处理：**
增加`--numberOfProcessors`和/或增加`--binSize`

* *bigWig文件太大：**
增加bin大小：`--binSize 50`或更大

### 验证错误

运行验证脚本来识别问题：
```bash
python scripts/validate_files.py --bam *.bam --bed regions.bed
```

脚本输出中解释的常见错误和解决方案。

## 参考文档

此技能包括全面的参考文档：

### references/tools_reference.md
组织的所有deepTools命令的完整文档类别：
- BAM 和 bigWig 处理工具（9 个工具）
- 质量控制工具（6 个工具）
- 可视化工具（3 个工具）
- 杂项工具（2 个工具）

 每个工具包括：
- 用途和概述
- 关键参数与解释
- 使用示例
- 重要说明和最佳实践

* *在以下情况下使用此参考：** 用户询问特定工具、参数或详细用法。

### 参考文献/工作流程.md
常见分析的完整工作流程示例：
- ChIP-seq 质量控制工作流程
- ChIP-seq 完整分析工作流程
- RNA-seq 覆盖工作流程
- ATAC-seq 分析工作流程
- 多样本比较工作流程
- 峰区域分析工作流程
- 故障排除和性能提示

* *在以下情况下使用此参考：** 用户需要完整分析

### references/normalization_methods.md
规范化方法综合指南：
- 每种方法的详细解释（RPGC、CPM、RPKM、BPM等）
- 何时使用每种方法
- 公式和解释
- 选择实验类型指导
- 常见陷阱和解决方案
- 快速参考表

* *在以下情况下使用此参考：** 用户询问标准化、比较样本或使用哪种方法。

### references/ effective_genome_sizes.md
有效基因组大小值和用法：
- 常见生物体值（人类、小鼠、苍蝇、蠕虫、斑马鱼）
- 特定读长值
- 计算方法
- 何时以及如何在命令中使用
- 自定义基因组计算说明

* *在以下情况下使用此参考：**用户需要基因组大小进行RPGC标准化或GC偏差校正。

## 帮助程序脚本

### 脚本/validate_files.py

验证BAM，bigWig和BED文件deepTools 分析。检查文件存在、索引和格式。

* *用法：**
```bash
python scripts/validate_files.py --bam sample1.bam sample2.bam \
    --bed peaks.bed --bigwig signal.bw
```

* *何时使用：**开始任何分析之前，或排除错误时。

### scripts/workflow_generator.py

为常见的 deepTools 生成可自定义的 bash 脚本模板

* *可用工作流程：**
- `chipseq_qc`：ChIP-seq 质量控制
- `chipseq_analysis`：完整 ChIP-seq 分析
- `rnaseq_coverage`：链特异性 RNA-seq 覆盖率
- `atacseq`：带有Tn5校正的ATAC-seq

* *用法：**
```bash
# List workflows
python scripts/workflow_generator.py --list

# Generate workflow
python scripts/workflow_generator.py chipseq_qc -o qc.sh \
    --input-bam Input.bam --chip-bams "ChIP1.bam ChIP2.bam" \
    --genome-size 2913022398 --threads 8

# Run generated workflow
chmod +x qc.sh
./qc.sh
```

* *何时使用：**用户请求标准工作流程或需要模板脚本来定制。

## 资产

### asset/quick_reference.md

快速参考卡，包含最常用命令、有效基因组大小和典型工作流程模式。

* *何时使用：**用户需要快速命令示例，无需详细文档。

## 处理用户请求

### 对于新用户

1. 从安装验证
2开始。使用 `scripts/validate_files.py`
3 验证输入文件。根据实验类型
4推荐适当的工作流程。使用`scripts/workflow_generator.py`
5生成工作流模板。定制和执行指南

### 对于有经验的用户

1. 为请求的操作提供特定的工具命令
2. 参考`references/tools_reference.md`
3中的相应部分。建议优化和最佳实践
4. 提供问题的故障排除

### 针对特定任务

* *“将 BAM 转换为 bigWig”：**
- 使用 bamCoverage 进行适当的标准化
- 根据用例推荐 RPGC 或 CPM
- 为生物体提供有效的基因组大小
- 建议相关参数（extendReads、 ignoreDuplicates, binSize)

* *“检查 ChIP 质量”：**
- 运行完整的 QC 工作流程或专门使用plotFingerprint
- 解释结果的解释
- 根据结果建议后续操作

* *“创建热图”：**
- 指导完成两步过程： computeMatrix→plotHeatmap
- 帮助选择适当的矩阵模式（参考点与比例区域）
- 建议可视化参数和聚类选项

* *“比较样本”：**
- 推荐bamCompare进行两个样本比较
- 建议multiBamSummary +plotCorrelation为多个样本
- 指导归一化方法选择

### 参考文档

当用户需要详细信息时：
- **工具详细信息**：直接到`references/tools_reference.md`
- **工作流程**：使用`references/workflows.md`进行完整的分析流程
- **标准化**：咨询`references/normalization_methods.md`以选择方法
- **基因组大小**：参考`references/effective_genome_sizes.md`

使用grep模式搜索参考文献：
```bash
# Find tool documentation
grep -A 20 "^### toolname" references/tools_reference.md

# Find workflow
grep -A 50 "^## Workflow Name" references/workflows.md

# Find normalization method
grep -A 15 "^### Method Name" references/normalization_methods.md
```

## 交互示例

* *用户：“我需要分析我的ChIP-seq 数据“**

 响应方法：
1. 询问可用的文件（BAM 文件、峰、基因）
2. 使用验证脚本
3 验证文件。生成chipseq_analysis工作流程模板
4. 为他们的特定文件和生物体定制
5. 解释脚本运行时的每个步骤

* *用户：“我应该使用哪种标准化？”**

响应方式：
1. 询问实验类型（ChIP-seq、RNA-seq 等）
2. 询问比较目标（样本内或样本间）
3. 查阅`references/normalization_methods.md`选型指南
4. 推荐适当的方法并有理由
5. 提供带有参数的命令示例

* *用户：“创建围绕TSS的热图”**

响应方法：
1. 验证 bigWig 和基因 BED 文件是否可用 
2. 在 TSS
3 处使用具有参考点模式的computeMatrix。使用适当的可视化参数 
4 生成绘图热图。如果数据集较大，建议聚类
5. 提供轮廓图作为补充

## 主要提醒

- **首先文件验证**：在分析之前始终验证输入文件
- **标准化很重要**：为比较类型选择适当的方法
- **仔细扩展读取**：对于 ChIP-seq 是，对于 RNA-seq 否
- **使用所有核心**：设置`--numberOfProcessors` 至可用内核
- **区域测试**：使用 `--region` 进行参数测试
- **首先检查 QC**：在详细分析之前运行质量控制
- **记录所有内容**：保存命令以实现可重复性
- **参考文档**：使用全面的参考资料进行详细分析指导
