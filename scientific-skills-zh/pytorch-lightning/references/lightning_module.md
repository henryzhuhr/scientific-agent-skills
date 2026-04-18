# LightningModule - 综合指南

## 概述

A `LightningModule` 将 PyTorch 代码组织成六个没有抽象的逻辑部分。代码仍然是纯粹的 PyTorch，只是组织得更好。 Trainer 处理设备管理、分布式采样和基础设施，同时保留完整的模型控制。

## 核心结构

```python
import lightning as L
import torch
import torch.nn.functional as F

class MyModel(L.LightningModule):
    def __init__(self, learning_rate=0.001):
        super().__init__()
        self.save_hyperparameters()  # Save init arguments
        self.model = YourNeuralNetwork()

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self.model(x)
        loss = F.cross_entropy(logits, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self.model(x)
        loss = F.cross_entropy(logits, y)
        acc = (logits.argmax(dim=1) == y).float().mean()
        self.log("val_loss", loss)
        self.log("val_acc", acc)

    def test_step(self, batch, batch_idx):
        x, y = batch
        logits = self.model(x)
        loss = F.cross_entropy(logits, y)
        acc = (logits.argmax(dim=1) == y).float().mean()
        self.log("test_loss", loss)
        self.log("test_acc", acc)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.hparams.learning_rate)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min')
        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": scheduler,
                "monitor": "val_loss"
            }
        }
```

## 基本方法

#### 训练管道方法

#### `training_step(batch, batch_idx)`
计算前向传递并返回损失。 Lightning 在自动优化模式下自动处理反向传播和优化器更新。

* *参数：**
- `batch` - 来自 DataLoader 的当前训练批次
- `batch_idx` - 当前批次的索引

* *返回：** 损失张量（标量）或带有“loss”的字典key

* *示例：**
```python
def training_step(self, batch, batch_idx):
    x, y = batch
    y_hat = self.model(x)
    loss = F.mse_loss(y_hat, y)

    # Log training metrics
    self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
    self.log("learning_rate", self.optimizers().param_groups[0]['lr'])

    return loss
```

#### `validation_step(batch, batch_idx)`
E根据验证数据评估模型。自动在禁用梯度和模型评估模式下运行。

* *参数：**
- `batch` - 当前验证批次
- `batch_idx` - 当前批次的索引

  * *返回：** 可选 - 损失或字典指标

* *示例：**
```python
def validation_step(self, batch, batch_idx):
    x, y = batch
    y_hat = self.model(x)
    loss = F.mse_loss(y_hat, y)

    # Lightning aggregates across validation batches automatically
    self.log("val_loss", loss, prog_bar=True)
    return loss
```

#### `test_step(batch, batch_idx)`
E根据测试数据评估模型。仅在使用 `trainer.test()` 显式调用时运行。训练完成后使用，通常在发布前使用。

* *参数：**
- `batch` - 当前测试批次
- `batch_idx` - 当前批次的索引

  * *返回：** 可选 - 损失或度量字典

#### `predict_step(batch, batch_idx, dataloader_idx=0)`
对数据运行推理。使用`trainer.predict()`.

时调用**参数：**
- `batch` - 当前批次
- `batch_idx` - 当前批次的索引
- `dataloader_idx` - 数据加载器的索引（如果多个）

* *返回：**预测（您需要的任何格式）

* *示例：**
```python
def predict_step(self, batch, batch_idx):
    x, y = batch
    return self.model(x)  # Return raw predictions
```

### 配置方法

#### `configure_optimizers()`
返回优化器和可选的学习率调度器。

* *返回格式：**

1. **单个优化器：**
```python
def configure_optimizers(self):
    return torch.optim.Adam(self.parameters(), lr=0.001)
```

2. **优化器+调度器：**
```python
def configure_optimizers(self):
    optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10)
    return [optimizer], [scheduler]
```

3. **具有调度程序监控的高级配置：**
```python
def configure_optimizers(self):
    optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer)
    return {
        "optimizer": optimizer,
        "lr_scheduler": {
            "scheduler": scheduler,
            "monitor": "val_loss",  # Metric to monitor
            "interval": "epoch",     # When to update (epoch/step)
            "frequency": 1,          # How often to update
            "strict": True           # Crash if monitored metric not found
        }
    }
```

