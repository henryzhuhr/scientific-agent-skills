# PufferLib 训练指南

## 概述

PuffeRL 是 PufferLib 的高性能训练算法，基于 CleanRL 的 PPO 和 LSTM，并通过专有研究改进进行了增强。通过优化的矢量化和高效的实现，实现每秒百万步的训练。

## 训练工作流程

### 基本训练循环

PuffeRL训练器提供三种核心方法：

```python
# Collect environment interactions
rollout_data = trainer.evaluate()

# Train on collected batch
train_metrics = trainer.train()

# Aggregate and log results
trainer.mean_and_log()
```

### CLI Training

通过命令快速启动训练line:

```bash
# Basic training
puffer train environment_name --train.device cuda --train.learning-rate 0.001

# Custom configuration
puffer train environment_name \
    --train.device cuda \
    --train.batch-size 32768 \
    --train.learning-rate 0.0003 \
    --train.num-iterations 10000
```

### Python 训练脚本

```python
import pufferlib
from pufferlib import PuffeRL

# Initialize environment
env = pufferlib.make('environment_name', num_envs=256)

# Create trainer
trainer = PuffeRL(
    env=env,
    policy=my_policy,
    device='cuda',
    learning_rate=3e-4,
    batch_size=32768,
    n_epochs=4,
    gamma=0.99,
    gae_lambda=0.95,
    clip_coef=0.2,
    ent_coef=0.01,
    vf_coef=0.5,
    max_grad_norm=0.5
)

# Training loop
for iteration in range(num_iterations):
    # Collect rollouts
    rollout_data = trainer.evaluate()

    # Train on batch
    train_metrics = trainer.train()

    # Log results
    trainer.mean_and_log()
```

## 关键训练参数

### 核心超参数

- **learning_rate**：优化器的学习率（默认值： 3e-4)
- **batch_size**：每个训练批次的时间步数（默认：32768）
- **n_epochs**：每个批次的训练纪元数（默认：4）
- **num_envs**：并行环境的数量（默认：256）
- **num_steps**：每次部署每个环境的步骤（默认值：128）

### PPO 参数

- **gamma**：折扣因子（默认值：0.99）
- **gae_lambda**：GAE 计算的 Lambda（默认值：0.95）
- **clip_coef**：PPO 裁剪系数（默认：0.2）
- **ent_coef**：探索的熵系数（默认：0.01）
- **vf_coef**：价值函数损失系数（默认：0.5）
- **max_grad_norm**：裁剪的最大梯度范数（默认：0.5）

### 性能参数

- **device**：计算设备（'cuda'或'cpu'）
- **compile**：使用torch.compile进行更快的训练（默认：True）
- **num_workers**：矢量化workers的数量（默认：auto）

## 分布式训练

### 多GPU训练

使用torchrun进行跨多个GPU的分布式训练：

```bash
torchrun --nproc_per_node=4 train.py \
    --train.device cuda \
    --train.batch-size 131072
```

### 多节点训练

用于跨多个节点的分布式训练：

```bash
# On main node (rank 0)
torchrun --nproc_per_node=8 \
    --nnodes=4 \
    --node_rank=0 \
    --master_addr=MASTER_IP \
    --master_port=29500 \
    train.py

# On worker nodes (rank 1, 2, 3)
torchrun --nproc_per_node=8 \
    --nnodes=4 \
    --node_rank=NODE_RANK \
    --master_addr=MASTER_IP \
    --master_port=29500 \
    train.py
```

## 监控和记录

### Logger集成

PufferLib 支持多个日志记录后端：

#### 权重和偏差

```python
from pufferlib import WandbLogger

logger = WandbLogger(
    project='my_project',
    entity='my_team',
    name='experiment_name',
    config=trainer_config
)

trainer = PuffeRL(env, policy, logger=logger)
```

#### Neptune

```python
from pufferlib import NeptuneLogger

logger = NeptuneLogger(
    project='my_team/my_project',
    name='experiment_name',
    api_token='YOUR_TOKEN'
)

trainer = PuffeRL(env, policy, logger=logger)
```

#### 否Logger

```python
from pufferlib import NoLogger

trainer = PuffeRL(env, policy, logger=NoLogger())
```

### 关键指标

训练日志包括：

- **性能指标**：
  - 每秒步数 (SPS)
  - 训练吞吐量
  - 每分钟的挂钟时间迭代

