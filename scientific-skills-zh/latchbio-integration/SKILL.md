---
name: latchbio-integration
description: 用于生物信息学工作流程的 Latch 平台。使用 Latch SDK、@workflow/@task 装饰器构建管道，部署无服务器工作流程、LatchFile/LatchDir、Nextflow/Snakemake 集成。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# LatchBio Integration

## 概述

Latch 是一个 Python 框架，用于将生物信息学工作流程构建和部署为无服务器管道。基于 Flyte 构建，使用 @workflow/@task 装饰器创建工作流、使用 LatchFile/LatchDir 管理云数据、配置资源以及集成 Nextflow/Snakemake 管道。

## 核心功能

Latch 平台提供四个主要功能领域：

### 1. 工作流创建和部署
- 使用 Python 定义无服务器工作流装饰器
- 支持原生 Python、Nextflow 和 Snakemake 管道
- 使用 Docker 自动容器化
- 自动生成的无代码用户界面
- 版本控制和可重复性

### 2. 数据管理
- 云存储抽象（LatchFile、 LatchDir)
- 带注册表的结构化数据组织（项目 → 表 → 记录）
- 带链接和枚举的类型安全数据操作
- 本地和云端之间的自动文件传输
- 文件选择的全局模式匹配

### 3. 资源配置
- 预配置任务装饰器（@small_task、@large_task、@small_gpu_task、@large_gpu_task）
- 自定义资源规格（CPU、内存、GPU、存储）
- GPU 支持（K80、V100、A100）
- 超时和存储配置
- 成本优化策略

### 4. 验证工作流程
- 生产就绪的预建管道
- 批量RNA-seq、DESeq2、通路分析
- 用于蛋白质结构预测的AlphaFold 和ColabFold
- 单细胞工具（ArchR、scVelo、emptyDropsR）
- CRISPR 分析、系统发育学等

## 快速入门

### 安装和设置

```bash
# Install Latch SDK
python3 -m uv pip install latch

# Login to Latch
latch login

# Initialize a new workflow
latch init my-workflow

# Register workflow to platform
latch register my-workflow
```

* *先决条件：**
- Docker 安装并运行
- 锁定帐户凭据
- Python 3.8+

### 基本工作流程示例

```python
from latch import workflow, small_task
from latch.types import LatchFile

@small_task
def process_file(input_file: LatchFile) -> LatchFile:
    """Process a single file"""
    # Processing logic
    return output_file

@workflow
def my_workflow(input_file: LatchFile) -> LatchFile:
    """
    My bioinformatics workflow

    Args:
        input_file: Input data file
    """
    return process_file(input_file=input_file)
```

## 何时使用此技能

遇到以下任一场景时应使用此技能：

* *工作流程开发：**
- “为 RNA-seq 分析创建 Latch 工作流程”
- “将我的管道部署到 Latch”
- “将我的 Nextflow 管道转换为 Latch”
- “向我的工作流程添加 GPU 支持”
- 使用`@workflow`、`@task` 装饰器

* *数据管理：**
- “在 Latch 注册表中组织我的测序数据”
- “如何使用 LatchFile 和 LatchDir？”
- “在 Latch 中设置样本跟踪”
- 使用 `latch:///`路径

* *资源配置：**
- “为闩锁上的AlphaFold配置GPU”
- “我的任务内存不足”
- “如何优化工作流程成本？”
- 使用任务装饰器

* *验证的工作流程：**
- “在锁存器上运行 AlphaFold”
- “使用 DESeq2 进行差异表达”
- “可用的预构建工作流程”
- 使用 `latch.verified` 模块

## 详细文档

此技能包括按功能组织的综合参考文档：

### references/workflow-creation.md
* *阅读此内容：**
- 创建和注册工作流程
- 任务定义和装饰器
- 支持 Python、Nextflow、Snakemake
- 启动计划和条件部分
- 工作流程执行（CLI 和编程）
- 多步骤和并行管道
- 注册问题故障排除

* *关键主题：**
- `latch init` 和 `latch register` 命令
- `@workflow` 和 `@task`装饰器
- LatchFile 和 LatchDir 基础知识
- 类型注释和文档字符串
- 使用预设参数启动计划
- 条件 UI 部分

### references/data-management.md
* *阅读此内容：**
- 带 LatchFile 和 LatchDir 的云存储
- 注册表系统（项目、表、记录）
- 链接记录和关系
- 枚举和类型列
- 批量操作和事务
- 与工作流程集成
- 帐户和工作区管理

* *关键主题：**
- `latch:///` 路径格式
- 文件传输和全局模式
- 创建和查询注册表
- 列类型（字符串、数字、文件、链接、枚举）
- 记录CRUD 操作
- 工作流-注册表集成

### 引用/资源配置.md
* *阅读此内容：**
- 任务资源装饰器
- 自定义 CPU、内存、GPU 配置
- GPU 类型（K80、V100、 A100)
- 超时和存储设置
- 资源优化策略
- 经济高效的工作流程设计
- 监控和调试

