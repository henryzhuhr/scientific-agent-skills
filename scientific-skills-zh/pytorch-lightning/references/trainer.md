# 训练器 - 综合指南

## 概述

训练器在将 PyTorch 代码组织到 LightningModule 中后自动执行训练工作流程。它自动处理循环详细信息、设备管理、回调、梯度操作、检查点和分布式训练。

## 核心目的

训练器管理：
- 自动启用/禁用梯度
- 运行训练、验证和测试数据加载器
- 在适当的时间调用回调
- 将批次放置在正确的位置设备
- 编排分布式训练
- 进度条和日志记录
- 检查点和提前停止

## 主要方法

### `fit(model, train_dataloaders=None, val_dataloaders=None, datamodule=None)`
运行完整的训练例程，包括可选的验证。

* *参数：**
- `model` - 用于训练的 LightningModule
- `train_dataloaders` - 训练数据加载器 
- `val_dataloaders` - 可选验证数据加载器 
- `datamodule` - 可选 LightningDataModule（替换） dataloaders)

* *示例：**
```python
# With DataLoaders
trainer = L.Trainer(max_epochs=10)
trainer.fit(model, train_loader, val_loader)

# With DataModule
trainer.fit(model, datamodule=dm)

# Continue training from checkpoint
trainer.fit(model, train_loader, ckpt_path="checkpoint.ckpt")
```

### `validate(model=None, dataloaders=None, datamodule=None)`
无需训练即可运行验证循环。

* *示例：**
```python
trainer = L.Trainer()
trainer.validate(model, val_loader)
```

### `test(model=None, dataloaders=None, datamodule=None)`
运行测试循环。仅在发布结果前使用。

* *示例：**
```python
trainer = L.Trainer()
trainer.test(model, test_loader)
```

### `predict(model=None, dataloaders=None, datamodule=None)`
对数据运行推理并返回

* *示例：**
```python
trainer = L.Trainer()
predictions = trainer.predict(model, predict_loader)
```

## 基本参数

### 训练持续时间

#### `max_epochs` (int)
训练的最大纪元数。默认值：1000

```python
trainer = L.Trainer(max_epochs=100)
```

#### `min_epochs` (int)
要训练的最小纪元数。默认值：无

```python
trainer = L.Trainer(min_epochs=10, max_epochs=100)
```

#### `max_steps` (int)
优化器步骤的最大数量。覆盖 max_epochs。默认值：-1（无限制）

```python
trainer = L.Trainer(max_steps=10000)
```

#### `max_time`（str或dict）
最大训练时间。对于有时间限制的集群很有用。

```python
# String format
trainer = L.Trainer(max_time="00:12:00:00")  # 12 hours

# Dictionary format
trainer = L.Trainer(max_time={"days": 1, "hours": 6})
```

### 硬件配置

#### `accelerator`（str 或加速器）
使用的硬件：“cpu”、“gpu”、“tpu”、“ipu”、“hpu”、“mps”或“auto”。默认值：“auto”

```python
trainer = L.Trainer(accelerator="gpu")
trainer = L.Trainer(accelerator="auto")  # Auto-detect available hardware
```

#### `devices`（int、list 或 str）
要使用的设备索引的数量或列表。

```python
# Use 2 GPUs
trainer = L.Trainer(devices=2, accelerator="gpu")

# Use specific GPUs
trainer = L.Trainer(devices=[0, 2], accelerator="gpu")

# Use all available devices
trainer = L.Trainer(devices="auto", accelerator="gpu")

# CPU with 4 cores
trainer = L.Trainer(devices=4, accelerator="cpu")
```

#### `strategy`（str 或策略）
分布式训练策略：“ddp”、“ddp_spawn”、“fsdp”、“deepspeed”等默认：“auto” 

```python
# Data Distributed Parallel
trainer = L.Trainer(strategy="ddp", accelerator="gpu", devices=4)

# Fully Sharded Data Parallel
trainer = L.Trainer(strategy="fsdp", accelerator="gpu", devices=4)

# DeepSpeed
trainer = L.Trainer(strategy="deepspeed_stage_2", accelerator="gpu", devices=4)
```

