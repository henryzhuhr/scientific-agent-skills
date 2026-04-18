# PufferLib 矢量化指南

## 概述

PufferLib 的矢量化系统可实现高性能并行环境模拟，通过受 EnvPool 启发的优化实现实现每秒数百万步。该系统以最小的开销支持同步和异步矢量化。

## 矢量化架构

### 关键优化

1. **共享内存缓冲区**：跨所有环境的单个统一缓冲区（与 Gymnasium 的每个环境缓冲区不同）
2. **忙等待标志**：工作人员忙等待解锁标志，而不是使用管道/队列
3. **零复制批处理**：连续的工作子集返回观察结果而不复制
4. **剩余环境**：模拟比异步返回批量大小更多的环境
5. **每个 Worker 多个环境**：优化轻量级环境的性能

### 性能特征

- **纯 Python 环境**：100k-500k SPS
- **基于 C 的环境**：100M+ SPS
- **带训练**：总计 400k-4M SPS
- **矢量化开销**：最佳配置时 <5%

## 创建矢量化环境

### 基本矢量化

```python
import pufferlib

# Automatic vectorization
env = pufferlib.make('environment_name', num_envs=256)

# With explicit configuration
env = pufferlib.make(
    'environment_name',
    num_envs=256,
    num_workers=8,
    envs_per_worker=32
)
```

### 手动矢量化

```python
from pufferlib import PufferEnv
from pufferlib.vectorization import Serial, Multiprocessing

# Serial vectorization (single process)
vec_env = Serial(
    env_creator=lambda: MyEnvironment(),
    num_envs=16
)

# Multiprocessing vectorization
vec_env = Multiprocessing(
    env_creator=lambda: MyEnvironment(),
    num_envs=256,
    num_workers=8
)
```

## 矢量化模式

### 串行矢量化

最适合调试和轻量级环境：

```python
from pufferlib.vectorization import Serial

vec_env = Serial(
    env_creator=env_creator_fn,
    num_envs=16
)

# All environments run in main process
# No multiprocessing overhead
# Easier debugging with standard tools
```

* *何时使用：**
- 开发和调试
- 非常快的环境（每步<1μs）
- 少量环境（< 32)
- 单线程分析

### 多处理矢量化

最适合大多数生产用例：

```python
from pufferlib.vectorization import Multiprocessing

vec_env = Multiprocessing(
    env_creator=env_creator_fn,
    num_envs=256,
    num_workers=8,
    envs_per_worker=32
)

# Parallel execution across workers
# True parallelism for CPU-bound environments
# Scales to hundreds of environments
```

* *何时使用：**
- 生产培训
- CPU 密集型环境
- 大规模并行模拟
- 最大化吞吐量

### 异步矢量化

对于具有可变步长时间的环境：

```python
vec_env = Multiprocessing(
    env_creator=env_creator_fn,
    num_envs=256,
    num_workers=8,
    mode='async',
    surplus_envs=32  # Simulate extra environments
)

# Returns batches as soon as ready
# Better GPU utilization
# Handles variable environment speeds
```

* *何时使用：**
- 可变环境步骤时间
- 最大化 GPU 利用率
- 基于网络的环境
- 外部模拟器

## 优化矢量化性能

### Worker配置

```python
import multiprocessing

# Calculate optimal workers
num_cpus = multiprocessing.cpu_count()

# Conservative (leave headroom for training)
num_workers = num_cpus - 2

# Aggressive (maximize environment throughput)
num_workers = num_cpus

# With hyperthreading
num_workers = num_cpus // 2  # Physical cores only
```

### 每个工作线程的环境

```python
# Fast environments (< 10μs per step)
envs_per_worker = 64  # More envs per worker

# Medium environments (10-100μs per step)
envs_per_worker = 32  # Balanced

# Slow environments (> 100μs per step)
envs_per_worker = 16  # Fewer envs per worker

# Calculate from target batch size
batch_size = 32768
num_workers = 8
envs_per_worker = batch_size // num_workers
```

### 批量大小调整

