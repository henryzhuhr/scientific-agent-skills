# Open Notebook 配置指南

## Docker 部署

Open Notebook 部署为 Docker Compose 堆栈，具有两个主要服务：应用程序服务器和 SurrealDB。

### 最小 docker-compose.yml

```yaml
version: "3.8"

services:
  surrealdb:
    image: surrealdb/surrealdb:latest
    command: start --user root --pass root rocksdb://data/database.db
    volumes:
      - surrealdb_data:/data
    ports:
      - "8000:8000"

  open-notebook:
    image: ghcr.io/lfnovo/open-notebook:latest
    depends_on:
      - surrealdb
    environment:
      - OPEN_NOTEBOOK_ENCRYPTION_KEY=${OPEN_NOTEBOOK_ENCRYPTION_KEY}
      - SURREAL_URL=ws://surrealdb:8000/rpc
      - SURREAL_NAMESPACE=open_notebook
      - SURREAL_DATABASE=open_notebook
    ports:
      - "8502:8502"   # Frontend UI
      - "5055:5055"   # REST API
    volumes:
      - on_uploads:/app/uploads

volumes:
  surrealdb_data:
  on_uploads:
```

### 启动Stack

```bash
# Set the encryption key (required)
export OPEN_NOTEBOOK_ENCRYPTION_KEY="your-secure-random-key"

# Start services
docker-compose up -d

# View logs
docker-compose logs -f open-notebook

# Stop services
docker-compose down

# Stop and remove data
docker-compose down -v
```

## 环境变量

### 必需

|变量|描述 |
|----------|--------------|
| `OPEN_NOTEBOOK_ENCRYPTION_KEY` |用于加密存储的 API 凭证的密钥。必须在首次启动前设置并保持一致。 |

### 数据库

|变量|默认|描述 |
|----------|---------|------------|
| `SURREAL_URL` | `ws://surrealdb:8000/rpc` | SurrealDB WebSocket 连接 URL |
| `SURREAL_NAMESPACE` | `open_notebook` | SurrealDB 命名空间 |
| `SURREAL_DATABASE` | `open_notebook` | SurrealDB数据库名称|
| `SURREAL_USER` | `root` | SurrealDB 用户名 |
| `SURREAL_PASS` | `root` | SurrealDB密码|

### 应用

|变量|默认|描述 |
|----------|---------|------------|
| `OPEN_NOTEBOOK_PASSWORD` |无 | Web UI 可选密码保护 |
| `UPLOAD_DIR` | `/app/uploads` |上传文件存储目录 |

### AI 提供商密钥（旧版）

API 密钥也可以通过环境变量设置以实现旧版兼容性。首选方法是使用凭据 API 或 UI。

|变量|供应商|
|----------|----------|
| `OPENAI_API_KEY` | OpenAI |
| `ANTHROPIC_API_KEY` |人择|
| `GOOGLE_API_KEY` |谷歌GenAI |
| `GROQ_API_KEY` |格罗克|
| `MISTRAL_API_KEY` |米斯特拉尔|
| `ELEVENLABS_API_KEY` | ElevenLabs |

## AI 提供商配置

### 通过 UI

1. 转至 **设置 > API 密钥**
2. 单击“**添加凭据**
3”。选择提供商，输入 API 密钥和可选的基本 URL
4. 单击“**测试连接**”以验证
5. 单击“**发现型号**”查找可用型号
6. 选择型号进行注册

### 通过API

```python
import requests

BASE_URL = "http://localhost:5055/api"

# 1. Create credential
cred = requests.post(f"{BASE_URL}/credentials", json={
    "provider": "anthropic",
    "name": "Anthropic Production",
    "api_key": "sk-ant-..."
}).json()

# 2. Test connection
test = requests.post(f"{BASE_URL}/credentials/{cred['id']}/test").json()
assert test["success"]

# 3. Discover and register models
discovered = requests.post(
    f"{BASE_URL}/credentials/{cred['id']}/discover"
).json()

requests.post(
    f"{BASE_URL}/credentials/{cred['id']}/register-models",
    json={"model_ids": [m["id"] for m in discovered["models"]]}
)

# 4. Auto-assign defaults
requests.post(f"{BASE_URL}/models/auto-assign")
```

### 使用 Ollama（免费本地推理）

对于无需 API 成本的免费 AI 推理，请使用 Ollama：

```yaml
# docker-compose-ollama.yml addition
services:
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
```

然后将 Ollama 配置为具有基本 URL `http://ollama:11434`.

## 的提供者配置

### 密码保护

设置`OPEN_NOTEBOOK_PASSWORD`需要身份验证：

```bash
export OPEN_NOTEBOOK_PASSWORD="your-ui-password"
```

### 反向代理（Nginx示例）

```nginx
server {
    listen 443 ssl;
    server_name notebook.example.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    location / {
        proxy_pass http://localhost:8502;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    location /api/ {
        proxy_pass http://localhost:5055/api/;
        proxy_set_header Host $host;
    }
}
```

## 备份和恢复

### 备份SurrealDB数据

```bash
# Export database
docker exec surrealdb surreal export \
  --conn ws://localhost:8000 \
  --user root --pass root \
  --ns open_notebook --db open_notebook \
  /tmp/backup.surql

# Copy backup from container
docker cp surrealdb:/tmp/backup.surql ./backup.surql
```

### 备份上传的文件

```bash
# Copy upload volume contents
docker cp open-notebook:/app/uploads ./uploads_backup/
```

### 恢复

```bash
# Import database backup
docker cp ./backup.surql surrealdb:/tmp/backup.surql
docker exec surrealdb surreal import \
  --conn ws://localhost:8000 \
  --user root --pass root \
  --ns open_notebook --db open_notebook \
  /tmp/backup.surql
```
