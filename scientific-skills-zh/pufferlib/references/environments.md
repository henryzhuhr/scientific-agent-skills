# PufferLib 环境指南

## 概述

PufferLib 提供了用于创建高性能自定义环境的 PufferEnv API，以及包含 20 多个预构建环境的 Ocean 套件。环境支持具有本机矢量化的单代理和多代理场景。

## PufferEnv API

### 核心特征

PufferEnv 旨在通过就地操作提高性能：
- 观察、操作和奖励从共享缓冲区对象初始化
- 所有操作就地发生以避免创建和复制数组
- 对单代理和多代理环境的本机支持
- 用于高效矢量化的平坦观察/操作空间

### 创建 PufferEnv

```python
import numpy as np
import pufferlib
from pufferlib import PufferEnv

class MyEnvironment(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Define observation and action spaces
        self.observation_space = self.make_space({
            'image': (84, 84, 3),
            'vector': (10,)
        })

        self.action_space = self.make_discrete(4)  # 4 discrete actions

        # Initialize state
        self.reset()

    def reset(self):
        """Reset environment to initial state."""
        # Reset internal state
        self.agent_pos = np.array([0, 0])
        self.step_count = 0

        # Return initial observation
        obs = {
            'image': np.zeros((84, 84, 3), dtype=np.uint8),
            'vector': np.zeros(10, dtype=np.float32)
        }

        return obs

    def step(self, action):
        """Execute one environment step."""
        # Update state based on action
        self.step_count += 1

        # Calculate reward
        reward = self._compute_reward()

        # Check if episode is done
        done = self.step_count >= 1000

        # Generate observation
        obs = self._get_observation()

        # Additional info
        info = {'episode': {'r': reward, 'l': self.step_count}} if done else {}

        return obs, reward, done, info

    def _compute_reward(self):
        """Compute reward for current state."""
        return 1.0

    def _get_observation(self):
        """Generate observation from current state."""
        return {
            'image': np.random.randint(0, 256, (84, 84, 3), dtype=np.uint8),
            'vector': np.random.randn(10).astype(np.float32)
        }
```

### 观察空间

#### 离散空间

```python
# Single discrete value
self.observation_space = self.make_discrete(10)  # Values 0-9

# Dict with discrete values
self.observation_space = self.make_space({
    'position': (1,),  # Continuous
    'type': self.make_discrete(5)  # Discrete
})
```

#### 连续空间

```python
# Box space (continuous)
self.observation_space = self.make_space({
    'image': (84, 84, 3),      # Image
    'vector': (10,),            # Vector
    'scalar': (1,)              # Single value
})
```

#### 多离散空间

```python
# Multiple discrete values
self.observation_space = self.make_multi_discrete([3, 5, 2])  # 3 values, 5 values, 2 values
```

### 操作Spaces

```python
# Discrete actions
self.action_space = self.make_discrete(4)  # 4 actions: 0, 1, 2, 3

# Continuous actions
self.action_space = self.make_space((3,))  # 3D continuous action

# Multi-discrete actions
self.action_space = self.make_multi_discrete([3, 3])  # Two 3-way discrete choices
```

## 多代理环境

PufferLib 具有原生多代理支持，统一处理单代理和多代理环境。

### 多代理 PufferEnv

```python
class MultiAgentEnv(PufferEnv):
    def __init__(self, num_agents=4, buf=None):
        super().__init__(buf)

        self.num_agents = num_agents

        # Per-agent observation space
        self.single_observation_space = self.make_space({
            'position': (2,),
            'velocity': (2,),
            'global': (10,)
        })

        # Per-agent action space
        self.single_action_space = self.make_discrete(5)

        self.reset()

    def reset(self):
        """Reset all agents."""
        self.agents = {f'agent_{i}': Agent(i) for i in range(self.num_agents)}

        # Return observations for all agents
        return {
            agent_id: self._get_obs(agent)
            for agent_id, agent in self.agents.items()
        }

    def step(self, actions):
        """Step all agents."""
        # actions is a dict: {agent_id: action}
        observations = {}
        rewards = {}
        dones = {}
        infos = {}

        for agent_id, action in actions.items():
            agent = self.agents[agent_id]

            # Update agent
            agent.update(action)

            # Generate results
            observations[agent_id] = self._get_obs(agent)
            rewards[agent_id] = self._compute_reward(agent)
            dones[agent_id] = agent.is_done()
            infos[agent_id] = {}

        # Check for global done condition
        dones['__all__'] = all(dones.values())

        return observations, rewards, dones, infos
```

## 海洋环境Suite

PufferLib 为 Ocean 套件提供了 20 多个预构建环境：

### 可用环境

#### 街机游戏
- **Atari**：通过街机学习环境的经典 Atari 2600 游戏
- **Procgen**：程序生成的游戏用于泛化测试

#### 基于网格的
- **Minigrid**：部分可观察的网格世界环境
- **Crafter**：开放式生存制作游戏
- **NetHack**：经典的Roguelike地下城爬行游戏
- **MiniHack**：简化的NetHack变体

#### Multi-Agent
- **PettingZoo**：多智能体环境套件（包括Butterfly）
- **MAgent**：大规模多智能体场景
- **神经MMO**：大规模多智能体生存游戏

#### Specialized
- **Pokemon Red**：经典口袋妖怪游戏环境
- **GPUDrive**：高性能驾驶模拟器
- **Griddly**：基于网格的游戏引擎
- **MicroRTS**：实时策略游戏

### 使用Ocean环境

```python
import pufferlib

# Make environment
env = pufferlib.make('procgen-coinrun', num_envs=256)

# With custom configuration
env = pufferlib.make(
    'atari-pong',
    num_envs=128,
    frameskip=4,
    framestack=4
)

# Multi-agent environment
env = pufferlib.make('pettingzoo-knights-archers-zombies', num_agents=4)
```

