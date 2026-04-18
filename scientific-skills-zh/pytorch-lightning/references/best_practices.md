# 最佳实践 - PyTorch Lightning

## 代码组织

### 1. 与工程分开研究

* *Good:**
```python
class MyModel(L.LightningModule):
    # Research code (what the model does)
    def training_step(self, batch, batch_idx):
        loss = self.compute_loss(batch)
        return loss

# Engineering code (how to train) - in Trainer
trainer = L.Trainer(
    max_epochs=100,
    accelerator="gpu",
    devices=4,
    strategy="ddp"
)
```

* *Bad:**
```python
# Mixing research and engineering logic
class MyModel(L.LightningModule):
    def training_step(self, batch, batch_idx):
        loss = self.compute_loss(batch)

        # Don't do device management manually
        loss = loss.cuda()

        # Don't do optimizer steps manually (unless manual optimization)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss
```

### 2. 使用LightningDataModule

* *好：**
```python
class MyDataModule(L.LightningDataModule):
    def __init__(self, data_dir, batch_size):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size

    def prepare_data(self):
        # Download data once
        download_data(self.data_dir)

    def setup(self, stage):
        # Load data per-process
        self.train_dataset = MyDataset(self.data_dir, split='train')
        self.val_dataset = MyDataset(self.data_dir, split='val')

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

# Reusable and shareable
dm = MyDataModule("./data", batch_size=32)
trainer.fit(model, datamodule=dm)
```

* *差：**
```python
# Scattered data logic
train_dataset = load_data()
val_dataset = load_data()
train_loader = DataLoader(train_dataset, ...)
val_loader = DataLoader(val_dataset, ...)
trainer.fit(model, train_loader, val_loader)
```

### 3.保持模型模块化

```python
class Encoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(...)

    def forward(self, x):
        return self.layers(x)

class Decoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(...)

    def forward(self, x):
        return self.layers(x)

class MyModel(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.encoder = Encoder()
        self.decoder = Decoder()

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)
```

## 设备不可知论

### 1. 切勿使用显式 CUDA 调用

* *坏：**
```python
x = x.cuda()
model = model.cuda()
torch.cuda.set_device(0)
```

* *好：**
```python
# Inside LightningModule
x = x.to(self.device)

# Or let Lightning handle it automatically
def training_step(self, batch, batch_idx):
    x, y = batch  # Already on correct device
    return loss
```

### 2. 使用 `self.device`属性

```python
class MyModel(L.LightningModule):
    def training_step(self, batch, batch_idx):
        # Create tensors on correct device
        noise = torch.randn(batch.size(0), 100).to(self.device)

        # Or use type_as
        noise = torch.randn(batch.size(0), 100).type_as(batch)
```

### 3.非参数的注册缓冲区

```python
class MyModel(L.LightningModule):
    def __init__(self):
        super().__init__()
        # Register buffers (automatically moved to correct device)
        self.register_buffer("running_mean", torch.zeros(100))

    def forward(self, x):
        # self.running_mean is automatically on correct device
        return x - self.running_mean
```

## 超参数管理

### 1.始终使用`save_hyperparameters()`

* *好：**
```python
class MyModel(L.LightningModule):
    def __init__(self, learning_rate, hidden_dim, dropout):
        super().__init__()
        self.save_hyperparameters()  # Saves all arguments

        # Access via self.hparams
        self.model = nn.Linear(self.hparams.hidden_dim, 10)

# Load from checkpoint with saved hparams
model = MyModel.load_from_checkpoint("checkpoint.ckpt")
print(model.hparams.learning_rate)  # Original value preserved
```

* *差：**
```python
class MyModel(L.LightningModule):
    def __init__(self, learning_rate, hidden_dim, dropout):
        super().__init__()
        self.learning_rate = learning_rate  # Manual tracking
        self.hidden_dim = hidden_dim
```

### 2. 忽略特定Arguments