4. **多个优化器（针对GAN等）：**
```python
def configure_optimizers(self):
    opt_g = torch.optim.Adam(self.generator.parameters(), lr=0.0002)
    opt_d = torch.optim.Adam(self.discriminator.parameters(), lr=0.0002)
    return [opt_g, opt_d]
```

#### `forward(*args, **kwargs)`
标准PyTorch前向方法。用于推理或作为训练步骤的一部分。

* *示例：**
```python
def forward(self, x):
    return self.model(x)

def training_step(self, batch, batch_idx):
    x, y = batch
    y_hat = self(x)  # Uses forward()
    return F.mse_loss(y_hat, y)
```

### 日志记录和指标

#### `log(name, value, **kwargs)`
记录指标，并自动减少纪元级别devices.

* *关键参数：**
- `name` - 指标名称（字符串）
- `value` - 指标值（张量或数字）
- `on_step` - 在当前步骤记录（默认值：training_step 中为 True，False否则）
- `on_epoch` - 在纪元结束时记录（默认：training_step 中为 False，否则为 True）
- `prog_bar` - 在进度条中显示（默认：False）
- `logger` - 发送到记录器后端（默认：True）
- `reduce_fx` - 归约函数：“mean”、“sum”、“max”、“min”（默认值：“mean”）
- `sync_dist` - 分布式训练中跨设备同步（默认值：False）

* *示例：**
```python
# Simple logging
self.log("train_loss", loss)

# Display in progress bar
self.log("accuracy", acc, prog_bar=True)

# Log per-step and per-epoch
self.log("loss", loss, on_step=True, on_epoch=True)

# Custom reduction for distributed training
self.log("batch_size", batch.size(0), reduce_fx="sum", sync_dist=True)
```

#### `log_dict(dictionary, **kwargs)`
同时记录多个指标。

* *示例：**
```python
metrics = {"train_loss": loss, "train_acc": acc, "learning_rate": lr}
self.log_dict(metrics, on_step=True, on_epoch=True)
```

#### `save_hyperparameters(*args, **kwargs)`
存储用于再现性和检查点恢复的初始化参数。调用`__init__()`.

* *示例：**
```python
def __init__(self, learning_rate, hidden_dim, dropout):
    super().__init__()
    self.save_hyperparameters()  # Saves all init args
    # Access via self.hparams.learning_rate, self.hparams.hidden_dim, etc.
```

## 关键属性

|物业 |描述 |
|----------|--------------|
| `self.current_epoch` |当前纪元号（0索引）|
| `self.global_step` |跨所有时期的总优化器步骤|
| `self.device` |当前设备（cuda:0、cpu等）|
| `self.global_rank` |分布式训练中的进程排名（0为主）|
| `self.local_rank` |当前节点上的 GPU 排名 |
| `self.hparams` |保存的超参数（通过 save_hyperparameters）|
| `self.trainer` |引用父 Trainer 实例 |
| `self.automatic_optimization` |是否使用自动优化（默认：True）|

## 手动优化

对于高级用例（GAN、强化学习、多个优化器），禁用自动优化：

```python
class GANModel(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.automatic_optimization = False
        self.generator = Generator()
        self.discriminator = Discriminator()

    def training_step(self, batch, batch_idx):
        opt_g, opt_d = self.optimizers()

        # Train generator
        opt_g.zero_grad()
        g_loss = self.compute_generator_loss(batch)
        self.manual_backward(g_loss)
        opt_g.step()

        # Train discriminator
        opt_d.zero_grad()
        d_loss = self.compute_discriminator_loss(batch)
        self.manual_backward(d_loss)
        opt_d.step()

        self.log_dict({"g_loss": g_loss, "d_loss": d_loss})

    def configure_optimizers(self):
        opt_g = torch.optim.Adam(self.generator.parameters(), lr=0.0002)
        opt_d = torch.optim.Adam(self.discriminator.parameters(), lr=0.0002)
        return [opt_g, opt_d]
```

## 重要的生命周期挂钩

### 设置和拆卸

#### `setup(stage)`
在拟合、验证、测试或预测开始时调用。对于特定于阶段的设置很有用。

* *参数：**
- `stage` - 'fit'、'validate'、'test' 或 'predict'

* *示例：**
```python
def setup(self, stage):
    if stage == 'fit':
        # Setup training-specific components
        self.train_dataset = load_train_data()
    elif stage == 'test':
        # Setup test-specific components
        self.test_dataset = load_test_data()
```

#### `teardown(stage)`
在拟合、验证、测试或预测结束时调用。清理资源。

