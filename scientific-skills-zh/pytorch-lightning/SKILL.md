---
name: pytorch-lightning
description: 深度学习框架（PyTorch Lightning）。将 PyTorch 代码组织到 LightningModules 中，为多 GPU/TPU 配置训练器，实现数据管道、回调、日志记录（W&B、TensorBoard）、分布式训练（DDP、FSDP、DeepSpeed），以进行可扩展的神经网络训练。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# PyTorch Lightning

## 概述

PyTorch Lightning 是一个深度学习框架，它组织 PyTorch 代码以消除样板文件，同时保持充分的灵活性。自动化训练工作流程、多设备编排，并在多个 GPU/TPU 上实现神经网络训练和扩展的最佳实践。

## 何时使用此技能

此技能应在以下情况下使用：
- 使用 PyTorch Lightning 构建、训练或部署神经网络
- 将 PyTorch 代码组织到 LightningModules 中
- 配置训练器用于多 GPU/TPU 训练
- 使用 LightningDataModules 实现数据管道
- 使用回调、日志记录和分布式训练策略（DDP、FSDP、DeepSpeed）
- 专业构建深度学习项目

## 核心功能

### 1. LightningModule - 模型定义

将PyTorch模型组织成六个逻辑部分：

1. **初始化** - `__init__()` 和 `setup()`
2. **训练循环** - `training_step(batch, batch_idx)`
3. **验证循环** - `validation_step(batch, batch_idx)`
4. **测试回路** - `test_step(batch, batch_idx)`
5. **预测** - `predict_step(batch, batch_idx)`
6. **优化器配置** - `configure_optimizers()`

  * *快速模板参考：** 请参阅 `scripts/template_lightning_module.py` 以获取完整的样板。

  * *详细文档：** 请阅读 `references/lightning_module.md` 以获取全面的方法文档、挂钩、属性和最佳实践。

### 2. 培训师 - 培训自动化

培训师自动执行训练循环、设备管理、梯度操作和回调。主要功能：

- 多 GPU/TPU 支持，具有策略选择（DDP、FSDP、DeepSpeed）
- 自动混合精度训练
- 梯度累积和裁剪
- 检查点和提前停止
- 进度条和日志记录

* *快速设置参考：** 请参阅`scripts/quick_trainer_setup.py` 适用于常见训练器配置。

* *详细文档：**阅读`references/trainer.md`了解所有参数、方法和配置选项。

### 3. LightningDataModule - 数据管道组织

将所有数据处理步骤封装在一个可重用的类中：

1. `prepare_data()` - 下载并处理数据（单进程）
2. `setup()` - 创建数据集并应用转换（每个 GPU）
3. `train_dataloader()` - 返回训练DataLoader
4. `val_dataloader()` - 返回验证DataLoader
5. `test_dataloader()` - 返回测试 DataLoader

* *快速模板参考：** 请参阅 `scripts/template_datamodule.py` 获取完整的样板。

* *详细文档：** 阅读 `references/data_module.md` 了解方法详细信息和使用模式。

### 4. 回调 - 可扩展训练逻辑

在特定训练中添加自定义功能无需修改您的 LightningModule 即可挂钩。内置回调包括：

- **ModelCheckpoint** - 保存最佳/最新模型
- **EarlyStopping** - 当指标达到稳定状态时停止
- **LearningRateMonitor** - 跟踪LR调度程序更改
- **BatchSizeFinder** - 自动确定最佳批量大小

* *详细文档：** 阅读 `references/callbacks.md` 了解内置回调和自定义回调创建。

### 5. 日志记录 - 实验跟踪

与多个日志平台集成：

- TensorBoard（默认）
- 权重和偏差 (WandbLogger)
- MLflow (MLFlowLogger)
- Neptune (NeptuneLogger)
- Comet (CometLogger)
- CSV (CSVLogger)

在任何 LightningModule 方法中使用 `self.log("metric_name", value)` 记录指标。

* *详细文档：** 阅读 `references/logging.md`记录器设置和配置。

### 6.分布式训练 - 扩展到多个设备

根据模型大小选择正确的策略：

- **DDP** - 适用于<500M参数的模型（ResNet，较小的transformers）
- **FSDP** - 适用于500M+参数的模型（较大的transformers，推荐Lightning用户）
- **DeepSpeed** - 用于尖端功能和细粒度控制

配置为： `Trainer(strategy="ddp", accelerator="gpu", devices=4)`

* *详细文档：**阅读`references/distributed_training.md`进行策略比较和配置。

### 7.最佳实践

- 设备无关代码-使用`self.device`而不是`.cuda()`
- 超参数保存-使用`__init__()`
 中的 `self.save_hyperparameters()`- 指标记录 - 使用 `self.log()` 进行跨设备自动聚合
- 再现性 - 使用 `seed_everything()` 和 `Trainer(deterministic=True)`
- 调试 - 使用 `Trainer(fast_dev_run=True)` 进行测试 1批处理

* *详细文档：**阅读`references/best_practices.md`以了解常见模式和陷阱。

## 快速工作流程

1. **定义模型：**
 ```python
 class MyModel(L.LightningModule):
 def __init__(self):
 super().__init__()
 self.save_hyperparameters()
 self.model = YourNetwork()

 deftraining_step(self,batch,batch_idx):
 x,y=batch
loss=F.cross_entropy(self.model(x),y)
 self.log("train_loss",loss)
返回loss

def configure_optimizers(self):
 返回 torch.optim.Adam(self.parameters())
 ```

2. **准备数据：**
 ```python
 # 选项1：直接DataLoaders
train_loader = DataLoader(train_dataset, batch_size=32)

 # 选项2：LightningDataModule（建议复用）
dm = MyDataModule(batch_size=32)
``

3. **训练：**
 ```python
 trainer = L.Trainer(max_epochs=10, Accelerator="gpu", devices=2)
 trainer.fit(model, train_loader) # 或 trainer.fit(model, datamodule=dm)
 ```

## 资源

### script/
常见 PyTorch Lightning 模式的可执行 Python 模板：

- `template_lightning_module.py` - 完整的 LightningModule 样板
- `template_datamodule.py` - 完整的 LightningDataModule 样板
- `quick_trainer_setup.py` - 通用训练器配置示例

### 参考文献/
每个 PyTorch Lightning 组件的详细文档：

- `lightning_module.md` - 综合 LightningModule 指南（方法、挂钩、属性）
- `trainer.md` - 训练器配置和参数
- `data_module.md` - LightningDataModule 模式和方法
- `callbacks.md` - 内置和自定义回调
- `logging.md` - 记录器集成和使用
- `distributed_training.md` - DDP、FSDP、DeepSpeed 比较和设置
- `best_practices.md` - 常见模式、提示和陷阱
