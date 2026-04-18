# Forge API 参考

## 概述

Forge 是 EvolutionaryScale 的云平台，用于可扩展的蛋白质设计和推理。它提供对完整 ESM3 模型系列的 API 访问，包括不可用于本地执行的大型模型。

* *主要优点：**
- 访问所有 ESM3 模型，包括 98B 参数版本
- 无本地 GPU 要求
- 可扩展批处理
- 自动更新到最新模型
- 生产就绪基础设施
- 异步/并发请求支持

## 入门

### 1.获取API令牌

注册并获取API令牌：https://forge.evolutionaryscale.ai

### 2.安装ESM SDK

```bash
pip install esm
```

Forge客户端包含在标准ESM包中。

### 3.基本连接

```python
from esm.sdk.forge import ESM3ForgeInferenceClient
from esm.sdk.api import ESMProtein, GenerationConfig

# Initialize client
client = ESM3ForgeInferenceClient(
    model="esm3-medium-2024-08",
    url="https://forge.evolutionaryscale.ai",
    token="<your-token-here>"
)

# Test connection
protein = ESMProtein(sequence="MPRT___KEND")
result = client.generate(protein, GenerationConfig(track="sequence", num_steps=8))
print(result.sequence)
```

## 可用型号

|型号 ID |参数|速度|品质 |使用案例 |
|---------|------------|--------|----------|----------|
| `esm3-small-2024-08` | 1.4B|最快|好 |快速原型制作、测试|
| `esm3-medium-2024-08` | 7B|快|优秀|生产，大多数应用|
| `esm3-large-2024-03` | 98B | 98B慢一点 |最佳|研究、关键设计|
| `esm3-medium-multimer-2024-09` | 7B|快|实验|蛋白质复合物 |

* *型号选择指南：**

- **开发/测试**：使用 `esm3-small-2024-08` 进行快速迭代
- **生产**：使用 `esm3-medium-2024-08` 获得最佳平衡
- **研究/关键**：使用 `esm3-large-2024-03` 获得最高平衡质量
- **复合体**：使用`esm3-medium-multimer-2024-09`（实验）

## ESM3ForgeInferenceClient API

### 初始化

```python
from esm.sdk.forge import ESM3ForgeInferenceClient

# Basic initialization
client = ESM3ForgeInferenceClient(
    model="esm3-medium-2024-08",
    token="<your-token>"
)

# With custom URL (for enterprise deployments)
client = ESM3ForgeInferenceClient(
    model="esm3-medium-2024-08",
    url="https://custom.forge.instance.com",
    token="<your-token>"
)

# With timeout configuration
client = ESM3ForgeInferenceClient(
    model="esm3-medium-2024-08",
    token="<your-token>",
    timeout=300  # 5 minutes
)
```

### 同步生成

标准阻塞生成调用：

```python
from esm.sdk.api import ESMProtein, GenerationConfig

# Basic generation
protein = ESMProtein(sequence="MPRT___KEND")
config = GenerationConfig(track="sequence", num_steps=8)

result = client.generate(protein, config)
print(f"Generated: {result.sequence}")
```

### 异步生成

用于并发处理多个蛋白质：

```python
import asyncio
from esm.sdk.api import ESMProtein, GenerationConfig

async def generate_many(client, proteins):
    """Generate multiple proteins concurrently."""
    tasks = []

    for protein in proteins:
        task = client.async_generate(
            protein,
            GenerationConfig(track="sequence", num_steps=8)
        )
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return results

# Usage
proteins = [
    ESMProtein(sequence=f"MPRT{'_' * 10}KEND"),
    ESMProtein(sequence=f"AGLV{'_' * 10}HSPQ"),
    ESMProtein(sequence=f"KEIT{'_' * 10}NDFL")
]

results = asyncio.run(generate_many(client, proteins))
print(f"Generated {len(results)} proteins")
```

### 使用BatchExecutor进行批处理

用于自动并发的大规模处理管理：

```python
from esm.sdk.forge import BatchExecutor
from esm.sdk.api import ESMProtein, GenerationConfig

# Create batch executor
executor = BatchExecutor(
    client=client,
    max_concurrent=10  # Process 10 requests concurrently
)

# Prepare batch of proteins
proteins = [ESMProtein(sequence=f"MPRT{'_' * 50}KEND") for _ in range(100)]
config = GenerationConfig(track="sequence", num_steps=25)

# Submit batch
batch_results = executor.submit_batch(
    proteins=proteins,
    config=config,
    progress_callback=lambda i, total: print(f"Processed {i}/{total}")
)

print(f"Completed {len(batch_results)} generations")
```

## 速率限制和配额

### 了解限制

Forge 基于以下条件实现速率限制：
- 每分钟请求数 (RPM)
- 每分钟令牌数 (TPM)
- 并发请求

* *典型限制（可能会更改）：**
- 免费套餐：60 RPM，5并发
- 专业级：300 RPM，20 个并发
- 企业版：自定义限制

### 处理速率限制

