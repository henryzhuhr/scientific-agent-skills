# SimPy 实时模拟

本指南介绍了 SimPy 中的实时模拟功能，其中模拟时间与挂钟时间同步。

## 概述

实时模拟将模拟时间与实际挂钟时间同步。这对于：

- **硬件在环 (HIL)** 测试
- **与模拟的人机交互**
- **实时约束下的算法行为分析**
- **系统集成** 测试
- **演示**目的

## 实时环境

将标准的`Environment`替换为`simpy.rt.RealtimeEnvironment`，实现实时同步。

### 基本用法

```python
import simpy.rt

def process(env):
    while True:
        print(f'Tick at {env.now}')
        yield env.timeout(1)

# Real-time environment with 1:1 time mapping
env = simpy.rt.RealtimeEnvironment(factor=1.0)
env.process(process(env))
env.run(until=5)
```

### 构造函数参数

```python
simpy.rt.RealtimeEnvironment(
    initial_time=0,      # Starting simulation time
    factor=1.0,          # Real time per simulation time unit
    strict=True          # Raise errors on timing violations
)
```

## 使用因子

进行时间缩放`factor`参数控制模拟时间如何映射到实时。

### 因子示例

```python
import simpy.rt
import time

def timed_process(env, label):
    start = time.time()
    print(f'{label}: Starting at {env.now}')
    yield env.timeout(2)
    elapsed = time.time() - start
    print(f'{label}: Completed at {env.now} (real time: {elapsed:.2f}s)')

# Factor = 1.0: 1 simulation time unit = 1 second
print('Factor = 1.0 (2 sim units = 2 seconds)')
env = simpy.rt.RealtimeEnvironment(factor=1.0)
env.process(timed_process(env, 'Normal speed'))
env.run()

# Factor = 0.5: 1 simulation time unit = 0.5 seconds
print('\nFactor = 0.5 (2 sim units = 1 second)')
env = simpy.rt.RealtimeEnvironment(factor=0.5)
env.process(timed_process(env, 'Double speed'))
env.run()

# Factor = 2.0: 1 simulation time unit = 2 seconds
print('\nFactor = 2.0 (2 sim units = 4 seconds)')
env = simpy.rt.RealtimeEnvironment(factor=2.0)
env.process(timed_process(env, 'Half speed'))
env.run()
```

* *因子解释：**
- `factor=1.0` → 1个模拟时间单位需要1个真实时间Second
- `factor=0.1` → 1 个模拟时间单位需要 0.1 真实秒（快 10 倍）
- `factor=60` → 1 个模拟时间单位需要 60 真实秒（1 分钟）

## 严格模式

### strict=True （默认）

如果计算超出分配的实时预算，则提高`RuntimeError`。

```python
import simpy.rt
import time

def heavy_computation(env):
    print(f'Starting computation at {env.now}')
    yield env.timeout(1)

    # Simulate heavy computation (exceeds 1 second budget)
    time.sleep(1.5)

    print(f'Computation done at {env.now}')

env = simpy.rt.RealtimeEnvironment(factor=1.0, strict=True)
env.process(heavy_computation(env))

try:
    env.run()
except RuntimeError as e:
    print(f'Error: {e}')
```

### strict=False

允许模拟运行速度比预期慢而不崩溃。

```python
import simpy.rt
import time

def heavy_computation(env):
    print(f'Starting at {env.now}')
    yield env.timeout(1)

    # Heavy computation
    time.sleep(1.5)

    print(f'Done at {env.now}')

env = simpy.rt.RealtimeEnvironment(factor=1.0, strict=False)
env.process(heavy_computation(env))
env.run()

print('Simulation completed (slower than real-time)')
```

* *使用strict=False 时：**
- 开发和调试
- 计算时间不可预测
- 可以接受比目标速率慢的运行速度
- 分析最坏情况行为

## 硬件在环示例

```python
import simpy.rt

class HardwareInterface:
    """Simulated hardware interface."""

    def __init__(self):
        self.sensor_value = 0

    def read_sensor(self):
        """Simulate reading from hardware sensor."""
        import random
        self.sensor_value = random.uniform(20.0, 30.0)
        return self.sensor_value

    def write_actuator(self, value):
        """Simulate writing to hardware actuator."""
        print(f'Actuator set to {value:.2f}')

def control_loop(env, hardware, setpoint):
    """Simple control loop running in real-time."""
    while True:
        # Read sensor
        sensor_value = hardware.read_sensor()
        print(f'[{env.now}] Sensor: {sensor_value:.2f}°C')

        # Simple proportional control
        error = setpoint - sensor_value
        control_output = error * 0.1

        # Write actuator
        hardware.write_actuator(control_output)

        # Control loop runs every 0.5 seconds
        yield env.timeout(0.5)

# Real-time environment: 1 sim unit = 1 second
env = simpy.rt.RealtimeEnvironment(factor=1.0, strict=False)
hardware = HardwareInterface()
setpoint = 25.0

env.process(control_loop(env, hardware, setpoint))
env.run(until=5)
```

## 人类交互示例

```python
import simpy.rt

def interactive_process(env):
    """Process that waits for simulated user input."""
    print('Simulation started. Events will occur in real-time.')

    yield env.timeout(2)
    print(f'[{env.now}] Event 1: System startup')

    yield env.timeout(3)
    print(f'[{env.now}] Event 2: Initialization complete')

    yield env.timeout(2)
    print(f'[{env.now}] Event 3: Ready for operation')

# Real-time environment for human-paced demonstration
env = simpy.rt.RealtimeEnvironment(factor=1.0)
env.process(interactive_process(env))
env.run()
```

