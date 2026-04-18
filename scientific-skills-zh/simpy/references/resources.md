# SimPy 共享资源

本指南涵盖了 SimPy 中的所有资源类型，用于对拥塞点进行建模和资源分配。

## 资源类型概述

SimPy 提供了三个主要类别的共享资源：

1. **资源** - 有限容量资源（例如气泵、服务器）
2. **容器** - 均质散装材料（例如油箱、筒仓）
3. **Stores** - Python 对象存储（例如，项目队列、仓库）

## 1. 资源

一次可以被有限数量的进程使用的模型资源。

### 资源（基本）

基本资源是具有指定的信号量容量.

```python
import simpy

env = simpy.Environment()
resource = simpy.Resource(env, capacity=2)

def process(env, resource, name):
    with resource.request() as req:
        yield req
        print(f'{name} has the resource at {env.now}')
        yield env.timeout(5)
        print(f'{name} releases the resource at {env.now}')

env.process(process(env, resource, 'Process 1'))
env.process(process(env, resource, 'Process 2'))
env.process(process(env, resource, 'Process 3'))
env.run()
```

* *关键属性：**
- `capacity` - 最大并发用户数（默认：1）
- `count` - 当前用户数
- `queue` - 排队列表请求

### PriorityResource

以优先级扩展基本资源（数字越小=优先级越高）。

```python
import simpy

env = simpy.Environment()
resource = simpy.PriorityResource(env, capacity=1)

def process(env, resource, name, priority):
    with resource.request(priority=priority) as req:
        yield req
        print(f'{name} (priority {priority}) has the resource at {env.now}')
        yield env.timeout(5)

env.process(process(env, resource, 'Low priority', priority=10))
env.process(process(env, resource, 'High priority', priority=1))
env.run()
```

* *用例：**
- 紧急服务（救护车在普通车辆之前）
- VIP客户队列
- 带优先级的作业调度

### PreemptiveResource

允许高优先级请求中断较低优先级用户。

```python
import simpy

env = simpy.Environment()
resource = simpy.PreemptiveResource(env, capacity=1)

def process(env, resource, name, priority):
    with resource.request(priority=priority) as req:
        try:
            yield req
            print(f'{name} acquired resource at {env.now}')
            yield env.timeout(10)
            print(f'{name} finished at {env.now}')
        except simpy.Interrupt:
            print(f'{name} was preempted at {env.now}')

env.process(process(env, resource, 'Low priority', priority=10))
env.process(process(env, resource, 'High priority', priority=1))
env.run()
```

* *用例：**
- 操作系统CPU 调度
- 急诊室triage
- 网络数据包优先级

## 2.容器

模型均质散装物料的生产和消耗（连续或离散）。

```python
import simpy

env = simpy.Environment()
container = simpy.Container(env, capacity=100, init=50)

def producer(env, container):
    while True:
        yield env.timeout(5)
        yield container.put(20)
        print(f'Produced 20. Level: {container.level}')

def consumer(env, container):
    while True:
        yield env.timeout(7)
        yield container.get(15)
        print(f'Consumed 15. Level: {container.level}')

env.process(producer(env, container))
env.process(consumer(env, container))
env.run(until=50)
```

* *关键属性：**
- `capacity` - 最大数量（默认： float('inf'))
- `level` - 当前金额
- `init` - 初始金额（默认：0）

* *操作：**
- `put(amount)` - 添加到容器（如果满则块）
- `get(amount)` - 从容器中取出（如果不够则阻塞）

* *使用案例：**
- 加油站油箱
- 制造中的缓冲存储
- 水库
- 电池电量

## 3. 商店

Python 对象的模型生产和消耗。

### Store (Basic)

通用 FIFO 对象存储。

```python
import simpy

env = simpy.Environment()
store = simpy.Store(env, capacity=2)

def producer(env, store):
    for i in range(5):
        yield env.timeout(2)
        item = f'Item {i}'
        yield store.put(item)
        print(f'Produced {item} at {env.now}')

def consumer(env, store):
    while True:
        yield env.timeout(3)
        item = yield store.get()
        print(f'Consumed {item} at {env.now}')

env.process(producer(env, store))
env.process(consumer(env, store))
env.run()
```

* *关键属性：**
- `capacity` - 最大项目数（默认：float('inf')）
- `items` - 存储的项目列表

* *操作：**
- `put(item)` - 添加项目到存储（如果已满则阻塞）
- `get()` - 删除并返回项目（如果为空则阻塞）

### FilterStore

允许基于过滤器函数。

```python
import simpy

env = simpy.Environment()
store = simpy.FilterStore(env, capacity=10)

def producer(env, store):
    for color in ['red', 'blue', 'green', 'red', 'blue']:
        yield env.timeout(1)
        yield store.put({'color': color, 'time': env.now})
        print(f'Produced {color} item at {env.now}')

def consumer(env, store, color):
    while True:
        yield env.timeout(2)
        item = yield store.get(lambda x: x['color'] == color)
        print(f'{color} consumer got item from {item["time"]} at {env.now}')

env.process(producer(env, store))
env.process(consumer(env, store, 'red'))
env.process(consumer(env, store, 'blue'))
env.run(until=15)
```

* *用例：**
- 仓库物品拣选（特定 SKU）
- 具有技能匹配的作业队列
- 按目的地进行数据包路由

### PriorityStore

按优先顺序检索的物品（最低的在前）。

```python
import simpy

class PriorityItem:
    def __init__(self, priority, data):
        self.priority = priority
        self.data = data

    def __lt__(self, other):
        return self.priority < other.priority

env = simpy.Environment()
store = simpy.PriorityStore(env, capacity=10)

def producer(env, store):
    items = [(10, 'Low'), (1, 'High'), (5, 'Medium')]
    for priority, name in items:
        yield env.timeout(1)
        yield store.put(PriorityItem(priority, name))
        print(f'Produced {name} priority item')

def consumer(env, store):
    while True:
        yield env.timeout(5)
        item = yield store.get()
        print(f'Retrieved {item.data} priority item')

env.process(producer(env, store))
env.process(consumer(env, store))
env.run()
```

* *用例：**
- 任务调度
- 打印作业队列
- 消息优先级

## 选择正确的资源类型

|场景 |资源类型 |
|---------|---------------|
|有限的服务器/机器|资源|
|基于优先级的排队 |优先资源|
|抢占式调度|抢占资源|
|燃料、水、散装材料|集装箱|
|通用项目队列 (FIFO) |店铺|
|选择性项目检索 | FilterStore |
|优先订购商品 | PriorityStore |

## 最佳实践

1. **容量规划**：根据系统约束
2设置实际容量。 **请求模式**：使用上下文管理器 (`with resource.request()`)进行自动清理
3. **错误处理**：将抢占式资源包装在 try- except 中以进行中断处理
4. **监控**：跟踪队列长度和利用率（请参阅监控.md）
5. **性能**：FilterStore和PriorityStore的检索时间为O(n)；大型商店明智使用
