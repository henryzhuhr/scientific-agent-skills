# 日志记录 - 综合指南

## 概述

PyTorch Lightning 支持多种日志记录集成，用于实验跟踪和可视化。默认情况下，Lightning 使用 TensorBoard，但您可以轻松切换或组合多个记录器。

## 支持的记录器

### TensorBoardLogger（默认）

记录到 TensorBoard 中的本地或远程文件系统格式.

* *安装：**
```bash
pip install tensorboard
```

* *使用：**
```python
from lightning.pytorch import loggers as pl_loggers

tb_logger = pl_loggers.TensorBoardLogger(
    save_dir="logs/",
    name="my_model",
    version="version_1",
    default_hp_metric=False
)

trainer = L.Trainer(logger=tb_logger)
```

* *查看日志：**
```bash
tensorboard --logdir logs/
```

### WandbLogger

基于云的实验跟踪的权重和偏差集成。

* *安装：**
```bash
pip install wandb
```

* *用法：**
```python
from lightning.pytorch import loggers as pl_loggers

wandb_logger = pl_loggers.WandbLogger(
    project="my-project",
    name="experiment-1",
    save_dir="logs/",
    log_model=True  # Log model checkpoints to W&B
)

trainer = L.Trainer(logger=wandb_logger)
```

* *功能：**
- 基于云的实验跟踪
- 模型版本控制
- 工件管理
- 协作功能
- 超参数扫描

### MLFlowLogger

ML 流跟踪集成.

* *安装：**
```bash
pip install mlflow
```

* *使用：**
```python
from lightning.pytorch import loggers as pl_loggers

mlflow_logger = pl_loggers.MLFlowLogger(
    experiment_name="my_experiment",
    tracking_uri="http://localhost:5000",
    run_name="run_1"
)

trainer = L.Trainer(logger=mlflow_logger)
```

### CometLogger

Comet.ml实验跟踪.

* *安装：**
```bash
pip install comet-ml
```

* *使用：**
```python
from lightning.pytorch import loggers as pl_loggers

comet_logger = pl_loggers.CometLogger(
    api_key="YOUR_API_KEY",
    project_name="my-project",
    experiment_name="experiment-1"
)

trainer = L.Trainer(logger=comet_logger)
```

### NeptuneLogger

Neptune.ai Integration.

* *安装：**
```bash
pip install neptune
```

* *用法：**
```python
from lightning.pytorch import loggers as pl_loggers

neptune_logger = pl_loggers.NeptuneLogger(
    api_key="YOUR_API_KEY",
    project="username/project-name",
    name="experiment-1"
)

trainer = L.Trainer(logger=neptune_logger)
```

### CSVLogger

以 YAML 和 CSV 格式记录到本地文件系统格式.

* *用法：**
```python
from lightning.pytorch import loggers as pl_loggers

csv_logger = pl_loggers.CSVLogger(
    save_dir="logs/",
    name="my_model",
    version="1"
)

trainer = L.Trainer(logger=csv_logger)
```

* *输出文件：**
- `metrics.csv` - 所有记录的指标
- `hparams.yaml` - 超参数

## 日志记录指标

### 基本日志记录

在LightningModule中使用`self.log()`：

```python
class MyModel(L.LightningModule):
    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.model(x)
        loss = F.cross_entropy(y_hat, y)

        # Log metric
        self.log("train_loss", loss)

        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.model(x)
        loss = F.cross_entropy(y_hat, y)
        acc = (y_hat.argmax(dim=1) == y).float().mean()

        # Log multiple metrics
        self.log("val_loss", loss)
        self.log("val_acc", acc)
```

### 日志记录参数

#### `on_step`（布尔）
在当前步骤记录。默认值：training_step 中为 True，否则为 False。

```python
self.log("loss", loss, on_step=True)
```

#### `on_epoch` (bool)
在纪元结束时累积并记录。默认值：training_step 中为 False，否则为 True。

```python
self.log("loss", loss, on_epoch=True)
```

#### `prog_bar` (bool)
在进度栏中显示。默认值：False。

```python
self.log("train_loss", loss, prog_bar=True)
```

#### `logger` (bool)
发送到记录器后端。默认值：True.

```python
self.log("internal_metric", value, logger=False)  # Don't log to external logger
```

#### `reduce_fx`（str 或可调用）
归约函数：“mean”、“sum”、“max”、“min”。默认值：“mean”。

```python
self.log("batch_size", batch.size(0), reduce_fx="sum")
```

#### `sync_dist` (bool)
在分布式训练中跨设备同步指标。默认值：False。

```python
self.log("loss", loss, sync_dist=True)
```

#### `rank_zero_only` (bool)
仅从等级 0 进程记录。默认值：False。

```python
self.log("debug_metric", value, rank_zero_only=True)
```

