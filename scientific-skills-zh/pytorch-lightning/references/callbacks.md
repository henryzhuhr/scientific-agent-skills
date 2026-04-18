# 回调 - 综合指南

## 概述

回调允许在训练中添加任意独立的程序，而不会弄乱您的LightningModule研究代码。它们在训练生命周期中的特定挂钩上执行自定义逻辑。

## 架构

Lightning 通过三个组件组织训练逻辑：
- **Trainer** - 工程基础设施
- **LightningModule** - 研究代码
- **回调** - 非必要功能（监控、检查点、自定义）行为）

## 创建自定义回调

基本结构：

```python
from lightning.pytorch.callbacks import Callback

class MyCustomCallback(Callback):
    def on_train_start(self, trainer, pl_module):
        print("Training is starting!")

    def on_train_end(self, trainer, pl_module):
        print("Training is done!")

# Use with Trainer
trainer = L.Trainer(callbacks=[MyCustomCallback()])
```

## 内置回调

### ModelCheckpoint

根据监控指标保存模型。

* *关键参数：**
- `dirpath` - 保存检查点的目录
- `filename` - 检查点文件名模式
- `monitor` - 要监视的指标
- `mode` - 受监视指标的“最小”或“最大”
- `save_top_k` - 数量保留的最佳模型
- `save_last` - 保存最后一个纪元检查点
- `every_n_epochs` - 保存每N个纪元
- `save_on_train_epoch_end` - 在训练纪元结束时保存与验证end

* *示例：**
```python
from lightning.pytorch.callbacks import ModelCheckpoint

# Save top 3 models based on validation loss
checkpoint_callback = ModelCheckpoint(
    dirpath="checkpoints/",
    filename="model-{epoch:02d}-{val_loss:.2f}",
    monitor="val_loss",
    mode="min",
    save_top_k=3,
    save_last=True
)

# Save every 10 epochs
checkpoint_callback = ModelCheckpoint(
    dirpath="checkpoints/",
    filename="model-{epoch:02d}",
    every_n_epochs=10,
    save_top_k=-1  # Save all
)

# Save best model based on accuracy
checkpoint_callback = ModelCheckpoint(
    dirpath="checkpoints/",
    filename="best-model",
    monitor="val_acc",
    mode="max",
    save_top_k=1
)

trainer = L.Trainer(callbacks=[checkpoint_callback])
```

* *访问保存的检查点：**
```python
# Get best model path
best_model_path = checkpoint_callback.best_model_path

# Get last checkpoint path
last_checkpoint = checkpoint_callback.last_model_path

# Get all checkpoint paths
all_checkpoints = checkpoint_callback.best_k_models
```

### EarlyStopping

当监控指标停止改善时停止训练。

* *Key参数：**
- `monitor` - 监控指标
- `patience` - 训练停止后没有改善的时期数
- `mode` - 监控指标的“最小值”或“最大值”
- `min_delta` - 符合条件的最小变化改进
- `verbose` - 打印消息
- `strict` - 如果找不到受监控的指标，则崩溃

  * *示例：** 
```python
from lightning.pytorch.callbacks import EarlyStopping

# Stop when validation loss stops improving
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=10,
    mode="min",
    verbose=True
)

# Stop when accuracy plateaus
early_stop = EarlyStopping(
    monitor="val_acc",
    patience=5,
    mode="max",
    min_delta=0.001  # Must improve by at least 0.001
)

trainer = L.Trainer(callbacks=[early_stop])
```

### LearningRateMonitor

跟踪学习率变化来自调度程序。

* *关键参数：**
- `logging_interval` - 何时记录：“step”或“epoch”
- `log_momentum` - 还记录动量值

* *示例：**
```python
from lightning.pytorch.callbacks import LearningRateMonitor

lr_monitor = LearningRateMonitor(logging_interval="step")
trainer = L.Trainer(callbacks=[lr_monitor])

# Logs learning rate automatically as "lr-{optimizer_name}"
```

