---
name: simpy
description: Python 中基于过程的离散事件仿真框架。在构建具有流程、队列、资源和基于时间的事件的系统（例如制造系统、服务运营、网络流量、物流或实体随时间与共享资源交互的任何系统）的模拟时，请使用此技能。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# SimPy - 离散事件仿真

## 概述

SimPy 是一个基于标准Python 的基于流程的离散事件仿真框架。使用 SimPy 对实体（客户、车辆、数据包等）相互交互并随时间竞争共享资源（服务器、机器、带宽等）的系统进行建模。

* *核心功能：**
- 使用 Python 生成器函数进行流程建模
- 共享资源管理（服务器、容器、商店）
- 事件驱动的调度和同步
- 与挂钟时间同步的实时模拟
- 全面监控和数据收集

## 何时使用此技能

在以下情况下使用SimPy 技能：

1. **建模离散事件系统** - 事件以不规则间隔发生的系统
2. **资源争用** - 实体争夺有限的资源（服务器、机器、员工）
3. **队列分析** - 研究等待线、服务时间和吞吐量
4. **流程优化** - 分析制造、物流或服务流程
5. **网络模拟** - 数据包路由、带宽分配、延迟分析
6. **容量规划** - 确定所需性能的最佳资源水平
7. **系统验证** - 在实现之前测试系统行为

* *不适合：**
- 固定时间步长的连续模拟（考虑SciPy ODE求解器）
- 无资源共享的独立进程
- 纯数学优化（考虑SciPy优化）

## 快速入门

### 基本模拟结构

```python
import simpy

def process(env, name):
    """A simple process that waits and prints."""
    print(f'{name} starting at {env.now}')
    yield env.timeout(5)
    print(f'{name} finishing at {env.now}')

# Create environment
env = simpy.Environment()

# Start processes
env.process(process(env, 'Process 1'))
env.process(process(env, 'Process 2'))

# Run simulation
env.run(until=10)
```

### 资源使用模式

```python
import simpy

def customer(env, name, resource):
    """Customer requests resource, uses it, then releases."""
    with resource.request() as req:
        yield req  # Wait for resource
        print(f'{name} got resource at {env.now}')
        yield env.timeout(3)  # Use resource
        print(f'{name} released resource at {env.now}')

env = simpy.Environment()
server = simpy.Resource(env, capacity=1)

env.process(customer(env, 'Customer 1', server))
env.process(customer(env, 'Customer 2', server))
env.run()
```

## 核心概念

### 1.环境

模拟环境管理时间和调度events.

```python
import simpy

# Standard environment (runs as fast as possible)
env = simpy.Environment(initial_time=0)

# Real-time environment (synchronized with wall-clock)
import simpy.rt
env_rt = simpy.rt.RealtimeEnvironment(factor=1.0)

# Run simulation
env.run(until=100)  # Run until time 100
env.run()  # Run until no events remain
```

### 2.进程

进程是使用Python生成器函数（带有`yield`语句的函数）定义的。

```python
def my_process(env, param1, param2):
    """Process that yields events to pause execution."""
    print(f'Starting at {env.now}')

    # Wait for time to pass
    yield env.timeout(5)

    print(f'Resumed at {env.now}')

    # Wait for another event
    yield env.timeout(3)

    print(f'Done at {env.now}')
    return 'result'

# Start the process
env.process(my_process(env, 'value1', 'value2'))
```

### 3. 事件

事件是进程同步的基本机制。处理产生事件并在触发这些事件时恢复。

* *常见事件类型：**
- `env.timeout(delay)` - 等待时间过去
- `resource.request()` - 请求资源
- `env.event()` - 创建自定义事件
- `env.process(func())` - 处理为一个事件
- `event1 & event2` - 等待所有事件(AllOf)
- `event1 | event2` - 等待任何事件(AnyOf)

## 资源

SimPy 为不同场景提供了多种资源类型。有关完整详细信息，请参阅 `references/resources.md`.

### 资源类型摘要

|资源类型 |使用案例|
|-------------|----------|
|资源 |容量有限（服务器、机器）|
|优先资源|基于优先级的排队|
|抢占资源 |高优先级可以中断低优先级|
|集装箱|散装物料（燃料、水）|
|商店 | Python对象存储（FIFO）|
|过滤器商店|选择性检索|
|优先存储|优先排序项 |

### 快速参考

```python
import simpy

env = simpy.Environment()

# Basic resource (e.g., servers)
resource = simpy.Resource(env, capacity=2)

# Priority resource
priority_resource = simpy.PriorityResource(env, capacity=1)

# Container (e.g., fuel tank)
fuel_tank = simpy.Container(env, capacity=100, init=50)

# Store (e.g., warehouse)
warehouse = simpy.Store(env, capacity=10)
```

## 常见模拟模式

### 模式1：客户-服务器队列

```python
import simpy
import random

def customer(env, name, server):
    arrival = env.now
    with server.request() as req:
        yield req
        wait = env.now - arrival
        print(f'{name} waited {wait:.2f}, served at {env.now}')
        yield env.timeout(random.uniform(2, 4))

def customer_generator(env, server):
    i = 0
    while True:
        yield env.timeout(random.uniform(1, 3))
        i += 1
        env.process(customer(env, f'Customer {i}', server))

env = simpy.Environment()
server = simpy.Resource(env, capacity=2)
env.process(customer_generator(env, server))
env.run(until=20)
```

### 模式2：生产者-消费者

