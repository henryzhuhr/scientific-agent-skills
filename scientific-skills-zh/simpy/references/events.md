# SimPy 事件系统

本指南涵盖了SimPy 中的事件系统，它构成了离散事件仿真的基础。

## 事件基础知识

事件是控制仿真流程的核心机制。进程产生事件并在触发这些事件时恢复。

### 事件生命周期

事件通过三种状态进行：

1. **未触发** - 初始状态为内存对象
2. **触发** - 安排在事件队列中； `triggered` 属性为 `True`
3. **已处理** - 从队列中删除并执行回调； `processed` 属性为 `True`

```python
import simpy

env = simpy.Environment()

# Create an event
event = env.event()
print(f'Triggered: {event.triggered}, Processed: {event.processed}')  # Both False

# Trigger the event
event.succeed(value='Event result')
print(f'Triggered: {event.triggered}, Processed: {event.processed}')  # True, False

# Run to process the event
env.run()
print(f'Triggered: {event.triggered}, Processed: {event.processed}')  # True, True
print(f'Value: {event.value}')  # 'Event result'
```

## 核心事件类型

### 超时

控制模拟中的时间进程。最常见的事件类型。

```python
import simpy

def process(env):
    print(f'Starting at {env.now}')
    yield env.timeout(5)
    print(f'Resumed at {env.now}')

    # Timeout with value
    result = yield env.timeout(3, value='Done')
    print(f'Result: {result} at {env.now}')

env = simpy.Environment()
env.process(process(env))
env.run()
```

* *用法：**
- `env.timeout(delay)` - 等待指定时间
- `env.timeout(delay, value=val)` - 等待并返回值

### 进程事件

进程本身就是事件，允许进程等待其他进程完成。

```python
import simpy

def worker(env, name, duration):
    print(f'{name} starting at {env.now}')
    yield env.timeout(duration)
    print(f'{name} finished at {env.now}')
    return f'{name} result'

def coordinator(env):
    # Start worker processes
    worker1 = env.process(worker(env, 'Worker 1', 5))
    worker2 = env.process(worker(env, 'Worker 2', 3))

    # Wait for worker1 to complete
    result = yield worker1
    print(f'Coordinator received: {result}')

    # Wait for worker2
    result = yield worker2
    print(f'Coordinator received: {result}')

env = simpy.Environment()
env.process(coordinator(env))
env.run()
```

### Event

可以手动触发的通用事件。

```python
import simpy

def waiter(env, event):
    print(f'Waiting for event at {env.now}')
    value = yield event
    print(f'Event received with value: {value} at {env.now}')

def triggerer(env, event):
    yield env.timeout(5)
    print(f'Triggering event at {env.now}')
    event.succeed(value='Hello!')

env = simpy.Environment()
event = env.event()
env.process(waiter(env, event))
env.process(triggerer(env, event))
env.run()
```

## 复合事件

### AllOf - 等待多个事件

当所有指定事件发生时触发。

```python
import simpy

def process(env):
    # Start multiple tasks
    task1 = env.timeout(3, value='Task 1 done')
    task2 = env.timeout(5, value='Task 2 done')
    task3 = env.timeout(4, value='Task 3 done')

    # Wait for all to complete
    results = yield simpy.AllOf(env, [task1, task2, task3])
    print(f'All tasks completed at {env.now}')
    print(f'Results: {results}')

    # Alternative syntax using & operator
    task4 = env.timeout(2)
    task5 = env.timeout(3)
    yield task4 & task5
    print(f'Tasks 4 and 5 completed at {env.now}')

env = simpy.Environment()
env.process(process(env))
env.run()
```

* *返回：**将事件映射到其值的字典

* *用例：**
- 并行任务完成
- 屏障同步
- 等待多个资源

### AnyOf - 等待任何事件

在至少发生一个指定事件时触发。

```python
import simpy

def process(env):
    # Start multiple tasks with different durations
    fast_task = env.timeout(2, value='Fast')
    slow_task = env.timeout(10, value='Slow')

    # Wait for first to complete
    results = yield simpy.AnyOf(env, [fast_task, slow_task])
    print(f'First task completed at {env.now}')
    print(f'Results: {results}')

    # Alternative syntax using | operator
    task1 = env.timeout(5)
    task2 = env.timeout(3)
    yield task1 | task2
    print(f'One of the tasks completed at {env.now}')

env = simpy.Environment()
env.process(process(env))
env.run()
```

