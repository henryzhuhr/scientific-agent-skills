---
name: pufferlib
description: 针对速度和规模进行优化的高性能强化学习框架。当您需要快速并行训练、矢量化环境、多代理系统或与游戏环境（Atari、Procgen、NetHack）集成时使用。与标准实现相比，速度提高了 2-10 倍。对于快速原型设计或具有大量文档的标准算法实现，请改用 stable-baselines3。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PufferLib - 高性能强化学习

## 概述

PufferLib 是一个高性能强化学习库，专为快速并行环境模拟和训练而设计。它通过优化的矢量化、本机多代理支持和高效的 PPO 实现 (PuffeRL)实现每秒数百万步的训练。该库提供了 20 多个环境的 Ocean 套件，并与 Gymnasium、PettingZoo 和专门的 RL 框架无缝集成。

## 何时使用此技能

在以下情况下使用此技能：
- **在任何环境（单或多代理）上使用 PPO 训练 RL 代理** 
- **使用 PufferEnv 创建自定义环境** API
- **优化性能**用于并行环境模拟（矢量化）
- **集成来自 Gymnasium、PettingZoo、Atari、Procgen 等的现有环境**。
- **使用 CNN、LSTM 或自定义架构开发策略**
- **将 RL** 扩展到每秒数百万步以加快速度实验
- **多智能体强化学习**，支持原生多智能体环境

## 核心能力

### 1.高性能训练（PuffeRL）

PuffeRL是PufferLib优化的PPO+LSTM训练算法，实现1M-4M步骤/秒.

* *快速开始训练：**
```bash
# CLI training
puffer train procgen-coinrun --train.device cuda --train.learning-rate 3e-4

# Distributed training
torchrun --nproc_per_node=4 train.py
```

* *Python 训练循环：**
```python
import pufferlib
from pufferlib import PuffeRL

# Create vectorized environment
env = pufferlib.make('procgen-coinrun', num_envs=256)

# Create trainer
trainer = PuffeRL(
    env=env,
    policy=my_policy,
    device='cuda',
    learning_rate=3e-4,
    batch_size=32768
)

# Training loop
for iteration in range(num_iterations):
    trainer.evaluate()  # Collect rollouts
    trainer.train()     # Train on batch
    trainer.mean_and_log()  # Log results
```

* *有关全面的训练指导**，请阅读 `references/training.md` 的内容：
- 完整的训练工作流程和 CLI选项
- 使用蛋白质进行超参数调整
- 分布式多GPU/多节点训练
- 记录器集成（权重和偏差、Neptune）
- 检查点和恢复训练
- 性能优化技巧
- 课程学习模式

### 2.环境开发(PufferEnv)

使用PufferEnv API创建自定义高性能环境。

* *基本环境结构：**
```python
import numpy as np
from pufferlib import PufferEnv

class MyEnvironment(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Define spaces
        self.observation_space = self.make_space((4,))
        self.action_space = self.make_discrete(4)

        self.reset()

    def reset(self):
        # Reset state and return initial observation
        return np.zeros(4, dtype=np.float32)

    def step(self, action):
        # Execute action, compute reward, check done
        obs = self._get_observation()
        reward = self._compute_reward()
        done = self._is_done()
        info = {}

        return obs, reward, done, info
```

 * *使用模板脚本：** `scripts/env_template.py` 提供完整的单智能体和多智能体环境模板，示例为：
- 不同的观察空间类型（向量、图像、字典）
- 动作空间变化（离散、连续、多离散）
- 多智能体环境结构
- 测试实用程序

* *如需完整的环境开发**，请阅读`references/environments.md`，了解：
- PufferEnv API 详细信息和就地操作模式
- 观察和操作空间定义
- 多智能体环境创建
- 海洋套件（20+ 预构建）环境）
- 性能优化（Python 到 C 工作流程）
- 环境包装器和最佳实践
- 调试和验证技术

### 3. 矢量化和性能

通过优化的并行仿真实现最大吞吐量。

* *矢量化设置：**
```python
import pufferlib

# Automatic vectorization
env = pufferlib.make('environment_name', num_envs=256, num_workers=8)

# Performance benchmarks:
# - Pure Python envs: 100k-500k SPS
# - C-based envs: 100M+ SPS
# - With training: 400k-4M total SPS
```

