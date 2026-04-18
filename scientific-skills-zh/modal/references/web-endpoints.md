# Modal Web 端点

## 目录

- [简单端点](#simple-endpoints)
- [部署](#deployment)
- [ASGI 应用程序](#asgi-apps-fastapi-starlette-fasthtml)
- [WSGI应用程序](#wsgi-apps-flask-django)
- [自定义 Web 服务器](#custom-web-servers)
- [WebSockets](#websockets)
- [身份验证](#authentication)
- [流媒体](#streaming)
- [并发](#concurrency)
- [限制](#limits)

## 简单端点

创建 Web 端点的最简单方法：

```python
import modal

app = modal.App("api-service")

@app.function()
@modal.fastapi_endpoint()
def hello(name: str = "World"):
    return {"message": f"Hello, {name}!"}
```

### POST端点

```python
@app.function()
@modal.fastapi_endpoint(method="POST")
def predict(data: dict):
    result = model.predict(data["text"])
    return {"prediction": result}
```

### 查询参数

参数从查询字符串中自动解析：

```python
@app.function()
@modal.fastapi_endpoint()
def search(query: str, limit: int = 10):
    return {"results": do_search(query, limit)}
```

访问方式：`https://your-app.modal.run?query=hello&limit=5`

## 部署

### 开发模式

```bash
modal serve script.py
```

- 创建临时公共URL
- 文件更改时热重载
- 非常适合开发和测试
- 停止命令时URL过期

### 生产部署

```bash
modal deploy script.py
```

- 创建永久 URL
- 在云中持久运行
- 根据流量自动缩放
- URL 格式：`https://<workspace>--<app-name>-<function-name>.modal.run`

## ASGI 应用程序（FastAPI、Starlette、 FastHTML)

对于完整框架应用程序，请使用 `@modal.asgi_app`:

```python
from fastapi import FastAPI

web_app = FastAPI()

@web_app.get("/")
async def root():
    return {"status": "ok"}

@web_app.post("/predict")
async def predict(request: dict):
    return {"result": model.run(request["input"])}

@app.function(image=image, gpu="L40S")
@modal.asgi_app()
def fastapi_app():
    return web_app
```

### 具有类生命周期

```python
@app.cls(gpu="L40S", image=image)
class InferenceService:
    @modal.enter()
    def load_model(self):
        self.model = load_model()

    @modal.asgi_app()
    def serve(self):
        from fastapi import FastAPI
        app = FastAPI()

        @app.post("/generate")
        async def generate(request: dict):
            return self.model.generate(request["prompt"])

        return app
```

## WSGI 应用程序（Flask、 Django)

```python
from flask import Flask

flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return {"status": "ok"}

@app.function(image=image)
@modal.wsgi_app()
def flask_server():
    return flask_app
```

WSGI 是同步的 — 并发输入在单独的线程上运行。

## 自定义 Web 服务器

对于非标准 Web 框架（aiohttp、Tornado、TGI）：

```python
@app.function(image=image, gpu="H100")
@modal.web_server(port=8000)
def serve():
    import subprocess
    subprocess.Popen([
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", "meta-llama/Llama-3-70B",
        "--host", "0.0.0.0",  # Must bind to 0.0.0.0, not localhost
        "--port", "8000",
    ])
```

 应用程序必须绑定到`0.0.0.0`（不是 `127.0.0.1`）.

## WebSockets

`@modal.asgi_app`、`@modal.wsgi_app` 和 `@modal.web_server` 支持：

```python
from fastapi import FastAPI, WebSocket

web_app = FastAPI()

@web_app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        result = process(data)
        await websocket.send_text(result)

@app.function()
@modal.asgi_app()
def ws_app():
    return web_app
```

 - 完整 WebSocket 协议 (RFC 6455)
- 每条消息最多 2 MiB
- 尚不支持 RFC 8441 或 RFC 7692

## 身份验证

### 代理身份验证令牌（内置）

Modal 通过代理身份验证提供一流的端点保护令牌：

```python
@app.function()
@modal.fastapi_endpoint()
def protected(text: str):
    return {"result": process(text)}
```

客户端包含`Modal-Key`和`Modal-Secret`标头进行身份验证。

### 自定义承载令牌

```python
from fastapi import Header, HTTPException

@app.function(secrets=[modal.Secret.from_name("auth-secret")])
@modal.fastapi_endpoint(method="POST")
def secure_predict(data: dict, authorization: str = Header(None)):
    import os
    expected = os.environ["AUTH_TOKEN"]
    if authorization != f"Bearer {expected}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"result": model.predict(data["text"])}
```

### 客户端 IP 访问

可用于地理位置、速率限制和访问控制。

## 流媒体

### 服务器发送的事件(SSE)

```python
from fastapi.responses import StreamingResponse

@app.function(gpu="H100")
@modal.fastapi_endpoint()
def stream_generate(prompt: str):
    def generate():
        for token in model.stream(prompt):
            yield f"data: {token}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

## 并发性

使用 `@modal.concurrent` 处理每个容器的多个请求：

```python
@app.function(gpu="L40S")
@modal.concurrent(max_inputs=10)
@modal.fastapi_endpoint(method="POST")
async def batch_predict(data: dict):
    return {"result": await model.predict_async(data["text"])}
```

## 限制

- 请求正文：最多 4 GiB
- 响应正文：无限制
- 速率限制：200个请求/秒（新帐户5秒突发）
- 没有容器处于活动状态时发生冷启动（使用`min_containers`来避免）
