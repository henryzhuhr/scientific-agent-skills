# LightningDataModule - 综合指南

## 概述

A LightningDataModule 是一个可重用、可共享的类，封装了 PyTorch Lightning 中的所有数据处理步骤。它通过标准化数据集的管理和跨项目共享的方式解决了分散的数据准备逻辑的问题。

## 它解决的核心问题

在传统的PyTorch工作流程中，数据处理分散在多个文件中，因此很难回答以下问题：
- “您使用了哪些分割？”
- “应用了哪些转换？”
- “如何数据准备好了吗？”

DataModules 集中此信息以实现可重复性和可重用性。

## 五个处理步骤

A DataModule 将数据处理组织为五个阶段：

1. **下载/标记化/处理** - 初始数据采集
2. **清理并保存** - 将处理后的数据保存到磁盘
3. **加载到数据集** - 创建 PyTorch 数据集对象
4. **应用转换** - 数据增强、标准化等。
5. **包裹在DataLoader** - 配置批处理和加载

## 主要方法

### `prepare_data()`
下载和处理数据。仅在单个进程上运行一次（未分布式）。

* *用于：**
- 下载数据集
- 标记文本
- 将处理后的数据保存到磁盘

* *重要：**不要在此处设置状态（例如，self.x = y）。状态不会传输到其他进程。

* *示例：**
```python
def prepare_data(self):
    # Download data (runs once)
    download_dataset("http://example.com/data.zip", "data/")

    # Tokenize and save (runs once)
    tokenize_and_save("data/raw/", "data/processed/")
```

### `setup(stage)`
创建数据集并应用转换。在分布式训练中的每个进程上运行。

* *参数：**
- `stage` - 'fit'、'validate'、'test'或'predict'

* *用途：**
- 创建训练/验证/测试分割
- 构建数据集对象
- 应用变换
- 设置状态（self.train_dataset = ...）

* *示例：**
```python
def setup(self, stage):
    if stage == 'fit':
        full_dataset = MyDataset("data/processed/")
        self.train_dataset, self.val_dataset = random_split(
            full_dataset, [0.8, 0.2]
        )

    if stage == 'test':
        self.test_dataset = MyDataset("data/processed/test/")

    if stage == 'predict':
        self.predict_dataset = MyDataset("data/processed/predict/")
```

### `train_dataloader()`
返回训练DataLoader.

* *示例：**
```python
def train_dataloader(self):
    return DataLoader(
        self.train_dataset,
        batch_size=self.batch_size,
        shuffle=True,
        num_workers=self.num_workers,
        pin_memory=True
    )
```

### `val_dataloader()`
返回验证数据加载器。

* *示例：**
```python
def val_dataloader(self):
    return DataLoader(
        self.val_dataset,
        batch_size=self.batch_size,
        shuffle=False,
        num_workers=self.num_workers,
        pin_memory=True
    )
```

### `test_dataloader()`
返回测试DataLoader。

* *示例：**
```python
def test_dataloader(self):
    return DataLoader(
        self.test_dataset,
        batch_size=self.batch_size,
        shuffle=False,
        num_workers=self.num_workers
    )
```

### `predict_dataloader()`
返回预测DataLoader(s).

* *示例：**
```python
def predict_dataloader(self):
    return DataLoader(
        self.predict_dataset,
        batch_size=self.batch_size,
        shuffle=False,
        num_workers=self.num_workers
    )
```

## 完整示例

```python
import lightning as L
from torch.utils.data import DataLoader, Dataset, random_split
import torch

class MyDataset(Dataset):
    def __init__(self, data_path, transform=None):
        self.data_path = data_path
        self.transform = transform
        self.data = self._load_data()

    def _load_data(self):
        # Load your data here
        return torch.randn(1000, 3, 224, 224)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        if self.transform:
            sample = self.transform(sample)
        return sample

class MyDataModule(L.LightningDataModule):
    def __init__(self, data_dir="./data", batch_size=32, num_workers=4):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.num_workers = num_workers

        # Transforms
        self.train_transform = self._get_train_transforms()
        self.test_transform = self._get_test_transforms()

    def _get_train_transforms(self):
        # Define training transforms
        return lambda x: x  # Placeholder

    def _get_test_transforms(self):
        # Define test/val transforms
        return lambda x: x  # Placeholder

    def prepare_data(self):
        # Download data (runs once on single process)
        # download_data(self.data_dir)
        pass

    def setup(self, stage=None):
        # Create datasets (runs on every process)
        if stage == 'fit' or stage is None:
            full_dataset = MyDataset(
                self.data_dir,
                transform=self.train_transform
            )
            train_size = int(0.8 * len(full_dataset))
            val_size = len(full_dataset) - train_size
            self.train_dataset, self.val_dataset = random_split(
                full_dataset, [train_size, val_size]
            )

        if stage == 'test' or stage is None:
            self.test_dataset = MyDataset(
                self.data_dir,
                transform=self.test_transform
            )

        if stage == 'predict':
            self.predict_dataset = MyDataset(
                self.data_dir,
                transform=self.test_transform
            )

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            pin_memory=True,
            persistent_workers=True if self.num_workers > 0 else False
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True,
            persistent_workers=True if self.num_workers > 0 else False
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers
        )

    def predict_dataloader(self):
        return DataLoader(
            self.predict_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers
        )
```