* *关键主题：**
- `@small_task`、`@large_task`、`@small_gpu_task`、 `@large_gpu_task`
- `@custom_task` 具有精确的规格
- 多 GPU 配置
- 按工作负载类型选择资源
- 平台限制和配额

### 引用/验证的工作流程.md
* *阅读此内容用于：**
- 预构建的生产工作流程
- Bulk RNA-seq 和 DESeq2
- AlphaFold 和 ColabFold
- 单细胞分析（ArchR、scVelo）
- CRISPR 编辑分析
- 通路丰富
- 与自定义工作流程集成

* *关键主题：**
- `latch.verified` 模块导入
- 可用的已验证工作流程
- 工作流程参数和选项
- 组合已验证和自定义步骤
- 版本管理

## 常见工作流程模式

### 完整的RNA-seq管道

```python
from latch import workflow, small_task, large_task
from latch.types import LatchFile, LatchDir

@small_task
def quality_control(fastq: LatchFile) -> LatchFile:
    """Run FastQC"""
    return qc_output

@large_task
def alignment(fastq: LatchFile, genome: str) -> LatchFile:
    """STAR alignment"""
    return bam_output

@small_task
def quantification(bam: LatchFile) -> LatchFile:
    """featureCounts"""
    return counts

@workflow
def rnaseq_pipeline(
    input_fastq: LatchFile,
    genome: str,
    output_dir: LatchDir
) -> LatchFile:
    """RNA-seq analysis pipeline"""
    qc = quality_control(fastq=input_fastq)
    aligned = alignment(fastq=qc, genome=genome)
    return quantification(bam=aligned)
```

### GPU加速工作流程

```python
from latch import workflow, small_task, large_gpu_task
from latch.types import LatchFile

@small_task
def preprocess(input_file: LatchFile) -> LatchFile:
    """Prepare data"""
    return processed

@large_gpu_task
def gpu_computation(data: LatchFile) -> LatchFile:
    """GPU-accelerated analysis"""
    return results

@workflow
def gpu_pipeline(input_file: LatchFile) -> LatchFile:
    """Pipeline with GPU tasks"""
    preprocessed = preprocess(input_file=input_file)
    return gpu_computation(data=preprocessed)
```

### 注册表集成工作流程

```python
from latch import workflow, small_task
from latch.registry.table import Table
from latch.registry.record import Record
from latch.types import LatchFile

@small_task
def process_and_track(sample_id: str, table_id: str) -> str:
    """Process sample and update Registry"""
    # Get sample from registry
    table = Table.get(table_id=table_id)
    records = Record.list(table_id=table_id, filter={"sample_id": sample_id})
    sample = records[0]

    # Process
    input_file = sample.values["fastq_file"]
    output = process(input_file)

    # Update registry
    sample.update(values={"status": "completed", "result": output})
    return "Success"

@workflow
def registry_workflow(sample_id: str, table_id: str):
    """Workflow integrated with Registry"""
    return process_and_track(sample_id=sample_id, table_id=table_id)
```

## 最佳实践

### 工作流程设计
1. 对所有参数使用类型注释
2. 编写清晰的文档字符串（出现在 UI 中）
3. 从标准任务装饰器开始，根据需要进行扩展
4. 将复杂的工作流程分解为模块化任务
5. 实施正确的错误处理

### 数据管理
6. 使用一致的文件夹结构
7. 在批量输入之前定义注册表架构
8. 使用关系的链接记录
9. 将元数据存储在注册表中以进行追溯

### 资源配置
10. 适当大小的资源（不要过度分配）
11. 仅当算法支持时才使用 GPU
12. 监控执行指标并优化
13. 尽可能设计并行执行

### 开发工作流程
14. 注册前使用 Docker 在本地进行测试
15. 对工作流代码
16使用版本控制。文档资源要求
17. 配置文件工作流程以确定实际需求

## 故障排除

### 常见问题

* *注册失败：**
- 确保 Docker 正在运行
- 使用 `latch login`
- 检查 Dockerfile 中的所有依赖项
- 使用用于详细日志的 `--verbose` 标志

* *资源问题：**
- 内存不足：增加任务装饰器中的内存
- 超时：增加超时参数
- 存储问题：增加临时存储_gib

* *数据访问：**
- 使用正确的`latch:///` 路径格式
- 验证工作区中是否存在文件
- 检查共享工作区的权限

* *类型错误：**
- 向所有参数添加类型注释
- 对文件/目录参数使用 LatchFile/LatchDir
- 确保工作流返回类型与实际匹配return

## 其他资源

- **官方文档**：https://docs.latch.bio
- **GitHub存储库**：https://github.com/latchbio/latch
- **Slack社区**：加入Latch SDK工作区
- **API参考**：https://docs.latch.bio/api/latch.html
- **博客**： https://blog.latch.bio

## 支持

如有问题或疑问：
1. 检查上面的文档链接
2. 搜索 GitHub 问题
3. 在 Slack 社区询问
4. 联系support@latch.bio
