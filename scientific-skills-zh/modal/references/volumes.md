# Modal 卷

## 目录

- [概述](#overview)
- [创建卷](#creating-volumes)
- [安装卷](#mounting-volumes)
- [读写文件](#reading-and-writing-files)
- [CLI 访问](#cli-access)
- [提交和重新加载](#commits-and-reloads)
- [并发访问](#concurrent-access)
- [卷 v2](#volumes-v2)
- [常见模式](#common-patterns)

## 概述

Volumes 是 Modal 的分布式文件系统，针对一次写入、多次读取的工作负载进行了优化，例如存储模型权重并将其分布在容器中。

 主要特征：
- 跨函数调用和持久化部署
- 可同时由多个功能安装
- 后台每隔几秒自动提交
- 容器关闭时的最终提交

## 创建卷

### 在代码中（延迟创建）

```python
vol = modal.Volume.from_name("my-volume", create_if_missing=True)
```

### 通过CLI

```bash
modal volume create my-volume

# v2 volume (beta)
modal volume create my-volume --version=2
```

### 编程 v2

```python
vol = modal.Volume.from_name("my-volume", create_if_missing=True, version=2)
```

## 挂载卷

通过 `volumes` 将卷挂载到函数参数：

```python
vol = modal.Volume.from_name("model-store", create_if_missing=True)

@app.function(volumes={"/models": vol})
def use_model():
    # Access files at /models/
    with open("/models/config.json") as f:
        config = json.load(f)
```

挂载多个卷：

```python
weights_vol = modal.Volume.from_name("weights")
data_vol = modal.Volume.from_name("datasets")

@app.function(volumes={"/weights": weights_vol, "/data": data_vol})
def train():
    ...
```

## 读写文件

### 写入

```python
@app.function(volumes={"/data": vol})
def save_results(results):
    import json
    import os

    os.makedirs("/data/outputs", exist_ok=True)
    with open("/data/outputs/results.json", "w") as f:
        json.dump(results, f)
```

### 读取

```python
@app.function(volumes={"/data": vol})
def load_results():
    with open("/data/outputs/results.json") as f:
        return json.load(f)
```

### 大文件（模型权重）

```python
@app.function(volumes={"/models": vol}, gpu="L40S")
def save_model():
    import torch
    model = train_model()
    torch.save(model.state_dict(), "/models/checkpoint.pt")

@app.function(volumes={"/models": vol}, gpu="L40S")
def load_model():
    import torch
    model = MyModel()
    model.load_state_dict(torch.load("/models/checkpoint.pt"))
    return model
```

## CLI访问

```bash
# List files
modal volume ls my-volume
modal volume ls my-volume /subdir/

# Upload files
modal volume put my-volume local_file.txt
modal volume put my-volume local_file.txt /remote/path/file.txt

# Download files
modal volume get my-volume /remote/file.txt local_file.txt

# Delete a volume
modal volume delete my-volume
```

## 提交和重新加载

模态自动提交卷每隔几秒和容器关闭时后台就会发生更改。

### 显式提交

强制立即提交：

```python
@app.function(volumes={"/data": vol})
def writer():
    with open("/data/file.txt", "w") as f:
        f.write("hello")
    vol.commit()  # Make immediately visible to other containers
```

### 重新加载

查看其他容器的更改：

```python
@app.function(volumes={"/data": vol})
def reader():
    vol.reload()  # Refresh to see latest writes
    with open("/data/file.txt") as f:
        return f.read()
```

## 并发访问

### v1 卷

- 建议最多 5 个并发提交
- 同一文件的并发修改的最后写入获胜
- 避免同一文件的并发修改
- 最多 500,000 个文件（索引节点）

### v2卷

- 数百个并发写入器（不同文件）
- 无文件计数限制
- 改进的随机访问性能
- 每个文件最多 1 TiB，每个目录 262,144 个文件

## 卷 v2

v2 卷（测试版）提供重大改进：

|特色| v1 | v2 |
|---------|----|----|
|最大文件数 | 500,000 |无限|
|并发写入 | 〜5 |数百 |
|最大文件大小 |无限制| 1 TiB |
|随机访问|有限公司|全力支持|
| HIPAA 合规性 |没有 |是 |
|硬链接|没有 |是 |

启用 v2:

```python
vol = modal.Volume.from_name("my-vol-v2", create_if_missing=True, version=2)
```

## 常见模式

### 模型权重存储

```python
vol = modal.Volume.from_name("model-weights", create_if_missing=True)

# Download once during image build
def download_weights():
    from huggingface_hub import snapshot_download
    snapshot_download("meta-llama/Llama-3-8B", local_dir="/models/llama3")

image = (
    modal.Image.debian_slim()
    .uv_pip_install("huggingface_hub")
    .run_function(download_weights, volumes={"/models": vol})
)
```

### 训练检查点

```python
@app.function(volumes={"/checkpoints": vol}, gpu="H100", timeout=86400)
def train():
    for epoch in range(100):
        train_one_epoch()
        torch.save(model.state_dict(), f"/checkpoints/epoch_{epoch}.pt")
        vol.commit()  # Save checkpoint immediately
```

### 函数之间共享数据

```python
data_vol = modal.Volume.from_name("shared-data", create_if_missing=True)

@app.function(volumes={"/data": data_vol})
def preprocess():
    # Write processed data
    df.to_parquet("/data/processed.parquet")

@app.function(volumes={"/data": data_vol})
def analyze():
    data_vol.reload()  # Ensure we see latest data
    df = pd.read_parquet("/data/processed.parquet")
    return df.describe()
```

### 性能提示

- 卷针对大文件进行了优化，而不是针对许多小文件
- 保持在 50,000 个文件和目录以下以获得最佳效果v1 性能
- 使用 Parquet 或其他柱状格式而不是许多小型 CSV
- 对于真正的临时数据，请使用 `ephemeral_disk` 而不是 Volumes
