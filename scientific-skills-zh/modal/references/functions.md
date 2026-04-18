# Modal 函数和类

## 目录

- [函数](#functions)
- [远程执行](#remote-execution)
- [带有生命周期钩子的类](#classes-with-lifecycle-hooks)
- [并行执行](#parallel-execution)
- [异步函数](#async-functions)
- [本地入口点](#local-entrypoints)
- [生成器](#generators)

## 函数

### 基本函数

```python
import modal

app = modal.App("my-app")

@app.function()
def compute(x: int, y: int) -> int:
    return x + y
```

### 函数参数

`@app.function()`装饰器接受：

|参数|类型 |描述|
|---------|------|----------|
| `image` | `Image` |容器镜像|
| `gpu` | `str` | GPU 类型（例如 `"H100"`、`"A100:2"`）|
| `cpu` | `float` | CPU核心|
| `memory` | `int` | MiB 中的内存 |
| `timeout` | `int` |最大执行时间（秒）|
| `secrets` | `list[Secret]` |注射的秘密|
| `volumes` | `dict[str, Volume]` |要安装的卷 |
| `schedule` | `Schedule` | Cron 或定期计划 |
| `max_containers` | `int` |最大集装箱数量|
| `min_containers` | `int` |最小保温容器|
| `retries` | `int` |失败重试次数|
| `concurrency_limit` | `int` |最大并发输入|
| `ephemeral_disk` | `int` | MiB 中的磁盘 |

## 远程执行

### `.remote()` — 同步调用

```python
result = compute.remote(3, 4)  # Runs in the cloud, blocks until done
```

### `.local()` — 本地执行

```python
result = compute.local(3, 4)  # Runs locally (for testing)
```

### `.spawn()` — 异步即发即忘

```python
call = compute.spawn(3, 4)  # Returns immediately
# ... do other work ...
result = call.get()  # Retrieve result later
```

`.spawn()` 支持最多 100 万个待处理输入。

## 具有生命周期挂钩的类

将 `@app.cls()` 用于要加载资源的有状态工作负载一次：

```python
@app.cls(gpu="L40S", image=image)
class Model:
    @modal.enter()
    def setup(self):
        """Runs once when the container starts."""
        import torch
        self.model = torch.load("/weights/model.pt")
        self.model.eval()

    @modal.method()
    def predict(self, text: str) -> dict:
        """Callable remotely."""
        return self.model(text)

    @modal.exit()
    def teardown(self):
        """Runs when the container shuts down."""
        cleanup_resources()
```

### 生命周期装饰器

|装饰 |运行时|
|---------|-------------|
| `@modal.enter()` |一旦容器启动，在任何输入之前 |
| `@modal.method()` |对于每个远程调用|
| `@modal.exit()` |容器关闭时 |

### 调用类方法

```python
# Create instance and call method
model = Model()
result = model.predict.remote("Hello world")

# Parallel calls
results = list(model.predict.map(["text1", "text2", "text3"]))
```

### 参数化类

```python
@app.cls()
class Worker:
    model_name: str = modal.parameter()

    @modal.enter()
    def load(self):
        self.model = load_model(self.model_name)

    @modal.method()
    def run(self, data):
        return self.model(data)

# Different model instances autoscale independently
gpt = Worker(model_name="gpt-4")
llama = Worker(model_name="llama-3")
```

## 并行执行

### `.map()` — 并行处理

处理多个跨容器的输入：

```python
@app.function()
def process(item):
    return heavy_computation(item)

@app.local_entrypoint()
def main():
    items = list(range(1000))
    results = list(process.map(items))
    print(f"Processed {len(results)} items")
```

- 结果以与输入相同的顺序返回
- Modal自动缩放容器以处理工作负载
- 使用`return_exceptions=True`收集错误而不是引发

### `.starmap()` —多参数并行

```python
@app.function()
def add(x, y):
    return x + y

results = list(add.starmap([(1, 2), (3, 4), (5, 6)]))
# [3, 7, 11]
```

### `.map()` 与 `order_outputs=False`

在顺序无关紧要时实现更快的吞吐量：

```python
for result in process.map(items, order_outputs=False):
    handle(result)  # Results arrive as they complete
```

## 异步函数

Modal原生支持异步/等待：

```python
@app.function()
async def fetch_data(url: str) -> str:
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

Async函数对于`@modal.concurrent()`处理每个容器的多个请求特别有用。

## 本地入口点

`@app.local_entrypoint()`在您的计算机上运行并编排远程调用：

```python
@app.local_entrypoint()
def main():
    # This code runs locally
    data = load_local_data()

    # These calls run in the cloud
    results = list(process.map(data))

    # Back to local
    save_results(results)
```

您还可以定义多个入口点并按函数名称进行选择：

```bash
modal run script.py::train
modal run script.py::evaluate
```

## 生成器

函数可以产生结果，因为它们是制作：

```python
@app.function()
def generate_data():
    for i in range(100):
        yield process(i)

@app.local_entrypoint()
def main():
    for result in generate_data.remote_gen():
        print(result)
```

## 重试

配置失败时自动重试：

```python
@app.function(retries=3)
def flaky_operation():
    ...
```

更多控制，请使用`modal.Retries`:

```python
@app.function(retries=modal.Retries(max_retries=3, backoff_coefficient=2.0))
def api_call():
    ...
```

## Timeouts

设置最大执行时间：

```python
@app.function(timeout=3600)  # 1 hour
def long_training():
    ...
```

默认超时为300秒（5分钟）。最大值为 86400 秒（24 小时）。
