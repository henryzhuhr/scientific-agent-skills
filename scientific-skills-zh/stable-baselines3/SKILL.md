---
name: stable-baselines3
description: 具有类似 scikit-learn 的 API 的可用于生产的强化学习算法（PPO、SAC、DQN、TD3、DDPG、A2C）。用于标准 RL 实验、快速原型设计和记录良好的算法实现。最适合在 Gymnasium 环境中进行单智能体强化学习。对于高性能并行训练、多代理系统或自定义矢量化环境，请改用 pufferlib。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Stable Baselines3

## 概述

Stable Baselines3 (SB3)是一个基于 PyTorch 的库，提供强化学习算法的可靠实现。该技能为使用 SB3 的统一 API 来训练 RL 智能体、创建自定义环境、实现回调和优化训练工作流程提供了全面的指导。

## 核心功能

### 1. 训练 RL 智能体

* *基本训练模式：**

```python
import gymnasium as gym
from stable_baselines3 import PPO

# Create environment
env = gym.make("CartPole-v1")

# Initialize agent
model = PPO("MlpPolicy", env, verbose=1)

# Train the agent
model.learn(total_timesteps=10000)

# Save the model
model.save("ppo_cartpole")

# Load the model (without prior instantiation)
model = PPO.load("ppo_cartpole", env=env)
```

* *重要注：**
- `total_timesteps` 为下限；由于批量收集，实际训练可能会超出此范围
- 使用 `model.load()` 作为静态方法，而不是在现有实例上
- 重播缓冲区不与模型一起保存以节省空间

  * *算法选择：**
 使用 `references/algorithms.md` 获取详细的算法特征和选择指导。快速参考：
- **PPO/A2C**：通用，支持所有动作空间类型，适合多重处理
- **SAC/TD3**：连续控制，离策略，样本高效
- **DQN**：离散动作，离策略
- **HER**：目标条件任务

请参阅`scripts/train_rl_agent.py`以获取具有最佳实践的完整培训模板。

### 2.自定义环境

* *要求：**
自定义环境必须继承自`gymnasium.Env`并实现：
- `__init__()`：定义action_space和Observation_space
- `reset(seed, options)`：返回初始观察和信息 dict
- `step(action)`：返回观察、奖励、终止、截断、信息
- `render()`：可视化（可选）
- `close()`：清理资源

* *关键约束：**
- 图像观测值必须是范围 [0, 255]内的 `np.uint8` 
- 尽可能使用通道优先格式（通道、高度、宽度）
- SB3 通过除以 255
 自动标准化图像- 如果满足以下条件，则在 policy_kwargs 中设置 `normalize_images=False`预归一化
- SB3不支持带有`start!=0`

的`Discrete`或`MultiDiscrete`空间**验证：**
```python
from stable_baselines3.common.env_checker import check_env

check_env(env, warn=True)
```

有关完整的自定义环境模板和`references/custom_environments.md`，请参见`scripts/custom_env_template.py` 

### 3.向量化环境

* *目的：**
向量化环境并行运行多个环境实例，加速训练并启用某些包装器（帧堆叠、标准化）。

* *类型：**
- **DummyVecEnv**：在当前进程上顺序执行（用于轻量级）环境）
- **SubprocVecEnv**：跨进程并行执行（适用于计算密集型环境）

* *快速设置：**
```python
from stable_baselines3.common.env_util import make_vec_env

# Create 4 parallel environments
env = make_vec_env("CartPole-v1", n_envs=4, vec_env_cls=SubprocVecEnv)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25000)
```

* *离策略优化：**
使用具有离策略算法（SAC、TD3、DQN）的多个环境时，设置 `gradient_steps=-1` 以在每个环境步骤执行一次梯度更新，平衡挂钟时间和采样效率。

* *API 差异：**
- `reset()` 仅返回观测值（`vec_env.reset_infos` 中提供的信息）
- `step()` 返回 4 元组： `(obs, rewards, dones, infos)` 不是 5 元组
- 环境在剧集后自动重置
- 通过 `infos[env_idx]["terminal_observation"]`

 提供终端观察有关包装器和高级用法的详细信息，请参阅 `references/vectorized_envs.md`。

### 4. 用于监控和监控的回调控制

* *用途：**
回调可以在不修改核心算法的情况下监控指标、保存检查点、实现提前停止和自定义训练逻辑。

* *常用回调：**
- **EvalCallback**：定期评估并保存最佳模型
- **CheckpointCallback**：每隔一段时间保存模型检查点
- **StopTrainingOnRewardThreshold**：达到目标奖励时停止
- **ProgressBarCallback**：定时显示训练进度

