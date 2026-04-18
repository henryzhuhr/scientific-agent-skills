# SimPy 监控和数据收集

本指南涵盖了SimPy中收集数据和监控模拟行为的技术。

## 监控策略

在实施监控之前，定义三件事：

1. **监视什么**：进程、资源、事件或系统状态
2. **何时监控**：在变化时、每隔一段时间或在特定事件时
3. **如何存储数据**：列表、文件、数据库或实时输出

## 1.过程监控

### 状态变量跟踪

通过记录变量变化来跟踪过程状态。

```python
import simpy

def customer(env, name, service_time, log):
    arrival_time = env.now
    log.append(('arrival', name, arrival_time))

    yield env.timeout(service_time)

    departure_time = env.now
    log.append(('departure', name, departure_time))

    wait_time = departure_time - arrival_time
    log.append(('wait_time', name, wait_time))

env = simpy.Environment()
log = []

env.process(customer(env, 'Customer 1', 5, log))
env.process(customer(env, 'Customer 2', 3, log))
env.run()

print('Simulation log:')
for entry in log:
    print(entry)
```

### 时间序列数据Collection

```python
import simpy

def system_monitor(env, system_state, data_log, interval):
    while True:
        data_log.append((env.now, system_state['queue_length'], system_state['utilization']))
        yield env.timeout(interval)

def process(env, system_state):
    while True:
        system_state['queue_length'] += 1
        yield env.timeout(2)
        system_state['queue_length'] -= 1
        system_state['utilization'] = system_state['queue_length'] / 10
        yield env.timeout(3)

env = simpy.Environment()
system_state = {'queue_length': 0, 'utilization': 0.0}
data_log = []

env.process(system_monitor(env, system_state, data_log, interval=1))
env.process(process(env, system_state))
env.run(until=20)

print('Time series data:')
for time, queue, util in data_log:
    print(f'Time {time}: Queue={queue}, Utilization={util:.2f}')
```

### 多变量跟踪

```python
import simpy

class SimulationData:
    def __init__(self):
        self.timestamps = []
        self.queue_lengths = []
        self.processing_times = []
        self.utilizations = []

    def record(self, timestamp, queue_length, processing_time, utilization):
        self.timestamps.append(timestamp)
        self.queue_lengths.append(queue_length)
        self.processing_times.append(processing_time)
        self.utilizations.append(utilization)

def monitored_process(env, data):
    queue_length = 0
    processing_time = 0
    utilization = 0.0

    for i in range(5):
        queue_length = i % 3
        processing_time = 2 + i
        utilization = queue_length / 10

        data.record(env.now, queue_length, processing_time, utilization)
        yield env.timeout(2)

env = simpy.Environment()
data = SimulationData()
env.process(monitored_process(env, data))
env.run()

print(f'Collected {len(data.timestamps)} data points')
```

## 2.资源监控

### Monkey-Patching Resources

Patch资源方法拦截并记录日志操作。

```python
import simpy

def patch_resource(resource, data_log):
    """Patch a resource to log all requests and releases."""

    # Save original methods
    original_request = resource.request
    original_release = resource.release

    # Create wrapper for request
    def logged_request(*args, **kwargs):
        req = original_request(*args, **kwargs)
        data_log.append(('request', resource._env.now, len(resource.queue)))
        return req

    # Create wrapper for release
    def logged_release(*args, **kwargs):
        result = original_release(*args, **kwargs)
        data_log.append(('release', resource._env.now, len(resource.queue)))
        return result

    # Replace methods
    resource.request = logged_request
    resource.release = logged_release

def user(env, name, resource):
    with resource.request() as req:
        yield req
        print(f'{name} using resource at {env.now}')
        yield env.timeout(3)
        print(f'{name} releasing resource at {env.now}')

env = simpy.Environment()
resource = simpy.Resource(env, capacity=1)
log = []

patch_resource(resource, log)

env.process(user(env, 'User 1', resource))
env.process(user(env, 'User 2', resource))
env.run()

print('\nResource log:')
for entry in log:
    print(entry)
```

