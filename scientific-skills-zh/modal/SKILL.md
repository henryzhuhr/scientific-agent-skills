---
name: modal
description: 用于在 GPU 和无服务器基础设施上运行 Python 的云计算平台。在部署 AI/ML 模型、运行 GPU 加速的工作负载、服务 Web 端点、调度批处理作业或将 Python 代码扩展到云时使用。每当用户提到 Modal、无服务器 GPU 计算、将 ML 模型部署到云、服务推理端点、在云中运行批处理或需要将 Python 工作负载扩展到本地计算机之外时，请使用此技能。当用户想要在 H100、A100 或其他云 GPU 上运行代码，或者需要为模型创建 Web API 时，也可以使用。
license: Apache-2.0
metadata:
  skill-author: K-Dense Inc.
---

# Modal

## 概述

Modal 是一个用于无服务器运行 Python 代码的云平台，重点关注 AI/ML 工作负载。主要功能：
- **GPU 计算**按需（T4、L4、A10、L40S、A100、H100、H200、B200）
- **无服务器功能**，可从零到数千个容器自动扩展
- **自定义容器映像**完全用 Python 代码构建
- **通过模型卷进行持久存储**权重和数据集
- **用于服务模型和 API 的 Web 端点**
- **通过 cron 或固定间隔安排作业**
- **亚秒级冷启动**用于低延迟推理

Modal 中的所有内容都定义为代码 - 不需要 YAML，不需要 Dockerfile（尽管两者都是

## 何时使用此技能

在以下情况下使用此技能：
- 在云中部署或提供 AI/ML 模型
- 运行 GPU 加速计算（训练、推理、微调）
- 创建无服务器 Web API 或端点
- 扩展批处理作业并行
- 安排重复任务（数据管道、重新训练、抓取）
- 需要持久云存储模型权重或数据集
- 想要在自定义容器环境中运行代码
- 构建作业队列或异步任务处理系统

## 安装和身份验证

### 安装

```bash
uv pip install modal
```

### 验证

在创建新凭据之前首选现有凭据：

1. 检查当前环境中是否已经存在`MODAL_TOKEN_ID`和`MODAL_TOKEN_SECRET`。
2. 如果没有，请检查本地 `.env` 文件中的这些值，并加载它们（如果适用于工作流程）。
3. 仅当两个源均未提供凭据时，才回退到交互式 `modal setup` 或生成新令牌。

```bash
modal setup
```

这将打开浏览器进行身份验证。对于 CI/CD 或无头环境，请使用环境变量：

```bash
export MODAL_TOKEN_ID=<your-token-id>
export MODAL_TOKEN_SECRET=<your-token-secret>
```

如果环境或 `.env` 中尚未提供代币，请在 https://modal.com/settings

Modal 提供免费套餐，每月 30 美元的积分。

* *参考**：有关详细设置和第一个应用程序演练，请参阅 `references/getting-started.md`。

## 核心概念

### 应用程序和功能

A Modal `App` 分组相关功能。用`@app.function()`装饰的函数在云端远程运行：

```python
import modal

app = modal.App("my-app")

@app.function()
def square(x):
    return x ** 2

@app.local_entrypoint()
def main():
    # .remote() runs in the cloud
    print(square.remote(42))
```

用`modal run script.py`运行。使用 `modal deploy script.py`.

* *参考**：请参阅 `references/functions.md` 了解生命周期挂钩、类、`.map()`、`.spawn()` 等。

### 容器镜像

Modal 从 Python 代码构建容器镜像。推荐的软件包安装程序为 `uv`：

```python
image = (
    modal.Image.debian_slim(python_version="3.11")
    .uv_pip_install("torch==2.8.0", "transformers", "accelerate")
    .apt_install("git")
)

@app.function(image=image)
def inference(prompt):
    from transformers import pipeline
    pipe = pipeline("text-generation", model="meta-llama/Llama-3-8B")
    return pipe(prompt)
```

 关键镜像方法：
- `.uv_pip_install()` — 使用 uv 安装 Python 软件包（推荐） 
- `.pip_install()` — 使用 pip 安装（后备）
- `.apt_install()` — 安装系统包
- `.run_commands()` — 在构建期间运行 shell 命令
- `.run_function()` — 在构建期间运行 Python（例如，下载模型权重）
- `.add_local_python_source()` — 添加本地模块
- `.env()` — 设置环境变量

