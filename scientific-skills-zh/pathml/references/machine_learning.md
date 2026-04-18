# 机器学习

## 概述

PathML 为计算病理学提供全面的机器学习功能，包括用于细胞核检测和分割的预构建模型、PyTorch 集成训练工作流程、公共数据集访问和基于 ONNX 的推理部署。该框架将图像预处理与深度学习无缝连接起来，以实现端到端病理学 ML 管道。

## 预构建模型

PathML 包括用于细胞核分析的最先进的预训练模型：

### HoVer-Net

* *HoVer-Net**（水平和垂直网络）同时执行细胞核实例分割和分类.

* *架构：**
- 具有三个预测分支的编码器-解码器结构：
  - **核像素 (NP)** - 核区域的二进制分割
  - **水平-垂直 (HV)** - 到核质心的距离映射
  - **分类 (NC)** - 核类型分类

* *细胞核类型：**
1. 上皮
2. 炎症
3. 结缔组织/软组织
4. 死亡/坏死
5. 背景

* *用法：**
```python
from pathml.ml import HoVerNet
import torch

# Load pre-trained model
model = HoVerNet(
    num_types=5,  # Number of nucleus types
    mode='fast',  # 'fast' or 'original'
    pretrained=True  # Load pre-trained weights
)

# Move to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Inference on tile
tile_image = torch.from_numpy(tile.image).permute(2, 0, 1).unsqueeze(0).float()
tile_image = tile_image.to(device)

with torch.no_grad():
    output = model(tile_image)

# Output contains:
# - output['np']: Nuclear pixel predictions
# - output['hv']: Horizontal-vertical maps
# - output['nc']: Classification predictions
```

* *后处理：**
```python
from pathml.ml import hovernet_postprocess

# Convert model outputs to instance segmentation
instance_map, type_map = hovernet_postprocess(
    np_pred=output['np'],
    hv_pred=output['hv'],
    nc_pred=output['nc']
)

# instance_map: Each nucleus has unique ID
# type_map: Each nucleus assigned a type (1-5)
```

### HACTNet

* *HACTNet**（分层细胞类型网络）执行具有不确定性的分层核分类quantification.

* *特征：**
- 层次分类（粗粒度到细粒度类型）
- 预测的不确定性估计
- 改进不平衡数据集的性能

```python
from pathml.ml import HACTNet

# Load model
model = HACTNet(
    num_classes_coarse=3,
    num_classes_fine=8,
    pretrained=True
)

# Inference
output = model(tile_image)
coarse_pred = output['coarse']  # Broad categories
fine_pred = output['fine']  # Specific cell types
uncertainty = output['uncertainty']  # Prediction confidence
```

## 训练工作流程

### 数据集准备

PathML 提供与 PyTorch 兼容的数据集类：

* *TileDataset：**
```python
from pathml.ml import TileDataset
from pathml.core import SlideDataset

# Create dataset from processed slides
tile_dataset = TileDataset(
    slide_dataset,
    tile_size=256,
    transform=None  # Optional augmentation transforms
)

# Access tiles
image, label = tile_dataset[0]
```

* *DataModule 集成：**
```python
from pathml.ml import PathMLDataModule

# Create train/val/test splits
data_module = PathMLDataModule(
    train_dataset=train_tile_dataset,
    val_dataset=val_tile_dataset,
    test_dataset=test_tile_dataset,
    batch_size=32,
    num_workers=4
)

# Use with PyTorch Lightning
trainer = pl.Trainer(max_epochs=100)
trainer.fit(model, data_module)
```

### 训练HoVer-Net

在自定义数据上训练 HoVer-Net 的完整工作流程：

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from pathml.ml import HoVerNet
from pathml.ml.datasets import PanNukeDataModule

# 1. Prepare data
data_module = PanNukeDataModule(
    data_dir='path/to/pannuke',
    batch_size=8,
    num_workers=4,
    tissue_types=['Breast', 'Colon']  # Specific tissue types
)

# 2. Initialize model
model = HoVerNet(
    num_types=5,
    mode='fast',
    pretrained=False  # Train from scratch or use pretrained=True for fine-tuning
)

# 3. Define loss function
class HoVerNetLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.mse_loss = nn.MSELoss()
        self.bce_loss = nn.BCEWithLogitsLoss()
        self.ce_loss = nn.CrossEntropyLoss()

    def forward(self, output, target):
        # Nuclear pixel branch loss
        np_loss = self.bce_loss(output['np'], target['np'])

        # Horizontal-vertical branch loss
        hv_loss = self.mse_loss(output['hv'], target['hv'])

        # Classification branch loss
        nc_loss = self.ce_loss(output['nc'], target['nc'])

        # Combined loss
        total_loss = np_loss + hv_loss + 2.0 * nc_loss
        return total_loss, {'np': np_loss, 'hv': hv_loss, 'nc': nc_loss}

