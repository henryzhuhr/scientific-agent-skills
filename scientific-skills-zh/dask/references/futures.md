# Dask Futures

## 概述

Dask futures 扩展了 Python 的 `concurrent.futures` 接口，支持立即（非延迟）任务执行。与延迟计算（用于 DataFrame、Arrays 和 Bags）不同，futures 在计算可能随时间演变或需要动态工作流构建的情况下提供了更大的灵活性。

## 核心概念

Futures 表示实时任务执行：
- 任务在提交时立即执行（不惰性）
- 每个 future 表示一个远程计算结果
- 之间的自动依赖关系跟踪futures
- 支持动态、不断发展的工作流程
- 直接控制任务调度和数据放置

## 关键功能

### 实时执行
- 任务提交后立即运行
- 无需显式`.compute()` 调用
- 通过以下方式获取结果`.result()` 方法

### 自动依赖关系管理
当您提交具有未来输入的任务时，Dask 自动处理依赖关系跟踪。一旦所有输入 future 完成，它们将被转移到单个工作程序上以进行高效计算。

### 动态工作流程
构建基于中间结果演变的计算：
- 根据先前结果提交新任务
- 条件执行路径
- 具有不同结构的迭代算法

## 何时使用Futures

* *使用 Futures When**：
- 构建动态、不断发展的工作流程
- 需要立即执行任务（而不是懒惰）
- 计算取决于运行时条件
- 需要对任务放置进行精细控制
- 实现自定义并行算法
- 需要有状态计算（使用actor)

* *使用其他集合时**：
- 静态、预定义的计算图（使用延迟、DataFrames、数组）
- 大型集合上的简单数据并行（使用 Bags、DataFrames）
- 标准数组/数据帧操作就足够了

## 设置客户端

期货需要分布式客户端：

```python
from dask.distributed import Client

# Local cluster (on single machine)
client = Client()

# Or specify resources
client = Client(n_workers=4, threads_per_worker=2)

# Or connect to existing cluster
client = Client('scheduler-address:8786')
```

## 提交任务

### 基本提交
```python
from dask.distributed import Client

client = Client()

# Submit single task
def add(x, y):
    return x + y

future = client.submit(add, 1, 2)

# Get result
result = future.result()  # Blocks until complete
print(result)  # 3
```

### 多个任务
```python
# Submit multiple independent tasks
futures = []
for i in range(10):
    future = client.submit(add, i, i)
    futures.append(future)

# Gather results
results = client.gather(futures)  # Efficient parallel gathering
```

### 映射结束输入
```python
# Apply function to multiple inputs
def square(x):
    return x ** 2

# Submit batch of tasks
futures = client.map(square, range(100))

# Gather results
results = client.gather(futures)
```

* *注意**：每个任务都会产生约1ms的开销，使得`map`不太适合数百万个微小任务。对于海量数据集，请使用 Bags 或 DataFrames。

## 使用 Futures

### 检查状态
```python
future = client.submit(expensive_function, arg)

# Check if complete
print(future.done())  # False or True

# Check status
print(future.status)  # 'pending', 'running', 'finished', or 'error'
```

### 非阻塞结果检索
```python
# Non-blocking check
if future.done():
    result = future.result()
else:
    print("Still computing...")

# Or use callbacks
def handle_result(future):
    print(f"Result: {future.result()}")

future.add_done_callback(handle_result)
```

### 错误处理
```python
def might_fail(x):
    if x < 0:
        raise ValueError("Negative value")
    return x ** 2

future = client.submit(might_fail, -5)

try:
    result = future.result()
except ValueError as e:
    print(f"Task failed: {e}")
```

## 任务依赖关系

### 自动依赖关系跟踪
```python
# Submit task
future1 = client.submit(add, 1, 2)

# Use future as input (creates dependency)
future2 = client.submit(add, future1, 10)  # Depends on future1

# Chain dependencies
future3 = client.submit(add, future2, 100)  # Depends on future2

# Get final result
result = future3.result()  # 113
```

### 复杂依赖关系
```python
# Multiple dependencies
a = client.submit(func1, x)
b = client.submit(func2, y)
c = client.submit(func3, a, b)  # Depends on both a and b

result = c.result()
```

## 数据移动优化

### 分散数据
预分散重要数据，避免重复传输：

```python
# Upload data to cluster once
large_dataset = client.scatter(big_data)  # Returns future

# Use scattered data in multiple tasks
futures = [client.submit(process, large_dataset, i) for i in range(100)]

# Each task uses the same scattered data without re-transfer
results = client.gather(futures)
```

### 高效聚集
使用`client.gather()`并发结果集合：

```python
# Better: Gather all at once (parallel)
results = client.gather(futures)

# Worse: Sequential result retrieval
results = [f.result() for f in futures]
```

## 即发即忘

对于不需要结果的副作用任务：

```python
from dask.distributed import fire_and_forget

def log_to_database(data):
    # Write to database, no return value needed
    database.write(data)

# Submit without keeping reference
future = client.submit(log_to_database, data)
fire_and_forget(future)

# Dask won't abandon this computation even without active future reference
```

## 性能特征

### 任务开销
- ~1ms 开销每个任务
- 适合：数千个任务
- 不适合：数百万个小任务

### Worker-to-Worker 通信
- 直接worker-to-worker 数据传输
- 往返延迟：~1ms
- 任务高效依赖项

### 内存管理
Dask 在本地跟踪活跃的 future。当未来由本地 Python 会话进行垃圾收集时，Dask 将随意删除该数据。