### 资源子类化

创建具有内置监控的自定义资源类。

```python
import simpy

class MonitoredResource(simpy.Resource):
    def __init__(self, env, capacity):
        super().__init__(env, capacity)
        self.data = []
        self.utilization_data = []

    def request(self, *args, **kwargs):
        req = super().request(*args, **kwargs)
        queue_length = len(self.queue)
        utilization = self.count / self.capacity
        self.data.append(('request', self._env.now, queue_length, utilization))
        self.utilization_data.append((self._env.now, utilization))
        return req

    def release(self, *args, **kwargs):
        result = super().release(*args, **kwargs)
        queue_length = len(self.queue)
        utilization = self.count / self.capacity
        self.data.append(('release', self._env.now, queue_length, utilization))
        self.utilization_data.append((self._env.now, utilization))
        return result

    def average_utilization(self):
        if not self.utilization_data:
            return 0.0
        return sum(u for _, u in self.utilization_data) / len(self.utilization_data)

def user(env, name, resource):
    with resource.request() as req:
        yield req
        print(f'{name} using resource at {env.now}')
        yield env.timeout(2)

env = simpy.Environment()
resource = MonitoredResource(env, capacity=2)

for i in range(5):
    env.process(user(env, f'User {i+1}', resource))

env.run()

print(f'\nAverage utilization: {resource.average_utilization():.2%}')
print(f'Total operations: {len(resource.data)}')
```

### 容器级监控

```python
import simpy

class MonitoredContainer(simpy.Container):
    def __init__(self, env, capacity, init=0):
        super().__init__(env, capacity, init)
        self.level_data = [(0, init)]

    def put(self, amount):
        result = super().put(amount)
        self.level_data.append((self._env.now, self.level))
        return result

    def get(self, amount):
        result = super().get(amount)
        self.level_data.append((self._env.now, self.level))
        return result

def producer(env, container, amount, interval):
    while True:
        yield env.timeout(interval)
        yield container.put(amount)
        print(f'Produced {amount}. Level: {container.level} at {env.now}')

def consumer(env, container, amount, interval):
    while True:
        yield env.timeout(interval)
        yield container.get(amount)
        print(f'Consumed {amount}. Level: {container.level} at {env.now}')

env = simpy.Environment()
container = MonitoredContainer(env, capacity=100, init=50)

env.process(producer(env, container, 20, 3))
env.process(consumer(env, container, 15, 4))
env.run(until=20)

print('\nLevel history:')
for time, level in container.level_data:
    print(f'Time {time}: Level={level}')
```

## 3.事件跟踪

### 环境步骤监控

通过修补环境的步骤功能来监控所有事件。

```python
import simpy

def trace(env, callback):
    """Trace all events processed by the environment."""

    def _trace_step():
        # Get next event before it's processed
        if env._queue:
            time, priority, event_id, event = env._queue[0]
            callback(time, priority, event_id, event)

        # Call original step
        return original_step()

    original_step = env.step
    env.step = _trace_step

def event_callback(time, priority, event_id, event):
    print(f'Event: time={time}, priority={priority}, id={event_id}, type={type(event).__name__}')

def process(env, name):
    print(f'{name}: Starting at {env.now}')
    yield env.timeout(5)
    print(f'{name}: Done at {env.now}')

env = simpy.Environment()
trace(env, event_callback)

env.process(process(env, 'Process 1'))
env.process(process(env, 'Process 2'))
env.run()
```

### 事件调度监控

跟踪事件发生时的情况Scheduled.