* *参考**：请参阅`references/images.md`了解Dockerfiles、micromamba、缓存、GPU构建步骤。

### GPU计算

通过`gpu`请求GPU参数：

```python
@app.function(gpu="H100")
def train_model():
    import torch
    device = torch.device("cuda")
    # GPU training code here

# Multiple GPUs
@app.function(gpu="H100:4")
def distributed_training():
    ...

# GPU fallback chain
@app.function(gpu=["H100", "A100-80GB", "A100-40GB"])
def flexible_inference():
    ...
```

 可用 GPU：T4、L4、A10、L40S、A100-40GB、A100-80GB、H100、H200、B200、B200+

- 每个容器最多 8 个 GPU（A10 除外：最多4)
- L40S 推荐用于推理（成本/性能平衡，48 GB VRAM）
- H100/A100 可自动升级到 H200/A100-80GB，无需额外费用
- 使用 `gpu="H100!"` 防止自动升级

* *参考**：GPU选择指导和多GPU训练请参见`references/gpu.md`。

### 卷（持久存储）

卷提供分布式、持久文件存储：

```python
vol = modal.Volume.from_name("model-weights", create_if_missing=True)

@app.function(volumes={"/data": vol})
def save_model():
    # Write to the mounted path
    with open("/data/model.pt", "wb") as f:
        torch.save(model.state_dict(), f)

@app.function(volumes={"/data": vol})
def load_model():
    model.load_state_dict(torch.load("/data/model.pt"))
```

- 针对一次写入、多次读取的工作负载（模型权重、数据集）进行了优化
- CLI 访问：`modal volume ls`、`modal volume put`、`modal volume get`
- 后台每隔几秒自动提交一次

* *参考**：参见`references/volumes.md` 用于 v2 卷、并发写入和最佳实践。

### Secrets

将凭据安全地传递给函数：

```python
@app.function(secrets=[modal.Secret.from_name("my-api-keys")])
def call_api():
    import os
    api_key = os.environ["API_KEY"]
    # Use the key
```

通过 CLI 创建机密：`modal secret create my-api-keys API_KEY=sk-xxx`

 或者从 `.env` 文件： `modal.Secret.from_dotenv()`

* *参考**：有关仪表板设置、多个密钥和模板，请参阅 `references/secrets.md`。

### Web 端点

将模型和 API 作为 Web 端点提供服务：

```python
@app.function()
@modal.fastapi_endpoint()
def predict(text: str):
    return {"result": model.predict(text)}
```

- `modal serve script.py` - 使用热重载和临时 URL 进行开发
  - `modal deploy script.py` - 使用永久 URL 进行生产部署
  - 支持 FastAPI、ASGI（Starlette、FastHTML）、WSGI（Flask、Django）、WebSockets
  - 请求主体高达 4 GiB，无限制响应size

* *参考**：请参阅 `references/web-endpoints.md` 了解 ASGI/WSGI 应用程序、流媒体、身份验证和 WebSockets。

### 计划作业

按计划运行功能：

```python
@app.function(schedule=modal.Cron("0 9 * * *"))  # Daily at 9 AM UTC
def daily_pipeline():
    # ETL, retraining, scraping, etc.
    ...

@app.function(schedule=modal.Period(hours=6))
def periodic_check():
    ...
```

 使用 `modal deploy script.py` 部署以激活Schedule.

- `modal.Cron("...")` — 标准 cron 语法，跨部署稳定
- `modal.Period(hours=N)` — 固定间隔，重新部署时重置
- 监视器在 Modal 仪表板中运行

* *参考**：有关 cron 语法和信息，请参阅 `references/scheduled-jobs.md` management.

### 扩展和并发

Modal 自动扩展容器。配置限制：

```python
@app.function(
    max_containers=100,    # Upper limit
    min_containers=2,      # Keep warm for low latency
    buffer_containers=5,   # Reserve capacity
    scaledown_window=300,  # Idle seconds before shutdown
)
def process(data):
    ...
```

与`.map()`并行处理输入：

```python
results = list(process.map([item1, item2, item3, ...]))
```

启用每个容器的并发请求处理：

```python
@app.function()
@modal.concurrent(max_inputs=10)
async def handle_request(req):
    ...
```

* *参考**：请参阅 `references/scaling.md` 了解 `.map()`、`.starmap()`、`.spawn()` 和限制。

