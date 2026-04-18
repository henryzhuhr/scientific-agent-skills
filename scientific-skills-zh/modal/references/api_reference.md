# Modal API参考

## 核心类

### modal.App

部署的主要单元。组相关函数。

```python
app = modal.App("my-app")
```

|方法|描述|
|--------|-------------|
| `app.function(**kwargs)` |注册函数的装饰器 |
| `app.cls(**kwargs)` |装饰器注册一个类|
| `app.local_entrypoint()` |本地入口点的装饰器 |

### modal.Function

A 由自动缩放容器池支持的无服务器函数。

|方法|描述|
|--------|-------------|
| `.remote(*args)` |在云端执行（同步）|
| `.local(*args)` |本地执行|
| `.spawn(*args)` |执行异步，返回`FunctionCall` |
| `.map(inputs)` |输入并行执行|
| `.starmap(inputs)` |使用多个参数并行执行|
| `.from_name(app, fn)` |引用已部署的函数|
| `.update_autoscaler(**kwargs)` |动态扩展更新 |

### modal.Cls

A 具有生命周期挂钩的无服务器类。

```python
@app.cls(gpu="L40S")
class MyClass:
    @modal.enter()
    def setup(self): ...

    @modal.method()
    def run(self, data): ...

    @modal.exit()
    def cleanup(self): ...
```

|装饰 |描述|
|---------|--------------|
| `@modal.enter()` |容器启动钩子|
| `@modal.exit()` |集装箱关闭钩|
| `@modal.method()` |公开为可调用方法 |
| `@modal.parameter()` |类级参数 |

## Image

### modal.Image

定义容器环境。

|方法|说明|
|--------|-------------|
| `.debian_slim(python_version=)` | Debian 基础镜像 |
| `.from_registry(tag)` | Docker Hub 镜像 |
| `.from_dockerfile(path)` |从 Dockerfile |
| 构建`.micromamba(python_version=)` |康达/曼巴碱|
| `.uv_pip_install(*pkgs)` |使用uv安装（推荐）|
| `.pip_install(*pkgs)` |使用 pip |
| 安装`.pip_install_from_requirements(path)` |从文件 |
| 安装`.apt_install(*pkgs)` |安装系统包|
| `.run_commands(*cmds)` |运行 shell 命令 |
| `.run_function(fn)` |在构建期间运行 Python |
| `.add_local_dir(local, remote)` |添加目录|
| `.add_local_file(local, remote)` |添加单个文件|
| `.add_local_python_source(module)` |添加Python模块|
| `.env(dict)` |设置环境变量|
| `.imports()` |用于远程导入的上下文管理器 |

## Storage

### modal.Volume

分布式持久文件存储。

```python
vol = modal.Volume.from_name("name", create_if_missing=True)
```

|方法|描述|
|--------|-------------|
| `.from_name(name)` |引用或创建卷 |
| `.commit()` |强制立即提交 |
| `.reload()` |刷新查看其他容器的写入 |

Mount: `@app.function(volumes={"/path": vol})`

### modal.NetworkFileSystem

Legacy 共享存储（已被 Volume 取代）.

## Secrets

### modal.Secret

安全凭证注入。

|方法|描述|
|--------|-------------|
| `.from_name(name)` |引用命名秘密|
| `.from_dict(dict)` |创建内联（仅限开发）|
| `.from_dotenv()` |从.env文件加载|

使用：`@app.function(secrets=[modal.Secret.from_name("x")])`

在函数中访问：`os.environ["KEY"]`

## 调度

### modal.Cron

```python
schedule = modal.Cron("0 9 * * *")  # Cron syntax
```

### modal.Period

```python
schedule = modal.Period(hours=6)  # Fixed interval
```

用法：`@app.function(schedule=modal.Cron("..."))`

## Web

### 装饰器

|装饰 |描述|
|---------|--------------|
| `@modal.fastapi_endpoint()` |简单 FastAPI 端点 |
| `@modal.asgi_app()` |完整的 ASGI 应用程序（FastAPI、Starlette）|
| `@modal.wsgi_app()` |完整的 WSGI 应用程序（Flask、Django）|
| `@modal.web_server(port=)` |自定义 Web 服务器 |

### 功能修饰符

|装饰 |描述|
|-----------|--------------|
| `@modal.concurrent(max_inputs=)` |处理每个容器的多个输入 |
| `@modal.batched(max_batch_size=, wait_ms=)` |动态输入批处理 |

## GPU 字符串

|字符串| GPU |
|--------|-----|
| `"T4"` | NVIDIA T4 16GB |
| `"L4"` | NVIDIA L4 24GB |
| `"A10"` | NVIDIA A10 24GB |
| `"L40S"` | NVIDIA L40S 48GB |
| `"A100-40GB"` | NVIDIA A100 40GB |
| `"A100-80GB"` | NVIDIA A100 80GB |
| `"H100"` | NVIDIA H100 80GB |
| `"H100!"` | H100（无自动升级）|
| `"H200"` | NVIDIA H200 141GB |
| `"B200"` | NVIDIA B200 192GB |
| `"B200+"` | B200或B300，B200价格|
| `"H100:4"` | 4x H100 |

## CLI 命令

|命令 |描述 |
|---------|-------------|
| `modal setup` |认证|
| `modal run <file>` |运行本地入口点|
| `modal serve <file>` |具有热重载功能的开发服务器|
| `modal deploy <file>` |生产部署|
| `modal app list` |列出已部署的应用程序|
| `modal app stop <name>` |停止应用程序|
| `modal volume create <name>` |创建卷|
| `modal volume ls <name>` |列出卷文件 |
| `modal volume put <name> <file>` |上传至卷|
| `modal volume get <name> <file>` |下载卷|
| `modal secret create <name> K=V` |创建秘密 |
| `modal secret list` |列出秘密 |
| `modal secret delete <name>` |删除秘密|
| `modal token set` |设置身份验证令牌 |
