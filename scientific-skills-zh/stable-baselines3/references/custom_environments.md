# 创建稳定基线的自定义环境3

本指南提供了创建与稳定基线兼容的自定义Gymnasium环境的全面信息3.

## 环境结构

### 所需方法

每个自定义环境必须继承自`gymnasium.Env`并实现：

```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class CustomEnv(gym.Env):
    def __init__(self):
        """Initialize environment, define action_space and observation_space"""
        super().__init__()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        """Reset environment to initial state"""
        super().reset(seed=seed)
        observation = self.observation_space.sample()
        info = {}
        return observation, info

    def step(self, action):
        """Execute one timestep"""
        observation = self.observation_space.sample()
        reward = 0.0
        terminated = False  # Episode ended naturally
        truncated = False   # Episode ended due to time limit
        info = {}
        return observation, reward, terminated, truncated, info

    def render(self):
        """Visualize environment (optional)"""
        pass

    def close(self):
        """Cleanup resources (optional)"""
        pass
```

### 方法详情

#### `__init__(self, ...)`

* *用途：**初始化环境，定义空间。

* *要求：**
- 必须调用 `super().__init__()`
- 必须定义 `self.action_space`
- 必须定义`self.observation_space`

* *示例：**
```python
def __init__(self, grid_size=10, max_steps=100):
    super().__init__()
    self.grid_size = grid_size
    self.max_steps = max_steps
    self.current_step = 0

    # Define spaces
    self.action_space = spaces.Discrete(4)
    self.observation_space = spaces.Box(
        low=0, high=grid_size-1, shape=(2,), dtype=np.float32
    )
```

#### `reset(self, seed=None, options=None)`

* *用途：**将环境重置为初始状态。

* *要求：**
- 必须调用`super().reset(seed=seed)`
- 必须返回 `(observation, info)` 元组
- 观察必须匹配 `observation_space`
- 信息必须是字典（可以是空）

* *示例：**
```python
def reset(self, seed=None, options=None):
    super().reset(seed=seed)

    # Initialize state
    self.agent_pos = self.np_random.integers(0, self.grid_size, size=2)
    self.goal_pos = self.np_random.integers(0, self.grid_size, size=2)
    self.current_step = 0

    observation = self._get_observation()
    info = {"episode": "started"}

    return observation, info
```

#### `step(self, action)`

* *用途：**在环境中执行一个时间步。

* *要求：**
- 必须返回5元组： `(observation, reward, terminated, truncated, info)`
- 行动必须根据 `action_space`
 有效 - 观察必须匹配 `observation_space`
- 奖励应为浮点数 
- 终止：如果情节自然结束（达到目标、失败等），则为 True 
- 截断：如果剧集因时间限制而结束则为 True
- 信息必须是字典

* *示例：**
```python
def step(self, action):
    # Apply action
    self.agent_pos += self._action_to_direction(action)
    self.agent_pos = np.clip(self.agent_pos, 0, self.grid_size - 1)
    self.current_step += 1

    # Calculate reward
    distance = np.linalg.norm(self.agent_pos - self.goal_pos)
    goal_reached = distance < 1.0

    if goal_reached:
        reward = 100.0
    else:
        reward = -distance * 0.1

    # Check termination conditions
    terminated = goal_reached
    truncated = self.current_step >= self.max_steps

    observation = self._get_observation()
    info = {"distance": distance, "steps": self.current_step}

    return observation, reward, terminated, truncated, info
```

## 空间类型

### 离散

用于离散操作（例如，{0, 1, 2, 3}).

```python
self.action_space = spaces.Discrete(4)  # 4 actions: 0, 1, 2, 3
```

* *重要：** SB3 不支持 `Discrete` 与 `start != 0` 的空格。始终从 0 开始。

### 框（连续）

对于范围内的连续值。

```python
# 1D continuous action in [-1, 1]
self.action_space = spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)

# 2D position observation
self.observation_space = spaces.Box(
    low=0, high=10, shape=(2,), dtype=np.float32
)

# 3D RGB image (channel-first format)
self.observation_space = spaces.Box(
    low=0, high=255, shape=(3, 84, 84), dtype=np.uint8
)
```

