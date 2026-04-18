# Modal GPU 计算

## 目录

- [可用 GPU](#available-gpus)
- [请求 GPU](#requesting-gpus)
- [GPU 选择指南](#gpu-selection-guide)
- [多 GPU](#multi-gpu)
- [GPU 后备链](#gpu-fallback-chains)
- [自动升级](#auto-upgrades)
- [多 GPU 训练](#multi-gpu-training)

## 可用 GPU

|图形处理器 |显存 |每个集装箱的最大数量 |最适合|
|-----|------|--------------------|----------|
| T4 | 16GB| 8 |预算推断，小型号|
| L4 | 24GB| 8 |推理、视频处理|
| A10| 24GB| 4 |推理、微调小模型|
| L40S | 48GB| 8 |推理（最佳成本/性能），中等模型 |
| A100-40GB | 40GB| 8 |训练、大模型推理|
| A100-80GB | 80GB| 8 |训练，大模型|
| RTX-PRO-6000 | 48GB| 8 |渲染、推理|
| H100 | 80GB| 8 |大规模训练，快速推理|
| H200 | 141 GB | 141 GB 8 |非常大的模型，训练|
| B200 | 192 GB | 192 GB 8 |最大型号，最大吞吐量|
| B200+ | 192 GB | 192 GB 8 | B200 或 B300、B200 定价 |

## 请求 GPU

### 基本请求

```python
@app.function(gpu="H100")
def train():
    import torch
    assert torch.cuda.is_available()
    print(f"Using: {torch.cuda.get_device_name(0)}")
```

### 字符串简写

```python
gpu="T4"           # Single T4
gpu="A100-80GB"    # Single A100 80GB
gpu="H100:4"       # Four H100s
```

### GPU 对象（高级）

```python
@app.function(gpu=modal.gpu.H100(count=2))
def multi_gpu():
    ...
```

## GPU选型指南

### 推理用

|型号尺寸|推荐GPU |为什么|
|---------|----------------|-----|
| < 7B 参数 | T4、L4 |高性价比、显存充足|
| 7B-13B 参数 | L40S |最佳性价比，48 GB VRAM |
| 13B-70B 参数 | A100-80GB、H100 |大VRAM，快速内存带宽|
| 70B+ 参数 | H100：2+、H200、B200 |多 GPU 或超大 VRAM |

### 用于训练

|任务|推荐显卡|
|------|----------------|
|微调（LoRA）| L40S、A100-40GB |
|全程微调小模型| A100-80GB |
|全面微调大模型| H100：4+、H200 |
|预训练| H100:8，B200:8 |

### 一般建议

L40S 是推理工作负载的最佳默认设置 - 它通过 48 GB GPU RAM 实现了成本和性能的完美平衡。

## 多 GPU

通过附加 `:count`:

```python
@app.function(gpu="H100:4")
def distributed():
    import torch
    print(f"GPUs available: {torch.cuda.device_count()}")
    # All 4 GPUs are on the same physical machine
```

 请求多个 GPU - 最多 8 个 GPU大多数类型（A10 最多 4 个）
- 所有 GPU 附加到同一物理机
- 请求 2 个以上 GPU 可能会导致更长的等待时间
- 最大 VRAM：8 x B200 = 1,536 GB

## GPU 回退链

指定 GPU 的优先级列表类型：

```python
@app.function(gpu=["H100", "A100-80GB", "L40S"])
def flexible():
    # Modal tries H100 first, then A100-80GB, then L40S
    ...
```

 当特定 GPU 不可用时，可用于减少排队时间。

## 自动升级

### H100 → H200

Modal 可以自动将 H100 请求升级到 H200，无需额外费用。为了防止这种情况：

```python
@app.function(gpu="H100!")  # Exclamation mark prevents auto-upgrade
def must_use_h100():
    ...
```

### A100 → A100-80GB

A100-40GB 请求可以升级到 80GB，无需额外费用。

### B200+

`gpu="B200+"` 允许Modal 以 B200 的价格在 B200 或 B300 GPU 上运行。需要 CUDA 13.0+。

## 多 GPU 训练

Modal 支持单节点上的多 GPU 训练。多节点训练处于私人测试阶段。

### PyTorch DDP示例

```python
@app.function(gpu="H100:4", image=image, timeout=86400)
def train_distributed():
    import torch
    import torch.distributed as dist

    dist.init_process_group(backend="nccl")
    local_rank = int(os.environ.get("LOCAL_RANK", 0))
    device = torch.device(f"cuda:{local_rank}")
    # ... training loop with DDP ...
```

### PyTorch Lightning

当使用重新执行Python入口点的框架（如PyTorch Lightning）时，可以是：

1. 设置策略为`ddp_spawn`或`ddp_notebook`
2. 或者作为子进程运行训练

```python
@app.function(gpu="H100:4", image=image)
def train():
    import subprocess
    subprocess.run(["python", "train_script.py"], check=True)
```

### Hugging Face Accelerate

```python
@app.function(gpu="A100-80GB:4", image=image)
def finetune():
    import subprocess
    subprocess.run([
        "accelerate", "launch",
        "--num_processes", "4",
        "train.py"
    ], check=True)
```