```python
class MyModel(L.LightningModule):
    def __init__(self, lr, model, dataset):
        super().__init__()
        # Don't save 'model' and 'dataset' (not serializable)
        self.save_hyperparameters(ignore=['model', 'dataset'])

        self.model = model
        self.dataset = dataset
```

### 3. 在 `configure_optimizers()`

```python
def configure_optimizers(self):
    # Use saved hyperparameters
    optimizer = torch.optim.Adam(
        self.parameters(),
        lr=self.hparams.learning_rate,
        weight_decay=self.hparams.weight_decay
    )
    return optimizer
```

## 记录最佳实践

### 1. 记录步骤和纪元中的超参数指标

```python
def training_step(self, batch, batch_idx):
    loss = self.compute_loss(batch)

    # Log per-step for detailed monitoring
    # Log per-epoch for aggregated view
    self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)

    return loss
```

### 2. 使用结构化日志记录

```python
def training_step(self, batch, batch_idx):
    # Organize with prefixes
    self.log("train/loss", loss)
    self.log("train/acc", acc)
    self.log("train/f1", f1)

def validation_step(self, batch, batch_idx):
    self.log("val/loss", loss)
    self.log("val/acc", acc)
    self.log("val/f1", f1)
```

### 3. 同步分布式训练中的指标

```python
def validation_step(self, batch, batch_idx):
    loss = self.compute_loss(batch)

    # IMPORTANT: sync_dist=True for proper aggregation across GPUs
    self.log("val_loss", loss, sync_dist=True)
```

### 4. 监控学习率

```python
from lightning.pytorch.callbacks import LearningRateMonitor

trainer = L.Trainer(
    callbacks=[LearningRateMonitor(logging_interval="step")]
)
```

## 再现性

### 1. 播种一切

```python
import lightning as L

# Set seed for reproducibility
L.seed_everything(42, workers=True)

trainer = L.Trainer(
    deterministic=True,  # Use deterministic algorithms
    benchmark=False      # Disable cudnn benchmarking
)
```

### 2. 避免非确定性操作

```python
# Bad: Non-deterministic
torch.use_deterministic_algorithms(False)

# Good: Deterministic
torch.use_deterministic_algorithms(True)
```

### 3.记录随机状态

```python
def on_save_checkpoint(self, checkpoint):
    # Save random states
    checkpoint['rng_state'] = {
        'torch': torch.get_rng_state(),
        'numpy': np.random.get_state(),
        'python': random.getstate()
    }

def on_load_checkpoint(self, checkpoint):
    # Restore random states
    if 'rng_state' in checkpoint:
        torch.set_rng_state(checkpoint['rng_state']['torch'])
        np.random.set_state(checkpoint['rng_state']['numpy'])
        random.setstate(checkpoint['rng_state']['python'])
```

## 调试

### 1.使用`fast_dev_run`

```python
# Test with 1 batch before full training
trainer = L.Trainer(fast_dev_run=True)
trainer.fit(model, datamodule=dm)
```

### 2. 限制训练数据

```python
# Use only 10% of data for quick iteration
trainer = L.Trainer(
    limit_train_batches=0.1,
    limit_val_batches=0.1
)
```

### 3. 启用异常检测

```python
# Detect NaN/Inf in gradients
trainer = L.Trainer(detect_anomaly=True)
```

### 4. 过拟合小批量上

```python
# Overfit on 10 batches to verify model capacity
trainer = L.Trainer(overfit_batches=10)
```

### 5. 配置文件代码

```python
# Find performance bottlenecks
trainer = L.Trainer(profiler="simple")  # or "advanced"
```

## 内存优化

### 1. 使用混合精度

```python
# FP16/BF16 mixed precision for memory savings and speed
trainer = L.Trainer(
    precision="16-mixed",   # V100, T4
    # or
    precision="bf16-mixed"  # A100, H100
)
```

### 2. 梯度累加

```python
# Simulate larger batch size without memory increase
trainer = L.Trainer(
    accumulate_grad_batches=4  # Accumulate over 4 batches
)
```