## 用法

```python
# Create DataModule
dm = MyDataModule(data_dir="./data", batch_size=64, num_workers=8)

# Use with Trainer
trainer = L.Trainer(max_epochs=10)
trainer.fit(model, datamodule=dm)

# Test
trainer.test(model, datamodule=dm)

# Predict
predictions = trainer.predict(model, datamodule=dm)

# Or use standalone in PyTorch
dm.prepare_data()
dm.setup(stage='fit')
train_loader = dm.train_dataloader()

for batch in train_loader:
    # Your training code
    pass
```

## 其他Hooks

### `transfer_batch_to_device(batch, device, dataloader_idx)`
用于将批次移动到设备的自定义逻辑。

* *示例：**
```python
def transfer_batch_to_device(self, batch, device, dataloader_idx):
    # Custom transfer logic
    if isinstance(batch, dict):
        return {k: v.to(device) for k, v in batch.items()}
    return super().transfer_batch_to_device(batch, device, dataloader_idx)
```

### `on_before_batch_transfer(batch, dataloader_idx)`
在传输到设备之前增强或修改批次（运行于CPU).

* *示例：**
```python
def on_before_batch_transfer(self, batch, dataloader_idx):
    # Apply CPU-based augmentations
    batch['image'] = apply_augmentation(batch['image'])
    return batch
```

### `on_after_batch_transfer(batch, dataloader_idx)`
传输到设备后增强或修改批次（运行于GPU).

* *示例：**
```python
def on_after_batch_transfer(self, batch, dataloader_idx):
    # Apply GPU-based augmentations
    batch['image'] = gpu_augmentation(batch['image'])
    return batch
```

### `state_dict()` / `load_state_dict(state_dict)`
保存并恢复 DataModule 状态checkpointing.

* *示例：**
```python
def state_dict(self):
    return {"current_fold": self.current_fold}

def load_state_dict(self, state_dict):
    self.current_fold = state_dict["current_fold"]
```

### `teardown(stage)`
之后的清理操作训练/测试/预测.

* *示例：**
```python
def teardown(self, stage):
    # Clean up resources
    if stage == 'fit':
        self.train_dataset = None
        self.val_dataset = None
```

## 高级模式

### 多重验证/测试数据加载器

返回以下列表或字典DataLoaders：

```python
def val_dataloader(self):
    return [
        DataLoader(self.val_dataset_1, batch_size=32),
        DataLoader(self.val_dataset_2, batch_size=32)
    ]

# Or with names (for logging)
def val_dataloader(self):
    return {
        "val_easy": DataLoader(self.val_easy, batch_size=32),
        "val_hard": DataLoader(self.val_hard, batch_size=32)
    }

# In LightningModule
def validation_step(self, batch, batch_idx, dataloader_idx=0):
    if dataloader_idx == 0:
        # Handle val_dataset_1
        pass
    else:
        # Handle val_dataset_2
        pass
```

### 交叉验证