criterion = HoVerNetLoss()

# 4. Configure optimizer
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=1e-4,
    weight_decay=1e-5
)

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode='min',
    factor=0.5,
    patience=10
)

# 5. Training loop
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    train_loss = 0.0

    for batch in data_module.train_dataloader():
        images = batch['image'].to(device)
        targets = {
            'np': batch['np_map'].to(device),
            'hv': batch['hv_map'].to(device),
            'nc': batch['type_map'].to(device)
        }

        optimizer.zero_grad()
        outputs = model(images)
        loss, loss_dict = criterion(outputs, targets)

        loss.backward()
        optimizer.step()

        train_loss += loss.item()

    # Validation
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for batch in data_module.val_dataloader():
            images = batch['image'].to(device)
            targets = {
                'np': batch['np_map'].to(device),
                'hv': batch['hv_map'].to(device),
                'nc': batch['type_map'].to(device)
            }
            outputs = model(images)
            loss, _ = criterion(outputs, targets)
            val_loss += loss.item()

    scheduler.step(val_loss)

    print(f"Epoch {epoch+1}/{num_epochs}")
    print(f"  Train Loss: {train_loss/len(data_module.train_dataloader()):.4f}")
    print(f"  Val Loss: {val_loss/len(data_module.val_dataloader()):.4f}")

    # Save checkpoint
    if (epoch + 1) % 10 == 0:
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': val_loss,
        }, f'hovernet_checkpoint_epoch_{epoch+1}.pth')
```

### PyTorch Lightning 集成

PathML 模型与 PyTorch Lightning 集成以简化训练：

```python
import pytorch_lightning as pl
from pathml.ml import HoVerNet
from pathml.ml.datasets import PanNukeDataModule

class HoVerNetModule(pl.LightningModule):
    def __init__(self, num_types=5, lr=1e-4):
        super().__init__()
        self.model = HoVerNet(num_types=num_types, pretrained=True)
        self.lr = lr
        self.criterion = HoVerNetLoss()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        images = batch['image']
        targets = {
            'np': batch['np_map'],
            'hv': batch['hv_map'],
            'nc': batch['type_map']
        }
        outputs = self(images)
        loss, loss_dict = self.criterion(outputs, targets)

        # Log metrics
        self.log('train_loss', loss, prog_bar=True)
        for key, val in loss_dict.items():
            self.log(f'train_{key}_loss', val)

        return loss

    def validation_step(self, batch, batch_idx):
        images = batch['image']
        targets = {
            'np': batch['np_map'],
            'hv': batch['hv_map'],
            'nc': batch['type_map']
        }
        outputs = self(images)
        loss, loss_dict = self.criterion(outputs, targets)

        self.log('val_loss', loss, prog_bar=True)
        for key, val in loss_dict.items():
            self.log(f'val_{key}_loss', val)

        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=10
        )
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'monitor': 'val_loss'
            }
        }

# Train with PyTorch Lightning
data_module = PanNukeDataModule(data_dir='path/to/pannuke', batch_size=8)
model = HoVerNetModule(num_types=5, lr=1e-4)

trainer = pl.Trainer(
    max_epochs=100,
    accelerator='gpu',
    devices=1,
    callbacks=[
        pl.callbacks.ModelCheckpoint(monitor='val_loss', mode='min'),
        pl.callbacks.EarlyStopping(monitor='val_loss', patience=20)
    ]
)

trainer.fit(model, data_module)
```

## Public数据集

PathML 提供对公共病理学数据集的便捷访问：

### PanNuke 数据集

* *PanNuke** 包含来自 19 种组织类型的 7,901 个组织学图像块，以及 5 种细胞类型的细胞核注释。

```python
from pathml.ml.datasets import PanNukeDataModule

# Load PanNuke dataset
pannuke = PanNukeDataModule(
    data_dir='path/to/pannuke',
    batch_size=16,
    num_workers=4,
    tissue_types=None,  # Use all tissue types, or specify list
    fold='all'  # 'fold1', 'fold2', 'fold3', or 'all'
)

# Access dataloaders
train_loader = pannuke.train_dataloader()
val_loader = pannuke.val_dataloader()
test_loader = pannuke.test_dataloader()

# Batch structure
for batch in train_loader:
    images = batch['image']  # Shape: (B, 3, 256, 256)
    inst_map = batch['inst_map']  # Instance segmentation map
    type_map = batch['type_map']  # Cell type map
    np_map = batch['np_map']  # Nuclear pixel map
    hv_map = batch['hv_map']  # Horizontal-vertical distance maps
    tissue_type = batch['tissue_type']  # Tissue category