### 3. 梯度检查点

```python
class MyModel(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = transformers.AutoModel.from_pretrained("bert-base")

        # Enable gradient checkpointing
        self.model.gradient_checkpointing_enable()
```

### 4. 清除缓存

```python
def on_train_epoch_end(self):
    # Clear collected outputs to free memory
    self.training_step_outputs.clear()

    # Clear CUDA cache if needed
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
```

### 5. 使用高效数据类型

```python
# Use appropriate precision
# FP32 for stability, FP16/BF16 for speed/memory

class MyModel(L.LightningModule):
    def __init__(self):
        super().__init__()
        # Use bfloat16 for better numerical stability than fp16
        self.model = MyTransformer().to(torch.bfloat16)
```

## 训练稳定性

### 1.梯度裁剪

```python
# Prevent gradient explosion
trainer = L.Trainer(
    gradient_clip_val=1.0,
    gradient_clip_algorithm="norm"  # or "value"
)
```

### 2.学习率热身

```python
def configure_optimizers(self):
    optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)

    scheduler = torch.optim.lr_scheduler.OneCycleLR(
        optimizer,
        max_lr=1e-2,
        total_steps=self.trainer.estimated_stepping_batches,
        pct_start=0.1  # 10% warmup
    )

    return {
        "optimizer": optimizer,
        "lr_scheduler": {
            "scheduler": scheduler,
            "interval": "step"
        }
    }
```

### 3. 监控梯度

```python
class MyModel(L.LightningModule):
    def on_after_backward(self):
        # Log gradient norms
        for name, param in self.named_parameters():
            if param.grad is not None:
                self.log(f"grad_norm/{name}", param.grad.norm())
```

### 4. 使用 EarlyStopping

```python
from lightning.pytorch.callbacks import EarlyStopping

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=10,
    mode="min",
    verbose=True
)

trainer = L.Trainer(callbacks=[early_stop])
```

## 检查点

### 1. 保存 Top-K 和 Last

```python
from lightning.pytorch.callbacks import ModelCheckpoint

checkpoint_callback = ModelCheckpoint(
    dirpath="checkpoints/",
    filename="{epoch}-{val_loss:.2f}",
    monitor="val_loss",
    mode="min",
    save_top_k=3,    # Keep best 3
    save_last=True   # Always save last for resuming
)

trainer = L.Trainer(callbacks=[checkpoint_callback])
```

### 2. 恢复训练

```python
# Resume from last checkpoint
trainer.fit(model, datamodule=dm, ckpt_path="last.ckpt")

# Resume from specific checkpoint
trainer.fit(model, datamodule=dm, ckpt_path="epoch=10-val_loss=0.23.ckpt")
```

### 3. 自定义检查点状态

```python
def on_save_checkpoint(self, checkpoint):
    # Add custom state
    checkpoint['custom_data'] = self.custom_data
    checkpoint['epoch_metrics'] = self.metrics

def on_load_checkpoint(self, checkpoint):
    # Restore custom state
    self.custom_data = checkpoint.get('custom_data', {})
    self.metrics = checkpoint.get('epoch_metrics', [])
```

## 测试

### 1. 单独训练和测试

```python
# Train
trainer = L.Trainer(max_epochs=100)
trainer.fit(model, datamodule=dm)

# Test ONLY ONCE before publishing
trainer.test(model, datamodule=dm)
```

### 2. 使用模型选择验证

```python
# Use validation for hyperparameter tuning
checkpoint_callback = ModelCheckpoint(monitor="val_loss", mode="min")
trainer = L.Trainer(callbacks=[checkpoint_callback])
trainer.fit(model, datamodule=dm)

# Load best model
best_model = MyModel.load_from_checkpoint(checkpoint_callback.best_model_path)

# Test only once with best model
trainer.test(best_model, datamodule=dm)
```

## 代码质量

### 1. 类型提示

