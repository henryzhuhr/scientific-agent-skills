# Dask Schedulers

## 概述

Dask 提供多个任务调度程序，每个任务调度程序适合不同的工作负载。调度程序决定任务的执行方式：顺序执行、并行线程执行、并行进程执行或跨集群分布。

## 调度程序类型

### 单机调度程序

#### 1. 本地线程（默认）

* *说明**：线程调度程序使用本地线程执行计算`concurrent.futures.ThreadPoolExecutor`.

* *何时使用**：
- NumPy、Pandas、scikit-learn 中的数值计算
- 释放 GIL（全局解释器锁）的库
- 操作受益于共享内存访问
- Dask 数组的默认值和 DataFrames

* *特性**：
- 低开销
- 线程之间共享内存
- 最适合 GIL 释放操作
- 不适合纯 Python 代码（GIL争用）

* *示例**：
```python
import dask.array as da

# Uses threads by default
x = da.random.random((10000, 10000), chunks=(1000, 1000))
result = x.mean().compute()  # Computed with threads
```

* *显式配置**：
```python
import dask

# Set globally
dask.config.set(scheduler='threads')

# Or per-compute
result = x.mean().compute(scheduler='threads')
```

#### 2.本地进程

* *描述**：使用的多处理调度程序`concurrent.futures.ProcessPoolExecutor`.

* *何时使用**：
- 具有 GIL 争用的纯 Python 代码
- 文本处理和 Python 集合
- 受益于进程隔离的操作
- CPU 绑定的 Python 代码

* *特性**：
- 绕过 GIL 限制
- 在进程之间产生数据传输成本
- 比线程更高的开销
- 非常适合具有小输入/输出的线性工作流程

* *示例**：
```python
import dask.bag as db

# Good for Python object processing
bag = db.read_text('data/*.txt')
result = bag.map(complex_python_function).compute(scheduler='processes')
```

* *显式配置**：
```python
import dask

# Set globally
dask.config.set(scheduler='processes')

# Or per-compute
result = computation.compute(scheduler='processes')
```

* *限制**：
- 数据必须可序列化（pickle）
- 进程创建的开销
- 数据复制的内存开销

#### 3.单线程（同步）

* *说明**：单线程同步调度器在本地线程中执行所有计算，完全没有并行性。

* *何时使用**：
- 使用 pdb 进行调试
- 使用标准 Python 工具进行分析
- 详细了解错误
- 开发和测试

  * *特性**：
- 无并行性
- 轻松调试
- 否开销
- 确定性执行

* *示例**：
```python
import dask

# Enable for debugging
dask.config.set(scheduler='synchronous')

# Now can use pdb
result = computation.compute()  # Runs in single thread
```

* *使用IPython调试**：
```python
# In IPython/Jupyter
%pdb on

dask.config.set(scheduler='synchronous')
result = problematic_computation.compute()  # Drops into debugger on error
```

### 分布式调度程序

#### 4.本地分布式

* *描述**：尽管它的名字，这个调度程序使用分布式调度程序基础设施在个人机器上有效运行。

* *何时使用**：
- 需要诊断仪表板
- 异步API
- 比多处理更好的数据局部性处理
- 在扩展到之前的开发cluster
- 希望在单机上实现分布式功能

* *特性**：
- 提供用于监控的仪表板
- 更好的内存管理
- 比线程/进程更多的开销
- 可以扩展到集群稍后

* *示例**：
```python
from dask.distributed import Client
import dask.dataframe as dd

# Create local cluster
client = Client()  # Automatically uses all cores

# Use distributed scheduler
ddf = dd.read_csv('data.csv')
result = ddf.groupby('category').mean().compute()

# View dashboard
print(client.dashboard_link)

# Clean up
client.close()
```

* *配置选项**：
```python
# Control resources
client = Client(
    n_workers=4,
    threads_per_worker=2,
    memory_limit='4GB'
)
```

#### 5. Cluster Distributed

* *说明**：用于使用分布式在多台机器上进行扩展Scheduler.

* *何时使用**：
- 数据超过单机容量
- 需要超出一台机器的计算能力
- 生产部署
- 集群计算环境（HPC、云）

* *特性**：
- 扩展到数百个机器
- 需要集群设置
- 网络通信开销
- 高级功能（自适应扩展、任务优先级）

* * Dask-Jobqueue (HPC)示例**：
```python
from dask_jobqueue import SLURMCluster
from dask.distributed import Client

# Create cluster on HPC with SLURM
cluster = SLURMCluster(
    cores=24,
    memory='100GB',
    walltime='02:00:00',
    queue='regular'
)

# Scale to 10 jobs
cluster.scale(jobs=10)

# Connect client
client = Client(cluster)

# Run computation
result = computation.compute()

client.close()
```

* * 示例Kubernetes 上的 Dask**:
```python
from dask_kubernetes import KubeCluster
from dask.distributed import Client

cluster = KubeCluster()
cluster.scale(20)  # 20 workers

client = Client(cluster)
result = computation.compute()

client.close()
```

## 调度程序配置

### 全局配置

```python
import dask

# Set scheduler globally for session
dask.config.set(scheduler='threads')
dask.config.set(scheduler='processes')
dask.config.set(scheduler='synchronous')
```

### 上下文Manager

```python
import dask

# Temporarily use different scheduler
with dask.config.set(scheduler='processes'):
    result = computation.compute()

# Back to default scheduler
result2 = computation2.compute()
```

### 每计算