- **学习指标**：
  - 情节奖励（平均值、最小值、最大值）
  - 情节长度
  - 价值函数损失
  - 策略损失
  - 熵
  - 解释方差
  - Clipfrac

- **环境指标**：
  - 特定于环境的奖励
  - 成功率
  - 自定义指标

### 终端仪表板

PufferLib 提供实时终端仪表板，显示：
- 训练进度
- 当前SPS
- 剧集统计
- 损失值
- GPU 利用率

## 检查点

### 保存检查点

```python
# Save checkpoint
trainer.save_checkpoint('checkpoint.pt')

# Save with additional metadata
trainer.save_checkpoint(
    'checkpoint.pt',
    metadata={'iteration': iteration, 'best_reward': best_reward}
)
```

### 加载检查点

```python
# Load checkpoint
trainer.load_checkpoint('checkpoint.pt')

# Resume training
for iteration in range(resume_iteration, num_iterations):
    trainer.evaluate()
    trainer.train()
    trainer.mean_and_log()
```

## 使用Protein进行超参数调整

Protein系统支持自动超参数和奖励调整：

```python
from pufferlib import Protein

# Define search space
search_space = {
    'learning_rate': [1e-4, 3e-4, 1e-3],
    'batch_size': [16384, 32768, 65536],
    'ent_coef': [0.001, 0.01, 0.1],
    'clip_coef': [0.1, 0.2, 0.3]
}

# Run hyperparameter search
protein = Protein(
    env_name='environment_name',
    search_space=search_space,
    num_trials=100,
    metric='mean_reward'
)

best_config = protein.optimize()
```

## 性能优化技巧

### 最大化吞吐量

1. **批量大小**：增加batch_size以充分利用GPU
2. **Num Envs**：CPU 和 GPU 利用率之间的平衡
3. **编译**：启用 torch.compile 以获得 10-20% 的加速 
4. **Workers**：根据环境复杂度调整num_workers
5. **设备**：始终使用“cuda”进行神经网络训练

### 环境速度

- 纯Python 环境：~100k-500k SPS
- 基于C 的环境：~4M SPS
- 训练开销：~1M-4M 总计 SPS

### 内存管理

- 如果 GPU 内存不足，则减少 batch_size
- 如果 CPU 内存不足，则减少 num_envs
- 使用梯度累积以获得大的有效批量大小

## 常见训练模式

### 课程学习

```python
# Start with easy tasks, gradually increase difficulty
difficulty_levels = [0.1, 0.3, 0.5, 0.7, 1.0]

for difficulty in difficulty_levels:
    env = pufferlib.make('environment_name', difficulty=difficulty)
    trainer = PuffeRL(env, policy)

    for iteration in range(iterations_per_level):
        trainer.evaluate()
        trainer.train()
        trainer.mean_and_log()
```

### 奖励塑造

```python
# Wrap environment with custom reward shaping
class RewardShapedEnv(pufferlib.PufferEnv):
    def step(self, actions):
        obs, rewards, dones, infos = super().step(actions)

        # Add shaped rewards
        shaped_rewards = rewards + 0.1 * proximity_bonus

        return obs, shaped_rewards, dones, infos
```

### 多阶段训练

```python
# Train in multiple stages with different configurations
stages = [
    {'learning_rate': 1e-3, 'iterations': 1000},   # Exploration
    {'learning_rate': 3e-4, 'iterations': 5000},   # Main training
    {'learning_rate': 1e-4, 'iterations': 2000}    # Fine-tuning
]

for stage in stages:
    trainer.learning_rate = stage['learning_rate']
    for iteration in range(stage['iterations']):
        trainer.evaluate()
        trainer.train()
        trainer.mean_and_log()
```

## 故障排除

### 低性能

- 检查环境是否正确矢量化
- 使用 `nvidia-smi`
 验证 GPU 利用率- 增加批量大小以使 GPU 饱和
- 启用编译模式
- 使用 `torch.profiler`

### 进行分析 

- 减少训练不稳定性Learning_rate
- 减少batch_size
- 增加num_envs 以获取更多样的样本
- 添加熵系数以进行更多探索
- 检查奖励缩放

### 内存问题

- 减少batch_size 或num_envs
- 使用梯度累积
- 如果导致OOM则禁用编译模式
- 检查自定义环境中的内存泄漏
