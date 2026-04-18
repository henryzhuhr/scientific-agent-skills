# 工作流程创建和注册

## 概述
Latch SDK 支持使用 Python 装饰器定义无服务器生物信息学工作流程，并通过自动容器化和 UI 生成来部署它们。

## 安装

安装 Latch SDK：
```bash
python3 -m pip install latch
```

* *先决条件：**
- Docker 必须在本地安装并运行
- 锁定帐户凭据

## 初始化新工作流程

创建新工作流程模板：
```bash
latch init <workflow-name>
```

这会生成一个工作流程目录，其中包含：
- `wf/__init__.py` - 主工作流程定义
- `Dockerfile` - 容器配置
- `version` - 版本跟踪文件

## 工作流程定义结构

### 基本工作流程示例

```python
from latch import workflow
from latch.types import LatchFile, LatchDir

@workflow
def my_workflow(input_file: LatchFile, output_dir: LatchDir) -> LatchFile:
    """
    Workflow description that appears in the UI

    Args:
        input_file: Input file description
        output_dir: Output directory description
    """
    return process_task(input_file, output_dir)
```

### 任务定义

任务是工作流程中的各个计算步骤：

```python
from latch import small_task, large_task

@small_task
def process_task(input_file: LatchFile, output_dir: LatchDir) -> LatchFile:
    """Task-level computation"""
    # Processing logic here
    return output_file
```

### 任务资源装饰器

SDK提供了多个任务满足不同资源需求的装饰器：

- `@small_task` - 轻量级任务的默认资源
- `@large_task` - 增加内存和CPU
- `@small_gpu_task` - 具有最少资源的启用GPU的任务
- `@large_gpu_task` - 具有最大资源的启用GPU的任务资源
- `@custom_task` - 自定义资源规范

## 注册工作流程

将工作流程注册到Latch平台：
```bash
latch register <workflow-directory>
```

注册流程：
1. 构建具有所有依赖项的 Docker 容器
2. 序列化工作流代码
3. 将容器上传到registry
4. 自动生成无代码 UI
5. 使工作流在平台上可用

### 注册输出

注册成功后：
- 工作流出现在Latch工作区中
- 使用参数形式自动生成UI
- 版本被跟踪并容器化
- 工作流可以立即执行

## 支持多管道语言

Latch 支持上传现有管道：
- **Python** - Native Latch SDK 工作流程
- **Nextflow** - 导入现有 Nextflow 管道
- **Snakemake** - 导入现有 Snakemake 管道

### Nextflow Integration

Import Nextflow pipelines:
```bash
latch register --nextflow <nextflow-directory>
```

### Snakemake Integration

Import Snakemake pipelines:
```bash
latch register --snakemake <snakemake-directory>
```

## 工作流程执行

### 从CLI

执行注册工作流程：
```bash
latch execute <workflow-name> --input-file <path> --output-dir <path>
```

### 来自Python

以编程方式执行工作流程：
```python
from latch.account import Account
from latch.executions import execute_workflow

account = Account.current()
execution = execute_workflow(
    workflow_name="my_workflow",
    parameters={
        "input_file": "/path/to/file",
        "output_dir": "/path/to/output"
    }
)
```

## 启动计划

启动计划定义预设参数配置：

```python
from latch.resources.launch_plan import LaunchPlan

# Define a launch plan with preset parameters
launch_plan = LaunchPlan.create(
    workflow_name="my_workflow",
    name="default_config",
    default_inputs={
        "input_file": "/data/sample.fastq",
        "output_dir": "/results"
    }
)
```

## 条件部分

使用条件参数部分创建动态UI：

```python
from latch.types import LatchParameter
from latch.resources.conditional import conditional_section

@workflow
def my_workflow(
    mode: str,
    advanced_param: str = conditional_section(
        condition=lambda inputs: inputs.mode == "advanced"
    )
):
    """Workflow with conditional parameters"""
    pass
```

## 最佳实践

1. **类型注释**：始终对工作流程参数使用类型提示
2. **文档字符串**：提供清晰的文档字符串 - 它们填充 UI 描述
3. **版本控制**：使用语义版本控制进行工作流更新
4. **测试**：注册之前在本地测试工作流程
5. **资源大小调整**：从较小的资源装饰器开始，然后根据需要进行扩展
6. **模块化设计**：将复杂的工作流程分解为可重用的任务
7. **错误处理**：在任务
8中实现正确的错误处理。 **日志记录**：使用Python日志记录进行调试和监控

## 常见模式

### 多步管道

```python
from latch import workflow, small_task
from latch.types import LatchFile

@small_task
def quality_control(input_file: LatchFile) -> LatchFile:
    """QC step"""
    return qc_output

@small_task
def alignment(qc_file: LatchFile) -> LatchFile:
    """Alignment step"""
    return aligned_output

@workflow
def rnaseq_pipeline(input_fastq: LatchFile) -> LatchFile:
    """RNA-seq analysis pipeline"""
    qc_result = quality_control(input_file=input_fastq)
    aligned = alignment(qc_file=qc_result)
    return aligned
```

### 并行处理

```python
from typing import List
from latch import workflow, small_task, map_task
from latch.types import LatchFile

@small_task
def process_sample(sample: LatchFile) -> LatchFile:
    """Process individual sample"""
    return processed_sample

@workflow
def batch_pipeline(samples: List[LatchFile]) -> List[LatchFile]:
    """Process multiple samples in parallel"""
    return map_task(process_sample)(sample=samples)
```

## 故障排除

### 常见问题

1. **Docker 未运行**：确保 Docker 守护进程处于活动状态
2. **身份验证错误**：运行 `latch login` 刷新凭证
3. **构建失败**：检查 Dockerfile 是否缺少依赖项
4. **类型错误**：确保所有参数都有正确的类型注释

### 调试模式

在注册期间启用详细日志记录：
```bash
latch register --verbose <workflow-directory>
```

## 参考文献

- 官方文档：https://docs.latch.bio
  - GitHub 存储库：https://github.com/latchbio/latch
  - Slack 社区：https://join.slack.com/t/latchbiosdk