```python
import simpy

def producer(env, store):
    item_id = 0
    while True:
        yield env.timeout(2)
        item = f'Item {item_id}'
        yield store.put(item)
        print(f'Produced {item} at {env.now}')
        item_id += 1

def consumer(env, store):
    while True:
        item = yield store.get()
        print(f'Consumed {item} at {env.now}')
        yield env.timeout(3)

env = simpy.Environment()
store = simpy.Store(env, capacity=10)
env.process(producer(env, store))
env.process(consumer(env, store))
env.run(until=20)
```

### 模式 3：并行任务执行

```python
import simpy

def task(env, name, duration):
    print(f'{name} starting at {env.now}')
    yield env.timeout(duration)
    print(f'{name} done at {env.now}')
    return f'{name} result'

def coordinator(env):
    # Start tasks in parallel
    task1 = env.process(task(env, 'Task 1', 5))
    task2 = env.process(task(env, 'Task 2', 3))
    task3 = env.process(task(env, 'Task 3', 4))

    # Wait for all to complete
    results = yield task1 & task2 & task3
    print(f'All done at {env.now}')

env = simpy.Environment()
env.process(coordinator(env))
env.run()
```

## 工作流程指南

### 步骤 1：定义系统

Identify:
- **实体**：什么在系统中移动？ （客户、零件、数据包）
- **资源**：有哪些限制？ （服务器、机器、带宽）
- **流程**：有哪些活动？ （到达、服务、出发）
- **指标**：衡量什么？ （等待时间、利用率、吞吐量）

### 步骤 2：实现流程函数

为每种流程类型创建生成器函数：

```python
def entity_process(env, name, resources, parameters):
    # Arrival logic
    arrival_time = env.now

    # Request resources
    with resource.request() as req:
        yield req

        # Service logic
        service_time = calculate_service_time(parameters)
        yield env.timeout(service_time)

    # Departure logic
    collect_statistics(env.now - arrival_time)
```

### 步骤 3：设置监控

使用监控实用程序收集数据。综合技术见`references/monitoring.md`。

```python
from scripts.resource_monitor import ResourceMonitor

# Create and monitor resource
resource = simpy.Resource(env, capacity=2)
monitor = ResourceMonitor(env, resource, "Server")

# After simulation
monitor.report()
```

### 步骤 4：运行和分析

```python
# Run simulation
env.run(until=simulation_time)

# Generate reports
monitor.report()
stats.report()

# Export data for further analysis
monitor.export_csv('results.csv')
```

## 高级功能

### 进程交互

进程可以通过事件、进程产量和中断进行交互。有关详细模式，请参阅 `references/process-interaction.md`。

* *关键机制：**
- **事件信号**：用于协调的共享事件
- **进程产量**：等待其他进程完成
- **中断**：强制恢复进程以抢占

### 实时仿真

将仿真与硬件在环或交互式应用的挂钟时间同步。请参见 `references/real-time.md`.

```python
import simpy.rt

env = simpy.rt.RealtimeEnvironment(factor=1.0)  # 1:1 time mapping
# factor=0.5 means 1 sim unit = 0.5 seconds (2x faster)
```

### 全面监控

监控进程、资源和事件。请参阅 `references/monitoring.md` 了解以下技术：
- 状态变量跟踪
- 资源猴子修补
- 事件跟踪
- 统计收集

## 脚本和模板

### basic_simulation_template.py

Complete用于构建队列模拟的模板：
- 可配置参数
- 统计收集
- 客户生成
- 资源使用
- 报告生成

* *用法：**
```python
from scripts.basic_simulation_template import SimulationConfig, run_simulation

config = SimulationConfig()
config.num_resources = 2
config.sim_time = 100
stats = run_simulation(config)
stats.report()
```

### resources_monitor.py

可重复使用的监控实用程序：
- `ResourceMonitor` - 跟踪单个资源
- `MultiResourceMonitor` - 监控多个资源
- `ContainerMonitor` - 跟踪容器级别
- 自动统计计算
- CSV 导出功能

* *用法：**
```python
from scripts.resource_monitor import ResourceMonitor

monitor = ResourceMonitor(env, resource, "My Resource")
# ... run simulation ...
monitor.report()
monitor.export_csv('data.csv')
```

## 参考文档

特定主题的详细指南：

- **`references/resources.md`** - 带示例的所有资源类型
- **`references/events.md`** -事件系统和模式
- **`references/process-interaction.md`** - 流程同步
- **`references/monitoring.md`** - 数据收集技术
- **`references/real-time.md`** - 实时模拟设置

## 最佳实践

1. **生成器函数**：在过程函数
2中始终使用`yield`。 **资源上下文管理器**：使用`with resource.request() as req:`进行自动清理
3. **再现性**：设置 `random.seed()` 以获得一致的结果 
4. **监控**：在整个模拟过程中收集数据，而不仅仅是在最后
5. **验证**：将简单案例与解析解
6进行比较。 **文档**：注释处理逻辑和参数选择
7. **模块化设计**：独立的流程逻辑、统计和配置

## 常见陷阱

1. **忘记产量**：进程必须产生事件才能暂停
2. **事件重用**：事件只能触发一次
3. **资源泄漏**：使用上下文管理器或确保release
4. **阻塞操作**：避免Python阻塞进程中的调用
5. **时间单位**：与时间单位解释
6保持一致。 **死锁**：确保至少一个流程能够取得进展

## 示例用例

- **制造**：机器调度、生产线、库存管理
- **医疗保健**：急诊室模拟、患者流程、人员分配
- **电信**：网络流量、数据包路由、带宽分配
- **交通**：交通流、物流、车辆路径
- **服务操作**：呼叫中心、零售结账、预约调度
- **计算机系统**：CPU调度、内存管理、I/O操作