```python
# Small batch (< 8k): Good for fast iteration
batch_size = 4096
num_envs = 256
steps_per_env = batch_size // num_envs  # 16 steps

# Medium batch (8k-32k): Good balance
batch_size = 16384
num_envs = 512
steps_per_env = 32

# Large batch (> 32k): Maximum throughput
batch_size = 65536
num_envs = 1024
steps_per_env = 64
```

## 共享内存优化

### 缓冲区管理

PufferLib使用共享内存进行零拷贝观察传递：

```python
import numpy as np
from multiprocessing import shared_memory

class OptimizedEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Environment will use provided shared buffer
        self.observation_space = self.make_space({'obs': (84, 84, 3)})

        # Observations written directly to shared memory
        self._obs_buffer = None

    def reset(self):
        # Write to shared memory in-place
        if self._obs_buffer is None:
            self._obs_buffer = np.zeros((84, 84, 3), dtype=np.uint8)

        self._render_to_buffer(self._obs_buffer)
        return {'obs': self._obs_buffer}

    def step(self, action):
        # In-place updates only
        self._update_state(action)
        self._render_to_buffer(self._obs_buffer)

        return {'obs': self._obs_buffer}, reward, done, info
```

### 零拷贝模式

```python
# BAD: Creates copies
def get_observation(self):
    obs = np.zeros((84, 84, 3))
    # ... fill obs ...
    return obs.copy()  # Unnecessary copy!

# GOOD: Reuses buffer
def get_observation(self):
    # Use pre-allocated buffer
    self._render_to_buffer(self._obs_buffer)
    return self._obs_buffer  # No copy

# BAD: Allocates new arrays
def step(self, action):
    new_state = self.state + action  # Allocates
    self.state = new_state
    return obs, reward, done, info

# GOOD: In-place operations
def step(self, action):
    self.state += action  # In-place
    return obs, reward, done, info
```

## 高级矢量化

### 自定义矢量化

```python
from pufferlib.vectorization import VectorEnv

class CustomVectorEnv(VectorEnv):
    """Custom vectorization implementation."""

    def __init__(self, env_creator, num_envs, **kwargs):
        super().__init__()

        self.envs = [env_creator() for _ in range(num_envs)]
        self.num_envs = num_envs

    def reset(self):
        """Reset all environments."""
        observations = [env.reset() for env in self.envs]
        return self._stack_obs(observations)

    def step(self, actions):
        """Step all environments."""
        results = [env.step(action) for env, action in zip(self.envs, actions)]

        obs, rewards, dones, infos = zip(*results)

        return (
            self._stack_obs(obs),
            np.array(rewards),
            np.array(dones),
            list(infos)
        )

    def _stack_obs(self, observations):
        """Stack observations into batch."""
        return np.stack(observations, axis=0)
```

### 分层矢量化

对于超大规模并行：

```python
# Outer: Multiprocessing vectorization (8 workers)
# Inner: Each worker runs serial vectorization (32 envs)
# Total: 256 parallel environments

def create_serial_vec_env():
    return Serial(
        env_creator=lambda: MyEnvironment(),
        num_envs=32
    )

outer_vec_env = Multiprocessing(
    env_creator=create_serial_vec_env,
    num_envs=8,  # 8 serial vec envs
    num_workers=8
)

# Total environments: 8 * 32 = 256
```

## 多代理矢量化

### 原生多代理支持

PufferLib将多代理环境视为一等公民：

```python
# Multi-agent environment automatically vectorized
env = pufferlib.make(
    'pettingzoo-knights-archers-zombies',
    num_envs=128,
    num_agents=4
)

# Observations: {agent_id: [batch_obs]} for each agent
# Actions: {agent_id: [batch_actions]} for each agent
# Rewards: {agent_id: [batch_rewards]} for each agent
```

### 自定义多代理矢量化

```python
class MultiAgentVectorEnv(VectorEnv):
    def step(self, actions):
        """
        Args:
            actions: Dict of {agent_id: [batch_actions]}

        Returns:
            observations: Dict of {agent_id: [batch_obs]}
            rewards: Dict of {agent_id: [batch_rewards]}
            dones: Dict of {agent_id: [batch_dones]}
            infos: List of dicts
        """
        # Distribute actions to environments
        env_actions = self._distribute_actions(actions)

        # Step each environment
        results = [env.step(act) for env, act in zip(self.envs, env_actions)]

        # Collect and batch results
        return self._batch_results(results)
```