```python
import time
from requests.exceptions import HTTPError

def generate_with_retry(client, protein, config, max_retries=3):
    """Generate with automatic retry on rate limit."""
    for attempt in range(max_retries):
        try:
            return client.generate(protein, config)
        except HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")

# Usage
result = generate_with_retry(client, protein, config)
```

### 实施自定义速率限制器

```python
import time
from collections import deque

class RateLimiter:
    """Simple rate limiter for API calls."""

    def __init__(self, max_per_minute=60):
        self.max_per_minute = max_per_minute
        self.calls = deque()

    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        now = time.time()

        # Remove old calls
        while self.calls and self.calls[0] < now - 60:
            self.calls.popleft()

        # Wait if at limit
        if len(self.calls) >= self.max_per_minute:
            sleep_time = 60 - (now - self.calls[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
            self.calls.popleft()

        self.calls.append(now)

# Usage
limiter = RateLimiter(max_per_minute=60)

for protein in proteins:
    limiter.wait_if_needed()
    result = client.generate(protein, config)
```

## 高级模式

### 流式传输结果

完成时处理结果：

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def stream_generate(client, proteins, config):
    """Stream results as they complete."""
    pending = {
        asyncio.create_task(client.async_generate(p, config)): i
        for i, p in enumerate(proteins)
    }

    results = [None] * len(proteins)

    while pending:
        done, pending = await asyncio.wait(
            pending.keys(),
            return_when=asyncio.FIRST_COMPLETED
        )

        for task in done:
            idx = pending.pop(task)
            result = await task
            results[idx] = result
            yield idx, result

# Usage
async def process_stream():
    async for idx, result in stream_generate(client, proteins, config):
        print(f"Completed protein {idx}: {result.sequence[:20]}...")

asyncio.run(process_stream())
```

### 带进度跟踪的批处理

```python
from tqdm import tqdm
import asyncio

async def batch_with_progress(client, proteins, config):
    """Process batch with progress bar."""
    results = []

    with tqdm(total=len(proteins)) as pbar:
        for protein in proteins:
            result = await client.async_generate(protein, config)
            results.append(result)
            pbar.update(1)

    return results

# Usage
results = asyncio.run(batch_with_progress(client, proteins, config))
```

### 检查点和恢复

对于长时间运行的批处理作业：

```python
import pickle
import os

class CheckpointedBatchProcessor:
    """Batch processor with checkpoint/resume capability."""

    def __init__(self, client, checkpoint_file="checkpoint.pkl"):
        self.client = client
        self.checkpoint_file = checkpoint_file
        self.completed = self.load_checkpoint()

    def load_checkpoint(self):
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'rb') as f:
                return pickle.load(f)
        return {}

    def save_checkpoint(self):
        with open(self.checkpoint_file, 'wb') as f:
            pickle.dump(self.completed, f)

    def process_batch(self, proteins, config):
        """Process batch with checkpointing."""
        results = {}

        for i, protein in enumerate(proteins):
            # Skip if already completed
            if i in self.completed:
                results[i] = self.completed[i]
                continue

            try:
                result = self.client.generate(protein, config)
                results[i] = result
                self.completed[i] = result

                # Save checkpoint every 10 items
                if i % 10 == 0:
                    self.save_checkpoint()

            except Exception as e:
                print(f"Error processing {i}: {e}")
                self.save_checkpoint()
                raise

        self.save_checkpoint()
        return results

# Usage
processor = CheckpointedBatchProcessor(client)
results = processor.process_batch(proteins, config)
```

## 错误处理

### 常见错误和解决方案

```python
from requests.exceptions import HTTPError, ConnectionError, Timeout

def robust_generate(client, protein, config):
    """Generate with comprehensive error handling."""
    try:
        return client.generate(protein, config)

    except HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid API token")
        elif e.response.status_code == 429:
            raise ValueError("Rate limit exceeded - slow down requests")
        elif e.response.status_code == 500:
            raise ValueError("Server error - try again later")
        else:
            raise

    except ConnectionError:
        raise ValueError("Network error - check internet connection")

    except Timeout:
        raise ValueError("Request timeout - try smaller protein or increase timeout")

    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")

# Usage with retry logic
def generate_with_full_retry(client, protein, config, max_retries=3):
    """Combine error handling with retry logic."""
    for attempt in range(max_retries):
        try:
            return robust_generate(client, protein, config)
        except ValueError as e:
            if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
```

## 成本优化

### 降低成本的策略

* *1.使用适当的模型尺寸：**

```python
# Use smaller model for testing
dev_client = ESM3ForgeInferenceClient(
    model="esm3-small-2024-08",
    token=token
)

# Use larger model only for final generation
prod_client = ESM3ForgeInferenceClient(
    model="esm3-large-2024-03",
    token=token
)
```

* *2。缓存结果：**

```python
import hashlib
import json

