---
name: get-available-resources
description: 此技能应在任何计算密集型科学任务开始时使用，以检测和报告可用的系统资源（CPU 内核、GPU、内存、磁盘空间）。它创建一个包含资源信息和战略建议的 JSON 文件，为计算方法决策提供信息，例如是否使用并行处理（joblib、多处理）、核外计算（Dask、Zarr）、GPU 加速（PyTorch、JAX）或内存高效策略。在运行分析、训练模型、处理大型数据集或任何资源限制很重要的任务之前使用此技能。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 获取可用资源

## 概述

检测可用计算资源并为科学计算任务生成战略建议。此技能可自动识别 CPU 功能、GPU 可用性（NVIDIA CUDA、AMD ROCm、Apple Silicon Metal）、内存限制和磁盘空间，以帮助就计算方法做出明智的决策。

## 何时使用此技能

在任何计算密集型任务之前主动使用此技能：

- **数据分析之前**：确定数据集是否可以加载到内存中或需要核外处理
- **模型训练之前**：检查 GPU 加速是否可用以及使用哪个后端
- **并行处理之前**：确定 joblib、多处理或 Dask 的最佳工作线程数量
- **大文件操作之前**：验证足够的磁盘空间和适当的存储策略
- **项目初始化时**：了解做出架构决策的基线功能

* *示例场景：**
- “帮我分析这个 50GB 基因组数据集”→ 首先使用此技能确定是否需要 Dask/Zarr
- “根据此数据训练神经网络”→使用此技能检测可用的 GPU 和后端
- “并行处理 10,000 个文件”→使用此技能确定最佳工作人员数量
- “运行计算密集型模拟”→使用此技能来了解资源限制

## 此技能如何工作

### 资源检测

该技能运行`scripts/detect_resources.py`以自动检测：

1. **CPU 信息**
  - 物理和逻辑核心计数
  - 处理器架构和型号
  - CPU 频率信息

2. **GPU 信息**
  - NVIDIA GPU：通过 nvidia-smi 检测，报告 VRAM、驱动程序版本、计算能力
  - AMD GPU：通过 rocm-smi 检测
  - Apple Silicon：检测具有金属支持和统一内存的 M1/M2/M3/M4 芯片

3. **内存信息**
  - 总和可用 RAM
  - 当前内存使用百分比
  - 交换空间可用性

4. **磁盘空间信息**
  - 工作目录的总磁盘空间和可用磁盘空间
  - 当前使用百分比

5. **操作系统信息**
  - 操作系统类型（macOS、Linux、Windows）
  - 操作系统版本和版本
  - Python版本

### 输出格式

该技能在当前工作目录中生成`.claude_resources.json`文件包含：

```json
{
  "timestamp": "2025-10-23T10:30:00",
  "os": {
    "system": "Darwin",
    "release": "25.0.0",
    "machine": "arm64"
  },
  "cpu": {
    "physical_cores": 8,
    "logical_cores": 8,
    "architecture": "arm64"
  },
  "memory": {
    "total_gb": 16.0,
    "available_gb": 8.5,
    "percent_used": 46.9
  },
  "disk": {
    "total_gb": 500.0,
    "available_gb": 200.0,
    "percent_used": 60.0
  },
  "gpu": {
    "nvidia_gpus": [],
    "amd_gpus": [],
    "apple_silicon": {
      "name": "Apple M2",
      "type": "Apple Silicon",
      "backend": "Metal",
      "unified_memory": true
    },
    "total_gpus": 1,
    "available_backends": ["Metal"]
  },
  "recommendations": {
    "parallel_processing": {
      "strategy": "high_parallelism",
      "suggested_workers": 6,
      "libraries": ["joblib", "multiprocessing", "dask"]
    },
    "memory_strategy": {
      "strategy": "moderate_memory",
      "libraries": ["dask", "zarr"],
      "note": "Consider chunking for datasets > 2GB"
    },
    "gpu_acceleration": {
      "available": true,
      "backends": ["Metal"],
      "suggested_libraries": ["pytorch-mps", "tensorflow-metal", "jax-metal"]
    },
    "large_data_handling": {
      "strategy": "disk_abundant",
      "note": "Sufficient space for large intermediate files"
    }
  }
}
```

### 战略建议

该技能生成上下文感知建议：

* *并行处理建议：**
- **高并行性（8+ 核心）**：使用 Dask、joblib 或多处理，workers = cores - 2
- **中等并行度（4-7 核）**：使用 joblib 或多处理，workers = 核 - 1
- **顺序（< 4 核）**：首选顺序处理以避免开销

* *内存策略建议：**
- **内存受限（< 4GB 可用）**：使用用于核外处理的 Zarr、Dask 或 H5py
- **中等内存（4-16GB 可用）**：对于 > 2GB 的数据集使用 Dask/ZarrZXXQNL26QXZ- **内存充足（> 16GB 可用）**：可以直接将大多数数据集加载到内存中