### DeviceStatsMonitor

记录设备性能指标（GPU/CPU/TPU）。

* *关键参数：**
- `cpu_stats` - 日志CPU统计信息

* *示例：**
```python
from lightning.pytorch.callbacks import DeviceStatsMonitor

device_stats = DeviceStatsMonitor(cpu_stats=True)
trainer = L.Trainer(callbacks=[device_stats])

# Logs: gpu_utilization, gpu_memory_usage, etc.
```

### ModelSummary / RichModelSummary

显示模型架构和参数count.

* *示例：**
```python
from lightning.pytorch.callbacks import ModelSummary, RichModelSummary

# Basic summary
summary = ModelSummary(max_depth=2)

# Rich formatted summary (prettier)
rich_summary = RichModelSummary(max_depth=3)

trainer = L.Trainer(callbacks=[rich_summary])
```

### Timer

跟踪并限制训练持续时间。

* *关键参数：**
- `duration` - 最大训练时间（timedelta 或 dict）
- `interval` - 检查间隔：“step”、“epoch”或“batch”

* *示例：**
```python
from lightning.pytorch.callbacks import Timer
from datetime import timedelta

# Limit training to 1 hour
timer = Timer(duration=timedelta(hours=1))

# Or using dict
timer = Timer(duration={"hours": 23, "minutes": 30})

trainer = L.Trainer(callbacks=[timer])
```

### BatchSizeFinder

自动查找最佳批次size.

* *示例：**
```python
from lightning.pytorch.callbacks import BatchSizeFinder

batch_finder = BatchSizeFinder(mode="power", steps_per_trial=3)

trainer = L.Trainer(callbacks=[batch_finder])
trainer.fit(model, datamodule=dm)

# Optimal batch size is set automatically
```

### GradientAccumulationScheduler

动态调度梯度累积步骤。

* *示例：**
```python
from lightning.pytorch.callbacks import GradientAccumulationScheduler

# Accumulate 4 batches for first 5 epochs, then 2 batches
accumulator = GradientAccumulationScheduler(scheduling={0: 4, 5: 2})

trainer = L.Trainer(callbacks=[accumulator])
```

### StochasticWeightAveraging (SWA)

应用随机权重平均以获得更好的泛化能力。

* *示例：**
```python
from lightning.pytorch.callbacks import StochasticWeightAveraging

swa = StochasticWeightAveraging(swa_lrs=1e-2, swa_epoch_start=0.8)

trainer = L.Trainer(callbacks=[swa])
```

## 自定义回调示例

### 简单日志记录回调

```python
class MetricsLogger(Callback):
    def __init__(self):
        self.metrics = []

    def on_validation_end(self, trainer, pl_module):
        # Access logged metrics
        metrics = trainer.callback_metrics
        self.metrics.append(dict(metrics))
        print(f"Validation metrics: {metrics}")
```

### 梯度监控回调

```python
class GradientMonitor(Callback):
    def on_after_backward(self, trainer, pl_module):
        # Log gradient norms
        for name, param in pl_module.named_parameters():
            if param.grad is not None:
                grad_norm = param.grad.norm().item()
                pl_module.log(f"grad_norm/{name}", grad_norm)
```

### 自定义检查点回调

```python
class CustomCheckpoint(Callback):
    def __init__(self, save_dir):
        self.save_dir = save_dir

    def on_train_epoch_end(self, trainer, pl_module):
        epoch = trainer.current_epoch
        if epoch % 5 == 0:  # Save every 5 epochs
            filepath = f"{self.save_dir}/custom-{epoch}.ckpt"
            trainer.save_checkpoint(filepath)
            print(f"Saved checkpoint: {filepath}")
```

### 模型冻结回调