## 性能监控

### 分析矢量化

```python
import time

def profile_vectorization(vec_env, num_steps=10000):
    """Profile vectorization performance."""
    start = time.time()

    vec_env.reset()

    for _ in range(num_steps):
        actions = vec_env.action_space.sample()
        vec_env.step(actions)

    elapsed = time.time() - start
    sps = (num_steps * vec_env.num_envs) / elapsed

    print(f"Steps per second: {sps:,.0f}")
    print(f"Time per step: {elapsed/num_steps*1000:.2f}ms")

    return sps
```

### 瓶颈分析

```python
import cProfile
import pstats

def analyze_bottlenecks(vec_env):
    """Identify vectorization bottlenecks."""
    profiler = cProfile.Profile()

    profiler.enable()

    vec_env.reset()
    for _ in range(1000):
        actions = vec_env.action_space.sample()
        vec_env.step(actions)

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
```

### 实时监控

```python
class MonitoredVectorEnv(VectorEnv):
    """Vector environment with performance monitoring."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.step_times = []
        self.step_count = 0

    def step(self, actions):
        start = time.perf_counter()

        result = super().step(actions)

        elapsed = time.perf_counter() - start
        self.step_times.append(elapsed)
        self.step_count += 1

        # Log every 1000 steps
        if self.step_count % 1000 == 0:
            mean_time = np.mean(self.step_times[-1000:])
            sps = self.num_envs / mean_time
            print(f"SPS: {sps:,.0f} | Step time: {mean_time*1000:.2f}ms")

        return result
```

## 故障排除

### 低吞吐量

```python
# Check configuration
print(f"Num envs: {vec_env.num_envs}")
print(f"Num workers: {vec_env.num_workers}")
print(f"Envs per worker: {vec_env.num_envs // vec_env.num_workers}")

# Profile single environment
single_env = MyEnvironment()
single_sps = profile_single_env(single_env)
print(f"Single env SPS: {single_sps:,.0f}")

# Compare vectorized
vec_sps = profile_vectorization(vec_env)
print(f"Vectorized SPS: {vec_sps:,.0f}")
print(f"Speedup: {vec_sps / single_sps:.1f}x")
```

### 内存问题

```python
# Reduce number of environments
num_envs = 128  # Instead of 256

# Reduce envs per worker
envs_per_worker = 16  # Instead of 32

# Use Serial mode for debugging
vec_env = Serial(env_creator, num_envs=16)
```

### 同步问题

```python
# Ensure thread-safe operations
import threading

class ThreadSafeEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)
        self.lock = threading.Lock()

    def step(self, action):
        with self.lock:
            return super().step(action)
```

## 最佳实践

### 配置指南

```python
# Start conservative
config = {
    'num_envs': 64,
    'num_workers': 4,
    'envs_per_worker': 16
}

# Scale up iteratively
config = {
    'num_envs': 256,     # 4x increase
    'num_workers': 8,     # 2x increase
    'envs_per_worker': 32 # 2x increase
}

# Monitor and adjust
if sps < target_sps:
    # Try increasing num_envs or num_workers
    pass
if memory_usage > threshold:
    # Reduce num_envs or envs_per_worker
    pass
```

### 环境设计

```python
# Minimize per-step allocations
class EfficientEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Pre-allocate all buffers
        self._obs = np.zeros((84, 84, 3), dtype=np.uint8)
        self._state = np.zeros(10, dtype=np.float32)

    def step(self, action):
        # Use pre-allocated buffers
        self._update_state_inplace(action)
        self._render_to_obs()

        return self._obs, reward, done, info
```

### 测试

```python
# Test vectorization matches serial
serial_env = Serial(env_creator, num_envs=4)
vec_env = Multiprocessing(env_creator, num_envs=4, num_workers=2)

# Run parallel and verify results match
serial_env.seed(42)
vec_env.seed(42)

serial_obs = serial_env.reset()
vec_obs = vec_env.reset()

assert np.allclose(serial_obs, vec_obs), "Vectorization mismatch!"
```
