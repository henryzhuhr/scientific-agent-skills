---
name: pathml
description: 全功能的计算病理学工具包。用于高级 WSI 分析，包括多重免疫荧光（CODEX、Vectra）、细胞核分割、组织图构建和病理数据的 ML 模型训练。支持 160 多种幻灯片格式。对于从 H&E 幻灯片中简单提取图块，histolab 可能更简单。
license: GPL-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# PathML

## 概述

PathML 是一个用于计算病理学工作流程的综合 Python 工具包，旨在促进全幻灯片病理图像的机器学习和图像分析。该框架提供了模块化、可组合的工具，用于加载不同的幻灯片格式、预处理图像、构建空间图、训练深度学习模型以及分析来自 CODEX 和多重免疫荧光等技术的多参数成像数据。

## 何时使用此技能

将此技能应用于：
- 以各种专有格式加载和处理整个幻灯片图像 (WSI)
- 预处理通过染色归一化进行 H&E 染色组织图像
- 细胞核检测、分割和分类工作流程
- 构建用于空间分析的细胞和组织图
- 在病理数据上训练或部署机器学习模型（HoVer-Net、HACTNet）
- 分析空间多参数成像（CODEX、Vectra、MERFISH）蛋白质组学
- 定量多重免疫荧光标记表达
- 使用 HDF5 存储管理大规模病理数据集
- 基于平铺的分析和拼接操作

## 核心功能

PathML 提供参考文件中详细记录的六个主要功能领域：

### 1. 图像加载和格式

从 160 多种专有格式加载整个幻灯片图像，包括 Aperio SVS、Hamamatsu NDPI、Leica SCN、Zeiss ZVI、DICOM 和 OME-TIFF。 PathML 自动处理供应商特定的格式，并提供用于访问图像金字塔、元数据和感兴趣区域的统一接口。

* *请参阅：** `references/image_loading.md` 了解支持的格式、加载策略以及使用不同的幻灯片类型。

### 2. 预处理管道

通过组合图像处理、质量控制、染色归一化、组织检测和掩模操作的转换来构建模块化预处理管道。 PathML 的 Pipeline 架构支持跨大型数据集进行可重复、可扩展的预处理。

* *关键转换：**
- `StainNormalizationHE` - Macenko/Vahadane 染色归一化
- `TissueDetectionHE`、`NucleusDetectionHE` - 组织/细胞核分割
- `MedianBlur`、`GaussianBlur` - 降噪
- `LabelArtifactTileHE` - 工件质量控制

* *参见：** `references/preprocessing.md` 了解完整的转换目录、管道构建和预处理工作流程。

### 3. 图形构建

构建表示细胞和组织级别的空间图关系。从分割对象中提取特征，创建适合图神经网络和空间分析的基于图的表示。

* *参见：** `references/graphs.md`，用于图构建方法、特征提取和空间分析工作流程。

### 4. 机器学习

训练和部署深度学习模型，用于核检测、分割和分类。 PathML 将 PyTorch 与预构建模型（HoVer-Net、HACTNet）、自定义 DataLoaders 和 ONNX 支持集成以进行推理。

* *关键模型：**
- **HoVer-Net** - 同步核分割和分类
- **HACTNet** - 分层细胞类型分类

* *参见：** `references/machine_learning.md` 用于模型训练、评估、推理工作流程以及使用公共数据集。

### 5. 多参数成像

分析来自 CODEX、Vectra、MERFISH 和其他多重成像平台的空间蛋白质组学和基因表达数据。 PathML 提供专门的幻灯片类和转换，用于处理多参数数据、使用 Mesmer 进行细胞分割以及量化工作流程。

* *参见：** `references/multiparametric.md` 用于 CODEX/Vectra 工作流程、细胞分割、标记定量以及与 AnnData.

### 的集成 6. 数据管理

E 使用 HDF5 格式高效存储和管理大型病理数据集。 PathML 处理针对机器学习工作流程优化的统一存储结构中的图块、掩码、元数据和提取的特征。

* *请参阅：** `references/data_management.md`，用于 HDF5 集成、图块管理、数据集组织和批处理策略。

## 快速入门

### 安装

```bash
# Install PathML
uv pip install pathml

# With optional dependencies for all features
uv pip install pathml[all]
```

### 基本工作流程示例

```python
from pathml.core import SlideData
from pathml.preprocessing import Pipeline, StainNormalizationHE, TissueDetectionHE

# Load a whole-slide image
wsi = SlideData.from_slide("path/to/slide.svs")

# Create preprocessing pipeline
pipeline = Pipeline([
    TissueDetectionHE(),
    StainNormalizationHE(target='normalize', stain_estimation_method='macenko')
])

# Run pipeline
pipeline.run(wsi)

# Access processed tiles
for tile in wsi.tiles:
    processed_image = tile.image
    tissue_mask = tile.masks['tissue']
```

### 常用工作流程

* *H&E图像分析：**
1. 使用适当的滑块等级 
2 加载 WSI。应用组织检测和染色标准化
3. 执行核检测或训练分割模型
4. 提取特征并构建空间图
5. 进行下游分析

* *多参数成像（CODEX）：**
1. 使用 `CODEXSlide`
2 加载 CODEX 载玻片。折叠多运行通道数据
3. 使用 Mesmer 模型 
4 分割细胞。量化标记表达
5. 导出到 AnnData 以进行单细胞分析

* *训练 ML 模型：**
1. 使用公共病理数据
2准备数据集。使用 PathML 数据集 
3 创建 PyTorch DataLoader。训练 HoVer-Net 或自定义模型
4. 对保留的测试集 
5 进行评估。使用 ONNX 进行部署以进行推理

## 参考详细文档

在处理特定任务时，请参阅相应的参考文件以获取全面信息：

- **加载图像：** `references/image_loading.md`
- **预处理工作流程：** `references/preprocessing.md`
- **空间分析：** `references/graphs.md`
- **模型训练：** `references/machine_learning.md`
- **CODEX/ Multiplex IF：** `references/multiparametric.md`
- **数据存储：** `references/data_management.md`

## 资源

该技能包括按功能领域组织的综合参考文档。每个参考文件包含详细的 API 信息、工作流程示例、最佳实践以及特定 PathML 功能的故障排除指南。

### 参考/

文档文件提供 PathML 功能的深入介绍：

- `image_loading.md` - 整个幻灯片图像格式、加载策略、幻灯片类
- `preprocessing.md` - 完整的转换目录、管道构建、预处理工作流程
- `graphs.md` - 图构建方法、特征提取、空间分析
- `machine_learning.md` - 模型架构、训练工作流程、评估、推理
- `multiparametric.md` - CODEX、Vectra、多重IF分析、细胞分割、定量
- `data_management.md` - HDF5 存储、切片管理、批处理、数据集组织

在处理特定计算病理学任务时根据需要加载这些参考文献。