#### `precision`（str或int）
浮点精度：“32-true”， “16-mixed”、“bf16-mixed”、“64-true”等

```python
# Mixed precision (FP16)
trainer = L.Trainer(precision="16-mixed")

# BFloat16 mixed precision
trainer = L.Trainer(precision="bf16-mixed")

# Full precision
trainer = L.Trainer(precision="32-true")
```

### 优化配置

#### `gradient_clip_val`（float）
梯度裁剪值。默认值：无

```python
# Clip gradients by norm
trainer = L.Trainer(gradient_clip_val=0.5)
```

#### `gradient_clip_algorithm` (str)
梯度裁剪算法：“范数”或“值”。默认值：“norm”

```python
trainer = L.Trainer(gradient_clip_val=0.5, gradient_clip_algorithm="norm")
```

#### `accumulate_grad_batches`（int或dict）
在优化器步骤之前累积N批梯度。

```python
# Accumulate over 4 batches
trainer = L.Trainer(accumulate_grad_batches=4)

# Different accumulation per epoch
trainer = L.Trainer(accumulate_grad_batches={0: 4, 5: 2, 10: 1})
```

### 验证配置

#### `check_val_every_n_epoch` (int)
每N个时期运行验证。默认值：1

```python
trainer = L.Trainer(check_val_every_n_epoch=10)
```

#### `val_check_interval`（整数或浮点）
在训练时期内检查验证的频率。

```python
# Check validation every 0.25 of training epoch
trainer = L.Trainer(val_check_interval=0.25)

# Check validation every 100 training batches
trainer = L.Trainer(val_check_interval=100)
```

#### `limit_val_batches`（整数或float)
限制验证批次。

```python
# Use only 10% of validation data
trainer = L.Trainer(limit_val_batches=0.1)

# Use only 50 validation batches
trainer = L.Trainer(limit_val_batches=50)

# Disable validation
trainer = L.Trainer(limit_val_batches=0)
```

#### `num_sanity_val_steps` (int)
在训练开始之前运行的验证批次数。默认值：2

```python
# Skip sanity check
trainer = L.Trainer(num_sanity_val_steps=0)

# Run 5 sanity validation steps
trainer = L.Trainer(num_sanity_val_steps=5)
```

### 日志记录和进度

#### `logger`（记录器或列表或布尔）
用于实验的记录器Tracking.

```python
from lightning.pytorch import loggers as pl_loggers

# TensorBoard logger
tb_logger = pl_loggers.TensorBoardLogger("logs/")
trainer = L.Trainer(logger=tb_logger)

# Multiple loggers
wandb_logger = pl_loggers.WandbLogger(project="my-project")
trainer = L.Trainer(logger=[tb_logger, wandb_logger])

# Disable logging
trainer = L.Trainer(logger=False)
```

#### `log_every_n_steps` (int)
在训练步骤中登录的频率。默认值：50

```python
trainer = L.Trainer(log_every_n_steps=10)
```

#### `enable_progress_bar` (bool)
显示进度条。默认值：True

```python
trainer = L.Trainer(enable_progress_bar=False)
```

### Callbacks

#### `callbacks`（列表）
训练期间使用的回调列表。

```python
from lightning.pytorch.callbacks import ModelCheckpoint, EarlyStopping

checkpoint_callback = ModelCheckpoint(
    monitor="val_loss",
    save_top_k=3,
    mode="min"
)

early_stop_callback = EarlyStopping(
    monitor="val_loss",
    patience=5,
    mode="min"
)

trainer = L.Trainer(callbacks=[checkpoint_callback, early_stop_callback])
```

### 检查点

#### `default_root_dir` (str)
日志和检查点的默认目录。默认值：当前工作目录

```python
trainer = L.Trainer(default_root_dir="./experiments/")
```

#### `enable_checkpointing` (bool)
启用自动检查点。默认值：True

```python
trainer = L.Trainer(enable_checkpointing=True)
```

### 调试

#### `fast_dev_run`（bool 或 int）
通过 train/val/test 运行单个批次（或 N 个批次）进行调试。