### 完整示例

```python
def training_step(self, batch, batch_idx):
    loss = self.compute_loss(batch)

    # Log per-step and per-epoch, display in progress bar
    self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)

    return loss

def validation_step(self, batch, batch_idx):
    loss = self.compute_loss(batch)
    acc = self.compute_accuracy(batch)

    # Log epoch-level metrics
    self.log("val_loss", loss, on_epoch=True)
    self.log("val_acc", acc, on_epoch=True, prog_bar=True)
```

### 记录多个指标

使用 `log_dict()` 记录多个指标一次：

```python
def training_step(self, batch, batch_idx):
    loss, acc, f1 = self.compute_metrics(batch)

    metrics = {
        "train_loss": loss,
        "train_acc": acc,
        "train_f1": f1
    }

    self.log_dict(metrics, on_step=True, on_epoch=True)

    return loss
```

## 记录超参数

### 自动超参数记录

在模型中使用`save_hyperparameters()`：

```python
class MyModel(L.LightningModule):
    def __init__(self, learning_rate, hidden_dim, dropout):
        super().__init__()
        # Automatically save and log hyperparameters
        self.save_hyperparameters()
```

### 手动超参数记录

```python
# In LightningModule
class MyModel(L.LightningModule):
    def __init__(self, learning_rate):
        super().__init__()
        self.save_hyperparameters()

# Or manually with logger
trainer.logger.log_hyperparams({
    "learning_rate": 0.001,
    "batch_size": 32
})
```

## 记录频率

默认情况下，Lightning 每 50 个训练步骤记录一次。使用 `log_every_n_steps` 进行调整：

```python
trainer = L.Trainer(log_every_n_steps=10)
```

## 多个记录器

同时使用多个记录器：

```python
from lightning.pytorch import loggers as pl_loggers

tb_logger = pl_loggers.TensorBoardLogger("logs/")
wandb_logger = pl_loggers.WandbLogger(project="my-project")
csv_logger = pl_loggers.CSVLogger("logs/")

trainer = L.Trainer(logger=[tb_logger, wandb_logger, csv_logger])
```

## 高级日志记录

### 日志记录图片

```python
import torchvision

def validation_step(self, batch, batch_idx):
    x, y = batch
    y_hat = self.model(x)

    # Log first batch of images once per epoch
    if batch_idx == 0:
        # Create image grid
        grid = torchvision.utils.make_grid(x[:8])

        # Log to TensorBoard
        self.logger.experiment.add_image("val_images", grid, self.current_epoch)

        # Log to Wandb
        if isinstance(self.logger, pl_loggers.WandbLogger):
            import wandb
            self.logger.experiment.log({
                "val_images": [wandb.Image(img) for img in x[:8]]
            })
```

### 记录直方图

```python
def on_train_epoch_end(self):
    # Log parameter histograms
    for name, param in self.named_parameters():
        self.logger.experiment.add_histogram(name, param, self.current_epoch)

        if param.grad is not None:
            self.logger.experiment.add_histogram(
                f"{name}_grad", param.grad, self.current_epoch
            )
```

### 记录模型图

```python
def on_train_start(self):
    # Log model architecture
    sample_input = torch.randn(1, 3, 224, 224).to(self.device)
    self.logger.experiment.add_graph(self.model, sample_input)
```

### 记录自定义绘图

```python
import matplotlib.pyplot as plt

def on_validation_epoch_end(self):
    # Create custom plot
    fig, ax = plt.subplots()
    ax.plot(self.validation_losses)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")

    # Log to TensorBoard
    self.logger.experiment.add_figure("loss_curve", fig, self.current_epoch)

    plt.close(fig)
```

### 记录文本

```python
def validation_step(self, batch, batch_idx):
    # Generate predictions
    predictions = self.generate_text(batch)

    # Log to TensorBoard
    self.logger.experiment.add_text(
        "predictions",
        f"Batch {batch_idx}: {predictions}",
        self.current_epoch
    )
```

### 记录音频

```python
def validation_step(self, batch, batch_idx):
    audio = self.generate_audio(batch)

    # Log to TensorBoard (audio is tensor of shape [1, samples])
    self.logger.experiment.add_audio(
        "generated_audio",
        audio,
        self.current_epoch,
        sample_rate=22050
    )
```

## 访问记录器LightningModule

```python
class MyModel(L.LightningModule):
    def training_step(self, batch, batch_idx):
        # Access logger experiment object
        logger = self.logger.experiment

        # For TensorBoard
        if isinstance(self.logger, pl_loggers.TensorBoardLogger):
            logger.add_scalar("custom_metric", value, self.global_step)

        # For Wandb
        if isinstance(self.logger, pl_loggers.WandbLogger):
            logger.log({"custom_metric": value})

        # For MLflow
        if isinstance(self.logger, pl_loggers.MLFlowLogger):
            logger.log_metric("custom_metric", value)
```

