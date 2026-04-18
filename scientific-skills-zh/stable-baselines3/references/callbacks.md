# Stable Baselines3 回调系统

本文档提供了有关 Stable Baselines3 中用于监控和控制训练的回调系统的全面信息。

## 概述

回调是在训练过程中的特定点调用的函数，用于：
- 监控训练指标
- 保存检查点
- 实施提前停止
- 记录自定义指标
- 动态调整超参数
- 触发评估

## 内置回调

### EvalCallback

E定期评估代理并保存最佳模型。

```python
from stable_baselines3.common.callbacks import EvalCallback

eval_callback = EvalCallback(
    eval_env,                                    # Separate evaluation environment
    best_model_save_path="./logs/best_model/",  # Where to save best model
    log_path="./logs/eval/",                    # Where to save evaluation logs
    eval_freq=10000,                            # Evaluate every N steps
    n_eval_episodes=5,                          # Number of episodes per evaluation
    deterministic=True,                         # Use deterministic actions
    render=False,                               # Render during evaluation
    verbose=1,
    warn=True,
)

model.learn(total_timesteps=100000, callback=eval_callback)
```

* *Key特点：**
- 根据平均奖励自动保存最佳模型
- 将评估指标记录到TensorBoard
- 如果达到奖励阈值可以停止训练

* *重要：**使用矢量化训练环境时，请调整`eval_freq`:
```python
# With 4 parallel environments, divide eval_freq by n_envs
eval_freq = 10000 // 4  # Evaluate every 10000 total environment steps
```

### CheckpointCallback

定期保存模型检查点。

```python
from stable_baselines3.common.callbacks import CheckpointCallback

checkpoint_callback = CheckpointCallback(
    save_freq=10000,                     # Save every N steps
    save_path="./logs/checkpoints/",     # Directory for checkpoints
    name_prefix="rl_model",              # Prefix for checkpoint files
    save_replay_buffer=True,             # Save replay buffer (off-policy only)
    save_vecnormalize=True,              # Save VecNormalize stats
    verbose=2,
)

model.learn(total_timesteps=100000, callback=checkpoint_callback)
```

* *输出文件：**
- `rl_model_10000_steps.zip` - 模型位于10k 步
- `rl_model_20000_steps.zip` - 20k 步模型
- 等

* *重要：** 调整 `save_freq` 以适应矢量化环境（除以 n_envs）。

### StopTrainingOnRewardThreshold

停止训练当平均奖励超过阈值时。

```python
from stable_baselines3.common.callbacks import StopTrainingOnRewardThreshold

stop_callback = StopTrainingOnRewardThreshold(
    reward_threshold=200,  # Stop when mean reward >= 200
    verbose=1,
)

# Must be used with EvalCallback
eval_callback = EvalCallback(
    eval_env,
    callback_on_new_best=stop_callback,  # Trigger when new best found
    eval_freq=10000,
    n_eval_episodes=5,
)

model.learn(total_timesteps=1000000, callback=eval_callback)
```

### StopTrainingOnNoModelImprovement

如果模型在 N 次评估中没有改善，则停止训练。

```python
from stable_baselines3.common.callbacks import StopTrainingOnNoModelImprovement

stop_callback = StopTrainingOnNoModelImprovement(
    max_no_improvement_evals=10,  # Stop after 10 evals with no improvement
    min_evals=20,                 # Minimum evaluations before stopping
    verbose=1,
)

# Use with EvalCallback
eval_callback = EvalCallback(
    eval_env,
    callback_after_eval=stop_callback,
    eval_freq=10000,
)

model.learn(total_timesteps=1000000, callback=eval_callback)
```

### StopTrainingOnMaxEpisodes

在达到最大次数后停止训练。

```python
from stable_baselines3.common.callbacks import StopTrainingOnMaxEpisodes

stop_callback = StopTrainingOnMaxEpisodes(
    max_episodes=1000,  # Stop after 1000 episodes
    verbose=1,
)

model.learn(total_timesteps=1000000, callback=stop_callback)
```

### ProgressBarCallback

在训练期间显示进度条（需要tqdm).

```python
from stable_baselines3.common.callbacks import ProgressBarCallback

progress_callback = ProgressBarCallback()

model.learn(total_timesteps=100000, callback=progress_callback)
```

* *输出：**
```
100%|██████████| 100000/100000 [05:23<00:00, 309.31it/s]
```

## 创建自定义回调

### BaseCallback 结构