* *关键优化：**
- 用于零拷贝观察传递的共享内存缓冲区
- 忙等待标志而不是管道/队列
- 用于异步返回的剩余环境
- 每个多个环境worker

* *对于向量化优化**，请阅读 `references/vectorization.md` 的内容：
- 架构和性能特征
- 工作线程和批量大小配置
- 串行、多处理、异步模式
- 共享内存和零复制模式
- 大容量的分层矢量化scale
- 多代理矢量化策略
- 性能分析和故障排除

### 4. 策略开发

使用可选实用程序将策略构建为标准 PyTorch 模块。

* *基本策略结构：**
```python
import torch.nn as nn
from pufferlib.pytorch import layer_init

class Policy(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()

        # Encoder
        self.encoder = nn.Sequential(
            layer_init(nn.Linear(obs_dim, 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, 256)),
            nn.ReLU()
        )

        # Actor and critic heads
        self.actor = layer_init(nn.Linear(256, num_actions), std=0.01)
        self.critic = layer_init(nn.Linear(256, 1), std=1.0)

    def forward(self, observations):
        features = self.encoder(observations)
        return self.actor(features), self.critic(features)
```

* *有关完整的策略开发**，请阅读 `references/policies.md` 的内容：
- 用于图像观察的 CNN 策略
- 具有优化 LSTM 的循环策略（推理速度提高 3 倍）
- 用于复杂观察的多输入策略
- 连续动作策略
- 多代理策略（共享参数与独立参数）
- 高级架构（注意力、残差）
- 观察归一化和梯度裁剪
- 策略调试和测试

### 5. 环境集成

无缝集成流行RL 的环境Frameworks.

* *Gymnasium 集成：**
```python
import gymnasium as gym
import pufferlib

# Wrap Gymnasium environment
gym_env = gym.make('CartPole-v1')
env = pufferlib.emulate(gym_env, num_envs=256)

# Or use make directly
env = pufferlib.make('gym-CartPole-v1', num_envs=256)
```

* *PettingZoo 多代理：**
```python
# Multi-agent environment
env = pufferlib.make('pettingzoo-knights-archers-zombies', num_envs=128)
```

* *支持的框架：**
- Gymnasium / OpenAI Gym
- PettingZoo（并行和 AEC）
- Atari (ALE)
- Procgen
- NetHack / MiniHack
- Minigrid
- 神经 MMO
- Crafter
- GPUDrive
- MicroRTS
- Griddly
- 以及更多...

* *有关集成详细信息**，请阅读 `references/integration.md`：
- 每个框架的完整集成示例
- 自定义包装器（观察、奖励、帧堆叠、操作）重复）
- 空间扁平化和反扁平化
- 环境注册
- 兼容性模式
- 性能考虑
- 集成调试

## 快速启动工作流程

### 用于训练现有环境

1. 从Ocean套件或兼容框架
2中选择环境。使用`scripts/train_template.py`作为起点
3. 为您的任务
4配置超参数。使用 CLI 或 Python 脚本
5 运行训练。使用权重和偏差或 Neptune
6 进行监控。优化参考`references/training.md`

### 创建自定义环境

1. 从`scripts/env_template.py`
2开始。定义观察和行动空间
3. 实现`reset()`和`step()`方法
4. 本地测试环境
5. 使用 `pufferlib.emulate()` 或 `make()`
6 进行矢量化。高级模式请参考`references/environments.md`
7. 如果需要，可使用 `references/vectorization.md` 进行优化

### 用于政策制定

1. 根据观察选择架构：
  - 矢量观察→ MLP 策略
  - 图像观察→ CNN 策略
  - 顺序任务→ LSTM 策略
  - 复杂观察→ 多输入策略
2. 使用`layer_init`进行适当的权重初始化
3. 遵循 `references/policies.md`
4 中的模式。在完整训练之前使用环境进行测试

### 用于性能优化

1. 配置文件当前吞吐量（每秒步数）
2. 检查矢量化配置（num_envs、num_workers）
3. 优化环境代码（就地操作、numpy 矢量化）
4. 考虑关键路径的 C 实现
5. 使用`references/vectorization.md`进行系统优化

## 资源

