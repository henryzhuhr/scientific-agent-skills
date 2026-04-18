# TimesFM

## 的系统要求硬件层

TimesFM 可以在各种硬件配置上运行。本指南可帮助您
为您的机器选择正确的设置和调整性能。

### 第 1 层：最小（仅 CPU，4–8 GB RAM）

- **用例**：轻度探索、单系列预测、原型设计
- **模型**：仅限 TimesFM 2.5 (200M)
- **批量大小**：`per_core_batch_size=4`
- **上下文**：限制 `max_context=512`
- **预期速度**：每 100 点系列约 2–5 秒

```python
model.compile(timesfm.ForecastConfig(
    max_context=512,
    max_horizon=128,
    per_core_batch_size=4,
    normalize_inputs=True,
    use_continuous_quantile_head=True,
    fix_quantile_crossing=True,
))
```

### 第 2 层：标准（CPU 16 GB 或 GPU 4–8 GB） VRAM)

- **用例**：批量预测（数十个系列）、评估、生产原型
- **模型**：TimesFM 2.5 (200M)
- **批量大小**：`per_core_batch_size=32` (CPU)或 `64` (GPU)
- **上下文**： `max_context=1024`
- **预期速度**：每 100 点系列约 0.5–1 秒 (GPU)

```python
model.compile(timesfm.ForecastConfig(
    max_context=1024,
    max_horizon=256,
    per_core_batch_size=64,
    normalize_inputs=True,
    use_continuous_quantile_head=True,
    fix_quantile_crossing=True,
))
```

### 第 3 层：生产（GPU 16+ GB VRAM 或 Apple Silicon 32+ GB）

- **用例**：大规模批量预测（数千个系列），长上下文
- **型号**：TimesFM 2.5 (200M)
- **批量大小**：`per_core_batch_size=128–256`
- **上下文**：`max_context=4096` 或更高
- **预期速度**：约0.1–0.3 秒/ 100 点系列

```python
model.compile(timesfm.ForecastConfig(
    max_context=4096,
    max_horizon=256,
    per_core_batch_size=128,
    normalize_inputs=True,
    use_continuous_quantile_head=True,
    fix_quantile_crossing=True,
))
```

### 第 4 层：旧型号（v1.0/v2.0 — 500M 参数）

- **⚠️ 警告**：TimesFM v2.0 (500M)需要 **≥ 16 GB RAM** (CPU)或 **≥ 8 GB VRAM** (GPU)
- **⚠️ 警告**：TimesFM v1.0 旧版 JAX 版本可能需要 **≥ 32 GB RAM**
- **建议**：除非您特别需要旧版检查点，否则使用 TimesFM 2.5

## 内存估计

### CPU 内存 (RAM)

近似值推理期间的RAM使用情况：

|组件|时代FM 2.5 (200M) |时代FM 2.0 (500M) |
| --------- | ------------------- | ------------------- |
|模型重量 | 〜800 MB | ~2 GB |
|运行时开销| 〜500 MB | ~1 GB |
|输入/输出缓冲器|每 1000 个系列约 200 MB |每 1000 个系列约 500 MB |
| **总计（小批量）** | **~1.5 GB** | **~3.5 GB** |
| **总计（大批量）** | **~3 GB** | **~6 GB** |

* *公式**：`RAM ≈ model_weights + 0.5 GB + (0.2 MB × num_series × context_length / 1000)`

### GPU 内存（VRAM）

|组件|时代FM 2.5 (200M) |
| --------- | ------------------- |
|模型重量 | ~800 MB |
| KV 缓存 + 激活 | ~200–500 MB（根据上下文缩放）|
|批处理缓冲区 | context=1024 |
| 时每 100 个系列约 100 MB **总计（批次=32）** | **~1.2 GB** |
| **总计（批次=128）** | **~1.8 GB** |
| **总计（批次=256）** | **~2.5 GB** |

### 磁盘空间

|项目 |尺寸|
| ---- | ---- |
| TimesFM 2.5 安全张量 | TimesFM 2.5 ~800 MB |
|拥抱人脸缓存开销| ~200 MB |
| **总下载量** | **~1 GB** |

模型权重从 Hugging Face Hub 下载一次并缓存在
`~/.cache/huggingface/`（或 `$HF_HOME`）中。

## GPU 选择指南

### NVIDIA GPU (CUDA)

|图形处理器 |显存 |推荐批次|备注|
| --- | ---- | ----------------- | ----- |
| RTX 3060 | 12GB| 64 | 64入门级好|
| RTX 3090 / 4090 | 24GB| 256 | 256非常适合生产|
| A100（40GB）| 40GB| 512 | 512云/HPC |
| A100（80 GB）| 80GB| 1024 | 1024云/HPC |
| T4 | 16GB| 128 | 128云（Colab、AWS）|
| V100 | 16–32 GB | 128–256 | 128–256云 |

### Apple Silicon (MPS)

|芯片|统一内存|推荐批次|备注|
| ---- | -------------- | ----------------- | ----- |
| M1 | 8–16 GB | 16–32 |可以工作，比 CUDA 慢 |
| M1 Pro/Max | M1 Pro/Max | 16–64 GB | 32–128 |性能好|
| M2/M3/M4 Pro/Max | 18–128 GB | 64–256 |优秀 |

### 仅 CPU

适用于任何具有足够 RAM 的 CPU。预计比 GPU 慢 5–20 倍。

## Python 和包要求

|要求 |最低 |推荐|
| ----------- | -------- | ----------- |
|蟒蛇 | 3.10 | 3.10 3.12+ |
|麻木 | 1.26.4 |最新|
|火炬| 2.0.0 |最新|
|拥抱脸集线器 | 0.23.0 |最新|
|安全张量 | 0.5.3 |最新 |

### 可选依赖项

|套餐 |目的|安装|
| -------- | -------- | -------- |
|贾克斯 |亚麻后端 | `pip install jax[cuda]` |
|亚麻|亚麻后端 | `pip install flax` |
| scikit-learn | XReg 协变量 | `pip install scikit-learn` |

## 操作系统兼容性

|操作系统 |状态 |备注|
| --| ------ | ----- |
| Linux（Ubuntu 20.04+）| ✅ 全力支持 | CUDA 最佳性能 |
| macOS 13+（文图拉）| ✅ 全力支持 | Apple Silicon 上的 MPS 加速 |
| Windows 11 + WSL2 | ✅ 支持 |使用WSL2以获得最佳体验|
| Windows（本机）| ⚠️部分| PyTorch 工作，一些边缘情况 |

## 故障排除

### 内存不足 (OOM)

```python
# Reduce batch size
model.compile(timesfm.ForecastConfig(
    per_core_batch_size=4,  # Start very small
    max_context=512,        # Reduce context
    ...
))

# Process in chunks
for i in range(0, len(inputs), 50):
    chunk = inputs[i:i+50]
    p, q = model.forecast(horizon=H, inputs=chunk)
```

### CPU 上的推理速度慢

```python
# Ensure matmul precision is set
import torch
torch.set_float32_matmul_precision("high")

# Use smaller context
model.compile(timesfm.ForecastConfig(
    max_context=256,  # Shorter context = faster
    ...
))
```

### 模型下载失败

```bash
# Set a different cache directory
export HF_HOME=/path/with/more/space

# Or download manually
huggingface-cli download google/timesfm-2.5-200m-pytorch
```
