---
name: dnanexus-integration
description: DNAnexus 云基因组学平台。构建应用程序/小程序、管理数据（上传/下载）、dxpy Python SDK、运行工作流程、FASTQ/BAM/VCF，用于基因组学管道开发和执行。
license: Unknown
compatibility: Requires a DNAnexus account
metadata:
    skill-author: K-Dense Inc.
---

# DNAnexus 集成

## 概述

DNAnexus 是一个用于生物医学数据分析和基因组学的云平台。构建和部署应用程序/小程序、管理数据对象、运行工作流程以及使用 dxpy Python SDK 进行基因组学管道开发和执行。

## 何时使用此技能

此技能应在以下情况下使用：
- 创建、构建或修改 DNAnexus 应用程序/小程序
- 上传、下载、搜索或组织文件和记录
- 运行分析、监控作业、创建工作流程
- 使用 dxpy 编写脚本与平台交互
- 设置 dxapp.json、使用 Docker 管理依赖项
- 处理 FASTQ、BAM、VCF 或其他生物信息学文件
- 管理项目、权限或平台资源

## 核心能力

该技能分为五个主要领域，每个领域都有详细的参考文档：

### 1.应用程序开发

* *目的**：创建在DNAnexus平台上运行的可执行程序（应用程序/小程序）。

* *关键操作**：
- 生成应用程序骨架`dx-app-wizard`
- 使用正确的入口点编写 Python 或 Bash 应用程序
- 处理输入/输出数据对象
- 使用 `dx build` 或 `dx build --app`
 进行部署

* *常见用途案例**：
- 生物信息学管道（比对、变异调用）
- 数据处理工作流程
- 质量控制和过滤
- 格式转换工具

* *参考**：请参阅`references/app-development.md` 了解：
- 完整的应用程序结构和Patterns
- Python 入口点装饰器
- 使用 dxpy 进行输入/输出处理
- 开发最佳实践
- 常见问题和解决方案

### 2. 数据操作

* *目的**：管理平台上的文件、记录和其他数据对象。

* *关键操作**：
- 使用 `dxpy.upload_local_file()` 和 `dxpy.download_dxfile()`
 上传/下载文件
- 按名称、属性或类型搜索数据对象
- 在项目之间克隆数据
- 管理项目文件夹和权限

* *常用案例**：
- 上传测序数据（FASTQ文件）
- 整理分析结果
- 搜索特定样本或实验
- 跨项目备份数据
- 管理参考基因组和注释

* *参考**：参见`references/data-operations.md`用于：
- 完整文件和记录操作
- 数据对象生命周期（打开/关闭状态）
- 搜索和发现模式
- 项目管理
- 批量操作

### 3. 作业执行

* *目的**：运行分析、监控执行和编排工作流程。

* *关键操作**：
- 使用 `applet.run()` 或 `app.run()`
 启动作业 - 监视作业状态和日志
- 创建并行处理的子作业
- 构建并运行多步骤工作流程
- 具有输出的链接作业参考文献

* *常见用例**：
- 对测序数据运行基因组学分析
- 并行处理多个样本
- 多步骤分析管道
- 监控长时间运行的计算
- 调试失败的作业

* *参考**：参见`references/job-execution.md` 用于：
- 完整作业生命周期和状态
- 工作流创建和编排
- 并行执行模式
- 作业监控和调试
- 资源管理

### 4. Python SDK (dxpy)

* *用途**：通过 Python 以编程方式访问 DNAnexus 平台。

* *关键操作**：
- 使用数据对象处理程序（DXFile、DXRecord、DXApplet 等）
- 将高级函数用于常见任务
- 为高级任务进行直接 API 调用操作
- 在对象之间创建链接和引用
- 搜索和发现平台资源

* *常见用例**：
- 用于数据管理的自动化脚本
- 自定义分析管道
- 批处理工作流程
- 与外部工具集成
- 数据迁移和组织

* *参考**：请参阅`references/python-sdk.md`了解：
- 完整的dxpy类参考
- 高级实用函数
- API方法文档
- 错误处理模式
- 常用代码模式

### 5.配置和依赖

* *目的**：配置应用元数据并管理依赖。

* *关键操作**：
- 写入包含输入、输出和运行规范的 dxapp.json
- 安装系统包 (execDepends)
- 捆绑自定义工具和资源
- 使用共享依赖项的资产
- 集成 Docker 容器
- 配置实例类型和超时

* *通用案例**：
- 定义应用程序输入/输出规范
- 安装生物信息学工具（samtools、bwa 等）
- 管理Python 包依赖关系
- 在复杂环境中使用Docker 镜像
- 选择计算资源

* *参考**：参见`references/configuration.md` for:
- 完整的 dxapp.json 规范
- 依赖管理策略
- Docker 集成模式
- 区域和资源配置
- 示例配置

## 快速入门示例

### 上传和分析数据

```python
import dxpy

# Upload input file
input_file = dxpy.upload_local_file("sample.fastq", project="project-xxxx")

# Run analysis
job = dxpy.DXApplet("applet-xxxx").run({
    "reads": dxpy.dxlink(input_file.get_id())
})

# Wait for completion
job.wait_on_done()

# Download results
output_id = job.describe()["output"]["aligned_reads"]["$dnanexus_link"]
dxpy.download_dxfile(output_id, "aligned.bam")
```