```python
# Run 1 batch of train/val/test
trainer = L.Trainer(fast_dev_run=True)

# Run 5 batches of train/val/test
trainer = L.Trainer(fast_dev_run=5)
```

#### `limit_train_batches`（int或float）
限制训练批次。

```python
# Use only 25% of training data
trainer = L.Trainer(limit_train_batches=0.25)

# Use only 100 training batches
trainer = L.Trainer(limit_train_batches=100)
```

#### `limit_test_batches`（int或float）
限制测试批次。

```python
trainer = L.Trainer(limit_test_batches=0.5)
```

#### `overfit_batches`（int 或 float）
对数据子集进行过拟合以进行调试。

```python
# Overfit on 10 batches
trainer = L.Trainer(overfit_batches=10)

# Overfit on 1% of data
trainer = L.Trainer(overfit_batches=0.01)
```

#### `detect_anomaly`（bool）
启用 PyTorch 异常检测以调试 NaN。默认值：False

```python
trainer = L.Trainer(detect_anomaly=True)
```

### 再现性

#### `deterministic`（bool 或 str）
控制确定性行为。默认值：False

```python
import lightning as L

# Seed everything
L.seed_everything(42, workers=True)

# Fully deterministic (may impact performance)
trainer = L.Trainer(deterministic=True)

# Warn if non-deterministic operations detected
trainer = L.Trainer(deterministic="warn")
```

#### `benchmark` (bool)
启用 cudnn 性能基准测试。默认值：False

```python
trainer = L.Trainer(benchmark=True)
```

### Miscellaneous

#### `enable_model_summary` (bool)
在训练前打印模型摘要。默认值：True

```python
trainer = L.Trainer(enable_model_summary=False)
```

#### `inference_mode` (bool)
使用 torch.inference_mode()而不是 torch.no_grad()进行验证/测试。默认值：True

```python
trainer = L.Trainer(inference_mode=True)
```

#### `profiler`（str 或 Profiler）
用于性能优化的配置文件代码。选项：“简单”、“高级”或自定义 Profiler。

```python
# Simple profiler
trainer = L.Trainer(profiler="simple")

# Advanced profiler
trainer = L.Trainer(profiler="advanced")
```

## 常用配置

### 基础训练
```python
trainer = L.Trainer(
    max_epochs=100,
    accelerator="auto",
    devices="auto"
)
trainer.fit(model, train_loader, val_loader)
```

### 多 GPU培训
```python
trainer = L.Trainer(
    max_epochs=100,
    accelerator="gpu",
    devices=4,
    strategy="ddp",
    precision="16-mixed"
)
trainer.fit(model, datamodule=dm)
```

### 带检查点的生产培训
```python
from lightning.pytorch.callbacks import ModelCheckpoint, EarlyStopping, LearningRateMonitor

checkpoint_callback = ModelCheckpoint(
    dirpath="checkpoints/",
    filename="{epoch}-{val_loss:.2f}",
    monitor="val_loss",
    mode="min",
    save_top_k=3,
    save_last=True
)

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=10,
    mode="min"
)

lr_monitor = LearningRateMonitor(logging_interval="step")

trainer = L.Trainer(
    max_epochs=100,
    accelerator="gpu",
    devices=2,
    strategy="ddp",
    precision="16-mixed",
    callbacks=[checkpoint_callback, early_stop, lr_monitor],
    log_every_n_steps=10,
    gradient_clip_val=1.0
)

trainer.fit(model, datamodule=dm)
```

### 调试配置
```python
trainer = L.Trainer(
    fast_dev_run=True,          # Run 1 batch
    accelerator="cpu",
    enable_progress_bar=True,
    log_every_n_steps=1,
    detect_anomaly=True
)
trainer.fit(model, train_loader, val_loader)
```

### 研究配置（重现性）
```python
import lightning as L

L.seed_everything(42, workers=True)

trainer = L.Trainer(
    max_epochs=100,
    accelerator="gpu",
    devices=1,
    deterministic=True,
    benchmark=False,
    precision="32-true"
)
trainer.fit(model, datamodule=dm)
```