```python
from stable_baselines3.common.callbacks import BaseCallback

class CustomCallback(BaseCallback):
    """
    Custom callback template.
    """

    def __init__(self, verbose=0):
        super().__init__(verbose)
        # Custom initialization

    def _init_callback(self) -> None:
        """
        Called once when training starts.
        Useful for initialization that requires access to model/env.
        """
        pass

    def _on_training_start(self) -> None:
        """
        Called before the first rollout starts.
        """
        pass

    def _on_rollout_start(self) -> None:
        """
        Called before collecting new samples (on-policy algorithms).
        """
        pass

    def _on_step(self) -> bool:
        """
        Called after every step in the environment.

        Returns:
            bool: If False, training will be stopped.
        """
        return True  # Continue training

    def _on_rollout_end(self) -> None:
        """
        Called after rollout ends (on-policy algorithms).
        """
        pass

    def _on_training_end(self) -> None:
        """
        Called at the end of training.
        """
        pass
```

### 有用属性

在回调内部，您可以访问：

- **`self.model`**：RL算法实例
- **`self.training_env`**：训练环境
- **`self.n_calls`**：调用`_on_step()`的次数
- **`self.num_timesteps`**：环境步骤总数
- **`self.locals`**：算法中的局部变量（因算法而异）
- **`self.globals`**：算法中的全局变量
- **`self.logger`**：TensorBoard/CSV 日志记录器
- **`self.parent`**：父回调（如果在CallbackList)

## 自定义回调示例

### 示例 1：记录自定义指标

```python
class LogCustomMetricsCallback(BaseCallback):
    """
    Log custom metrics to TensorBoard.
    """

    def __init__(self, verbose=0):
        super().__init__(verbose)
        self.episode_rewards = []

    def _on_step(self) -> bool:
        # Check if episode ended
        if self.locals["dones"][0]:
            # Log episode reward
            episode_reward = self.locals["infos"][0].get("episode", {}).get("r", 0)
            self.episode_rewards.append(episode_reward)

            # Log to TensorBoard
            self.logger.record("custom/episode_reward", episode_reward)
            self.logger.record("custom/mean_reward_last_100",
                             np.mean(self.episode_rewards[-100:]))

        return True
```

### 示例 2：调整学习率

```python
class LinearScheduleCallback(BaseCallback):
    """
    Linearly decrease learning rate during training.
    """

    def __init__(self, initial_lr=3e-4, final_lr=3e-5, verbose=0):
        super().__init__(verbose)
        self.initial_lr = initial_lr
        self.final_lr = final_lr

    def _on_step(self) -> bool:
        # Calculate progress (0 to 1)
        progress = self.num_timesteps / self.locals["total_timesteps"]

        # Linear interpolation
        new_lr = self.initial_lr + (self.final_lr - self.initial_lr) * progress

        # Update learning rate
        for param_group in self.model.policy.optimizer.param_groups:
            param_group["lr"] = new_lr

        # Log learning rate
        self.logger.record("train/learning_rate", new_lr)

        return True
```

### 示例 3：移动时提前停止Average

```python
class EarlyStoppingCallback(BaseCallback):
    """
    Stop training if moving average of rewards doesn't improve.
    """

    def __init__(self, check_freq=10000, min_reward=200, window=100, verbose=0):
        super().__init__(verbose)
        self.check_freq = check_freq
        self.min_reward = min_reward
        self.window = window
        self.rewards = []

    def _on_step(self) -> bool:
        # Collect episode rewards
        if self.locals["dones"][0]:
            reward = self.locals["infos"][0].get("episode", {}).get("r", 0)
            self.rewards.append(reward)

        # Check every check_freq steps
        if self.n_calls % self.check_freq == 0 and len(self.rewards) >= self.window:
            mean_reward = np.mean(self.rewards[-self.window:])
            if self.verbose > 0:
                print(f"Mean reward: {mean_reward:.2f}")

            if mean_reward >= self.min_reward:
                if self.verbose > 0:
                    print(f"Stopping: reward threshold reached!")
                return False  # Stop training

        return True  # Continue training
```

### 示例 4：通过自定义指标保存最佳模型

```python
class SaveBestModelCallback(BaseCallback):
    """
    Save model when custom metric is best.
    """

    def __init__(self, check_freq=1000, save_path="./best_model/", verbose=0):
        super().__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path
        self.best_score = -np.inf

    def _init_callback(self) -> None:
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            # Calculate custom metric (example: policy entropy)
            custom_metric = self.locals.get("entropy_losses", [0])[-1]

            if custom_metric > self.best_score:
                self.best_score = custom_metric
                if self.verbose > 0:
                    print(f"New best! Saving model to {self.save_path}")
                self.model.save(os.path.join(self.save_path, "best_model"))

        return True
```

### 示例 5：记录环境特定信息

```python
class EnvironmentInfoCallback(BaseCallback):
    """
    Log custom info from environment.
    """

    def _on_step(self) -> bool:
        # Access info dict from environment
        info = self.locals["infos"][0]

        # Log custom metrics from environment
        if "distance_to_goal" in info:
            self.logger.record("env/distance_to_goal", info["distance_to_goal"])

        if "success" in info:
            self.logger.record("env/success_rate", info["success"])

        return True
```