* *对于图像重要：**
- 必须是 `dtype=np.uint8` 在范围 [0, 255]
- 使用**通道优先**格式：（通道，高度，宽度）
- SB3通过除以255
自动标准化-如果预标准化，则在policy_kwargs中设置`normalize_images=False`

### MultiDiscrete

对于多个离散变量。

```python
# Two discrete variables: first with 3 options, second with 4 options
self.action_space = spaces.MultiDiscrete([3, 4])
```

### MultiBinary

对于二元向量。

```python
# 5 binary flags
self.action_space = spaces.MultiBinary(5)  # e.g., [0, 1, 1, 0, 1]
```

### Dict

对于字典观察（例如，将图像与

```python
self.observation_space = spaces.Dict({
    "image": spaces.Box(low=0, high=255, shape=(3, 64, 64), dtype=np.uint8),
    "vector": spaces.Box(low=-10, high=10, shape=(4,), dtype=np.float32),
    "discrete": spaces.Discrete(3),
})
```

* *重要：**使用 Dict 观察时，使用 `"MultiInputPolicy"` 而不是 `"MlpPolicy"`.

```python
model = PPO("MultiInputPolicy", env, verbose=1)
```

### Tuple

用于元组观察（较少

```python
self.observation_space = spaces.Tuple((
    spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32),
    spaces.Discrete(3),
))
```

## 重要约束和最佳实践

### 数据类型

- **观察：** 使用 `np.float32` 获取连续值
- **图像：** 在范围 [0, 255]
- **奖励：** 返回 Python float 或 `np.float32`
- **终止/截断：** 返回 Python bool

### 随机数生成

始终使用 `self.np_random`再现性：

```python
def reset(self, seed=None, options=None):
    super().reset(seed=seed)
    # Use self.np_random instead of np.random
    random_pos = self.np_random.integers(0, 10, size=2)
    random_float = self.np_random.random()
```

### 剧集终止

- **终止：** 自然结局（目标达成、特工死亡等）
- **截断：** 人工结局（时间限制、外部）中断）

```python
def step(self, action):
    # ... environment logic ...

    goal_reached = self._check_goal()
    time_limit_exceeded = self.current_step >= self.max_steps

    terminated = goal_reached  # Natural ending
    truncated = time_limit_exceeded  # Time limit

    return observation, reward, terminated, truncated, info
```

### 信息字典

使用信息字典进行调试和日志记录：

```python
info = {
    "episode_length": self.current_step,
    "distance_to_goal": distance,
    "success": goal_reached,
    "total_reward": self.cumulative_reward,
}
```

* *特殊键：**
- `"terminal_observation"`：由VecEnv自动添加剧集结束

## 高级功能

### 元数据

提供渲染信息：

```python
class CustomEnv(gym.Env):
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 30,
    }

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        # ...
```

### 渲染模式

```python
def render(self):
    if self.render_mode == "human":
        # Print or display for human viewing
        print(f"Agent at {self.agent_pos}")

    elif self.render_mode == "rgb_array":
        # Return numpy array (height, width, 3) for video recording
        canvas = np.zeros((500, 500, 3), dtype=np.uint8)
        # Draw environment on canvas
        return canvas
```

### 目标条件环境（针对HER)

对于事后经验回放，使用特定的观察结构：

```python
self.observation_space = spaces.Dict({
    "observation": spaces.Box(low=-10, high=10, shape=(3,), dtype=np.float32),
    "achieved_goal": spaces.Box(low=-10, high=10, shape=(3,), dtype=np.float32),
    "desired_goal": spaces.Box(low=-10, high=10, shape=(3,), dtype=np.float32),
})

def compute_reward(self, achieved_goal, desired_goal, info):
    """Required for HER environments"""
    distance = np.linalg.norm(achieved_goal - desired_goal)
    return -distance
```

## 环境验证

在训练之前始终验证您的环境：

```python
from stable_baselines3.common.env_checker import check_env

env = CustomEnv()
check_env(env, warn=True)
```

* *常见验证错误：**