* *保留引用**：
```python
# Keep reference to prevent deletion
important_result = client.submit(expensive_calc, data)

# Use result multiple times
future1 = client.submit(process1, important_result)
future2 = client.submit(process2, important_result)
```

## 高级协调

### 分布式基元

* *队列**:
```python
from dask.distributed import Queue

queue = Queue()

def producer():
    for i in range(10):
        queue.put(i)

def consumer():
    results = []
    for _ in range(10):
        results.append(queue.get())
    return results

# Submit tasks
client.submit(producer)
result_future = client.submit(consumer)
results = result_future.result()
```

* *锁**:
```python
from dask.distributed import Lock

lock = Lock()

def critical_section():
    with lock:
        # Only one task executes this at a time
        shared_resource.update()
```
ZXQ NL50QXZ**事件**：
```python
from dask.distributed import Event

event = Event()

def waiter():
    event.wait()  # Blocks until event is set
    return "Event occurred"

def setter():
    time.sleep(5)
    event.set()

# Start both tasks
wait_future = client.submit(waiter)
set_future = client.submit(setter)

result = wait_future.result()  # Waits for setter to complete
```

* *变量**：
```python
from dask.distributed import Variable

var = Variable('my-var')

# Set value
var.set(42)

# Get value from tasks
def reader():
    return var.get()

future = client.submit(reader)
print(future.result())  # 42
```

## Actors

对于有状态、快速变化的工作流程，Actors 可以使工作人员到工作人员的往返延迟约为 1 毫秒，同时绕过调度程序协调。

### 创建 Actors
```python
from dask.distributed import Client

client = Client()

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count

    def get_count(self):
        return self.count

# Create actor on worker
counter = client.submit(Counter, actor=True).result()

# Call methods
future1 = counter.increment()
future2 = counter.increment()
result = counter.get_count().result()
print(result)  # 2
```

### Actor 用例
- 有状态服务（数据库、缓存）
- 快速变化的状态
- 复杂的协调模式
- 实时流应用程序

## 常见模式

### 令人尴尬的并行任务
```python
from dask.distributed import Client

client = Client()

def process_item(item):
    # Independent computation
    return expensive_computation(item)

# Process many items in parallel
items = range(1000)
futures = client.map(process_item, items)

# Gather all results
results = client.gather(futures)
```

### 动态任务提交
```python
def recursive_compute(data, depth):
    if depth == 0:
        return process(data)

    # Split and recurse
    left, right = split(data)
    left_future = client.submit(recursive_compute, left, depth - 1)
    right_future = client.submit(recursive_compute, right, depth - 1)

    # Combine results
    return combine(left_future.result(), right_future.result())

# Start computation
result_future = client.submit(recursive_compute, initial_data, 5)
result = result_future.result()
```

### 参数Sweep
```python
from itertools import product

def run_simulation(param1, param2, param3):
    # Run simulation with parameters
    return simulate(param1, param2, param3)

# Generate parameter combinations
params = product(range(10), range(10), range(10))

# Submit all combinations
futures = [client.submit(run_simulation, p1, p2, p3) for p1, p2, p3 in params]

# Gather results as they complete
from dask.distributed import as_completed

for future in as_completed(futures):
    result = future.result()
    process_result(result)
```

### 具有依赖关系的管道
```python
# Stage 1: Load data
load_futures = [client.submit(load_data, file) for file in files]

# Stage 2: Process (depends on stage 1)
process_futures = [client.submit(process, f) for f in load_futures]

# Stage 3: Aggregate (depends on stage 2)
agg_future = client.submit(aggregate, process_futures)

# Get final result
result = agg_future.result()
```

### 迭代算法
```python
# Initialize
state = client.scatter(initial_state)

# Iterate
for iteration in range(num_iterations):
    # Compute update based on current state
    state = client.submit(update_function, state)

    # Check convergence
    converged = client.submit(check_convergence, state)
    if converged.result():
        break

# Get final state
final_state = state.result()
```

## 最佳实践

### 1. 预分散大数据
```python
# Upload once, use many times
large_data = client.scatter(big_dataset)
futures = [client.submit(process, large_data, i) for i in range(100)]
```

### 2. 使用Gather进行批量检索
```python
# Efficient: Parallel gathering
results = client.gather(futures)

# Inefficient: Sequential
results = [f.result() for f in futures]
```

### 3. 管理内存参考文献
```python
# Keep important futures
important = client.submit(expensive_calc, data)

# Use multiple times
f1 = client.submit(use_result, important)
f2 = client.submit(use_result, important)

# Clean up when done
del important
```

### 4. 适当处理错误
```python
futures = client.map(might_fail, inputs)

# Check for errors
results = []
errors = []
for future in as_completed(futures):
    try:
        results.append(future.result())
    except Exception as e:
        errors.append(e)
```

### 5. 使用as_completed进行渐进式处理
```python
from dask.distributed import as_completed

futures = client.map(process, items)

# Process results as they arrive
for future in as_completed(futures):
    result = future.result()
    handle_result(result)
```

## 调试提示

### 监控仪表板
查看Dask仪表板可以看到：
- 任务进度
- Worker利用率
- 内存使用
- 任务依赖关系

### 检查任务状态
```python
# Inspect future
print(future.status)
print(future.done())

# Get traceback on error
try:
    future.result()
except Exception:
    print(future.traceback())
```

### 配置文件任务
```python
# Get performance data
client.profile(filename='profile.html')
```