```python
class FreezeUnfreeze(Callback):
    def __init__(self, freeze_until_epoch=10):
        self.freeze_until_epoch = freeze_until_epoch

    def on_train_epoch_start(self, trainer, pl_module):
        epoch = trainer.current_epoch

        if epoch < self.freeze_until_epoch:
            # Freeze backbone
            for param in pl_module.backbone.parameters():
                param.requires_grad = False
        else:
            # Unfreeze backbone
            for param in pl_module.backbone.parameters():
                param.requires_grad = True
```

### 学习率查找器回调

```python
class LRFinder(Callback):
    def __init__(self, min_lr=1e-5, max_lr=1e-1, num_steps=100):
        self.min_lr = min_lr
        self.max_lr = max_lr
        self.num_steps = num_steps
        self.lrs = []
        self.losses = []

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        if batch_idx >= self.num_steps:
            trainer.should_stop = True
            return

        # Exponential LR schedule
        lr = self.min_lr * (self.max_lr / self.min_lr) ** (batch_idx / self.num_steps)
        optimizer = trainer.optimizers[0]
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr

        self.lrs.append(lr)
        self.losses.append(outputs['loss'].item())

    def on_train_end(self, trainer, pl_module):
        # Plot LR vs Loss
        import matplotlib.pyplot as plt
        plt.plot(self.lrs, self.losses)
        plt.xscale('log')
        plt.xlabel('Learning Rate')
        plt.ylabel('Loss')
        plt.savefig('lr_finder.png')
```

### 预测保存程序回调

```python
class PredictionSaver(Callback):
    def __init__(self, save_path):
        self.save_path = save_path
        self.predictions = []

    def on_predict_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        self.predictions.append(outputs)

    def on_predict_end(self, trainer, pl_module):
        # Save all predictions
        torch.save(self.predictions, self.save_path)
        print(f"Predictions saved to {self.save_path}")
```

## 可用的挂钩

### 设置和拆卸
- `setup(trainer, pl_module, stage)` - 在拟合/测试/预测开始时调用
- `teardown(trainer, pl_module, stage)` - 在拟合/测试/预测结束时调用

### 训练生命周期
- `on_fit_start(trainer, pl_module)` - 在开始时调用fit
- `on_fit_end(trainer, pl_module)` - 在 fit 结束时调用
- `on_train_start(trainer, pl_module)` - 在训练开始时调用
- `on_train_end(trainer, pl_module)` - 在训练结束时调用

### Epoch Boundaries
- `on_train_epoch_start(trainer, pl_module)` - 在训练时期开始时调用
- `on_train_epoch_end(trainer, pl_module)` - 在训练时期结束时调用
- `on_validation_epoch_start(trainer, pl_module)` - 在验证开始时调用
- `on_validation_epoch_end(trainer, pl_module)` - 在验证结束时调用
- `on_test_epoch_start(trainer, pl_module)` - 在验证开始时调用测试开始
- `on_test_epoch_end(trainer, pl_module)` - 测试结束时调用

### 批次边界
- `on_train_batch_start(trainer, pl_module, batch, batch_idx)` - 训练前批次
- `on_train_batch_end(trainer, pl_module, outputs, batch, batch_idx)` - 训练后批次
- `on_validation_batch_start(trainer, pl_module, batch, batch_idx)` - 验证前批次
- `on_validation_batch_end(trainer, pl_module, outputs, batch, batch_idx)` - 验证后批次

### 梯度事件
- `on_before_backward(trainer, pl_module, loss)` - 在loss.backward()之前
- `on_after_backward(trainer, pl_module)` - 在loss.backward()之后
- `on_before_optimizer_step(trainer, pl_module, optimizer)` - 在optimizer.step()之前

### 检查点事件
- `on_save_checkpoint(trainer, pl_module, checkpoint)` - 何时保存检查点
- `on_load_checkpoint(trainer, pl_module, checkpoint)` - 加载检查点时

### 异常处理
- `on_exception(trainer, pl_module, exception)` - 发生异常时

## 状态管理

用于需要持久化的回调检查点：