## 监控实时性能

```python
import simpy.rt
import time

class RealTimeMonitor:
    def __init__(self):
        self.step_times = []
        self.drift_values = []

    def record_step(self, sim_time, real_time, expected_real_time):
        self.step_times.append(sim_time)
        drift = real_time - expected_real_time
        self.drift_values.append(drift)

    def report(self):
        if self.drift_values:
            avg_drift = sum(self.drift_values) / len(self.drift_values)
            max_drift = max(abs(d) for d in self.drift_values)
            print(f'\nReal-time performance:')
            print(f'Average drift: {avg_drift*1000:.2f} ms')
            print(f'Maximum drift: {max_drift*1000:.2f} ms')

def monitored_process(env, monitor, start_time, factor):
    for i in range(5):
        step_start = time.time()
        yield env.timeout(1)

        real_elapsed = time.time() - start_time
        expected_elapsed = env.now * factor
        monitor.record_step(env.now, real_elapsed, expected_elapsed)

        print(f'Sim time: {env.now}, Real time: {real_elapsed:.2f}s, ' +
              f'Expected: {expected_elapsed:.2f}s')

start = time.time()
factor = 1.0
env = simpy.rt.RealtimeEnvironment(factor=factor, strict=False)
monitor = RealTimeMonitor()

env.process(monitored_process(env, monitor, start, factor))
env.run()
monitor.report()
```

## 混合实时和快速仿真

```python
import simpy.rt

def background_simulation(env):
    """Fast background simulation."""
    for i in range(100):
        yield env.timeout(0.01)
    print(f'Background simulation completed at {env.now}')

def real_time_display(env):
    """Real-time display updates."""
    for i in range(5):
        print(f'Display update at {env.now}')
        yield env.timeout(1)

# Note: This is conceptual - SimPy doesn't directly support mixed modes
# Consider running separate simulations or using strict=False
env = simpy.rt.RealtimeEnvironment(factor=1.0, strict=False)
env.process(background_simulation(env))
env.process(real_time_display(env))
env.run()
```

## 将标准转换为实时

将标准模拟转换为实时非常简单：

```python
import simpy
import simpy.rt

def process(env):
    print(f'Event at {env.now}')
    yield env.timeout(1)
    print(f'Event at {env.now}')
    yield env.timeout(1)
    print(f'Event at {env.now}')

# Standard simulation (runs instantly)
print('Standard simulation:')
env = simpy.Environment()
env.process(process(env))
env.run()

# Real-time simulation (2 real seconds)
print('\nReal-time simulation:')
env_rt = simpy.rt.RealtimeEnvironment(factor=1.0)
env_rt.process(process(env_rt))
env_rt.run()
```

## 最佳实践

1. **因素选择**：根据硬件/人类限制选择因素
  - 人类交互：`factor=1.0`（1:1 时间映射）
  - 快速硬件：`factor=0.01`（快 100 倍）
  - 慢速进程：`factor=60`（1 sim 单位 = 1 分钟）

2. **严格模式使用**：
  - 使用 `strict=True` 进行时序验证
  - 使用 `strict=False` 进行开发和可变工作负载

3. **计算预算**：确保流程逻辑的执行速度快于超时持续时间

4. **错误处理**：将实时运行包装在 try-除了时序违规

5 中。 **测试策略**：
 - 使用标准环境进行开发（快速迭代）
  - 使用实时环境进行测试（验证）
  - 使用适当的因素和严格的设置进行部署

6. **性能监控**：跟踪模拟和实时之间的漂移

7. **优雅降级**：当时序保证不重要时使用 `strict=False`

## 常见模式

### 定期实时任务

```python
import simpy.rt

def periodic_task(env, name, period, duration):
    """Task that runs periodically in real-time."""
    while True:
        start = env.now
        print(f'{name}: Starting at {start}')

        # Simulate work
        yield env.timeout(duration)

        print(f'{name}: Completed at {env.now}')

        # Wait for next period
        elapsed = env.now - start
        wait_time = period - elapsed
        if wait_time > 0:
            yield env.timeout(wait_time)

env = simpy.rt.RealtimeEnvironment(factor=1.0)
env.process(periodic_task(env, 'Task', period=2.0, duration=0.5))
env.run(until=6)
```

### 同步多设备控制

```python
import simpy.rt

def device_controller(env, device_id, update_rate):
    """Control loop for individual device."""
    while True:
        print(f'Device {device_id}: Update at {env.now}')
        yield env.timeout(update_rate)

# All devices synchronized to real-time
env = simpy.rt.RealtimeEnvironment(factor=1.0)

# Different update rates for different devices
env.process(device_controller(env, 'A', 1.0))
env.process(device_controller(env, 'B', 0.5))
env.process(device_controller(env, 'C', 2.0))

env.run(until=5)
```

## 限制

1. **性能**：实时模拟增加了开销；不适合高频事件
2. **同步**：单线程；所有进程共享相同的时基
3. **精度**：受限于Python的时间分辨率和系统调度
4. **严格模式**：在计算密集型进程中可能会频繁引发错误
5. **取决于平台**：计时精度因操作系统而异