### Epoch Boundaries

#### `on_train_epoch_start()` / `on_train_epoch_end()`
在每次训练开始/结束时调用epoch.

* *示例：**
```python
def on_train_epoch_end(self):
    # Compute epoch-level metrics
    all_preds = torch.cat(self.training_step_outputs)
    epoch_metric = compute_custom_metric(all_preds)
    self.log("epoch_metric", epoch_metric)
    self.training_step_outputs.clear()  # Free memory
```

#### `on_validation_epoch_start()` / `on_validation_epoch_end()`
在验证 epoch 开始/结束时调用。

#### `on_test_epoch_start()` / `on_test_epoch_end()`
在测试时期的开始/结束时调用。

### 渐变钩子

#### `on_before_backward(loss)`
在loss.backward()之前调用。

#### `on_after_backward()`
在loss.backward()之后但在优化器步骤之前调用。

* *示例-梯度检查：**
```python
def on_after_backward(self):
    # Log gradient norms
    grad_norm = torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)
    self.log("grad_norm", grad_norm)
```

### 检查点挂钩

#### `on_save_checkpoint(checkpoint)`
自定义检查点保存。添加额外状态保存。

* *示例：**
```python
def on_save_checkpoint(self, checkpoint):
    checkpoint['custom_state'] = self.custom_data
```

#### `on_load_checkpoint(checkpoint)`
自定义检查点加载。恢复额外状态。

* *示例：**
```python
def on_load_checkpoint(self, checkpoint):
    self.custom_data = checkpoint.get('custom_state', default_value)
```

## 最佳实践

### 1. 设备无关
切勿使用显式 `.cuda()` 或 `.cpu()` 调用。 Lightning 自动处理设备放置。

* *差：**
```python
x = x.cuda()
model = model.cuda()
```

* *好：**
```python
x = x.to(self.device)  # Inside LightningModule
# Or let Lightning handle it automatically
```

### 2. 分布式训练安全
不要手动创建 `DistributedSampler`。 Lightning 会自动处理此问题。

* *Bad:**
```python
sampler = DistributedSampler(dataset)
DataLoader(dataset, sampler=sampler)
```

* *Good:**
```python
DataLoader(dataset, shuffle=True)  # Lightning converts to DistributedSampler
```

### 3. 指标聚合
使用 `self.log()` 进行自动跨设备缩减，而不是手动采集。

* *Bad:**
```python
self.validation_outputs.append(loss)

def on_validation_epoch_end(self):
    avg_loss = torch.stack(self.validation_outputs).mean()
```

* *Good:**
```python
self.log("val_loss", loss)  # Automatic aggregation
```

### 4.超参数跟踪
始终使用`self.save_hyperparameters()`以简化模型reloading.

* *示例：**
```python
def __init__(self, learning_rate, hidden_dim):
    super().__init__()
    self.save_hyperparameters()

# Later: Load from checkpoint
model = MyModel.load_from_checkpoint("checkpoint.ckpt")
print(model.hparams.learning_rate)
```

### 5. 验证放置
在单个设备上运行验证，以确保每个样本仅评估一次。 Lightning 通过正确的策略配置自动处理此问题。

## 从检查点加载

```python
# Load model with saved hyperparameters
model = MyModel.load_from_checkpoint("path/to/checkpoint.ckpt")

# Override hyperparameters if needed
model = MyModel.load_from_checkpoint(
    "path/to/checkpoint.ckpt",
    learning_rate=0.0001  # Override saved value
)

# Use for inference
model.eval()
predictions = model(data)
```

## 常见模式

### 梯度累积
让 Lightning 处理梯度累加：

```python
trainer = L.Trainer(accumulate_grad_batches=4)
```

### 梯度裁剪
在训练器中配置：

```python
trainer = L.Trainer(gradient_clip_val=0.5, gradient_clip_algorithm="norm")
```

### 混合精度训练
在训练器中配置精度训练器：

```python
trainer = L.Trainer(precision="16-mixed")  # or "bf16-mixed", "32-true"
```

### 学习率预热
configure_optimizers中实现：

```python
def configure_optimizers(self):
    optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
    scheduler = {
        "scheduler": torch.optim.lr_scheduler.OneCycleLR(
            optimizer,
            max_lr=0.01,
            total_steps=self.trainer.estimated_stepping_batches
        ),
        "interval": "step"
    }
    return [optimizer], [scheduler]
```