### 限时训练（集群）
```python
trainer = L.Trainer(
    max_time={"hours": 23, "minutes": 30},  # SLURM time limit
    max_epochs=1000,
    callbacks=[ModelCheckpoint(save_last=True)]
)
trainer.fit(model, datamodule=dm)

# Resume from checkpoint
trainer.fit(model, datamodule=dm, ckpt_path="last.ckpt")
```

### 大模型训练（FSDP）
```python
from lightning.pytorch.strategies import FSDPStrategy

trainer = L.Trainer(
    max_epochs=100,
    accelerator="gpu",
    devices=8,
    strategy=FSDPStrategy(
        activation_checkpointing_policy={nn.TransformerEncoderLayer},
        cpu_offload=False
    ),
    precision="bf16-mixed",
    accumulate_grad_batches=4
)
trainer.fit(model, datamodule=dm)
```

## 恢复中训练

### 来自检查点
```python
# Resume from specific checkpoint
trainer.fit(model, datamodule=dm, ckpt_path="epoch=10-val_loss=0.23.ckpt")

# Resume from last checkpoint
trainer.fit(model, datamodule=dm, ckpt_path="last.ckpt")
```

### 查找最后一个检查点
```python
from lightning.pytorch.callbacks import ModelCheckpoint

checkpoint_callback = ModelCheckpoint(save_last=True)
trainer = L.Trainer(callbacks=[checkpoint_callback])
trainer.fit(model, datamodule=dm)

# Get path to last checkpoint
last_checkpoint = checkpoint_callback.last_model_path
```

## 从LightningModule访问Trainer

在LightningModule中，通过以下方式访问Trainer `self.trainer`:

```python
class MyModel(L.LightningModule):
    def training_step(self, batch, batch_idx):
        # Access trainer properties
        current_epoch = self.trainer.current_epoch
        global_step = self.trainer.global_step
        max_epochs = self.trainer.max_epochs

        # Access callbacks
        for callback in self.trainer.callbacks:
            if isinstance(callback, ModelCheckpoint):
                print(f"Best model: {callback.best_model_path}")

        # Access logger
        self.trainer.logger.log_metrics({"custom": value})
```

## 训练师属性

|属性 |描述|
|-----------|--------------|
| `trainer.current_epoch` |当前纪元（0索引）|
| `trainer.global_step` |优化器总步骤|
| `trainer.max_epochs` |配置的最大纪元 |
| `trainer.max_steps` |配置的最大步数|
| `trainer.callbacks` |回调列表|
| `trainer.logger` |记录器实例|
| `trainer.strategy` |训练策略|
| `trainer.estimated_stepping_batches` |预计训练总步骤 |

## 最佳实践

### 1. 从 Fast Dev Run 开始
在完整训练之前始终使用 `fast_dev_run=True` 进行测试：

```python
trainer = L.Trainer(fast_dev_run=True)
trainer.fit(model, datamodule=dm)
```

### 2. 使用渐变裁剪
防止渐变爆炸：

```python
trainer = L.Trainer(gradient_clip_val=1.0, gradient_clip_algorithm="norm")
```

### 3.启用混合精度
加快现代GPU上的训练：

```python
trainer = L.Trainer(precision="16-mixed")  # or "bf16-mixed" for A100+
```

### 4.正确保存检查点
始终保存最后一个检查点resuming:

```python
checkpoint_callback = ModelCheckpoint(
    save_top_k=3,
    save_last=True,
    monitor="val_loss"
)
```

### 5. 监控学习率
用 LearningRate跟踪 LR 变化监控:

```python
from lightning.pytorch.callbacks import LearningRateMonitor

trainer = L.Trainer(callbacks=[LearningRateMonitor(logging_interval="step")])
```

### 6. 使用 DataModule 实现复现性
封装数据逻辑在 DataModule 中：

```python
# Better than passing DataLoaders directly
trainer.fit(model, datamodule=dm)
```

### 7. 设置研究的确定性
确保出版物的可重复性：

```python
L.seed_everything(42, workers=True)
trainer = L.Trainer(deterministic=True)
```
