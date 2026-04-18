# Modal 资源配置

## CPU

### 请求 CPU

```python
@app.function(cpu=4.0)
def compute():
    ...
```

- 值是 **物理核心**，而不是 vCPU
- 默认：0.125 个核心
- Modal 自动设置`OPENBLAS_NUM_THREADS`、`OMP_NUM_THREADS`、`MKL_NUM_THREADS` 基于您的 CPU 请求

### CPU 限制

- 默认软限制：高于 CPU 请求的 16 个物理内核
- 设置显式限制以防止噪声邻居效应：

```python
@app.function(cpu=4.0)  # Request 4 cores
def bounded_compute():
    ...
```

## 内存

### 请求内存

```python
@app.function(memory=16384)  # 16 GiB in MiB
def large_data():
    ...
```

- **MiB** 中的值（兆字节）
- 默认：128 MiB

### 内存限制

将硬内存限制设置为 OOM-kill 超出的容器它们：

```python
@app.function(memory=8192)  # 8 GiB request and limit
def bounded_memory():
    ...
```

这可以防止为失控内存泄漏付费。

## 临时磁盘

用于容器生命周期内的临时存储：

```python
@app.function(ephemeral_disk=102400)  # 100 GiB in MiB
def process_dataset():
    # Temporary files at /tmp or anywhere in the container filesystem
    ...
```

- **MiB**
- 中的值默认：每个容器 512 GiB 配额
- 最大：3,145,728 MiB (3 TiB)
- 容器关闭时数据丢失
- 使用卷进行持久存储

出于计费目的，较大的磁盘请求会以 20:1 的比率增加内存请求。

## 超时

```python
@app.function(timeout=3600)  # 1 hour in seconds
def long_running():
    ...
```

- 默认：300 秒（5 分钟）
- 最长：86,400 秒（24 小时）
- 超时到期时函数被终止

## 计费

您的收费基于 **以较高者为准**：您的资源请求或实际使用情况。

|资源 |计费依据 |
|---------|----------------|
|中央处理器|最大（请求，使用）|
|内存|最大（请求，使用）|
|图形处理器 | GPU分配时间|
|磁盘 |以 20:1 的比例增加内存计费 |

### 成本优化技巧

- 仅请求您需要的内容
- 使用适当的 GPU 层（L40S 超过 H100 用于推理）
- 设置 `scaledown_window` 以最大限度地减少空闲时间
- 使用 `min_containers=0`当冷启动可接受时
- 使用`.map()`批量输入而不是单独的`.remote()`调用

## 完整示例

```python
@app.function(
    cpu=8.0,              # 8 physical cores
    memory=32768,         # 32 GiB
    gpu="L40S",           # L40S GPU
    ephemeral_disk=204800, # 200 GiB temp disk
    timeout=7200,         # 2 hours
    max_containers=50,
    min_containers=1,
)
def full_pipeline(data_path: str):
    ...
```