## 链接多个回调

使用`CallbackList`组合多个回调：

```python
from stable_baselines3.common.callbacks import CallbackList

callback_list = CallbackList([
    eval_callback,
    checkpoint_callback,
    progress_callback,
    custom_callback,
])

model.learn(total_timesteps=100000, callback=callback_list)
```

或者直接传递一个列表：

```python
model.learn(
    total_timesteps=100000,
    callback=[eval_callback, checkpoint_callback, custom_callback]
)
```

## 基于事件的回调

回调可以在特定上触发其他回调events:

```python
from stable_baselines3.common.callbacks import EventCallback

# Stop training when reward threshold reached
stop_callback = StopTrainingOnRewardThreshold(reward_threshold=200)

# Evaluate periodically and trigger stop_callback when new best found
eval_callback = EvalCallback(
    eval_env,
    callback_on_new_best=stop_callback,  # Triggered when new best model
    eval_freq=10000,
)
```

## 记录到 TensorBoard

使用 `self.logger.record()` 记录指标：

```python
class TensorBoardCallback(BaseCallback):
    def _on_step(self) -> bool:
        # Log scalar
        self.logger.record("custom/my_metric", value)

        # Log multiple metrics
        self.logger.record("custom/metric1", value1)
        self.logger.record("custom/metric2", value2)

        # Logger automatically writes to TensorBoard
        return True
```

* *查看TensorBoard：**
```bash
tensorboard --logdir ./logs/
```

## 高级模式

### 课程学习

```python
class CurriculumCallback(BaseCallback):
    """
    Increase task difficulty over time.
    """

    def __init__(self, difficulty_schedule, verbose=0):
        super().__init__(verbose)
        self.difficulty_schedule = difficulty_schedule

    def _on_step(self) -> bool:
        # Update environment difficulty based on progress
        progress = self.num_timesteps / self.locals["total_timesteps"]

        for threshold, difficulty in self.difficulty_schedule:
            if progress >= threshold:
                self.training_env.env_method("set_difficulty", difficulty)

        return True
```

### 基于人群培训

```python
class PopulationBasedCallback(BaseCallback):
    """
    Adjust hyperparameters based on performance.
    """

    def __init__(self, check_freq=10000, verbose=0):
        super().__init__(verbose)
        self.check_freq = check_freq
        self.performance_history = []

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            # Evaluate performance
            perf = self._evaluate_performance()
            self.performance_history.append(perf)

            # Adjust hyperparameters if performance plateaus
            if len(self.performance_history) >= 3:
                recent = self.performance_history[-3:]
                if max(recent) - min(recent) < 0.01:  # Plateau detected
                    self._adjust_hyperparameters()

        return True

    def _adjust_hyperparameters(self):
        # Example: increase learning rate
        for param_group in self.model.policy.optimizer.param_groups:
            param_group["lr"] *= 1.2
```

## 调试技巧

### 打印可用属性

```python
class DebugCallback(BaseCallback):
    def _on_step(self) -> bool:
        if self.n_calls == 1:
            print("Available in self.locals:")
            for key in self.locals.keys():
                print(f"  {key}: {type(self.locals[key])}")
        return True
```

### 常见问题

1. **未调用回调：**
  - 确保回调已传递到 `model.learn()`
  - 检查 `_on_step()` 是否返回 `True`

2. **回调中的属性错误：**
  - 并非所有属性在所有回调中都可用
  - 使用 `self.locals.get("key", default)` 以确保安全

3. **内存泄漏：**
  - 不要在回调状态下存储大型数组
  - 定期清除缓冲区

4. **性能影响：**
  - 最小化`_on_step()`中的计算（每一步调用）
  - 使用`check_freq`限制昂贵的操作

## 最佳实践

1. **使用适当的回调计时：**
  - `_on_step()`：对于每一步都会更改的指标
  - `_on_rollout_end()`：对于通过推出计算的指标
  - `_init_callback()`：对于一次性初始化

2. **高效记录：**
  - 不要记录每个步骤（损害性能）
  - 汇总指标并定期记录

3. **处理矢量化环境：**
  - 请记住，`dones`、`infos` 等是数组
  - 检查每个环境的 `dones[i]`

4. **独立测试回调：**
  - 创建简单的测试用例
  - 在长时间训练运行之前验证回调行为

5. **记录自定义回调：**
  - 清除文档字符串
  - 注释中的示例用法

## 其他资源

- 官方SB3回调指南：https://stable-baselines3.readthedocs.io/en/master/guide/callbacks.html
- 回调API参考： https://stable-baselines3.readthedocs.io/en/master/common/callbacks.html
- TensorBoard 文档：https://www.tensorflow.org/tensorboard