```

* *组织类型可用：**
乳房、结肠、前列腺、肺、肾、胃、膀胱、食道、子宫颈、肝脏、甲状腺、头颈、睾丸、肾上腺、胰腺、胆管、卵巢、皮肤、子宫

### TCGA 数据集

访问癌症基因组图谱数据集：

```python
from pathml.ml.datasets import TCGADataModule

# Load TCGA dataset
tcga = TCGADataModule(
    data_dir='path/to/tcga',
    cancer_type='BRCA',  # Breast cancer
    batch_size=32,
    tile_size=224
)
```

### 自定义数据集集成

为 PathML 工作流程创建自定义数据集：

```python
from torch.utils.data import Dataset
import numpy as np
from pathlib import Path

class CustomPathologyDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = Path(data_dir)
        self.image_paths = list(self.data_dir.glob('images/*.png'))
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # Load image
        image_path = self.image_paths[idx]
        image = np.array(Image.open(image_path))

        # Load corresponding annotation
        annot_path = self.data_dir / 'annotations' / f'{image_path.stem}.npy'
        annotation = np.load(annot_path)

        # Apply transforms
        if self.transform:
            image = self.transform(image)

        return {
            'image': torch.from_numpy(image).permute(2, 0, 1).float(),
            'annotation': torch.from_numpy(annotation).long(),
            'path': str(image_path)
        }

# Use in PathML workflow
dataset = CustomPathologyDataset('path/to/data')
dataloader = DataLoader(dataset, batch_size=16, shuffle=True, num_workers=4)
```

## 数据增强

应用增强以改进模型泛化：

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

# Define augmentation pipeline
train_transform = A.Compose([
    A.RandomRotate90(p=0.5),
    A.Flip(p=0.5),
    A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1, p=0.5),
    A.GaussianBlur(blur_limit=(3, 7), p=0.3),
    A.ElasticTransform(alpha=1, sigma=50, alpha_affine=50, p=0.3),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2()
])

val_transform = A.Compose([
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2()
])

# Apply to dataset
train_dataset = TileDataset(slide_dataset, transform=train_transform)
val_dataset = TileDataset(val_slide_dataset, transform=val_transform)
```

## 模型评估

### 指标

E 使用病理特定指标评估模型性能：

```python
from pathml.ml.metrics import (
    dice_coefficient,
    aggregated_jaccard_index,
    panoptic_quality
)

# Dice coefficient for segmentation
dice = dice_coefficient(pred_mask, true_mask)

# Aggregated Jaccard Index (AJI) for instance segmentation
aji = aggregated_jaccard_index(pred_inst, true_inst)

# Panoptic Quality (PQ) for joint segmentation and classification
pq, sq, rq = panoptic_quality(pred_inst, true_inst, pred_types, true_types)

print(f"Dice: {dice:.4f}")
print(f"AJI: {aji:.4f}")
print(f"PQ: {pq:.4f}, SQ: {sq:.4f}, RQ: {rq:.4f}")
```

### 评估Loop

```python
from pathml.ml.metrics import evaluate_hovernet

# Comprehensive HoVer-Net evaluation
model.eval()
all_preds = []
all_targets = []

with torch.no_grad():
    for batch in test_loader:
        images = batch['image'].to(device)
        outputs = model(images)

        # Post-process predictions
        for i in range(len(images)):
            inst_pred, type_pred = hovernet_postprocess(
                outputs['np'][i],
                outputs['hv'][i],
                outputs['nc'][i]
            )
            all_preds.append({'inst': inst_pred, 'type': type_pred})
            all_targets.append({
                'inst': batch['inst_map'][i],
                'type': batch['type_map'][i]
            })

# Compute metrics
results = evaluate_hovernet(all_preds, all_targets)

print(f"Detection F1: {results['detection_f1']:.4f}")
print(f"Classification Accuracy: {results['classification_acc']:.4f}")
print(f"Panoptic Quality: {results['pq']:.4f}")
```

## ONNX Inference

使用 ONNX 部署模型进行生产推理：

### 导出到 ONNX

```python
import torch
from pathml.ml import HoVerNet

# Load trained model
model = HoVerNet(num_types=5, pretrained=True)
model.eval()

# Create dummy input
dummy_input = torch.randn(1, 3, 256, 256)

# Export to ONNX
torch.onnx.export(
    model,
    dummy_input,
    'hovernet_model.onnx',
    export_params=True,
    opset_version=11,
    input_names=['input'],
    output_names=['np_output', 'hv_output', 'nc_output'],
    dynamic_axes={
        'input': {0: 'batch_size'},
        'np_output': {0: 'batch_size'},
        'hv_output': {0: 'batch_size'},
        'nc_output': {0: 'batch_size'}
    }
)
```

