# Dask 最佳实践

## 性能优化原则

### 首先从更简单的解决方案开始

在使用 Dask 实现并行计算之前，探索这些替代方案：
 - 针对特定问题的更好算法
  - 高效的文件格式（Parquet、HDF5、Zarr 而不是CSV)
- 通过 Numba 或 Cython 编译代码
- 用于开发和测试的数据采样

这些替代方案通常比分布式系统提供更好的回报，并且应该在扩展到并行计算之前耗尽。

### 块大小策略

* *关键规则**：块应该足够小，以便许多块适合工作人员的可用内存一次。

* *推荐目标**：大小块，以便工作人员可以在不超过可用内存的情况下每个核心容纳10个块。

* *为什么重要**：
- 太大的块：内存溢出和低效的并行化
- 太小的块：过多的调度开销

* *示例计算**：
- 8 个内核，32 GB RAM
- 目标：每个块约 400 MB（32 GB/8 个内核/10 个块）

### 使用仪表板进行监控

Dask 仪表板提供了以下基本可见性：
- 工作线程状态和资源利用率
- 任务进度和瓶颈
- 内存使用模式
- 性能特征

访问仪表板以了解并行工作负载中实际缓慢的部分，而不是猜测优化。

## 要避免的关键陷阱

### 1. 之前不要在本地创建大型对象Dask

* *错误的方法**：
```python
import pandas as pd
import dask.dataframe as dd

# Loads entire dataset into memory first
df = pd.read_csv('large_file.csv')
ddf = dd.from_pandas(df, npartitions=10)
```

* *正确的方法**：
```python
import dask.dataframe as dd

# Let Dask handle the loading
ddf = dd.read_csv('large_file.csv')
```

* *为什么**：使用pandas或NumPy加载数据首先强制调度程序序列化并将这些对象嵌入到任务图中，这违背了并行计算。

* *关键原理**：使用Dask方法加载数据，并使用Dask控制结果。

### 2.避免重复compute()调用

* *错误的方法**：
```python
results = []
for item in items:
    result = dask_computation(item).compute()  # Each compute is separate
    results.append(result)
```

* *正确的方法**：
```python
computations = [dask_computation(item) for item in items]
results = dask.compute(*computations)  # Single compute for all
```

* *为什么**：在循环中调用计算会阻止Dask：
- 并行化不同的计算
- 共享中间体结果
- 优化整体任务图

### 3. 不要构建过大的任务图

* *症状**：
- 一次计算数百万个任务
- 调度开销严重
- 计算前延迟较长开始

* *解决方案**：
- 增加块大小以减少任务数量
- 使用 `map_partitions` 或 `map_blocks` 来融合操作
- 将计算分解为具有中间持久性的较小块
- 考虑问题是否真正需要分布式计算

* *示例使用map_partitions**：
```python
# Instead of applying function to each row
ddf['result'] = ddf.apply(complex_function, axis=1)  # Many tasks

# Apply to entire partitions at once
ddf = ddf.map_partitions(lambda df: df.assign(result=complex_function(df)))
```

## 基础设施注意事项

### 调度程序选择

* *使用线程**：
- 使用GIL释放库（NumPy，Pandas， scikit-learn)
- 受益于共享内存的操作
- 具有数组/数据帧操作的单机工作负载

* *使用进程**：
- 文本处理和Python集合操作
- GIL绑定的纯Python代码
- 需要进程的操作隔离

* *使用分布式调度程序**：
- 多机集群
- 需要诊断仪表板
- 异步API
- 更好的数据局部性处理

### 线程配置

* *建议**：在数字上每个进程的目标是大约4个线程

* *基本原理**：
- 并行性和开销之间的平衡
- 允许高效使用 CPU 内核
- 降低上下文切换成本

### 内存管理

* * 持久策略性**：
```python
# Persist intermediate results that are reused
intermediate = expensive_computation(data).persist()
result1 = intermediate.operation1().compute()
result2 = intermediate.operation2().compute()
```

* *完成后清除内存**：
```python
# Explicitly delete large objects
del intermediate
```

## 数据加载最佳实践

### 使用适当的文件格式

* *对于表格数据**：
- Parquet：柱状、压缩、快速过滤
- CSV：仅适用于小数据或初始摄取

* *对于数组数据**：
- HDF5：适用于数值数组
- Zarr：云原生、并行友好
- NetCDF：带有元数据的科学数据

### 优化数据摄取

* *读取多个文件高效**：
```python
# Use glob patterns to read multiple files in parallel
ddf = dd.read_parquet('data/year=2024/month=*/day=*.parquet')
```

* *尽早指定有用的列**：
```python
# Only read needed columns
ddf = dd.read_parquet('data.parquet', columns=['col1', 'col2', 'col3'])
```

## 常见模式和解决方案

### 模式：尴尬的并行问题

对于独立计算，使用期货：
```python
from dask.distributed import Client

client = Client()
futures = [client.submit(func, arg) for arg in args]
results = client.gather(futures)
```

### 模式：数据预处理管道

使用Bags进行初始ETL，然后转换为结构化格式：
```python
import dask.bag as db

# Process raw JSON
bag = db.read_text('logs/*.json').map(json.loads)
bag = bag.filter(lambda x: x['status'] == 'success')

# Convert to DataFrame for analysis
ddf = bag.to_dataframe()
```

### 模式：迭代算法

之间保存数据迭代次数：
```python
data = dd.read_parquet('data.parquet')
data = data.persist()  # Keep in memory across iterations

for iteration in range(num_iterations):
    data = update_function(data)
    data = data.persist()  # Persist updated version
```

## 调试技巧

### 使用单线程调度器

用于使用pdb进行调试或详细错误检查：
```python
import dask

dask.config.set(scheduler='synchronous')
result = computation.compute()  # Runs in single thread for debugging
```

### 检查任务图Size

计算前检查任务数量：
```python
print(len(ddf.__dask_graph__()))  # Should be reasonable, not millions
```

### 先在小数据上验证

缩放前在小子集上测试逻辑：
```python
# Test on first partition
sample = ddf.head(1000)
# Validate results
# Then scale to full dataset
```

## 性能故障排除

### 症状：计算开始缓慢

* *可能原因**：任务图太大
* *解决方案**：增加块大小或使用map_partitions

### 症状：内存错误

* *可能原因**：
- 块太大
- 中间太多结果
- 用户函数中的内存泄漏

* *解决方案**：
- 减少块大小
- 策略性地使用 persist()并在完成后删除
- 分析用户函数的内存问题

### 症状：并行化较差

* *可能原因**：
- 数据依赖性阻碍并行性
- 块太大（没有足够的任务）
- Python代码上的线程与GIL争用

* *解决方案**：
- 重组计算以减少依赖性
- 增加分区数量
- 切换到多处理Python代码
的调度程序
