# Modal入门指南

## 安装

使用uv（推荐）或pip安装Modal：

```bash
# Recommended
uv pip install modal

# Alternative
pip install modal
```

## 身份验证

### 交互设置

```bash
modal setup
```

这将打开浏览器进行身份验证并在本地存储凭据。

### Headless / CI/CD 设置

对于没有浏览器的环境，请使用基于令牌的身份验证：

1. 在 https://modal.com/settings
2 生成令牌。设置环境变量：

```bash
export MODAL_TOKEN_ID=<your-token-id>
export MODAL_TOKEN_SECRET=<your-token-secret>
```

或使用CLI：

```bash
modal token set --token-id <id> --token-secret <secret>
```

### 免费Tier

Modal提供30美元/月的免费积分。免费套餐不需要信用卡。

## 您的第一个应用程序

### Hello World

创建文件`hello.py`：

```python
import modal

app = modal.App("hello-world")

@app.function()
def greet(name: str) -> str:
    return f"Hello, {name}! This ran in the cloud."

@app.local_entrypoint()
def main():
    result = greet.remote("World")
    print(result)
```

运行它：

```bash
modal run hello.py
```

什么发生：
1. Modal 打包您的代码
2. 在云中创建容器
3. 远程执行`greet()`
4. 将结果返回到本地计算机

### 了解流程

- `modal.App("name")` — 创建命名应用程序
- `@app.function()` — 标记远程执行的函数
- `@app.local_entrypoint()` — 定义本地入口点（在您的计算机上运行）
- `.remote()` — 调用云端函数
- `.local()` — 调用本地函数（用于测试）

### 运行模式

|命令 |描述 |
|---------|-------------|
| `modal run script.py` |运行`@app.local_entrypoint()`函数|
| `modal serve script.py` |通过热重载启动开发服务器（对于 Web 端点）|
| `modal deploy script.py` |部署到生产（持久） |

### 简单的 Web Scraper

```python
import modal

app = modal.App("web-scraper")

image = modal.Image.debian_slim().uv_pip_install("httpx", "beautifulsoup4")

@app.function(image=image)
def scrape(url: str) -> str:
    import httpx
    from bs4 import BeautifulSoup

    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()[:1000]

@app.local_entrypoint()
def main():
    result = scrape.remote("https://example.com")
    print(result)
```

### GPU 加速推理

```python
import modal

app = modal.App("gpu-inference")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .uv_pip_install("torch", "transformers", "accelerate")
)

@app.function(gpu="L40S", image=image)
def generate(prompt: str) -> str:
    from transformers import pipeline
    pipe = pipeline("text-generation", model="gpt2", device="cuda")
    result = pipe(prompt, max_length=100)
    return result[0]["generated_text"]

@app.local_entrypoint()
def main():
    print(generate.remote("The future of AI is"))
```

## 项目结构

Modal 应用程序通常是单个 Python 文件，但可以组织成模块：

```
my-project/
├── app.py           # Main app with @app.local_entrypoint()
├── inference.py     # Inference functions
├── training.py      # Training functions
└── common.py        # Shared utilities
```

使用`modal.Image.add_local_python_source()`将本地模块包含在容器镜像中。

## 关键概念总结

|概念|它的作用 |
|---------|-------------|
| `App` |将相关功能分组为可部署单元 |
| `Function` |由自动缩放容器支持的无服务器功能 |
| `Image` |定义容器环境（包、文件）|
| `Volume` |持久分布式文件存储|
| `Secret` |安全凭证注入|
| `Schedule` | Cron 或定期作业调度 |
| `gpu` |函数的 GPU 类型/数量 |

## 后续步骤

 - 请参阅 `functions.md` 了解高级函数模式
  - 请参阅 `images.md` 了解自定义容器环境
  - 请参阅 `gpu.md` 了解 GPU 选择和配置
  - 请参阅 `web-endpoints.md` 了解服务 API
