# Stable Baselines3

中的矢量化环境本文档提供了有关 Stable Baselines3 中矢量化环境的全面信息，以实现高效并行训练。

## 概述

矢量化环境将多个独立环境实例堆叠到单个环境中，该环境可批量处理操作和观察。您无需一次与一个环境交互，而是同时与 `n` 环境交互。

* *优点：**
- **速度：** 并行执行显着加速训练
- **样本效率：**更快地收集更多样的体验
- **所需：** 帧堆叠和标准化包装器
- **更好用于：** on-policy 算法（PPO、A2C）

## VecEnv Types

### DummyVecEnv

在当前 Python 进程上顺序执行环境。

```python
from stable_baselines3.common.vec_env import DummyVecEnv

# Method 1: Using make_vec_env
from stable_baselines3.common.env_util import make_vec_env

env = make_vec_env("CartPole-v1", n_envs=4, vec_env_cls=DummyVecEnv)

# Method 2: Manual creation
def make_env():
    def _init():
        return gym.make("CartPole-v1")
    return _init

env = DummyVecEnv([make_env() for _ in range(4)])
```

 * *何时使用：**
- 轻量级环境（CartPole，简单网格）
- 当多处理开销 > 计算时间时
- 调试（更容易跟踪错误）
- 单线程环境

* *性能：** 无实际并行性（顺序执行）。

### SubprocVecEnv

执行每个

```python
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env

env = make_vec_env("CartPole-v1", n_envs=8, vec_env_cls=SubprocVecEnv)
```

* *何时使用：**
- 计算成本高昂的环境（物理模拟、3D 游戏）
- 当环境计算时间证明多处理开销合理时
- 当您需要真正的并行时执行

* *重要：**使用forkserver或spawn时需要在`if __name__ == "__main__":`中包装代码：

```python
if __name__ == "__main__":
    env = make_vec_env("CartPole-v1", n_envs=8, vec_env_cls=SubprocVecEnv)
    model = PPO("MlpPolicy", env)
    model.learn(total_timesteps=100000)
```

* *性能：**跨CPU核心的真正并行性。

## 使用make_vec_env快速设置

创建矢量化的最简单方法环境：

```python
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv

# Basic usage
env = make_vec_env("CartPole-v1", n_envs=4)

# With SubprocVecEnv
env = make_vec_env("CartPole-v1", n_envs=8, vec_env_cls=SubprocVecEnv)

# With custom environment kwargs
env = make_vec_env(
    "MyEnv-v0",
    n_envs=4,
    env_kwargs={"difficulty": "hard", "max_steps": 500}
)

# With custom seed
env = make_vec_env("CartPole-v1", n_envs=4, seed=42)
```

## API 与标准 Gym 的差异

矢量化环境具有与标准 Gym 环境不同的 API：

### reset()

* *标准健身房：**
```python
obs, info = env.reset()
```

* *VecEnv：**
```python
obs = env.reset()  # Returns only observations (numpy array)
# Access info via env.reset_infos (list of dicts)
infos = env.reset_infos
```

### 步骤()

* *标准Gym:**
```python
obs, reward, terminated, truncated, info = env.step(action)
```

* *VecEnv:**
```python
obs, rewards, dones, infos = env.step(actions)
# Returns 4-tuple instead of 5-tuple
# dones = terminated | truncated
# actions is an array of shape (n_envs,) or (n_envs, action_dim)
```

### 自动重置

* *VecEnv 在剧集时自动重置环境end:**

```python
obs = env.reset()  # Shape: (n_envs, obs_dim)
for _ in range(1000):
    actions = env.action_space.sample()  # Shape: (n_envs,)
    obs, rewards, dones, infos = env.step(actions)
    # If dones[i] is True, env i was automatically reset
    # Final observation before reset available in infos[i]["terminal_observation"]
```

### 终端观测

当剧集结束时，访问真正的最终观测：

```python
obs, rewards, dones, infos = env.step(actions)

for i, done in enumerate(dones):
    if done:
        # The obs[i] is already the reset observation
        # True terminal observation is in info
        terminal_obs = infos[i]["terminal_observation"]
        print(f"Episode ended with terminal observation: {terminal_obs}")
```

## 使用矢量化环境进行训练

### 策略算法（PPO、 A2C)

On-policy 算法从向量化中受益匪浅：

```python
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv

# Create vectorized environment
env = make_vec_env("CartPole-v1", n_envs=8, vec_env_cls=SubprocVecEnv)

# Train
model = PPO("MlpPolicy", env, verbose=1, n_steps=128)
model.learn(total_timesteps=100000)

# With n_envs=8 and n_steps=128:
# - Collects 8*128=1024 steps per rollout
# - Updates after every 1024 steps
```

* *经验法则：** 对 on-policy 方法使用 4-16 个并行环境。

### Off-Policy 算法（SAC、TD3、 DQN)

离策略算法可以使用向量化，但获益较少：

