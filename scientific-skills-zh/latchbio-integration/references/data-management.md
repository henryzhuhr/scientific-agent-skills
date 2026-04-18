# 数据管理

## 概述
Latch 通过云存储抽象（LatchFile、LatchDir）和用于组织实验数据的结构化Registry 系统提供全面的数据管理。

## 云存储：LatchFile 和LatchDir

### LatchFile

表示Latch 云存储中的一个文件system.

```python
from latch.types import LatchFile

# Create reference to existing file
input_file = LatchFile("latch:///data/sample.fastq")

# Access file properties
file_path = input_file.local_path  # Local path when executing
file_remote = input_file.remote_path  # Cloud storage path
```

### LatchDir

代表Latch的云存储系统中的一个目录。

```python
from latch.types import LatchDir

# Create reference to directory
output_dir = LatchDir("latch:///results/experiment_1")

# Directory operations
all_files = output_dir.glob("*.bam")  # Find files matching pattern
subdirs = output_dir.iterdir()  # List contents
```

### 路径格式

Latch存储使用特殊的URL方案：
- **Latch paths**：`latch:///path/to/file`
- **本地路径**：工作流执行时自动解析
- **S3 paths**：配置后可直接使用

### 文件传输

本地执行和云存储之间自动传输文件：

```python
from latch import small_task
from latch.types import LatchFile

@small_task
def process_file(input_file: LatchFile) -> LatchFile:
    # File is automatically downloaded to local execution
    local_path = input_file.local_path

    # Process the file
    with open(local_path, 'r') as f:
        data = f.read()

    # Write output
    output_path = "output.txt"
    with open(output_path, 'w') as f:
        f.write(processed_data)

    # Automatically uploaded back to cloud storage
    return LatchFile(output_path, "latch:///results/output.txt")
```

### 全局模式

使用模式匹配查找文件：

```python
from latch.types import LatchDir

data_dir = LatchDir("latch:///data")

# Find all FASTQ files
fastq_files = data_dir.glob("**/*.fastq")

# Find files in subdirectories
bam_files = data_dir.glob("alignments/**/*.bam")

# Multiple patterns
results = data_dir.glob("*.{bam,sam}")
```

## 注册表系统

注册表提供包含项目、表和记录的结构化数据组织。

### 注册表架构

```
Account/Workspace
└── Projects
    └── Tables
        └── Records
```

### 使用项目

```python
from latch.registry.project import Project

# Get or create a project
project = Project.create(
    name="RNA-seq Analysis",
    description="Bulk RNA-seq experiments"
)

# List existing projects
all_projects = Project.list()

# Get project by ID
project = Project.get(project_id="proj_123")
```

### 使用表

表存储结构化数据记录：

```python
from latch.registry.table import Table

# Create a table
table = Table.create(
    project_id=project.id,
    name="Samples",
    columns=[
        {"name": "sample_id", "type": "string"},
        {"name": "condition", "type": "string"},
        {"name": "replicate", "type": "number"},
        {"name": "fastq_file", "type": "file"}
    ]
)

# List tables in project
tables = Table.list(project_id=project.id)

# Get table by ID
table = Table.get(table_id="tbl_456")
```

### 列类型

支持的数据类型：
- `string` - 文本数据
- `number` - 数值（整数或浮点数）
- `boolean` - 真/假值
- `date` - 日期值
- `file` - LatchFile引用
- `directory` - LatchDir 引用
- `link` - 对其他表中的记录的引用
- `enum` - 预定义列表中的枚举值

### 使用记录

```python
from latch.registry.record import Record

# Create a record
record = Record.create(
    table_id=table.id,
    values={
        "sample_id": "S001",
        "condition": "treated",
        "replicate": 1,
        "fastq_file": LatchFile("latch:///data/S001.fastq")
    }
)

# Bulk create records
records = Record.bulk_create(
    table_id=table.id,
    records=[
        {"sample_id": "S001", "condition": "treated"},
        {"sample_id": "S002", "condition": "control"}
    ]
)

# Query records
all_records = Record.list(table_id=table.id)
filtered = Record.list(
    table_id=table.id,
    filter={"condition": "treated"}
)

# Update record
record.update(values={"replicate": 2})

# Delete record
record.delete()
```

### 链接记录

创建表之间的关系：