* *自定义回调结构：**
```python
from stable_baselines3.common.callbacks import BaseCallback

class CustomCallback(BaseCallback):
    def _on_training_start(self):
        # Called before first rollout
        pass

    def _on_step(self):
        # Called after each environment step
        # Return False to stop training
        return True

    def _on_rollout_end(self):
        # Called at end of rollout
        pass
```

* *可用属性：**
- `self.model`：RL 算法实例
- `self.num_timesteps`：总环境步骤
- `self.training_env`：训练环境

* *链接回调：**
```python
from stable_baselines3.common.callbacks import CallbackList

callback = CallbackList([eval_callback, checkpoint_callback, custom_callback])
model.learn(total_timesteps=10000, callback=callback)
```

有关全面的回调文档，请参阅`references/callbacks.md`。

### 5.模型持久性和检查

* *保存和加载中：**
```python
# Save model
model.save("model_name")

# Save normalization statistics (if using VecNormalize)
vec_env.save("vec_normalize.pkl")

# Load model
model = PPO.load("model_name", env=env)

# Load normalization statistics
vec_env = VecNormalize.load("vec_normalize.pkl", vec_env)
```

* *参数访问：**
```python
# Get parameters
params = model.get_parameters()

# Set parameters
model.set_parameters(params)

# Access PyTorch state dict
state_dict = model.policy.state_dict()
```

### 6.评估与录制

* *评估：**
```python
from stable_baselines3.common.evaluation import evaluate_policy

mean_reward, std_reward = evaluate_policy(
    model,
    env,
    n_eval_episodes=10,
    deterministic=True
)
```

* *视频录制：**
```python
from stable_baselines3.common.vec_env import VecVideoRecorder

# Wrap environment with video recorder
env = VecVideoRecorder(
    env,
    "videos/",
    record_video_trigger=lambda x: x % 2000 == 0,
    video_length=200
)
```

完整的评估和录制模板请参阅 `scripts/evaluate_agent.py`。

### 7. 高级功能

* *学习率表：**
```python
def linear_schedule(initial_value):
    def func(progress_remaining):
        # progress_remaining goes from 1 to 0
        return progress_remaining * initial_value
    return func

model = PPO("MlpPolicy", env, learning_rate=linear_schedule(0.001))
```

* *多输入策略（字典观察）：**
```python
model = PPO("MultiInputPolicy", env, verbose=1)
```
 当观察是字典时使用（例如，将图像与传感器数据相结合）。

* *事后经验回放：**
```python
from stable_baselines3 import SAC, HerReplayBuffer

model = SAC(
    "MultiInputPolicy",
    env,
    replay_buffer_class=HerReplayBuffer,
    replay_buffer_kwargs=dict(
        n_sampled_goal=4,
        goal_selection_strategy="future",
    ),
)
```

* *TensorBoard集成：**
```python
model = PPO("MlpPolicy", env, tensorboard_log="./tensorboard/")
model.learn(total_timesteps=10000)
```

## 工作流程指南

* *启动新的 RL 项目：**

1. **定义问题**：确定观察空间、行动空间和奖励结构
2. **选择算法**：使用`references/algorithms.md`进行选择指导
3. **创建/适应环境**：如果需要，请使用 `scripts/custom_env_template.py`
4. **验证环境**：在训练
5之前始终运行`check_env()`。 **设置训练**：使用`scripts/train_rl_agent.py`作为起始模板
6. **添加监控**：实现评估和检查点回调
7. **优化性能**：考虑 speed
8 的矢量化环境。 **评估和迭代**：使用`scripts/evaluate_agent.py`进行评估

* *常见问题：**

- **内存错误**：减少离策略算法的 `buffer_size` 或使用更少的并行环境
- **训练缓慢**：在并行环境中考虑 SubprocVecEnv
- **不稳定的训练**：尝试不同的算法，调整超参数，或检查奖励缩放
- **导入错误**：确保安装 `stable_baselines3`： `uv pip install stable-baselines3[extra]`

## 资源

### 脚本/
- `train_rl_agent.py`：具有最佳实践的完整培训脚本模板
- `evaluate_agent.py`：代理评估和视频录制模板
- `custom_env_template.py`：自定义健身房环境模板

### 参考文献/
- `algorithms.md`：详细算法对比与选择指南
- `custom_environments.md`：综合自定义环境创建指南
- `callbacks.md`：完整回调系统参考
- `vectorized_envs.md`：矢量化环境使用和包装器

## 安装

```bash
# Basic installation
uv pip install stable-baselines3

# With extra dependencies (Tensorboard, etc.)
uv pip install stable-baselines3[extra]
```