```python
import simpy

class MonitoredEnvironment(simpy.Environment):
    def __init__(self):
        super().__init__()
        self.scheduled_events = []

    def schedule(self, event, priority=simpy.core.NORMAL, delay=0):
        super().schedule(event, priority, delay)
        scheduled_time = self.now + delay
        self.scheduled_events.append((scheduled_time, priority, type(event).__name__))

def process(env, name, delay):
    print(f'{name}: Scheduling timeout for {delay} at {env.now}')
    yield env.timeout(delay)
    print(f'{name}: Resumed at {env.now}')

env = MonitoredEnvironment()
env.process(process(env, 'Process 1', 5))
env.process(process(env, 'Process 2', 3))
env.run()

print('\nScheduled events:')
for time, priority, event_type in env.scheduled_events:
    print(f'Time {time}, Priority {priority}, Type {event_type}')
```

## 4.统计监控

### 队列统计

```python
import simpy

class QueueStatistics:
    def __init__(self):
        self.arrival_times = []
        self.departure_times = []
        self.queue_lengths = []
        self.wait_times = []

    def record_arrival(self, time, queue_length):
        self.arrival_times.append(time)
        self.queue_lengths.append(queue_length)

    def record_departure(self, arrival_time, departure_time):
        self.departure_times.append(departure_time)
        self.wait_times.append(departure_time - arrival_time)

    def average_wait_time(self):
        return sum(self.wait_times) / len(self.wait_times) if self.wait_times else 0

    def average_queue_length(self):
        return sum(self.queue_lengths) / len(self.queue_lengths) if self.queue_lengths else 0

def customer(env, resource, stats):
    arrival_time = env.now
    stats.record_arrival(arrival_time, len(resource.queue))

    with resource.request() as req:
        yield req
        departure_time = env.now
        stats.record_departure(arrival_time, departure_time)
        yield env.timeout(2)

env = simpy.Environment()
resource = simpy.Resource(env, capacity=1)
stats = QueueStatistics()

for i in range(5):
    env.process(customer(env, resource, stats))

env.run()

print(f'Average wait time: {stats.average_wait_time():.2f}')
print(f'Average queue length: {stats.average_queue_length():.2f}')
```

## 5.数据导出

### CSV导出

```python
import simpy
import csv

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time', 'Metric', 'Value'])
        writer.writerows(data)

def monitored_simulation(env, data_log):
    for i in range(10):
        data_log.append((env.now, 'queue_length', i % 3))
        data_log.append((env.now, 'utilization', (i % 3) / 10))
        yield env.timeout(1)

env = simpy.Environment()
data = []
env.process(monitored_simulation(env, data))
env.run()

export_to_csv(data, 'simulation_data.csv')
print('Data exported to simulation_data.csv')
```

### 实时绘图（需要matplotlib）

```python
import simpy
import matplotlib.pyplot as plt

class RealTimePlotter:
    def __init__(self):
        self.times = []
        self.values = []

    def update(self, time, value):
        self.times.append(time)
        self.values.append(value)

    def plot(self, title='Simulation Results'):
        plt.figure(figsize=(10, 6))
        plt.plot(self.times, self.values)
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title(title)
        plt.grid(True)
        plt.show()

def monitored_process(env, plotter):
    value = 0
    for i in range(20):
        value = value * 0.9 + (i % 5)
        plotter.update(env.now, value)
        yield env.timeout(1)

env = simpy.Environment()
plotter = RealTimePlotter()
env.process(monitored_process(env, plotter))
env.run()

plotter.plot('Process Value Over Time')
```

## 最佳实践

1. **最小化开销**：仅监控必要的内容；过多的日志记录会减慢模拟速度

2. **结构化数据**：对复杂数据点使用类或命名元组

3. **时间戳**：始终在监控数据中包含时间戳

4. **聚合**：对于长时间模拟，聚合数据而不是存储每个事件

5. **惰性评估**：模拟后考虑收集原始数据和计算统计数据

6. **内存管理**：对于很长时间的模拟，定期将数据刷新到磁盘

7. **验证**：验证监控代码不会影响模拟行为

8. **关注点分离**：将监控代码与模拟逻辑分开

9. **可重用组件**：创建可在模拟中重用的通用监控类