```python
class CrossValidationDataModule(L.LightningDataModule):
    def __init__(self, data_dir, batch_size, num_folds=5):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.num_folds = num_folds
        self.current_fold = 0

    def setup(self, stage=None):
        full_dataset = MyDataset(self.data_dir)
        fold_size = len(full_dataset) // self.num_folds

        # Create fold indices
        indices = list(range(len(full_dataset)))
        val_start = self.current_fold * fold_size
        val_end = val_start + fold_size

        val_indices = indices[val_start:val_end]
        train_indices = indices[:val_start] + indices[val_end:]

        self.train_dataset = Subset(full_dataset, train_indices)
        self.val_dataset = Subset(full_dataset, val_indices)

    def set_fold(self, fold):
        self.current_fold = fold

    def state_dict(self):
        return {"current_fold": self.current_fold}

    def load_state_dict(self, state_dict):
        self.current_fold = state_dict["current_fold"]

# Usage
dm = CrossValidationDataModule("./data", batch_size=32, num_folds=5)

for fold in range(5):
    dm.set_fold(fold)
    trainer = L.Trainer(max_epochs=10)
    trainer.fit(model, datamodule=dm)
```

### 超参数保存

```python
class MyDataModule(L.LightningDataModule):
    def __init__(self, data_dir, batch_size=32, num_workers=4):
        super().__init__()
        # Save hyperparameters
        self.save_hyperparameters()

    def setup(self, stage=None):
        # Access via self.hparams
        print(f"Batch size: {self.hparams.batch_size}")
```

## 最佳实践

#### 1.单独的prepare_data和setup
- `prepare_data()` - 下载/处理（单进程，无状态）
- `setup()` - 创建数据集（每个进程，设置状态）

### 2.使用stage参数
检查`setup()`中的stage，避免不必要的工作：

```python
def setup(self, stage):
    if stage == 'fit':
        # Only load train/val data when fitting
        self.train_dataset = ...
        self.val_dataset = ...
    elif stage == 'test':
        # Only load test data when testing
        self.test_dataset = ...
```

### 3. 用于 GPU 训练的引脚内存
在 DataLoaders 中启用 `pin_memory=True` 以实现更快的 GPU 传输：

```python
def train_dataloader(self):
    return DataLoader(..., pin_memory=True)
```

### 4. 使用持久Workers
防止worker在纪元之间重新启动：

```python
def train_dataloader(self):
    return DataLoader(
        ...,
        num_workers=4,
        persistent_workers=True
    )
```

### 5.避免验证/测试中的随机播放
切勿随机播放验证或测试数据：

```python
def val_dataloader(self):
    return DataLoader(..., shuffle=False)  # Never True
```

### 6.Make DataModules Reusable
接受`__init__`:

中的配置参数```python
class MyDataModule(L.LightningDataModule):
    def __init__(self, data_dir, batch_size, num_workers, augment=True):
        super().__init__()
        self.save_hyperparameters()
```

### 7. 文档数据结构
添加解释数据格式和期望的文档字符串：

```python
class MyDataModule(L.LightningDataModule):
    """
    DataModule for XYZ dataset.

    Data format: (image, label) tuples
    - image: torch.Tensor of shape (C, H, W)
    - label: int in range [0, num_classes)

    Args:
        data_dir: Path to data directory
        batch_size: Batch size for dataloaders
        num_workers: Number of data loading workers
    """
```

## 常见陷阱

### 1. 设置状态prepare_data
* *错误：**
```python
def prepare_data(self):
    self.dataset = load_data()  # State not transferred to other processes!
```

* *正确：**
```python
def prepare_data(self):
    download_data()  # Only download, no state

def setup(self, stage):
    self.dataset = load_data()  # Set state here
```

### 2.不使用阶段参数
* *低效：**
```python
def setup(self, stage):
    self.train_dataset = load_train()
    self.val_dataset = load_val()
    self.test_dataset = load_test()  # Loads even when just fitting
```

* *高效：**
```python
def setup(self, stage):
    if stage == 'fit':
        self.train_dataset = load_train()
        self.val_dataset = load_val()
    elif stage == 'test':
        self.test_dataset = load_test()
```

### 3.忘记返回DataLoaders
* *错误：**
```python
def train_dataloader(self):
    DataLoader(self.train_dataset, ...)  # Forgot return!
```

* *正确：**
```python
def train_dataloader(self):
    return DataLoader(self.train_dataset, ...)
```

## 与 Trainer

```python
# Initialize DataModule
dm = MyDataModule(data_dir="./data", batch_size=64)

# All data loading is handled by DataModule
trainer = L.Trainer(max_epochs=10)
trainer.fit(model, datamodule=dm)

# DataModule handles validation too
trainer.validate(model, datamodule=dm)

# And testing
trainer.test(model, datamodule=dm)

# And prediction
predictions = trainer.predict(model, datamodule=dm)
```
 集成
