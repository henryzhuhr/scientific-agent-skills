# 验证工作流程

## 概述
Latch 验证工作流程是由 Latch 工程师开发和维护的生产就绪型预构建生物信息学管道。这些工作流程被顶级制药公司和生物技术公司用于研究和发现。

## 可在 Python SDK 中使用

`latch.verified` 模块提供从 Python 代码对经过验证的工作流程的编程访问。

### 导入经过验证的工作流程

```python
from latch.verified import (
    bulk_rnaseq,
    deseq2,
    mafft,
    trim_galore,
    alphafold,
    colabfold
)
```

## 已验证核心工作流程

### 批量 RNA 序列分析

* *比对和定量：**
```python
from latch.verified import bulk_rnaseq
from latch.types import LatchFile

# Run bulk RNA-seq pipeline
results = bulk_rnaseq(
    fastq_r1=LatchFile("latch:///data/sample_R1.fastq.gz"),
    fastq_r2=LatchFile("latch:///data/sample_R2.fastq.gz"),
    reference_genome="hg38",
    output_dir="latch:///results/rnaseq"
)
```

* *功能：**
- 使用 FastQC 读取质量控制
- 适配器修整 
- 与 STAR 或 STAR 比对HISAT2
- 使用 featureCounts 进行基因级定量
- MultiQC 报告生成

### 差异表达分析

* *DESeq2:**
```python
from latch.verified import deseq2
from latch.types import LatchFile

# Run differential expression analysis
results = deseq2(
    count_matrix=LatchFile("latch:///data/counts.csv"),
    sample_metadata=LatchFile("latch:///data/metadata.csv"),
    design_formula="~ condition",
    output_dir="latch:///results/deseq2"
)
```

* * 功能：**
- 归一化和方差稳定性
- 差异表达测试
- MA图和火山图
- PCA可视化
- 注释结果表

### 通路分析

* *富集分析：**
```python
from latch.verified import pathway_enrichment

results = pathway_enrichment(
    gene_list=LatchFile("latch:///data/deg_list.txt"),
    organism="human",
    databases=["GO_Biological_Process", "KEGG", "Reactome"],
    output_dir="latch:///results/pathways"
)
```

* *支持的数据库：**
- 基因本体 (GO)
- KEGG 路径
- Reactome
- WikiPathways
- MSigDB集合

### 序列比对

* *MAFFT 多重序列比对：**
```python
from latch.verified import mafft
from latch.types import LatchFile

aligned = mafft(
    input_fasta=LatchFile("latch:///data/sequences.fasta"),
    algorithm="auto",
    output_format="fasta"
)
```

* *功能：**
- 多种比对算法（FFT-NS-1、FFT-NS-2、G-INS-i、 L-INS-i)
- 自动算法选择
- 支持大对齐
- 多种输出格式

### 适配器和质量修剪

* *修剪丰富：**
```python
from latch.verified import trim_galore

trimmed = trim_galore(
    fastq_r1=LatchFile("latch:///data/sample_R1.fastq.gz"),
    fastq_r2=LatchFile("latch:///data/sample_R2.fastq.gz"),
    quality_threshold=20,
    adapter_auto_detect=True
)
```

* *功能：**
- 自动接头检测
- 质量修剪
- 快速QC集成
- 支持单端和配对端

## 蛋白质结构预测

### AlphaFold

* *标准AlphaFold：**
```python
from latch.verified import alphafold
from latch.types import LatchFile

structure = alphafold(
    sequence_fasta=LatchFile("latch:///data/protein.fasta"),
    model_preset="monomer",
    use_templates=True,
    output_dir="latch:///results/alphafold"
)
```

* *功能：**
- 单体和多聚体预测
- 基于模板的建模选项
- MSA生成
- 置信度指标（pLDDT、PAE）
- PDB结构输出

* *模型预设：**
- `monomer`：单蛋白链
- `monomer_casp14`：CASP14 竞赛版本
- `monomer_ptm`：具有 pTM 置信度
- `multimer`：蛋白质复合物

### ColabFold

* *优化的 AlphaFold 替代方案：**
```python
from latch.verified import colabfold

structure = colabfold(
    sequence_fasta=LatchFile("latch:///data/protein.fasta"),
    num_models=5,
    use_amber_relax=True,
    output_dir="latch:///results/colabfold"
)
```

* *功能：**
- 比标准 AlphaFold
- MMseqs2 基于 MSA 生成
- 多个模型预测
- 琥珀色松弛
- 按置信度排名

* *优点：**
- MSA 生成速度加快 3-5 倍
- 计算成本更低
- 与 AlphaFold 类似的精度

## 单细胞分析

### ArchR (scATAC-seq)

* *染色质可及性分析：**
```python
from latch.verified import archr

results = archr(
    fragments_file=LatchFile("latch:///data/fragments.tsv.gz"),
    genome="hg38",
    output_dir="latch:///results/archr"
)
```

* *功能：**
- 箭头文件生成
- 质量控制指标
- 降维
- 聚类
- 峰识别
- 基序富集

### scVelo（RNA速度）

* *RNA速度分析：**
```python
from latch.verified import scvelo

results = scvelo(
    adata_file=LatchFile("latch:///data/adata.h5ad"),
    mode="dynamical",
    output_dir="latch:///results/scvelo"
)
```

* *特征：**
- 拼接/未拼接定量
- 速度估计
- 动力学建模
- 轨迹推断
- 可视化

### emptyDropsR（细胞调用）