* *返回：**包含已完成事件及其值的字典

* *用例：**
- 比赛条件
- 超时机制
- 先响应场景

## 事件触发方法

事件可以通过三种方式触发：

### success(value=None)

将事件标记为成功。

```python
event = env.event()
event.succeed(value='Success!')
```

### 失败（异常）

将事件标记为因异常而失败。

```python
def process(env):
    event = env.event()
    event.fail(ValueError('Something went wrong'))

    try:
        yield event
    except ValueError as e:
        print(f'Caught exception: {e}')

env = simpy.Environment()
env.process(process(env))
env.run()
```

### 触发器（事件）

复制另一个事件的结果。

```python
event1 = env.event()
event1.succeed(value='Original')

event2 = env.event()
event2.trigger(event1)  # event2 now has same outcome as event1
```

## 回调

当事件触发时执行的附加函数。

```python
import simpy

def callback(event):
    print(f'Callback executed! Event value: {event.value}')

def process(env):
    event = env.timeout(5, value='Done')
    event.callbacks.append(callback)
    yield event

env = simpy.Environment()
env.process(process(env))
env.run()
```

* *注意：**从进程产生事件会自动添加进程的resume方法作为回调。

## 事件共享

多个进程可以等待相同的事件event.

```python
import simpy

def waiter(env, name, event):
    print(f'{name} waiting at {env.now}')
    value = yield event
    print(f'{name} resumed with {value} at {env.now}')

def trigger_event(env, event):
    yield env.timeout(5)
    event.succeed(value='Go!')

env = simpy.Environment()
shared_event = env.event()

env.process(waiter(env, 'Process 1', shared_event))
env.process(waiter(env, 'Process 2', shared_event))
env.process(waiter(env, 'Process 3', shared_event))
env.process(trigger_event(env, shared_event))

env.run()
```

* *用例：**
- 广播信号
- 屏障同步
- 协调进程恢复

## 高级事件模式

### 超时取消

```python
import simpy

def process_with_timeout(env):
    work = env.timeout(10, value='Work complete')
    timeout = env.timeout(5, value='Timeout!')

    # Race between work and timeout
    result = yield work | timeout

    if work in result:
        print(f'Work completed: {result[work]}')
    else:
        print(f'Timed out: {result[timeout]}')

env = simpy.Environment()
env.process(process_with_timeout(env))
env.run()
```

### 事件链

```python
import simpy

def event_chain(env):
    # Create chain of dependent events
    event1 = env.event()
    event2 = env.event()
    event3 = env.event()

    def trigger_sequence(env):
        yield env.timeout(2)
        event1.succeed(value='Step 1')
        yield env.timeout(2)
        event2.succeed(value='Step 2')
        yield env.timeout(2)
        event3.succeed(value='Step 3')

    env.process(trigger_sequence(env))

    # Wait for sequence
    val1 = yield event1
    print(f'{val1} at {env.now}')
    val2 = yield event2
    print(f'{val2} at {env.now}')
    val3 = yield event3
    print(f'{val3} at {env.now}')

env = simpy.Environment()
env.process(event_chain(env))
env.run()
```

### 条件事件

```python
import simpy

def conditional_process(env):
    temperature = 20

    if temperature > 25:
        yield env.timeout(5)  # Cooling required
        print('System cooled')
    else:
        yield env.timeout(1)  # No cooling needed
        print('Temperature acceptable')

env = simpy.Environment()
env.process(conditional_process(env))
env.run()
```

## 最佳实践

1. **始终产生事件**：进程必须产生事件才能暂停执行
2. **不要多次触发事件**：事件只能触发一次
3. **处理失败**：当产生可能失败的事件时使用 try- except 
4. **并行的复合事件**：使用 AllOf/AnyOf 进行并发操作
5. **用于广播的共享事件**：多个进程可以产生相同的事件
6. **用于数据传递的事件值**：使用事件值在进程之间传递结果
