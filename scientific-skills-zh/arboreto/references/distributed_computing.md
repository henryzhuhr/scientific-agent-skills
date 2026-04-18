# Arboreto分布式计算

Arboreto利用Dask进行并行计算，实现从单机多核处理到多节点集群环境的高效GRN推理。

## 计算架构

GRN推理本质上是可并行的：
- 每个目标基因的回归模型都可以训练独立地
- Arboreto 将计算表示为Dask 任务图
- 任务分布在可用计算资源上

## 本地多核处理（默认）

默认情况下，arboreto 使用本地上所有可用的CPU 核心machine:

```python
from arboreto.algo import grnboost2

# Automatically uses all local cores
network = grnboost2(expression_data=expression_matrix, tf_names=tf_names)
```

这对于大多数用例来说已经足够了，不需要额外的配置。

## 自定义本地Dask客户端

为了对本地资源进行细粒度控制，创建一个自定义Dask客户端：

```python
from distributed import LocalCluster, Client
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Configure local cluster
    local_cluster = LocalCluster(
        n_workers=10,              # Number of worker processes
        threads_per_worker=1,       # Threads per worker
        memory_limit='8GB'          # Memory limit per worker
    )

    # Create client
    custom_client = Client(local_cluster)

    # Run inference with custom client
    network = grnboost2(
        expression_data=expression_matrix,
        tf_names=tf_names,
        client_or_address=custom_client
    )

    # Clean up
    custom_client.close()
    local_cluster.close()
```

### 自定义客户端的好处
- **资源控制**：限制CPU和内存使用
- **多次运行**：为不同的参数集重复使用同一客户端
- **监控**：访问Dask仪表板以获取性能见解

## 使用相同的多次推理运行客户端

重复使用单个 Dask 客户端进行具有不同参数的多次推理运行：

```python
from distributed import LocalCluster, Client
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Initialize client once
    local_cluster = LocalCluster(n_workers=8, threads_per_worker=1)
    client = Client(local_cluster)

    # Run multiple inferences
    network_seed1 = grnboost2(
        expression_data=expression_matrix,
        tf_names=tf_names,
        client_or_address=client,
        seed=666
    )

    network_seed2 = grnboost2(
        expression_data=expression_matrix,
        tf_names=tf_names,
        client_or_address=client,
        seed=777
    )

    # Different algorithms with same client
    from arboreto.algo import genie3
    network_genie3 = genie3(
        expression_data=expression_matrix,
        tf_names=tf_names,
        client_or_address=client
    )

    # Clean up once
    client.close()
    local_cluster.close()
```

## 分布式集群计算

对于非常大的数据集，连接到在集群上运行的远程 Dask 分布式调度程序：

### 步骤 1：设置Dask 调度程序（在集群头节点上）
```bash
dask-scheduler
# Output: Scheduler at tcp://10.118.224.134:8786
```

### 步骤 2：启动 Dask Workers（在集群计算节点上）
```bash
dask-worker tcp://10.118.224.134:8786
```

### 步骤 3：从以下位置连接客户端
```python
from distributed import Client
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Connect to remote scheduler
    scheduler_address = 'tcp://10.118.224.134:8786'
    cluster_client = Client(scheduler_address)

    # Run inference on cluster
    network = grnboost2(
        expression_data=expression_matrix,
        tf_names=tf_names,
        client_or_address=cluster_client
    )

    cluster_client.close()
```

### 集群配置最佳实践

* *Worker配置**：
```bash
dask-worker tcp://scheduler:8786 \
    --nprocs 4 \              # Number of processes per node
    --nthreads 1 \            # Threads per process
    --memory-limit 16GB       # Memory per process
```

* *用于大规模推理**：
- 使用更多具有中等内存的worker而不是更少具有大内存的worker
- 设置`threads_per_worker=1`以避免scikit-learn中的GIL争用
- 监视内存使用情况以防止worker被kill

## 监控调试

### Dask仪表板

访问Dask仪表板实时监控：

```python
from distributed import Client

client = Client()  # Prints dashboard URL
# Dashboard available at: http://localhost:8787/status
```

仪表板显示：
- **任务进度**：任务数量已完成/待处理
- **资源使用**：每个工作线程的 CPU、内存
- **任务流**：计算的实时可视化
- **性能**：瓶颈识别

### 详细输出

启用详细日志记录以跟踪推理进度：

```python
network = grnboost2(
    expression_data=expression_matrix,
    tf_names=tf_names,
    verbose=True
)
```

## 性能优化技巧

### 1. 数据格式
- **尽可能使用 Pandas DataFrame**：Dask 操作比 NumPy 更高效
- **减少数据大小**：在推理之前过滤低方差基因

### 2. Worker 配置
- **CPU 密集型任务**：设置 `threads_per_worker=1`，增加`n_workers`
- **内存密集型任务**：增加每个worker的`memory_limit`

### 3.集群设置
- **网络**：确保节点之间的高带宽、低延迟网络
- **存储**：对大型数据集使用共享文件系统或对象存储
- **调度**：分配专用节点，避免资源争用

### 4.转录因子过滤
- **限制TF列表**：提供特定的TF名称减少计算
```python
# Full search (slow)
network = grnboost2(expression_data=matrix)

# Filtered search (faster)
network = grnboost2(expression_data=matrix, tf_names=known_tfs)
```

## 示例：大规模单细胞分析

处理单细胞的完整工作流程簇上的 RNA-seq 数据：

```python
from distributed import Client
from arboreto.algo import grnboost2
import pandas as pd

if __name__ == '__main__':
    # Connect to cluster
    client = Client('tcp://cluster-scheduler:8786')

    # Load large single-cell dataset (50,000 cells x 20,000 genes)
    expression_data = pd.read_csv('scrnaseq_data.tsv', sep='\t')

    # Load cell-type-specific TFs
    tf_names = pd.read_csv('tf_list.txt', header=None)[0].tolist()

    # Run distributed inference
    network = grnboost2(
        expression_data=expression_data,
        tf_names=tf_names,
        client_or_address=client,
        verbose=True,
        seed=42
    )

    # Save results
    network.to_csv('grn_results.tsv', sep='\t', index=False)

    client.close()
```

这种方法可以分析在单台机器上不切实际的数据集。