* *空液滴检测：**
```python
from latch.verified import emptydrops

filtered_matrix = emptydrops(
    raw_matrix_dir=LatchDir("latch:///data/raw_feature_bc_matrix"),
    fdr_threshold=0.01
)
```

* *特点：**
- 区分细胞与空滴
- 基于FDR的阈值
- 环境RNA去除
- 与10X数据兼容

## 基因编辑分析

### CRISPResso2

* *CRISPR 编辑评估：**
```python
from latch.verified import crispresso2

results = crispresso2(
    fastq_r1=LatchFile("latch:///data/sample_R1.fastq.gz"),
    amplicon_sequence="AGCTAGCTAG...",
    guide_rna="GCTAGCTAGC",
    output_dir="latch:///results/crispresso"
)
```

* *功能：**
- Indel 定量
- 碱基编辑分析
- Prime 编辑分析
- HDR定量
- 等位基因频率图

## 系统发育

### 系统发育树构建

```python
from latch.verified import phylogenetics

tree = phylogenetics(
    alignment_file=LatchFile("latch:///data/aligned.fasta"),
    method="maximum_likelihood",
    bootstrap_replicates=1000,
    output_dir="latch:///results/phylo"
)
```

* *功能：**
- 多树构建方法
- Bootstrap 支持
- 树可视化
- 模型选择

## 工作流程集成

### 在自定义管道中使用经过验证的工作流程

```python
from latch import workflow, small_task
from latch.verified import bulk_rnaseq, deseq2
from latch.types import LatchFile, LatchDir

@workflow
def complete_rnaseq_analysis(
    fastq_files: List[LatchFile],
    metadata: LatchFile,
    output_dir: LatchDir
) -> LatchFile:
    """
    Complete RNA-seq analysis pipeline using verified workflows
    """
    # Run alignment for each sample
    aligned_samples = []
    for fastq in fastq_files:
        result = bulk_rnaseq(
            fastq_r1=fastq,
            reference_genome="hg38",
            output_dir=output_dir
        )
        aligned_samples.append(result)

    # Aggregate counts and run differential expression
    count_matrix = aggregate_counts(aligned_samples)
    deseq_results = deseq2(
        count_matrix=count_matrix,
        sample_metadata=metadata,
        design_formula="~ condition"
    )

    return deseq_results
```

## 最佳实践

### 何时使用经过验证的工作流程

* *使用经过验证的工作流程：**
1. 标准分析管道
2. 行之有效的方法
3. 生产就绪分析
4. 可重复研究
5. 经过验证的生物信息学工具

* *构建自定义工作流程：**
1. 新颖的分析方法
2. 自定义预处理步骤
3. 与专有工具
4集成。实验管道
5. 高度专业化的工作流程

### 结合已验证和自定义

```python
from latch import workflow, small_task
from latch.verified import alphafold
from latch.types import LatchFile

@small_task
def preprocess_sequence(raw_fasta: LatchFile) -> LatchFile:
    """Custom preprocessing"""
    # Custom logic here
    return processed_fasta

@small_task
def postprocess_structure(pdb_file: LatchFile) -> LatchFile:
    """Custom post-analysis"""
    # Custom analysis here
    return analysis_results

@workflow
def custom_structure_pipeline(input_fasta: LatchFile) -> LatchFile:
    """
    Combine custom steps with verified AlphaFold
    """
    # Custom preprocessing
    processed = preprocess_sequence(raw_fasta=input_fasta)

    # Use verified AlphaFold
    structure = alphafold(
        sequence_fasta=processed,
        model_preset="monomer_ptm"
    )

    # Custom post-processing
    results = postprocess_structure(pdb_file=structure)

    return results
```

## 访问工作流程文档

### 平台内文档

每个经过验证的工作流程包括：
- 参数说明
- 输入/输出规范
- 方法详细信息
- 引文信息
- 示例用法

### 查看可用工作流程

```python
from latch.verified import list_workflows

# List all available verified workflows
workflows = list_workflows()

for workflow in workflows:
    print(f"{workflow.name}: {workflow.description}")
```

## 版本管理

### 工作流程版本

已验证的工作流程已进行版本控制和维护：
- 错误修复和改进
- 添加新功能
- 维护向后兼容性
- 可用版本固定

### 使用特定版本

```python
from latch.verified import bulk_rnaseq

# Use specific version
results = bulk_rnaseq(
    fastq_r1=input_file,
    reference_genome="hg38",
    workflow_version="2.1.0"
)
```

## 支持和更新

### 获取帮助

- **文档**：https://docs.latch.bio
- **Slack 社区**：Latch SDK 工作区
- **支持**：support@latch.bio
- **GitHub 问题**：报告错误和请求功能

### 工作流程更新

已验证工作流程定期更新：
- 工具版本升级
- 性能改进
- 错误修复
- 新功能

订阅更新通知的发行说明。

## 常见用例

### 完整RNA-seq研究

```python
# 1. Quality control and alignment
aligned = bulk_rnaseq(fastq=samples)

# 2. Differential expression
deg = deseq2(counts=aligned)

# 3. Pathway enrichment
pathways = pathway_enrichment(genes=deg)
```

### 蛋白质结构分析

```python
# 1. Predict structure
structure = alphafold(sequence=protein_seq)

# 2. Custom analysis
results = analyze_structure(pdb=structure)
```

### 单细胞工作流程

```python
# 1. Filter cells
filtered = emptydrops(matrix=raw_counts)

# 2. RNA velocity
velocity = scvelo(adata=filtered)
```
