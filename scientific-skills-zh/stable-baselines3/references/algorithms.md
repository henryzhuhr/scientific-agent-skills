# Stable Baselines3算法参考

本文档提供了Stable Baselines3中所有RL算法的详细特征，以帮助为特定任务选择正确的算法。

## 算法比较表

|算法|类型 |行动空间|样品效率 |训练速度|使用案例|
|---------|------|----------------|--------------------|----------------|----------|
| **PPO** |在保单 |全部 |中等|快|通用、稳定|
| **A2C** |在保单 |全部 |低|非常快|快速原型设计，多重处理|
| **SAC** |政策外 |连续|高|中等|连续控制，样品高效|
| **TD3** |政策外 |连续 |高|中等|连续控制，确定性|
| **DDPG** |政策外 |连续|高|中等|连续控制（用TD3代替）|
| **DQN** |政策外 |离散|中等|中等|离散动作，Atari 游戏 |
| **她** |政策外 |全部 |非常高 |中等|目标条件任务|
| **复发性 PPO** |在保单 |全部 |中等|慢|部分可观测性（POMDP）|

## 详细算法特征

### PPO（邻近策略优化）

* *概述：**通用的同策略算法，在许多任务中具有良好的性能。

* *优点：**
- 稳定可靠训练
- 适用于所有动作空间类型（离散、框、多重离散、多重二进制）
- 样本效率和训练速度之间的良好平衡
- 非常适合矢量化环境的多重处理
- 易于调整

* * 缺点：**
- 样本效率低于离策略方法
- 需要许多环境交互

* *最适合：**
- 通用RL任务
- 当稳定性很重要时
- 当你有廉价的环境模拟时
- 具有连续或离散动作的任务

* *超参数指导：**
- `n_steps`：2048-4096 表示连续，128-256 表示 Atari
- `learning_rate`：3e-4 是一个很好的默认值
- `n_epochs`：10 表示连续，4 表示连续Atari
- `batch_size`：64
- `gamma`：0.99（长集为0.995-0.999）

### A2C（优势演员评论家）

* *概述：** A3C的同步变体，比PPO简单但更少稳定。

* *优点：**
- 非常快速的训练（比 PPO 简单）
- 适用于所有动作空间类型
- 适合快速原型设计
- 内存效率

* *缺点：**
- 稳定性低于PPO
- 需要仔细的超参数调整
- 样本效率较低

* *最适合：**
- 快速实验
- 当训练速度至关重要时
- 简单环境

* *超参数指导：**
- `n_steps`：5-256，取决于任务
- `learning_rate`：7e-4
- `gamma`：0.99

### SAC（Soft Actor-Critic）

 * *概述：**具有熵正则化的离策略算法， 

* *优点：**
- 出色的样本效率
- 非常稳定的训练
- 自动熵调整
- 通过随机策略进行良好的探索
- 最先进的机器人

* *弱点：**
- 仅支持连续动作空间（Box）
- 比策略方法更慢的挂钟时间
- 更复杂的超参数

* *最适合：**
- 连续控制（机器人，物理）模拟）
- 当样本效率至关重要时
- 昂贵的环境模拟
- 需要良好探索的任务

* *超参数指导：**
- `learning_rate`：3e-4
- `buffer_size`：大多数为1M任务
- `learning_starts`：10000
- `batch_size`：256
- `tau`：0.005（目标网络更新率）
- `train_freq`：1与`gradient_steps=-1` 最佳性能

### TD3（双延迟 DDPG）

* *概述：**改进的DDPG，具有双Q学习和延迟策略更新。

* *优点：**
- 样本效率高
- 确定性策略（有利于部署）
- 比DDPG更稳定
- 适合连续控制

* *缺点：**
- 仅支持连续动作空间（方框）
- 比SAC
更少的探索-需要仔细调整

* *最适合：**
- 连续控制任务
- 当首选确定性策略时
- 样本高效学习

* *超参数指导：**
- `learning_rate`: 1e-3
- `buffer_size`: 1M
- `learning_starts`: 10000
- `batch_size`: 100
- `policy_delay`：2（每2个评论家更新更新策略）

### DDPG（深度确定性策略梯度）

* *概述：**早期离策略连续控制算法。

* *优点：**
- 连续动作空间支持
- 离策略学习

* *缺点：**
- 稳定性不如 TD3 或 SAC
- 对超参数敏感
- 通常优于 TD3

* * 最适合：**
- 传统兼容性
- **建议：** 使用新项目采用 TD3

### DQN（深度 Q 网络）

* *概述：** 用于离散操作空间的经典离策略算法。

* * 优点：**
- 离散操作的样本效率
- 经验重播可重用过去的数据
- 在Atari 游戏

* *弱点：**
- 仅支持离散动作空间
- 如果没有适当调整可能会不稳定
- 高估偏差

* *最适合：**
- 离散动作任务
- Atari 游戏和类似游戏环境
- 当样本效率很重要时

* *超参数指导：**
- `learning_rate`：1e-4
- `buffer_size`：100K-1M，具体取决于任务
- `learning_starts`： 50000 雅达利
- `batch_size`：32
- `exploration_fraction`：0.1
- `exploration_final_eps`：0.05

* *变体：**
- **QR-DQN**：分布式强化学习版本，可实现更好的价值估计
- **可屏蔽 DQN**：适用于具有动作屏蔽的环境