### ONNX 运行时Inference

```python
import onnxruntime as ort
import numpy as np

# Load ONNX model
session = ort.InferenceSession('hovernet_model.onnx')

# Prepare input
input_name = session.get_inputs()[0].name
tile_image = preprocess_tile(tile)  # Normalize, transpose to (1, 3, H, W)

# Run inference
outputs = session.run(None, {input_name: tile_image})
np_output, hv_output, nc_output = outputs

# Post-process
inst_map, type_map = hovernet_postprocess(np_output, hv_output, nc_output)
```

### 批量推理管道

```python
from pathml.core import SlideData
from pathml.preprocessing import Pipeline
import onnxruntime as ort

def run_onnx_inference_pipeline(slide_path, onnx_model_path):
    # Load slide
    wsi = SlideData.from_slide(slide_path)
    wsi.generate_tiles(level=1, tile_size=256, stride=256)

    # Load ONNX model
    session = ort.InferenceSession(onnx_model_path)
    input_name = session.get_inputs()[0].name

    # Inference on all tiles
    results = []
    for tile in wsi.tiles:
        # Preprocess
        tile_array = preprocess_tile(tile.image)

        # Inference
        outputs = session.run(None, {input_name: tile_array})

        # Post-process
        inst_map, type_map = hovernet_postprocess(*outputs)

        results.append({
            'coords': tile.coords,
            'instance_map': inst_map,
            'type_map': type_map
        })

    return results

# Run on slide
results = run_onnx_inference_pipeline('slide.svs', 'hovernet_model.onnx')
```

## 迁移学习

在自定义上微调预训练模型数据集：

```python
from pathml.ml import HoVerNet

# Load pre-trained model
model = HoVerNet(num_types=5, pretrained=True)

# Freeze encoder layers for initial training
for name, param in model.named_parameters():
    if 'encoder' in name:
        param.requires_grad = False

# Fine-tune only decoder and classification heads
optimizer = torch.optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=1e-4
)

# Train for a few epochs
train_for_n_epochs(model, train_loader, optimizer, num_epochs=10)

# Unfreeze all layers for full fine-tuning
for param in model.parameters():
    param.requires_grad = True

# Continue training with lower learning rate
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
train_for_n_epochs(model, train_loader, optimizer, num_epochs=50)
```

## 最佳实践

1. **在可用时使用预训练模型：**
  - 从 pretrained=True 开始以获得更好的初始化
  - 对特定于域的数据进行微调

2. **应用适当的数据增强：**
  - 旋转、翻转以实现方向不变性
  - 颜色抖动以处理染色变化
  - 生物变异性的弹性变形

3. **监控多个指标：**
  - 分别跟踪检测、分段和分类
  - 使用超出标准精度的特定领域指标（AJI、PQ）

4. **处理类别不平衡：**
  - 稀有细胞类型的加权损失函数
  - 对少数类别进行过采样
  - 困难示例的焦点损失

5. **在不同的组织类型上进行验证：**
  - 确保不同组织之间的泛化
  - 在保留的解剖部位上进行测试

6. **优化推理：**
  - 导出到 ONNX 以加快部署速度
  - 批量切片以提高 GPU 利用率
  - 尽可能使用混合精度 (FP16)

7. **定期保存检查点：**
  - 根据验证指标保留最佳模型
  - 保存优化器状态以恢复训练

## 常见问题和解决方案

 * *问题：细胞核边界分割不良**
  - 使用HV图（水平-垂直）来分离接触的细胞核
  - 增加HV损失项
- 应用形态学后处理

* *问题：相似细胞类型的错误分类**
- 增加分类损失权重
- 添加分层分类（HACTNet）
- 增强混淆类的训练数据

* *问题：训练是否不稳定收敛**
- 降低学习率
- 使用梯度裁剪： `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`
- 检查数据预处理问题

* *问题：训练期间内存不足**
- 减少批量大小
- 使用梯度累积
- 启用混合精度训练： `torch.cuda.amp`

* *问题：模型对训练数据过度拟合**
- 增加数据增强
- 添加丢失层
- 减少模型容量
- 基于验证损失使用早期停止

## 其他资源

- **PathML ML API：** https://pathml.readthedocs.io/en/latest/api_ml_reference.html
- **HoVer-Net 论文：** Graham 等人，“HoVer-Net：多组织组织学图像中细胞核的同步分割和分类”，医学图像分析，2019
- **PanNuke数据集：** https://warwick.ac.uk/fac/cross_fac/tia/data/pannuke
- **PyTorch Lightning：** https://www.pytorchlightning.ai/
- **ONNX 运行时：** https://onnxruntime.ai/