```python
from stable_baselines3 import SAC
from stable_baselines3.common.env_util import make_vec_env

# Use fewer environments (1-4)
env = make_vec_env("Pendulum-v1", n_envs=4)

# Set gradient_steps=-1 for efficiency
model = SAC(
    "MlpPolicy",
    env,
    verbose=1,
    train_freq=1,
    gradient_steps=-1,  # Do 1 gradient step per env step (4 total with 4 envs)
)
model.learn(total_timesteps=50000)
```

 * *经验法则：** 对于离策略方法使用 1-4 个并行环境。

## 用于向量化环境的包装器

### VecNormalize

使用运行统计对观察和奖励进行标准化。

```python
from stable_baselines3.common.vec_env import VecNormalize

env = make_vec_env("Pendulum-v1", n_envs=4)

# Wrap with normalization
env = VecNormalize(
    env,
    norm_obs=True,        # Normalize observations
    norm_reward=True,     # Normalize rewards
    clip_obs=10.0,        # Clip normalized observations
    clip_reward=10.0,     # Clip normalized rewards
    gamma=0.99,           # Discount factor for reward normalization
)

# Train
model = PPO("MlpPolicy", env)
model.learn(total_timesteps=50000)

# Save model AND normalization statistics
model.save("ppo_pendulum")
env.save("vec_normalize.pkl")

# Load for evaluation
env = make_vec_env("Pendulum-v1", n_envs=1)
env = VecNormalize.load("vec_normalize.pkl", env)
env.training = False  # Don't update stats during evaluation
env.norm_reward = False  # Don't normalize rewards during evaluation

model = PPO.load("ppo_pendulum", env=env)
```

* *何时使用：**
- 连续控制任务（特别是MuJoCo）
- 当观察尺度变化很大时
- 当奖励很高时方差

* *重要：**
- 统计数据不与模型一起保存 - 单独保存
- 在评估期间禁用训练和奖励归一化

### VecFrameStack

堆叠来自多个连续帧的观察结果。

```python
from stable_baselines3.common.vec_env import VecFrameStack

env = make_vec_env("PongNoFrameskip-v4", n_envs=8)

# Stack 4 frames
env = VecFrameStack(env, n_stack=4)

# Now observations have shape: (n_envs, n_stack, height, width)
model = PPO("CnnPolicy", env)
model.learn(total_timesteps=1000000)
```

* *何时使用：**
- Atari 游戏（堆栈 4 帧）
- 需要速度信息的环境
- 部分可观测性问题

### VecVideoRecorder

记录代理视频行为.

```python
from stable_baselines3.common.vec_env import VecVideoRecorder

env = make_vec_env("CartPole-v1", n_envs=1)

# Record videos
env = VecVideoRecorder(
    env,
    video_folder="./videos/",
    record_video_trigger=lambda x: x % 2000 == 0,  # Record every 2000 steps
    video_length=200,  # Max video length
    name_prefix="training"
)

model = PPO("MlpPolicy", env)
model.learn(total_timesteps=10000)
```

* *输出：** `./videos/`目录中的MP4视频。

### VecCheckNan

检查观察和奖励中的NaN或无限值。

```python
from stable_baselines3.common.vec_env import VecCheckNan

env = make_vec_env("CustomEnv-v0", n_envs=4)

# Add NaN checking (useful for debugging)
env = VecCheckNan(env, raise_exception=True, warn_once=True)

model = PPO("MlpPolicy", env)
model.learn(total_timesteps=10000)
```

* *当使用：**
- 调试自定义环境
- 捕获数值不稳定性
- 验证环境实现

### VecTransposeImage

将图像观察值从（高度、宽度、通道）转置为（通道、高度、宽度）。

```python
from stable_baselines3.common.vec_env import VecTransposeImage

env = make_vec_env("PongNoFrameskip-v4", n_envs=4)

# Convert HWC to CHW format
env = VecTransposeImage(env)

model = PPO("CnnPolicy", env)
```

* *何时使用：**
- 当环境以 HWC 格式返回图像时
- SB3 需要 CNN 策略的 CHW 格式

## 高级用法

### 自定义VecEnv

创建自定义矢量化环境：

```python
from stable_baselines3.common.vec_env import DummyVecEnv
import gymnasium as gym

class CustomVecEnv(DummyVecEnv):
    def step_wait(self):
        # Custom logic before/after stepping
        obs, rewards, dones, infos = super().step_wait()
        # Modify observations/rewards/etc
        return obs, rewards, dones, infos
```

### 环境方法调用

在包装环境上调用方法：

```python
env = make_vec_env("MyEnv-v0", n_envs=4)

# Call method on all environments
env.env_method("set_difficulty", "hard")

# Call method on specific environment
env.env_method("reset_level", indices=[0, 2])

# Get attribute from all environments
levels = env.get_attr("current_level")
```

### 设置属性

```python
# Set attribute on all environments
env.set_attr("difficulty", "hard")

# Set attribute on specific environments
env.set_attr("max_steps", 1000, indices=[1, 3])
```