```python
class StatefulCallback(Callback):
    def __init__(self):
        self.counter = 0

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        self.counter += 1

    def state_dict(self):
        return {"counter": self.counter}

    def load_state_dict(self, state_dict):
        self.counter = state_dict["counter"]

    @property
    def state_key(self):
        # Unique identifier for this callback
        return "my_stateful_callback"
```

## 最佳实践

### 1. 保持回调隔离
E每个回调应该是独立的：

```python
# Good: Self-contained
class MyCallback(Callback):
    def __init__(self):
        self.data = []

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        self.data.append(outputs['loss'].item())

# Bad: Depends on external state
global_data = []

class BadCallback(Callback):
    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        global_data.append(outputs['loss'].item())  # External dependency
```

### 2. 避免内部回调依赖关系
回调不应依赖于其他回调：

```python
# Bad: Callback B depends on Callback A
class CallbackA(Callback):
    def __init__(self):
        self.value = 0

class CallbackB(Callback):
    def __init__(self, callback_a):
        self.callback_a = callback_a  # Tight coupling

# Good: Independent callbacks
class CallbackA(Callback):
    def __init__(self):
        self.value = 0

class CallbackB(Callback):
    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        # Access trainer state instead
        value = trainer.callback_metrics.get('metric')
```

### 3. 切勿手动调用回调方法
让 Lightning 自动调用回调：

```python
# Bad: Manual invocation
callback = MyCallback()
callback.on_train_start(trainer, model)  # Don't do this

# Good: Let Trainer handle it
trainer = L.Trainer(callbacks=[MyCallback()])
```

### 4. 为任何设计执行顺序
Callbacks可以按任何顺序执行，所以不要依赖于特定的顺序：

```python
# Good: Order-independent
class GoodCallback(Callback):
    def on_train_epoch_end(self, trainer, pl_module):
        # Use trainer state, not other callbacks
        metrics = trainer.callback_metrics
        self.log_metrics(metrics)
```

### 5.对非必要逻辑使用回调
将核心研究代码保留在LightningModule中，使用回调进行辅助功能：

```python
# Good separation
class MyModel(L.LightningModule):
    # Core research logic here
    def training_step(self, batch, batch_idx):
        return loss

# Non-essential monitoring in callback
class MonitorCallback(Callback):
    def on_validation_end(self, trainer, pl_module):
        # Monitoring logic
        pass
```

## 常见模式

### 组合多个回调

```python
from lightning.pytorch.callbacks import (
    ModelCheckpoint,
    EarlyStopping,
    LearningRateMonitor,
    DeviceStatsMonitor
)

callbacks = [
    ModelCheckpoint(monitor="val_loss", mode="min", save_top_k=3),
    EarlyStopping(monitor="val_loss", patience=10, mode="min"),
    LearningRateMonitor(logging_interval="step"),
    DeviceStatsMonitor()
]

trainer = L.Trainer(callbacks=callbacks)
```

### 条件回调激活

```python
class ConditionalCallback(Callback):
    def __init__(self, activate_after_epoch=10):
        self.activate_after_epoch = activate_after_epoch

    def on_train_epoch_end(self, trainer, pl_module):
        if trainer.current_epoch >= self.activate_after_epoch:
            # Only active after specified epoch
            self.do_something(trainer, pl_module)
```

### 多阶段训练回调

```python
class MultiStageTraining(Callback):
    def __init__(self, stage_epochs=[10, 20, 30]):
        self.stage_epochs = stage_epochs
        self.current_stage = 0

    def on_train_epoch_start(self, trainer, pl_module):
        epoch = trainer.current_epoch

        if epoch in self.stage_epochs:
            self.current_stage += 1
            print(f"Entering stage {self.current_stage}")

            # Adjust learning rate for new stage
            for optimizer in trainer.optimizers:
                for param_group in optimizer.param_groups:
                    param_group['lr'] *= 0.1
```