```python
# Define table with link column
results_table = Table.create(
    project_id=project.id,
    name="Results",
    columns=[
        {"name": "sample", "type": "link", "target_table": samples_table.id},
        {"name": "alignment_bam", "type": "file"},
        {"name": "gene_counts", "type": "file"}
    ]
)

# Create record with link
result_record = Record.create(
    table_id=results_table.id,
    values={
        "sample": sample_record.id,  # Link to sample record
        "alignment_bam": LatchFile("latch:///results/aligned.bam"),
        "gene_counts": LatchFile("latch:///results/counts.tsv")
    }
)

# Access linked data
sample_data = result_record.values["sample"].resolve()
```

### 枚举列

使用预定义的列值：

```python
table = Table.create(
    project_id=project.id,
    name="Experiments",
    columns=[
        {
            "name": "status",
            "type": "enum",
            "options": ["pending", "running", "completed", "failed"]
        }
    ]
)
```

### 事务和批量更新

E高效更新多条记录：

```python
from latch.registry.transaction import Transaction

# Start transaction
with Transaction() as txn:
    for record in records:
        record.update(values={"status": "processed"}, transaction=txn)
    # Changes committed when exiting context
```

## 与工作流程集成

### 在工作流程中使用注册表

```python
from latch import workflow, small_task
from latch.types import LatchFile
from latch.registry.table import Table
from latch.registry.record import Record

@small_task
def process_and_save(sample_id: str, table_id: str) -> str:
    # Get sample from registry
    table = Table.get(table_id=table_id)
    records = Record.list(
        table_id=table_id,
        filter={"sample_id": sample_id}
    )
    sample = records[0]

    # Process file
    input_file = sample.values["fastq_file"]
    # ... processing logic ...

    # Save results back to registry
    sample.update(values={
        "status": "completed",
        "results_file": output_file
    })

    return "Success"

@workflow
def registry_workflow(sample_id: str, table_id: str):
    """Workflow integrated with Registry"""
    return process_and_save(sample_id=sample_id, table_id=table_id)
```

### 在数据上自动执行工作流程

将工作流程配置为在将数据添加到注册表文件夹时自动运行：

```python
from latch.resources.launch_plan import LaunchPlan

# Create launch plan that watches a folder
launch_plan = LaunchPlan.create(
    workflow_name="rnaseq_pipeline",
    name="auto_process",
    trigger_folder="latch:///incoming_data",
    default_inputs={
        "output_dir": "latch:///results"
    }
)
```

## 帐户和工作空间管理

### 帐户信息

```python
from latch.account import Account

# Get current account
account = Account.current()

# Account properties
workspace_id = account.id
workspace_name = account.name
```

### 团队工作空间

访问共享团队工作空间：

```python
# List available workspaces
workspaces = Account.list()

# Switch workspace
Account.set_current(workspace_id="ws_789")
```

## 数据操作函数

### 加入数据

`latch.functions`模块提供数据操作实用程序：

```python
from latch.functions import left_join, inner_join, outer_join, right_join

# Join tables
combined = left_join(
    left_table=table1,
    right_table=table2,
    on="sample_id"
)
```

### 过滤

```python
from latch.functions import filter_records

# Filter records
filtered = filter_records(
    table=table,
    condition=lambda record: record["replicate"] > 1
)
```

### 机密管理

安全地存储和检索机密：

```python
from latch.functions import get_secret

# Retrieve secret in workflow
api_key = get_secret("api_key")
```

## 最佳做法

1. **路径组织**：使用一致的文件夹结构（例如，`/data`、`/results`、`/logs`）
2. **注册表架构**：在批量数据输入之前定义表架构
3. **链接记录**：使用链接来维护实验之间的关系
4. **批量操作**：使用事务更新多个记录
5. **文件命名**：使用一致的描述性文件命名约定
6. **元数据**：将实验元数据存储在注册表中以进行追溯
7. **验证**：创建记录时验证数据类型
8. **清理**：定期归档或删除未使用的数据

## 常见模式

### 样本跟踪

```python
# Create samples table
samples = Table.create(
    project_id=project.id,
    name="Samples",
    columns=[
        {"name": "sample_id", "type": "string"},
        {"name": "collection_date", "type": "date"},
        {"name": "raw_fastq_r1", "type": "file"},
        {"name": "raw_fastq_r2", "type": "file"},
        {"name": "status", "type": "enum", "options": ["pending", "processing", "complete"]}
    ]
)
```

### 结果组织

```python
# Create results table linked to samples
results = Table.create(
    project_id=project.id,
    name="Analysis Results",
    columns=[
        {"name": "sample", "type": "link", "target_table": samples.id},
        {"name": "alignment_bam", "type": "file"},
        {"name": "variants_vcf", "type": "file"},
        {"name": "qc_metrics", "type": "file"}
    ]
)
```