### 搜索和下载文件

```python
import dxpy

# Find BAM files from a specific experiment
files = dxpy.find_data_objects(
    classname="file",
    name="*.bam",
    properties={"experiment": "exp001"},
    project="project-xxxx"
)

# Download each file
for file_result in files:
    file_obj = dxpy.DXFile(file_result["id"])
    filename = file_obj.describe()["name"]
    dxpy.download_dxfile(file_result["id"], filename)
```

### 创建简单应用程序

```python
# src/my-app.py
import dxpy
import subprocess

@dxpy.entry_point('main')
def main(input_file, quality_threshold=30):
    # Download input
    dxpy.download_dxfile(input_file["$dnanexus_link"], "input.fastq")

    # Process
    subprocess.check_call([
        "quality_filter",
        "--input", "input.fastq",
        "--output", "filtered.fastq",
        "--threshold", str(quality_threshold)
    ])

    # Upload output
    output_file = dxpy.upload_local_file("filtered.fastq")

    return {
        "filtered_reads": dxpy.dxlink(output_file)
    }

dxpy.run()
```

## 工作流程决策树

使用DNAnexus时，遵循此决策树：

1. **需要创建新的可执行文件？**
  - 是 → 使用 **应用程序开发** (references/app-development.md)
  - 否 → 继续步骤 2

2. **需要管理文件或数据？**
  - 是 → 使用 **数据操作** (references/data-operations.md)
  - 否 → 继续步骤 3

3. **需要运行分析或工作流程？**
  - 是 → 使用 **作业执行** (references/job-execution.md)
  - 否 → 继续步骤 4

4. **编写 Python 脚本实现自动化？**
  - 是 → 使用 **Python SDK** (references/python-sdk.md)
  - 否 → 继续执行步骤 5

5. **配置应用程序设置或依赖项？**
  - 是→使用**配置** (references/configuration.md)

通常您需要同时使用多种功能（例如，应用程序开发+配置，或数据操作+作业执行）。

## 安装和身份验证

### 安装dxpy

```bash
uv pip install dxpy
```

### 登录 DNAnexus

```bash
dx login
```

这将验证您的会话并设置对项目和数据的访问。

### 验证安装

```bash
dx --version
dx whoami
```

## 常见模式

### 模式1：批量处理

使用相同的分析处理多个文件：

```python
# Find all FASTQ files
files = dxpy.find_data_objects(
    classname="file",
    name="*.fastq",
    project="project-xxxx"
)

# Launch parallel jobs
jobs = []
for file_result in files:
    job = dxpy.DXApplet("applet-xxxx").run({
        "input": dxpy.dxlink(file_result["id"])
    })
    jobs.append(job)

# Wait for all completions
for job in jobs:
    job.wait_on_done()
```

### 模式2：多步流水线

链式多个分析一起：

```python
# Step 1: Quality control
qc_job = qc_applet.run({"reads": input_file})

# Step 2: Alignment (uses QC output)
align_job = align_applet.run({
    "reads": qc_job.get_output_ref("filtered_reads")
})

# Step 3: Variant calling (uses alignment output)
variant_job = variant_applet.run({
    "bam": align_job.get_output_ref("aligned_bam")
})
```

### 模式3：数据组织

系统地组织分析结果：

```python
# Create organized folder structure
dxpy.api.project_new_folder(
    "project-xxxx",
    {"folder": "/experiments/exp001/results", "parents": True}
)

# Upload with metadata
result_file = dxpy.upload_local_file(
    "results.txt",
    project="project-xxxx",
    folder="/experiments/exp001/results",
    properties={
        "experiment": "exp001",
        "sample": "sample1",
        "analysis_date": "2025-10-20"
    },
    tags=["validated", "published"]
)
```

## 最佳实践

1. **错误处理**：始终将 API 调用包装在 try- except 块
2 中。 **资源管理**：为工作负载选择适当的实例类型
3. **数据组织**：使用一致的文件夹结构和元数据
4. **成本优化**：归档旧数据，使用适当的存储类别
5. **文档**：在 dxapp.json
6 中包含清晰的描述。 **测试**：在生产使用
7之前测试具有各种输入类型的应用程序。 **版本控制**：对应用程序使用语义版本控制
8. **安全**：切勿在源代码中对凭据进行硬编码
9. **日志记录**：包括用于调试
10 的信息性日志消息。 **清理**：删除临时文件和失败的作业

## 资源

该技能包含详细的参考文档：

### references/

- **app-development.md** - 构建和部署应用程序/小程序的完整指南
- **data-operations.md** - 文件管理、记录、搜索和项目操作
- **job-execution.md** - 运行作业、工作流、监控和并行处理
- **python-sdk.md** - 包含所有类和内容的综合 dxpy 库参考函数
- **configuration.md** - dxapp.json 规范和依赖管理

当您需要有关特定操作的详细信息或处理复杂任务时加载这些参考。

## 获取帮助

- 官方文档：https://documentation.dnanexus.com/
- API 参考： http://autodoc.dnanexus.com/
- GitHub 存储库：https://github.com/dnanexus/dx-toolkit
- 支持：support@dnanexus.com