1. **“观察结果不在范围内”**
  - 检查观察结果是否保持在定义的空间内
  - 确保正确的dtype（盒子空间的np.float32）

2. **“重置应返回元组”**
  - 返回`(observation, info)`，而不仅仅是观察

3. **“步骤应返回 5 元组”**
  - 返回 `(obs, reward, terminated, truncated, info)`

4. **“操作超出范围”**
  - 验证 action_space 定义与预期操作匹配

5. **“观察/操作数据类型不匹配”**
  - 确保观察结果与空间数据类型匹配（通常为 np.float32）

## 环境注册

向 Gymnasium 注册您的环境：

```python
import gymnasium as gym
from gymnasium.envs.registration import register

register(
    id="MyCustomEnv-v0",
    entry_point="my_module:CustomEnv",
    max_episode_steps=200,
    kwargs={"grid_size": 10},  # Default kwargs
)

# Now can use with gym.make
env = gym.make("MyCustomEnv-v0")
```

## 测试自定义环境

### 基础测试

```python
def test_environment(env, n_episodes=5):
    """Test environment with random actions"""
    for episode in range(n_episodes):
        obs, info = env.reset()
        episode_reward = 0
        done = False
        steps = 0

        while not done:
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            episode_reward += reward
            steps += 1
            done = terminated or truncated

        print(f"Episode {episode+1}: Reward={episode_reward:.2f}, Steps={steps}")
```

### 训练测试

```python
from stable_baselines3 import PPO

def train_test(env, timesteps=10000):
    """Quick training test"""
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=timesteps)

    # Evaluate
    obs, info = env.reset()
    for _ in range(100):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            break
```

## 常见模式

### 网格世界

```python
class GridWorldEnv(gym.Env):
    def __init__(self, size=10):
        super().__init__()
        self.size = size
        self.action_space = spaces.Discrete(4)  # up, down, left, right
        self.observation_space = spaces.Box(0, size-1, shape=(2,), dtype=np.float32)
```

### 连续控制

```python
class ContinuousEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(8,), dtype=np.float32)
```

### 基于图像的环境

```python
class VisionEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(4)
        # Channel-first: (channels, height, width)
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(3, 84, 84), dtype=np.uint8
        )
```

### 多模态环境

```python
class MultiModalEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Dict({
            "image": spaces.Box(0, 255, shape=(3, 64, 64), dtype=np.uint8),
            "sensors": spaces.Box(-10, 10, shape=(4,), dtype=np.float32),
        })
```

## 性能注意事项

### 高效观察生成

```python
# Pre-allocate arrays
def __init__(self):
    # ...
    self._obs_buffer = np.zeros(self.observation_space.shape, dtype=np.float32)

def _get_observation(self):
    # Reuse buffer instead of allocating new array
    self._obs_buffer[0] = self.agent_x
    self._obs_buffer[1] = self.agent_y
    return self._obs_buffer
```

### 向量化

使环境操作可向量化：

```python
# Good: Uses numpy operations
def step(self, action):
    direction = np.array([[0,1], [0,-1], [1,0], [-1,0]])[action]
    self.pos = np.clip(self.pos + direction, 0, self.size-1)

# Avoid: Python loops when possible
# for i in range(len(self.agents)):
#     self.agents[i].update()
```

## 故障排除

### “观察超出范围”
- 检查所有观察在定义的空间内
- 验证正确的dtype（np.float32与np.float64）

### “观察/奖励中的NaN或Inf”
- 添加检查：`assert np.isfinite(reward)`
- 使用`VecCheckNan`包装来捕获问题

### “策略无法学习”
- 检查奖励缩放（标准化奖励）
- 验证观察标准化
- 确保奖励信号有意义
- 检查探索是否足够

### “训练崩溃”
- 验证环境`check_env()`
- 检查自定义环境中的竞争条件
- 验证操作/观察空间是否一致

## 其他资源

- 模板：请参阅 `scripts/custom_env_template.py`
- 体育馆文档： https://gymnasium.farama.org/
- SB3 自定义环境指南：https://stable-baselines3.readthedocs.io/en/master/guide/custom_env.html