```python
# Specify scheduler per compute call
result = computation.compute(scheduler='threads')
result = computation.compute(scheduler='processes')
result = computation.compute(scheduler='synchronous')
```

### 分布式客户端

```python
from dask.distributed import Client

# Using client automatically sets distributed scheduler
client = Client()

# All computations use distributed scheduler
result = computation.compute()

client.close()
```

## 选择正确的调度程序

### 决策矩阵

|工作负载类型 |推荐调度程序 |基本原理 |
|------------------------|------------------------|-----------|
| NumPy/Pandas 操作 |线程（默认）| GIL释放，共享内存|
|纯Python对象|流程|避免 GIL 争用 |
|文本/日志处理 |流程| Python 密集型操作 |
|调试|同步|调试方便，确定性|
|需要仪表板|本地分布式|监控与诊断|
|多机|集群分布式|超过单机容量|
|小数据，快速任务 |主题 |最低开销|
|大数据、单机|本地分布式|更好的内存管理 |

### 性能注意事项

* *线程**：
- 开销：每个任务约 10 µs
- 最适合：数字运算
- 内存：共享
- GIL：受以下因素影响GIL

* *进程**：
- 开销：每个任务约 10 毫秒
- 最适合：Python 操作
- 内存：在进程之间复制
- GIL：不受影响

* *同步**：
- 开销：每个任务约 1 µs任务
- 最适合：调试
- 内存：无并行性
- GIL：不相关

* *分布式**：
- 开销：每个任务约1 毫秒
- 最适合：复杂工作流程、监控
- 内存：由管理Scheduler
- GIL：工作人员可以使用线程或进程

## 分布式调度程序的线程配置

### 设置线程计数

```python
from dask.distributed import Client

# Control thread/worker configuration
client = Client(
    n_workers=4,           # Number of worker processes
    threads_per_worker=2   # Threads per worker process
)
```

### 推荐配置

* *对于数字工作负载**：
- 每个进程的目标是大约 4 个线程
- 并行性和开销之间的平衡
- 示例：8 个核心 → 2 个工作线程，每个工作线程 4

* *对于 Python 工作负载**：
- 使用更多工作线程和更少线程
- 示例：8 个核心 → 8 个工作线程，每个线程 1每个

### 环境变量

```bash
# Set thread count via environment
export DASK_NUM_WORKERS=4
export DASK_THREADS_PER_WORKER=2

# Or via config file
```

## 常见模式

### 开发到生产

```python
# Development: Use local distributed for testing
from dask.distributed import Client
client = Client(processes=False)  # In-process for debugging

# Production: Scale to cluster
from dask.distributed import Client
client = Client('scheduler-address:8786')
```

### 混合工作负载

```python
import dask
import dask.dataframe as dd

# Use threads for DataFrame operations
ddf = dd.read_parquet('data.parquet')
result1 = ddf.mean().compute(scheduler='threads')

# Use processes for Python code
import dask.bag as db
bag = db.read_text('logs/*.txt')
result2 = bag.map(parse_log).compute(scheduler='processes')
```

### 调试工作流程

```python
import dask

# Step 1: Debug with synchronous scheduler
dask.config.set(scheduler='synchronous')
result = problematic_computation.compute()

# Step 2: Test with threads
dask.config.set(scheduler='threads')
result = computation.compute()

# Step 3: Scale with distributed
from dask.distributed import Client
client = Client()
result = computation.compute()
```

## 监控和诊断

### 仪表板访问（仅限分布式）

```python
from dask.distributed import Client

client = Client()

# Get dashboard URL
print(client.dashboard_link)
# Opens dashboard in browser showing:
# - Task progress
# - Worker status
# - Memory usage
# - Task stream
# - Resource utilization
```

### 性能分析

```python
# Profile computation
from dask.distributed import Client

client = Client()
result = computation.compute()

# Get performance report
client.profile(filename='profile.html')
```

### 资源监控

```python
# Check worker info
client.scheduler_info()

# Get current tasks
client.who_has()

# Memory usage
client.run(lambda: psutil.virtual_memory().percent)
```

## 高级配置

### 自定义执行器

```python
from concurrent.futures import ThreadPoolExecutor
import dask

# Use custom thread pool
with ThreadPoolExecutor(max_workers=4) as executor:
    dask.config.set(pool=executor)
    result = computation.compute(scheduler='threads')
```

### 自适应缩放（分布式）

```python
from dask.distributed import Client

client = Client()

# Enable adaptive scaling
client.cluster.adapt(minimum=2, maximum=10)

# Cluster scales based on workload
result = computation.compute()
```

### 工作插件

```python
from dask.distributed import Client, WorkerPlugin

class CustomPlugin(WorkerPlugin):
    def setup(self, worker):
        # Initialize worker-specific resources
        worker.custom_resource = initialize_resource()

client = Client()
client.register_worker_plugin(CustomPlugin())
```

## 故障排除

### 线程性能缓慢
* *问题**：线程调度程序的纯Python 代码速度缓慢
* *解决方案**：切换到进程或分布式调度程序

### 进程内存错误
* *问题**：数据太大，无法在之间进行pickle/复制进程
* *解决方案**：使用线程或分布式调度程序

### 调试困难
* *问题**：无法将pdb与并行调度程序一起使用
* *解决方案**：使用同步调度程序进行调试

### 任务开销高
* *问题**：许多微小导致开销的任务
* *解决方案**：使用线程调度程序（最低开销）或增加块大小