### HER（事后经验重播）

* *概述：** 不是独立算法，而是目标条件的重播缓冲策略tasks.

* *优点：**
- 显着改善稀疏奖励设置中的学习
- 通过重新标记目标从失败中学习
- 适用于任何离策略算法（SAC、TD3、DQN）

* * 缺点：**
- 仅适用于目标条件环境
- 需要特定的观察结构（带有“观察”、“实现目标”、“期望目标”的字典）

* *最适合：**
- 目标条件任务（机器人操作、导航）
- 稀疏奖励环境
- 目标明确但奖励有限的任务binary

* *用法：**
```python
from stable_baselines3 import SAC, HerReplayBuffer

model = SAC(
    "MultiInputPolicy",
    env,
    replay_buffer_class=HerReplayBuffer,
    replay_buffer_kwargs=dict(
        n_sampled_goal=4,
        goal_selection_strategy="future",  # or "episode", "final"
    ),
)
```

### RecurrentPPO

* *概述：** PPO 具有用于处理部分可观察性的 LSTM 策略。

* *优点：**
- 处理部分可观察性(POMDP)
- 可以学习时间依赖性
- 适合需要内存的任务

* *弱点：**
- 训练速度比标准 PPO
- 调整更复杂
- 需要顺序数据

* *最好对于：**
- 部分可观测环境
- 需要内存的任务（例如，没有完整地图的导航）
- 时间序列问题

## 算法选择指南

### 决策树

1. **您的操作空间是什么？**
  - **连续（方框）** → 考虑 PPO、SAC 或 TD3
  - **离散** → 考虑 PPO、A2C 或 DQN
  - **多离散/多二进制** → 使用 PPO 或 A2C

2. **样本效率是否至关重要？**
  - **是（昂贵的模拟）** → 使用离策略：SAC、TD3、DQN 或 HER
  - **否（廉价模拟）** → 使用在策略：PPO、A2C

3. **您需要快速挂钟训练吗？**
  - **是** → 在矢量化环境中使用 PPO 或 A2C
  - **否** → 任何算法都可以工作

4. **任务是否以稀疏奖励为目标条件？**
  - **是** → 将 HER 与 SAC 或 TD3
 结合使用 - **否** → 继续使用标准算法

5. **环境是否部分可观察？**
  - **是** → 使用 RecurrentPPO
  - **否** → 使用标准算法

### 快速建议

- **开始/一般任务：** PPO
- **连续控制/机器人：** SAC
- **离散操作/Atari：** DQN 或 PPO
- **目标条件/稀疏奖励：** SAC + HER
- **快速原型制作：** A2C
- **样本效率关键：** SAC、TD3 或 DQN
- **部分可观察性：** 循环 PPO

## 训练配置提示

### 对于在策略算法（PPO、A2C）

```python
# Use vectorized environments for speed
env = make_vec_env(env_id, n_envs=8, vec_env_cls=SubprocVecEnv)

model = PPO(
    "MlpPolicy",
    env,
    n_steps=2048,  # Collect this many steps per environment before update
    batch_size=64,
    n_epochs=10,
    learning_rate=3e-4,
    gamma=0.99,
)
```

### 对于离策略算法（SAC、TD3、DQN）

```python
# Fewer environments, but use gradient_steps=-1 for efficiency
env = make_vec_env(env_id, n_envs=4)

model = SAC(
    "MlpPolicy",
    env,
    buffer_size=1_000_000,
    learning_starts=10000,
    batch_size=256,
    train_freq=1,
    gradient_steps=-1,  # Do 1 gradient step per env step (4 with 4 envs)
    learning_rate=3e-4,
)
```

## 通用陷阱

1. **将 DQN 与连续操作结合使用** - DQN 仅适用于离散操作
2. **不使用带有 PPO/A2C 的矢量化环境** - 浪费潜在的加速 
3. **使用的环境太少** - 策略方法需要许多样本
4. **使用太大的重播缓冲区** - 可能导致内存问题
5. **不调整学习率** - 对于稳定训练
6至关重要。 **忽略奖励缩放** - 标准化奖励以更好地学习
7. **错误的策略类型** - 对图像使用“CnnPolicy”，对字典观察使用“MultiInputPolicy”

## 性能基准

常见基准上的近似预期性能（平均奖励）：

### 连续控制（MuJoCo）
- **HalfCheetah-v3**：PPO〜1800，SAC ~12000, TD3 ~9500
- **料斗-v3**: PPO ~2500, SAC ~3600, TD3 ~3600
- **Walker2d-v3**: PPO ~3000, SAC ~5500, TD3 ~5000

### 离散控制(Atari)
- **Breakout**：PPO ~400，DQN ~300
- **Pong**：PPO ~20，DQN ~20
- **太空入侵者**：PPO ~1000，DQN ~800

* 注：性能随超参数和训练的不同而显着变化时间.*

## 其他资源

- **RL Baselines3 Zoo**：预先训练的代理和超参数的集合：https://github.com/DLR-RM/rl-baselines3-zoo
- **超参数调优**：使用Optuna进行系统调优
- **自定义策略**：扩展自定义网络架构的基本策略
- **贡献Repo**：用于实验算法的 SB3-Contrib（QR-DQN、TQC 等）