```python
from typing import Any, Dict, Tuple
import torch
from torch import Tensor

class MyModel(L.LightningModule):
    def training_step(self, batch: Tuple[Tensor, Tensor], batch_idx: int) -> Tensor:
        x, y = batch
        loss = self.compute_loss(x, y)
        return loss

    def configure_optimizers(self) -> Dict[str, Any]:
        optimizer = torch.optim.Adam(self.parameters())
        return {"optimizer": optimizer}
```

### 2. Docstrings

```python
class MyModel(L.LightningModule):
    """
    My awesome model for image classification.

    Args:
        num_classes: Number of output classes
        learning_rate: Learning rate for optimizer
        hidden_dim: Hidden dimension size
    """

    def __init__(self, num_classes: int, learning_rate: float, hidden_dim: int):
        super().__init__()
        self.save_hyperparameters()
```

### 3. 属性方法

```python
class MyModel(L.LightningModule):
    @property
    def learning_rate(self) -> float:
        """Current learning rate."""
        return self.hparams.learning_rate

    @property
    def num_parameters(self) -> int:
        """Total number of parameters."""
        return sum(p.numel() for p in self.parameters())
```

## 常见陷阱

### 1. 忘记返回损失

* *差：**
```python
def training_step(self, batch, batch_idx):
    loss = self.compute_loss(batch)
    self.log("train_loss", loss)
    # FORGOT TO RETURN LOSS!
```

* *好：**
```python
def training_step(self, batch, batch_idx):
    loss = self.compute_loss(batch)
    self.log("train_loss", loss)
    return loss  # MUST return loss
```

### 2. 不同步指标DDP

* *差：**
```python
def validation_step(self, batch, batch_idx):
    self.log("val_acc", acc)  # Wrong value with multi-GPU!
```

* *好：**
```python
def validation_step(self, batch, batch_idx):
    self.log("val_acc", acc, sync_dist=True)  # Correct aggregation
```

### 3. 手动设备管理

* *差：**
```python
def training_step(self, batch, batch_idx):
    x = x.cuda()  # Don't do this
    y = y.cuda()
```

* *好：**
```python
def training_step(self, batch, batch_idx):
    # Lightning handles device placement
    x, y = batch  # Already on correct device
```

### 4. 不使用`self.log()`

* *差：**
```python
def training_step(self, batch, batch_idx):
    loss = self.compute_loss(batch)
    self.training_losses.append(loss)  # Manual tracking
    return loss
```

* *好：**
```python
def training_step(self, batch, batch_idx):
    loss = self.compute_loss(batch)
    self.log("train_loss", loss)  # Automatic logging
    return loss
```

### 5.修改批次In-Place

* *差：**
```python
def training_step(self, batch, batch_idx):
    x, y = batch
    x[:] = self.augment(x)  # In-place modification can cause issues
```

* *好：**
```python
def training_step(self, batch, batch_idx):
    x, y = batch
    x = self.augment(x)  # Create new tensor
```

## 性能提示

### 1. 使用 DataLoader Workers

```python
def train_dataloader(self):
    return DataLoader(
        self.train_dataset,
        batch_size=32,
        num_workers=4,           # Use multiple workers
        pin_memory=True,         # Faster GPU transfer
        persistent_workers=True  # Keep workers alive
    )
```

### 2. 启用基准模式（如果固定输入大小）

```python
trainer = L.Trainer(benchmark=True)
```

### 3. 使用自动批量大小查找

```python
from lightning.pytorch.tuner import Tuner

trainer = L.Trainer()
tuner = Tuner(trainer)

# Find optimal batch size
tuner.scale_batch_size(model, datamodule=dm, mode="power")

# Then train
trainer.fit(model, datamodule=dm)
```

### 4.优化数据加载

```python
# Use faster image decoding
import torch
import torchvision.transforms as T

transforms = T.Compose([
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Use PIL-SIMD for faster image loading
# pip install pillow-simd
```