* *GPU 加速建议：**
- **检测到 NVIDIA GPU**：使用 PyTorch、TensorFlow、JAX、CuPy 或 RAPIDS
- **检测到 AMD GPU**：使用 PyTorch-ROCm 或 TensorFlow-ROCm
- **检测到 Apple Silicon**：将 PyTorch 与 MPS 后端、TensorFlow-Metal 或JAX-Metal
- **未检测到 GPU**：使用 CPU 优化的库

* *大数据处理建议：**
- **磁盘受限（< 10GB）**：使用流式或压缩策略
- **中等磁盘（10-100GB）**：使用 Zarr、H5py 或 Parquet 格式
- **磁盘充裕（> 100GB）**：可以自由创建大型中间文件

## 用法说明

### 步骤1：运行资源检测

在任何计算密集型任务开始时执行检测脚本：

```bash
python scripts/detect_resources.py
```

可选参数：
- `-o, --output <path>`：指定自定义输出路径（默认：`.claude_resources.json`）
- `-v, --verbose`：将完整资源信息打印到stdout

### 步骤2：读取并应用建议

运行检测后，读取生成的`.claude_resources.json`文件以告知计算决策：

```python
# Example: Use recommendations in code
import json

with open('.claude_resources.json', 'r') as f:
    resources = json.load(f)

# Check parallel processing strategy
if resources['recommendations']['parallel_processing']['strategy'] == 'high_parallelism':
    n_jobs = resources['recommendations']['parallel_processing']['suggested_workers']
    # Use joblib, Dask, or multiprocessing with n_jobs workers

# Check memory strategy
if resources['recommendations']['memory_strategy']['strategy'] == 'memory_constrained':
    # Use Dask, Zarr, or H5py for out-of-core processing
    import dask.array as da
    # Load data in chunks

# Check GPU availability
if resources['recommendations']['gpu_acceleration']['available']:
    backends = resources['recommendations']['gpu_acceleration']['backends']
    # Use appropriate GPU library based on available backend
```

### 步骤3：做出明智的决策

使用资源信息和做出战略选择的建议：

* *用于数据加载：**
```python
memory_available_gb = resources['memory']['available_gb']
dataset_size_gb = 10

if dataset_size_gb > memory_available_gb * 0.5:
    # Dataset is large relative to memory, use Dask
    import dask.dataframe as dd
    df = dd.read_csv('large_file.csv')
else:
    # Dataset fits in memory, use pandas
    import pandas as pd
    df = pd.read_csv('large_file.csv')
```

* *用于并行处理：**
```python
from joblib import Parallel, delayed

n_jobs = resources['recommendations']['parallel_processing'].get('suggested_workers', 1)

results = Parallel(n_jobs=n_jobs)(
    delayed(process_function)(item) for item in data
)
```

* *用于GPU加速：**
```python
import torch

if 'CUDA' in resources['gpu']['available_backends']:
    device = torch.device('cuda')
elif 'Metal' in resources['gpu']['available_backends']:
    device = torch.device('mps')
else:
    device = torch.device('cpu')

model = model.to(device)
```

## 依赖项

检测脚本需要以下Python包：

```bash
uv pip install psutil
```

所有其他功能使用Python标准库模块（json、os、platform、subprocess、sys、pathlib）。

## 平台支持

- **macOS**：完全支持，包括Apple Silicon（M1/M2/M3/M4） GPU 检测
- **Linux**：完全支持包括 NVIDIA (nvidia-smi)和 AMD (rocm-smi) GPU 检测
- **Windows**：完全支持包括 NVIDIA GPU 检测

## 最佳实践

1. **早期运行**：在项目开始时或主要计算任务之前执行资源检测
2. **定期重新运行**：系统资源随时间变化（内存使用、磁盘空间）
3. **扩展前检查**：在扩展并行工作线程或数据大小之前验证资源
4. **记录决策**：将 `.claude_resources.json` 文件保留在项目目录中，以记录资源感知决策
5. **与版本控制一起使用**：不同的机器有不同的功能；资源文件有助于保持可移植性

## 故障排除

* *未检测到 GPU：**
- 确保安装了 GPU 驱动程序（nvidia-smi、rocm-smi 或适用于 Apple Silicon 的 system_profiler）
- 检查 GPU 实用程序是否在系统 PATH
- 验证 GPU 是否被其他进程使用

* *脚本执行失败：**
- 确保安装了 psutil：`uv pip install psutil`
- 检查 Python 版本兼容性 (Python 3.6+)
- 验证脚本是否具有执行权限：`chmod +x scripts/detect_resources.py`

* *内存读数不准确：**
- 内存读数是快照；实际可用内存不断变化
- 在检测准确的“可用”内存之前关闭其他应用程序
- 考虑多次运行检测并平均结果