## 性能优化

### 选择环境数量

* *在线策略（PPO、A2C）：**
```python
# General rule: 4-16 environments
# More environments = faster data collection
n_envs = 8
env = make_vec_env("CartPole-v1", n_envs=n_envs)

# Adjust n_steps to maintain same rollout length
# Total steps per rollout = n_envs * n_steps
model = PPO("MlpPolicy", env, n_steps=128)  # 8*128 = 1024 steps/rollout
```

* *离线策略（SAC、TD3、 DQN):**
```python
# General rule: 1-4 environments
# More doesn't help as much (replay buffer provides diversity)
n_envs = 4
env = make_vec_env("Pendulum-v1", n_envs=n_envs)

model = SAC("MlpPolicy", env, gradient_steps=-1)  # 1 grad step per env step
```

### CPU 内核利用率

```python
import multiprocessing

# Use one less than total cores (leave one for Python main process)
n_cpus = multiprocessing.cpu_count() - 1
env = make_vec_env("MyEnv-v0", n_envs=n_cpus, vec_env_cls=SubprocVecEnv)
```

### 内存注意事项

```python
# Large replay buffer + many environments = high memory usage
# Reduce buffer size if memory constrained
model = SAC(
    "MlpPolicy",
    env,
    buffer_size=100_000,  # Reduced from 1M
)
```

## 常见问题

### 问题：“无法腌制本地对象”

* *原因：** SubprocVecEnv 需要可腌制环境。

* *解决方案：** 在类/函数之外定义环境创建：

```python
# Bad
def train():
    def make_env():
        return gym.make("CartPole-v1")
    env = SubprocVecEnv([make_env for _ in range(4)])

# Good
def make_env():
    return gym.make("CartPole-v1")

if __name__ == "__main__":
    env = SubprocVecEnv([make_env for _ in range(4)])
```

### 问题：单一环境和矢量化 env 之间的行为不同

* *原因：** 自动重置

* *解决方案：** 正确处理终端观测：

```python
obs, rewards, dones, infos = env.step(actions)
for i, done in enumerate(dones):
    if done:
        terminal_obs = infos[i]["terminal_observation"]
        # Process terminal_obs if needed
```

### 问题：SubprocVecEnv 比 DummyVecEnv

* * 原因：** 环境太轻量（多处理开销 > 计算）。

* *解决方案：** 使用适用于简单环境的 DummyVecEnv：

```python
# For CartPole, use DummyVecEnv
env = make_vec_env("CartPole-v1", n_envs=8, vec_env_cls=DummyVecEnv)
```

### 问题：使用 SubprocVecEnv

进行训练时崩溃**原因：** 环境未正确隔离或具有共享状态。

* *解决方案：**
- 确保环境没有共享全局状态
- 将代码包装在`if __name__ == "__main__":`
中-使用DummyVecEnv进行调试

## 最佳实践

1. **使用适当的 VecEnv 类型：**
  - DummyVecEnv：简单环境（CartPole、基本网格）
  - SubprocVecEnv：复杂环境（MuJoCo、Unity、3D 游戏）

2. **调整矢量化的超参数：**
  - 在回调中将 `eval_freq`、`save_freq` 除以 `n_envs`
  - 为 on-policy 算法保持相同的 `n_steps * n_envs`

3. **保存标准化统计数据：**
  - 始终使用模型保存 VecNormalize 统计数据
  - 在评估期间禁用训练

4. **监控内存使用情况：**
  - 更多环境 = 更多内存
  - 如果需要，减少缓冲区大小

5. **首先使用 DummyVecEnv 进行测试：**
  - 更轻松地调试
  - 确保环境在并行化之前工作

## 示例

### 基本训练循环

```python
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv

# Create vectorized environment
env = make_vec_env("CartPole-v1", n_envs=8, vec_env_cls=SubprocVecEnv)

# Train
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)

# Evaluate
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, infos = env.step(action)
```

### 标准化

```python
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecNormalize

# Create and normalize
env = make_vec_env("Pendulum-v1", n_envs=4)
env = VecNormalize(env, norm_obs=True, norm_reward=True)

# Train
model = PPO("MlpPolicy", env)
model.learn(total_timesteps=50000)

# Save both
model.save("model")
env.save("vec_normalize.pkl")

# Load for evaluation
eval_env = make_vec_env("Pendulum-v1", n_envs=1)
eval_env = VecNormalize.load("vec_normalize.pkl", eval_env)
eval_env.training = False
eval_env.norm_reward = False

model = PPO.load("model", env=eval_env)
```

## 其他资源

- 官方SB3 VecEnv指南：https://stable-baselines3.readthedocs.io/en/master/guide/vec_envs.html
- VecEnv API参考： https://stable-baselines3.readthedocs.io/en/master/common/vec_env.html
- 多处理最佳实践：https://docs.python.org/3/library/multiprocessing.html