class ForgeCache:
    """Cache Forge API results locally."""

    def __init__(self, cache_dir="forge_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_cache_key(self, protein, config):
        """Generate cache key from inputs."""
        data = {
            'sequence': protein.sequence,
            'config': str(config)
        }
        return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def get(self, protein, config):
        """Get cached result."""
        key = self.get_cache_key(protein, config)
        path = os.path.join(self.cache_dir, f"{key}.pkl")

        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)
        return None

    def set(self, protein, config, result):
        """Cache result."""
        key = self.get_cache_key(protein, config)
        path = os.path.join(self.cache_dir, f"{key}.pkl")

        with open(path, 'wb') as f:
            pickle.dump(result, f)

# Usage
cache = ForgeCache()

def cached_generate(client, protein, config):
    """Generate with caching."""
    cached = cache.get(protein, config)
    if cached:
        return cached

    result = client.generate(protein, config)
    cache.set(protein, config, result)
    return result
```

* *3。批量相似请求：**

将相似的生成任务分组以减少开销：

```python
def batch_similar_tasks(proteins, max_batch_size=50):
    """Group proteins by similar properties."""
    # Sort by length for efficient processing
    sorted_proteins = sorted(proteins, key=lambda p: len(p.sequence))

    batches = []
    current_batch = []

    for protein in sorted_proteins:
        current_batch.append(protein)

        if len(current_batch) >= max_batch_size:
            batches.append(current_batch)
            current_batch = []

    if current_batch:
        batches.append(current_batch)

    return batches
```

## 监控和日志记录

### 跟踪API使用情况

```python
import logging
from datetime import datetime

class ForgeMonitor:
    """Monitor Forge API usage."""

    def __init__(self):
        self.calls = []
        self.errors = []

    def log_call(self, model, protein_length, duration, success=True, error=None):
        """Log API call."""
        entry = {
            'timestamp': datetime.now(),
            'model': model,
            'protein_length': protein_length,
            'duration': duration,
            'success': success,
            'error': str(error) if error else None
        }

        if success:
            self.calls.append(entry)
        else:
            self.errors.append(entry)

    def get_stats(self):
        """Get usage statistics."""
        total_calls = len(self.calls) + len(self.errors)
        success_rate = len(self.calls) / total_calls if total_calls > 0 else 0
        avg_duration = sum(c['duration'] for c in self.calls) / len(self.calls) if self.calls else 0

        return {
            'total_calls': total_calls,
            'successful': len(self.calls),
            'failed': len(self.errors),
            'success_rate': success_rate,
            'avg_duration': avg_duration
        }

# Usage
monitor = ForgeMonitor()

def monitored_generate(client, protein, config):
    """Generate with monitoring."""
    start = time.time()

    try:
        result = client.generate(protein, config)
        duration = time.time() - start
        monitor.log_call(
            model=client.model,
            protein_length=len(protein.sequence),
            duration=duration,
            success=True
        )
        return result

    except Exception as e:
        duration = time.time() - start
        monitor.log_call(
            model=client.model,
            protein_length=len(protein.sequence),
            duration=duration,
            success=False,
            error=e
        )
        raise

# Check stats
print(monitor.get_stats())
```

## AWS SageMaker部署

For专用基础设施和企业使用：

### 部署选项

1. **AWS Marketplace 列表**：通过 AWS SageMaker Marketplace
2 部署 ESM3。 **自定义端点**：配置专用推理端点
3. **批量转换**：使用 SageMaker 批量转换进行大规模处理

### 优势

- 专用计算资源
- 基础设施之外没有速率限制
- 数据保留在您的 AWS 环境中
- 与 AWS 服务集成
- 自定义实例类型和扩展

* *更多信息：**
- AWS Marketplace：https://aws.amazon.com/marketplace/seller-profile?id=seller-iw2nbscescndm
- 联系 EvolutionaryScale 获取企业许可

## 最佳实践摘要

1. **身份验证**：安全地存储令牌（环境变量、秘密管理器）
2. **速率限制**：实施指数退避并遵守限制
3. **错误处理**：始终处理网络错误并重试
4. **缓存**：缓存重复查询的结果
5. **模型选择**：为任务
6使用适当的模型大小。 **批处理**：对多种蛋白质使用异步/批处理
7. **监控**：跟踪使用情况和成本
8. **检查点**：保存长时间运行作业的进度

## 故障排除

### 连接问题

```python
# Test connection
try:
    client = ESM3ForgeInferenceClient(model="esm3-medium-2024-08", token=token)
    test_protein = ESMProtein(sequence="MPRTK")
    result = client.generate(test_protein, GenerationConfig(track="sequence", num_steps=1))
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
```

### 令牌验证

```python
def validate_token(token):
    """Validate API token."""
    try:
        client = ESM3ForgeInferenceClient(
            model="esm3-small-2024-08",
            token=token
        )
        # Make minimal test call
        test = ESMProtein(sequence="MPR")
        client.generate(test, GenerationConfig(track="sequence", num_steps=1))
        return True
    except HTTPError as e:
        if e.response.status_code == 401:
            return False
        raise
```

## 其他资源

- **Forge平台**：https://forge.evolutionaryscale.ai
- **API 文档**：查看 Forge 仪表板了解最新 API 规范
- **社区支持**：Slack 社区 https://bit.ly/3FKwcWd
- **企业联系人**：联系 EvolutionaryScale 进行自定义部署
