# Modal 缩放和并发

## 目录

- [自动缩放](#autoscaling)
- [配置](#configuration)
- [并行执行](#parallel-execution)
- [并发输入](#concurrent-inputs)
- [动态批处理](#dynamic-batching)
- [动态自动缩放器更新](#dynamic-autoscaler-updates)
- [限制](#limits)

## Autoscaling

Modal 自动管理每个容器的容器池功能：
- 在没有新输入容量时启动容器
- 关闭闲置容器以节省成本
- 从零（闲置时无成本）扩展到数千个容器

基本自动缩放无需配置 - 它开箱即用。

## 配置

微调自动缩放行为：

```python
@app.function(
    max_containers=100,     # Upper limit on container count
    min_containers=2,       # Keep 2 warm (reduces cold starts)
    buffer_containers=5,    # Reserve 5 extra for burst traffic
    scaledown_window=300,   # Wait 5 min idle before shutting down
)
def handle_request(data):
    ...
```

|参数|默认|描述 |
|---------|---------|------------|
| `max_containers` |无限 |容器总量硬性上限|
| `min_containers` | 0 |最低保温容器（即使闲置时也需要花钱）|
| `buffer_containers` | 0 |额外的容器以防止排队|
| `scaledown_window` | 60|关机前的空闲时间秒数 |

### 权衡

- 更高的 `min_containers` = 更低的延迟、更高的成本
- 更高的 `buffer_containers` = 更少的排队、更高的成本
- 更低的 `scaledown_window` = 更快地节省成本、更多的冷启动

## 并行执行

### `.map()` — 处理多个输入

```python
@app.function()
def process(item):
    return heavy_computation(item)

@app.local_entrypoint()
def main():
    items = list(range(10_000))
    results = list(process.map(items))
```

Modal 自动扩展容器以处理工作负载。结果保持输入顺序。

### `.map()` 选项

```python
# Unordered results (faster)
for result in process.map(items, order_outputs=False):
    handle(result)

# Collect errors instead of raising
results = list(process.map(items, return_exceptions=True))
for r in results:
    if isinstance(r, Exception):
        print(f"Error: {r}")
```

### `.starmap()` — 多参数

```python
@app.function()
def add(x, y):
    return x + y

results = list(add.starmap([(1, 2), (3, 4), (5, 6)]))
# [3, 7, 11]
```

### `.spawn()` —即发即忘

```python
# Returns immediately
call = process.spawn(large_data)

# Check status or get result later
result = call.get()
```

 最多 100 万个待处理的 `.spawn()` 调用。

## 并发输入

默认情况下，每个容器一次处理一个输入。使用`@modal.concurrent`处理多个：

```python
@app.function(gpu="L40S")
@modal.concurrent(max_inputs=10)
async def predict(text: str):
    result = await model.predict_async(text)
    return result
```

这非常适合 I/O 密集型工作负载或异步推理，其中单个 GPU 可以处理多个请求。

### 使用 Web 端点

```python
@app.function(gpu="L40S")
@modal.concurrent(max_inputs=20)
@modal.asgi_app()
def web_service():
    return fastapi_app
```

## 动态批处理

将输入收集到批次中以提高 GPU 效率利用：

```python
@app.function(gpu="L40S")
@modal.batched(max_batch_size=32, wait_ms=100)
async def batch_predict(texts: list[str]):
    # Called with up to 32 texts at once
    embeddings = model.encode(texts)
    return list(embeddings)
```

- `max_batch_size` — 每批的最大输入
- `wait_ms` — 处理之前等待更多输入的时间
- 函数接收一个列表，并且必须返回相同长度的列表

## 动态自动缩放器更新

在运行时调整自动缩放而不重新部署：

```python
@app.function()
def scale_up_for_peak():
    process = modal.Function.from_name("my-app", "process")
    process.update_autoscaler(min_containers=10, buffer_containers=20)

@app.function()
def scale_down_after_peak():
    process = modal.Function.from_name("my-app", "process")
    process.update_autoscaler(min_containers=1, buffer_containers=2)
```

设置在下次部署时恢复为装饰器值。

## 限制

|资源 |极限|
|----------|--------|
|待处理的输入（未分配）| 2,000 |
|总输入（正在运行 + 待处理）| 25,000 |
|待定 `.spawn()` 输入 | 1,000,000 |
|每个 `.map()` 的并发输入 | 1,000 |
|速率限制（Web 端点）| 200 req/s |

 超出这些限制会触发 `Resource Exhausted` 错误。实现弹性重试逻辑。