### 脚本/

* *train_template.py** - 完整的训练脚本模板包含：
- 环境创建和配置
- 策略初始化
- 记录器集成（WandB， Neptune）
- 带检查点的训练循环
- 命令行参数解析
- 多GPU分布式训练设置

* *env_template.py** - 环境实现模板：
- 单代理PufferEnv示例（网格世界）
- 多代理PufferEnv示例（合作）导航）
- 多个观察/动作空间模式
- 测试实用程序

### 参考文献/

* *training.md** - 综合培训指南：
- 培训工作流程和 CLI 选项
- 超参数配置
- 分布式训练（多 GPU、多节点）
- 监控和记录
- 检查点
- 蛋白质超参数调整
- 性能优化
- 常用训练模式
- 故障排除

* *environments.md** - 环境开发指南：
- PufferEnv API 和特性
- 观察和动作空间
- 多智能体环境
- 海洋套件环境
- 自定义环境开发工作流程
- Python 到 C 的优化路径
- 第三方环境集成
- 包装器和最佳实践
- 调试

* *向量化.md** - 向量化优化：
- 架构和关键优化
- 矢量化模式（串行、多处理、异步）
- 工作程序和批处理配置
- 共享内存和零复制模式
- 高级矢量化（分层，自定义）
- 多代理矢量化
- 性能监控和分析
- 故障排除和最佳实践

* *policies.md** - 策略架构指南：
- 基本策略结构
- 图像的CNN策略
- 具有优化的LSTM策略
- 多输入策略
- 连续操作策略
- 多代理策略
- 高级架构（注意力、残差）
- 观察处理和展开
- 初始化和归一化
- 调试和测试

* *integration.md** - 框架集成指南：
- Gymnasium 集成
- PettingZoo 集成（并行和AEC)
- 第三方环境（Procgen、NetHack、Minigrid 等）
- 自定义包装器（观察、奖励、框架堆叠等）
- 空间转换和展开
- 环境注册
- 兼容性模式
- 性能注意事项
- 调试集成

## 成功提示

1. **从简单开始**：在创建自定义环境之前从海洋环境或体育馆集成开始

2. **早期分析**：从一开始就测量每秒的步数，以识别瓶颈

3. **使用模板**：`scripts/train_template.py` 和 `scripts/env_template.py` 提供坚实的起点

4. **根据需要阅读参考资料**：每个参考文件都是独立的，并专注于特定功能

5. **逐步优化**：从 Python 开始，分析，然后根据需要使用 C 优化关键路径

6. **利用矢量化**：PufferLib 的矢量化是实现高吞吐量

7 的关键。 **监控训练**：使用 WandB 或 Neptune 跟踪实验并尽早发现问题

8. **测试环境**：在扩大训练规模之前验证环境逻辑

9. **检查现有环境**：Ocean suite提供20多个预建环境

10. **使用正确的初始化**：始终使用 `pufferlib.pytorch` 中的 `layer_init` 进行策略

## 常见用例

### 标准基准培训
```python
# Atari
env = pufferlib.make('atari-pong', num_envs=256)

# Procgen
env = pufferlib.make('procgen-coinrun', num_envs=256)

# Minigrid
env = pufferlib.make('minigrid-empty-8x8', num_envs=256)
```

### 多代理学习
```python
# PettingZoo
env = pufferlib.make('pettingzoo-pistonball', num_envs=128)

# Shared policy for all agents
policy = create_policy(env.observation_space, env.action_space)
trainer = PuffeRL(env=env, policy=policy)
```

### 自定义任务开发
```python
# Create custom environment
class MyTask(PufferEnv):
    # ... implement environment ...

# Vectorize and train
env = pufferlib.emulate(MyTask, num_envs=256)
trainer = PuffeRL(env=env, policy=my_policy)
```

### 高性能优化
```python
# Maximize throughput
env = pufferlib.make(
    'my-env',
    num_envs=1024,      # Large batch
    num_workers=16,     # Many workers
    envs_per_worker=64  # Optimize per worker
)
```

## 安装

```bash
uv pip install pufferlib
```

## 文档

- 官方文档：https://puffer.ai/docs.html
- GitHub：https://github.com/PufferAI/PufferLib
- Discord：提供社区支持