### 资源配置

```python
@app.function(
    cpu=4.0,              # Physical cores (not vCPUs)
    memory=16384,         # MiB
    ephemeral_disk=51200, # MiB (up to 3 TiB)
    timeout=3600,         # Seconds
)
def heavy_computation():
    ...
```

 默认：0.125 个 CPU 内核，128 MiB 内存。按最大（请求、使用）计费。

* *参考**：有关限制和计费详细信息，请参阅 `references/resources.md`。

## 具有生命周期挂钩的类

对于有状态工作负载（例如，加载一次模型并服务多个请求）：

```python
@app.cls(gpu="L40S", image=image)
class Predictor:
    @modal.enter()
    def load_model(self):
        self.model = load_heavy_model()  # Runs once on container start

    @modal.method()
    def predict(self, text: str):
        return self.model(text)

    @modal.exit()
    def cleanup(self):
        ...  # Runs on container shutdown
```

 调用： `Predictor().predict.remote("hello")`

## 常用工作流模式

### GPU模型推理服务

```python
import modal

app = modal.App("llm-service")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .uv_pip_install("vllm")
)

@app.cls(gpu="H100", image=image, min_containers=1)
class LLMService:
    @modal.enter()
    def load(self):
        from vllm import LLM
        self.llm = LLM(model="meta-llama/Llama-3-70B")

    @modal.method()
    @modal.fastapi_endpoint(method="POST")
    def generate(self, prompt: str, max_tokens: int = 256):
        outputs = self.llm.generate([prompt], max_tokens=max_tokens)
        return {"text": outputs[0].outputs[0].text}
```

### 批处理流水线

```python
app = modal.App("batch-pipeline")
vol = modal.Volume.from_name("pipeline-data", create_if_missing=True)

@app.function(volumes={"/data": vol}, cpu=4.0, memory=8192)
def process_chunk(chunk_id: int):
    import pandas as pd
    df = pd.read_parquet(f"/data/input/chunk_{chunk_id}.parquet")
    result = heavy_transform(df)
    result.to_parquet(f"/data/output/chunk_{chunk_id}.parquet")
    return len(result)

@app.local_entrypoint()
def main():
    chunk_ids = list(range(100))
    results = list(process_chunk.map(chunk_ids))
    print(f"Processed {sum(results)} total rows")
```

### 预定数据管道

```python
app = modal.App("etl-pipeline")

@app.function(
    schedule=modal.Cron("0 */6 * * *"),  # Every 6 hours
    secrets=[modal.Secret.from_name("db-credentials")],
)
def etl_job():
    import os
    db_url = os.environ["DATABASE_URL"]
    # Extract, transform, load
    ...
```

## CLI 参考

|命令 |描述 |
|---------|-------------|
| `modal setup` |使用 Modal |
| 进行身份验证`modal run script.py` |运行脚本的本地入口点 |
| `modal serve script.py` |具有热重载功能的开发服务器|
| `modal deploy script.py` |部署到生产|
| `modal volume ls <name>` |列出卷中的文件 |
| `modal volume put <name> <file>` |将文件上传到卷 |
| `modal volume get <name> <file>` |从卷 |
| 下载文件`modal secret create <name> K=V` |创建秘密|
| `modal secret list` |列出秘密|
| `modal app list` |列出已部署的应用程序|
| `modal app stop <name>` |停止已部署的应用程序 |

## 参考文件

每个主题的详细文档：

- `references/getting-started.md` — 安装、身份验证、第一个应用程序
- `references/functions.md` — 函数、类、生命周期挂钩、远程执行
- `references/images.md` — 容器映像、包安装、缓存
- `references/gpu.md` — GPU 类型、选择、多 GPU、训练
- `references/volumes.md` — 持久存储、文件管理、v2 卷
- `references/secrets.md` — 凭证、环境变量、dotenv
- `references/web-endpoints.md` — FastAPI、ASGI/WSGI、流、身份验证、WebSockets
- `references/scheduled-jobs.md` — Cron、定期计划、管理
- `references/scaling.md` — 自动缩放、并发、.map()、限制
- `references/resources.md` — CPU、内存、磁盘、超时配置
- `references/examples.md` — 常见用例和模式
- `references/api_reference.md` — 关键 API 类和方法

 当需要超出本概述的详细信息时，请阅读这些文件。
