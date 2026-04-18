# Modal Secrets

## 概述

Modal Secrets 将凭据和敏感数据作为环境变量安全地传递给函数。机密以加密方式存储，并且仅可供您的工作区使用。

## 创建机密

### 通过 CLI

```bash
# Create with key-value pairs
modal secret create my-api-keys API_KEY=sk-xxx DB_PASSWORD=hunter2

# Create from existing environment variables
modal secret create my-env-keys API_KEY=$API_KEY

# List all secrets
modal secret list

# Delete a secret
modal secret delete my-api-keys
```

### 通过仪表板

导航到 https://modal.com/secrets 以创建和管理机密。模板可用于常见服务（Postgres、MongoDB、Hugging Face、权重和偏差等）。

### 编程（内联）

```python
# From a dictionary (useful for development)
secret = modal.Secret.from_dict({"API_KEY": "sk-xxx"})

# From a .env file
secret = modal.Secret.from_dotenv()

# From a named secret (created via CLI or dashboard)
secret = modal.Secret.from_name("my-api-keys")
```

## 在函数中使用 Secrets

### 基本用法

```python
@app.function(secrets=[modal.Secret.from_name("my-api-keys")])
def call_api():
    import os
    api_key = os.environ["API_KEY"]
    # Use the key
    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
    return response.json()
```

### 多个秘密

```python
@app.function(secrets=[
    modal.Secret.from_name("openai-keys"),
    modal.Secret.from_name("database-creds"),
])
def process():
    import os
    openai_key = os.environ["OPENAI_API_KEY"]
    db_url = os.environ["DATABASE_URL"]
    ...
```

 秘密按顺序应用 - 如果两个秘密定义相同的密钥，则后一个获胜。

### 使用类

```python
@app.cls(secrets=[modal.Secret.from_name("huggingface")])
class ModelService:
    @modal.enter()
    def load(self):
        import os
        token = os.environ["HF_TOKEN"]
        self.model = AutoModel.from_pretrained("model-name", token=token)
```

### 来自.env文件

```python
# Reads .env file from current directory
@app.function(secrets=[modal.Secret.from_dotenv()])
def local_dev():
    import os
    api_key = os.environ["API_KEY"]
```

`.env`文件格式：

```
API_KEY=sk-xxx
DATABASE_URL=postgres://user:pass@host/db
DEBUG=false
```

## 常见秘密模板

|服务 |典型按键 |
|---------|--------------|
|开放人工智能 | `OPENAI_API_KEY` |
|拥抱脸| `HF_TOKEN` |
|亚马逊AWS | `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` |
| Postgres | `PGHOST`、`PGPORT`、`PGUSER`、`PGPASSWORD`、`PGDATABASE` |
|权重和偏差| `WANDB_API_KEY` |
| GitHub | `GITHUB_TOKEN` |

## 安全说明

- 秘密在静态和传输过程中进行加密
- 仅可访问工作区中的功能
- 切勿记录或打印秘密值
- 在生产中使用 `.from_name()`（不`.from_dict()`)
- 通过仪表板或 CLI
 定期轮换机密
