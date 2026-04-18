# Modal 容器镜像

## 目录

- [概述](#overview)
- [基础镜像](#base-images)
- [安装软件包](#installing-packages)
- [系统软件包](#system-packages)
- [Shell 命令](#shell-commands)
- [构建期间运行 Python](#running-python-during-build)
- [添加本地文件](#adding-local-files)
- [环境变量](#environment-variables)
- [Dockerfiles](#dockerfiles)
- [替代包管理器](#alternative-package-managers)
- [图像缓存](#image-caching)
- [处理仅远程导入](#handling-remote-only-imports)

## 概述

Every Modal 函数在由 `Image` 构建的容器内运行。默认情况下，Modal 使用与本地解释器具有相同 Python 次要版本的 Debian Linux 映像。

 映像是延迟构建的 - Modal 仅在首次调用使用它的函数时构建/拉取映像。缓存图层以便快速重建。

## 基础图像

```python
# Default: Debian slim with your local Python version
image = modal.Image.debian_slim()

# Specific Python version
image = modal.Image.debian_slim(python_version="3.11")

# From Docker Hub
image = modal.Image.from_registry("nvidia/cuda:12.4.0-devel-ubuntu22.04")

# From a Dockerfile
image = modal.Image.from_dockerfile("./Dockerfile")
```

## 安装包

### uv（推荐）

`uv_pip_install` 使用 uv 包管理器实现快速、可靠安装：

```python
image = (
    modal.Image.debian_slim(python_version="3.11")
    .uv_pip_install(
        "torch==2.8.0",
        "transformers>=4.40",
        "accelerate",
        "scipy",
    )
)
```

Pin 版本以实现可重复性。 uv 比 pip 更快地解析依赖项。

### pip (后备)

```python
image = modal.Image.debian_slim().pip_install(
    "numpy==1.26.0",
    "pandas==2.1.0",
)
```

### 来自requirements.txt

```python
image = modal.Image.debian_slim().pip_install_from_requirements("requirements.txt")
```

### Private软件包

```python
image = (
    modal.Image.debian_slim()
    .pip_install_private_repos(
        "github.com/org/private-repo",
        git_user="username",
        secrets=[modal.Secret.from_name("github-token")],
    )
)
```

## 系统软件包

通过apt安装Linux软件包：

```python
image = (
    modal.Image.debian_slim()
    .apt_install("ffmpeg", "libsndfile1", "git", "curl")
    .uv_pip_install("librosa", "soundfile")
)
```

## Shell命令

在映像期间运行任意命令build:

```python
image = (
    modal.Image.debian_slim()
    .run_commands(
        "wget https://example.com/data.tar.gz",
        "tar -xzf data.tar.gz -C /opt/data",
        "rm data.tar.gz",
    )
)
```

### With GPU

一些构建步骤需要 GPU 访问（例如，编译 CUDA 内核）：

```python
image = (
    modal.Image.debian_slim()
    .uv_pip_install("torch")
    .run_commands("python -c 'import torch; torch.cuda.is_available()'", gpu="A100")
)
```

## 在构建期间运行 Python

将 Python 函数作为构建步骤执行 - 对于下载模型很有用权重：

```python
def download_model():
    from huggingface_hub import snapshot_download
    snapshot_download("meta-llama/Llama-3-8B", local_dir="/models/llama3")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .uv_pip_install("huggingface_hub", "torch", "transformers")
    .run_function(download_model, secrets=[modal.Secret.from_name("huggingface")])
)
```

生成的文件系统（包括下载的文件）被快照到映像中。

## 添加本地文件

### 本地目录

```python
image = modal.Image.debian_slim().add_local_dir(
    local_path="./config",
    remote_path="/root/config",
)
```

默认情况下，文件在容器启动时添加（不烘焙到镜像层中）。使用 `copy=True` 来烘焙它们。

### 本地 Python 模块

```python
image = modal.Image.debian_slim().add_local_python_source("my_module")
```

这使用 Python 的导入系统来查找并包含模块。

### 单个文件

```python
image = modal.Image.debian_slim().add_local_file(
    local_path="./model_config.json",
    remote_path="/root/config.json",
)
```

## 环境变量

```python
image = (
    modal.Image.debian_slim()
    .env({
        "TRANSFORMERS_CACHE": "/cache",
        "TOKENIZERS_PARALLELISM": "false",
        "HF_HOME": "/cache/huggingface",
    })
)
```

名称和值必须是字符串。

## Dockerfiles

从现有Dockerfiles构建：

```python
image = modal.Image.from_dockerfile("./Dockerfile")

# With build context
image = modal.Image.from_dockerfile("./Dockerfile", context_mount=modal.Mount.from_local_dir("."))
```

## 替代包管理器

### Micromamba / Conda

对于需要协调系统和Python包安装的包：

```python
image = (
    modal.Image.micromamba(python_version="3.11")
    .micromamba_install("cudatoolkit=11.8", "cudnn=8.6", channels=["conda-forge"])
    .uv_pip_install("torch")
)
```

## 图像缓存

Modal每层缓存图像（每个方法调用）。破坏一层上的缓存会级联到所有后续层。

### 优化技巧

1. **按更改频率对层进行排序**：将稳定的依赖关系放在第一位，频繁更改的代码放在最后
2. **固定版本**：未固定版本可能会以不同方式解析并破坏缓存
3. **单独的大型安装**：将重型软件包（torch、tensorflow）放在早期层中

### 强制重建

```python
# Single layer
image = modal.Image.debian_slim().apt_install("git", force_build=True)
```

```bash
# All images in a run
MODAL_FORCE_BUILD=1 modal run script.py

# Rebuild without updating cache
MODAL_IGNORE_CACHE=1 modal run script.py
```

## 处理仅远程导入

当软件包仅在容器中可用（不在本地）时，使用条件导入：

```python
@app.function(image=image)
def process():
    import torch  # Only available in the container
    return torch.cuda.device_count()
```

对于跨函数共享的模块级导入，请使用 `Image.imports()` 上下文管理器：

```python
with image.imports():
    import torch
    import transformers
```

这会在本地阻止 `ImportError`，同时使导入在容器中可用。