## 自定义环境开发

### 开发工作流程

1. **Python 中的原型**：从纯 Python PufferEnv
2 开始。 **优化关键路径**：识别瓶颈
3. **用 C 实现**：在 C
4 中重写性能关键代码。 **创建绑定**：使用 Python C API
5. **编译**：构建为扩展模块
6. **注册**：添加到Ocean套件

### 性能基准

- **纯Python**：100k-500k步/秒
- **C实现**：100M+步/秒
- **使用Python env训练**：总计约400k SPS
- **使用 C env 进行训练**：总共约 4M SPS

### Python 优化技巧

```python
# Use NumPy operations instead of Python loops
# Bad
for i in range(len(array)):
    array[i] = array[i] * 2

# Good
array *= 2

# Pre-allocate arrays instead of appending
# Bad
observations = []
for i in range(n):
    observations.append(generate_obs())

# Good
observations = np.empty((n, obs_shape), dtype=np.float32)
for i in range(n):
    observations[i] = generate_obs()

# Use in-place operations
# Bad
new_state = state + delta

# Good
state += delta
```

### C 扩展示例

```c
// my_env.c
#include <Python.h>
#include <numpy/arrayobject.h>

// Fast environment step implementation
static PyObject* fast_step(PyObject* self, PyObject* args) {
    PyArrayObject* state;
    int action;

    if (!PyArg_ParseTuple(args, "O!i", &PyArray_Type, &state, &action)) {
        return NULL;
    }

    // High-performance C implementation
    // ...

    return Py_BuildValue("Ofi", obs, reward, done);
}

static PyMethodDef methods[] = {
    {"fast_step", fast_step, METH_VARARGS, "Fast environment step"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "my_env_c",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_my_env_c(void) {
    import_array();
    return PyModule_Create(&module);
}
```

## 第三方环境集成

### Gymnasium环境

```python
import gymnasium as gym
import pufferlib

# Wrap Gymnasium environment
gym_env = gym.make('CartPole-v1')
puffer_env = pufferlib.emulate(gym_env, num_envs=256)

# Or use make directly
env = pufferlib.make('gym-CartPole-v1', num_envs=256)
```

### PettingZoo 环境

```python
from pettingzoo.butterfly import pistonball_v6
import pufferlib

# Wrap PettingZoo environment
pz_env = pistonball_v6.env()
puffer_env = pufferlib.emulate(pz_env, num_envs=128)

# Or use make directly
env = pufferlib.make('pettingzoo-pistonball', num_envs=128)
```

### 自定义包装器

```python
class CustomWrapper(pufferlib.PufferEnv):
    """Wrapper to modify environment behavior."""

    def __init__(self, base_env, buf=None):
        super().__init__(buf)
        self.base_env = base_env
        self.observation_space = base_env.observation_space
        self.action_space = base_env.action_space

    def reset(self):
        obs = self.base_env.reset()
        # Modify observation
        return self._process_obs(obs)

    def step(self, action):
        # Modify action
        modified_action = self._process_action(action)

        obs, reward, done, info = self.base_env.step(modified_action)

        # Modify outputs
        obs = self._process_obs(obs)
        reward = self._process_reward(reward)

        return obs, reward, done, info
```

## 环境最佳实践

### 状态管理

```python
# Store minimal state, compute on demand
class EfficientEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)
        self.agent_pos = np.zeros(2)  # Minimal state

    def _get_observation(self):
        # Compute full observation on demand
        observation = np.zeros((84, 84, 3), dtype=np.uint8)
        self._render_scene(observation, self.agent_pos)
        return observation
```

### 奖励缩放

```python
# Normalize rewards to reasonable range
def step(self, action):
    # ... environment logic ...

    # Scale large rewards
    raw_reward = compute_raw_reward()
    reward = np.clip(raw_reward / 100.0, -10, 10)

    return obs, reward, done, info
```

### 剧集终止

```python
def step(self, action):
    # ... environment logic ...

    # Multiple termination conditions
    timeout = self.step_count >= self.max_steps
    success = self._check_success()
    failure = self._check_failure()

    done = timeout or success or failure

    info = {
        'TimeLimit.truncated': timeout,
        'success': success
    }

    return obs, reward, done, info
```

### 内存效率

```python
# Reuse buffers instead of allocating new ones
class MemoryEfficientEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Pre-allocate observation buffer
        self._obs_buffer = np.zeros((84, 84, 3), dtype=np.uint8)

    def _get_observation(self):
        # Reuse buffer, modify in place
        self._render_scene(self._obs_buffer)
        return self._obs_buffer  # Return view, not copy
```

## 调试环境

### 验证检查

```python
# Add assertions to catch bugs
def step(self, action):
    assert self.action_space.contains(action), f"Invalid action: {action}"

    obs, reward, done, info = self._step_impl(action)

    assert self.observation_space.contains(obs), "Invalid observation"
    assert np.isfinite(reward), "Non-finite reward"

    return obs, reward, done, info
```

### 渲染

```python
class DebuggableEnv(PufferEnv):
    def __init__(self, buf=None, render_mode=None):
        super().__init__(buf)
        self.render_mode = render_mode

    def render(self):
        """Render environment for debugging."""
        if self.render_mode == 'human':
            # Display to screen
            self._display_scene()
        elif self.render_mode == 'rgb_array':
            # Return image
            return self._render_to_array()
```

### 记录

```python
import logging

logger = logging.getLogger(__name__)

def step(self, action):
    logger.debug(f"Step {self.step_count}: action={action}")

    obs, reward, done, info = self._step_impl(action)

    if done:
        logger.info(f"Episode finished: reward={self.total_reward}")

    return obs, reward, done, info
```