## 自定义记录器

继承`Logger`创建自定义记录器：

```python
from lightning.pytorch.loggers import Logger
from lightning.pytorch.utilities import rank_zero_only

class MyCustomLogger(Logger):
    def __init__(self, save_dir):
        super().__init__()
        self.save_dir = save_dir
        self._name = "my_logger"
        self._version = "0.1"

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @rank_zero_only
    def log_metrics(self, metrics, step):
        # Log metrics to your backend
        print(f"Step {step}: {metrics}")

    @rank_zero_only
    def log_hyperparams(self, params):
        # Log hyperparameters
        print(f"Hyperparameters: {params}")

    @rank_zero_only
    def save(self):
        # Save logger state
        pass

    @rank_zero_only
    def finalize(self, status):
        # Cleanup when training ends
        pass

# Usage
custom_logger = MyCustomLogger(save_dir="logs/")
trainer = L.Trainer(logger=custom_logger)
```

## 最佳实践

### 1. 记录步骤和纪元指标

```python
# Good: Track both granular and aggregate metrics
self.log("train_loss", loss, on_step=True, on_epoch=True)
```

### 2. 对关键指标使用进度条

```python
# Show important metrics in progress bar
self.log("val_acc", acc, prog_bar=True)
```

### 3. 同步分布式训练中的指标

```python
# Ensure correct aggregation across GPUs
self.log("val_loss", loss, sync_dist=True)
```

### 4. 对数学习率

```python
from lightning.pytorch.callbacks import LearningRateMonitor

trainer = L.Trainer(callbacks=[LearningRateMonitor(logging_interval="step")])
```

### 5. 对数梯度范数

```python
def on_after_backward(self):
    # Monitor gradient flow
    grad_norm = torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=float('inf'))
    self.log("grad_norm", grad_norm)
```

### 6. 使用描述性指标名称

```python
# Good: Clear naming convention
self.log("train/loss", loss)
self.log("train/accuracy", acc)
self.log("val/loss", val_loss)
self.log("val/accuracy", val_acc)
```

### 7. 记录超参数

```python
# Always save hyperparameters for reproducibility
class MyModel(L.LightningModule):
    def __init__(self, **kwargs):
        super().__init__()
        self.save_hyperparameters()
```

### 8. 不要过于频繁地记录

```python
# Avoid logging every step for expensive operations
if batch_idx % 100 == 0:
    self.log_images(batch)
```

## 常见模式

### 结构化日志记录

```python
def training_step(self, batch, batch_idx):
    loss, metrics = self.compute_loss_and_metrics(batch)

    # Organize logs with prefixes
    self.log("train/loss", loss)
    self.log_dict({f"train/{k}": v for k, v in metrics.items()})

    return loss

def validation_step(self, batch, batch_idx):
    loss, metrics = self.compute_loss_and_metrics(batch)

    self.log("val/loss", loss)
    self.log_dict({f"val/{k}": v for k, v in metrics.items()})
```

### 条件日志记录

```python
def training_step(self, batch, batch_idx):
    loss = self.compute_loss(batch)

    # Log expensive metrics less frequently
    if self.global_step % 100 == 0:
        expensive_metric = self.compute_expensive_metric(batch)
        self.log("expensive_metric", expensive_metric)

    self.log("train_loss", loss)
    return loss
```

### 多任务日志记录

```python
def training_step(self, batch, batch_idx):
    x, y_task1, y_task2 = batch

    loss_task1 = self.compute_task1_loss(x, y_task1)
    loss_task2 = self.compute_task2_loss(x, y_task2)
    total_loss = loss_task1 + loss_task2

    # Log per-task metrics
    self.log_dict({
        "train/loss_task1": loss_task1,
        "train/loss_task2": loss_task2,
        "train/loss_total": total_loss
    })

    return total_loss
```

## 故障排除

### 公制发现错误

如果调度程序出现“未找到指标”错误：

```python
# Make sure metric is logged with logger=True
self.log("val_loss", loss, logger=True)

# And configure scheduler to monitor it
def configure_optimizers(self):
    optimizer = torch.optim.Adam(self.parameters())
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer)
    return {
        "optimizer": optimizer,
        "lr_scheduler": {
            "scheduler": scheduler,
            "monitor": "val_loss"  # Must match logged metric name
        }
    }
```

### 指标在分布式训练中未同步

```python
# Enable sync_dist for proper aggregation
self.log("val_acc", acc, sync_dist=True)
```

### 记录器未保存

```python
# Ensure logger has write permissions
trainer = L.Trainer(
    logger=pl_loggers.TensorBoardLogger("logs/"),
    default_root_dir="outputs/"  # Ensure directory exists and is writable
)
```
