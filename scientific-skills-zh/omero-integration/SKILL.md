---
name: omero-integration
description: 显微镜数据管理平台。通过 Python 访问图像、检索数据集、分析像素、管理 ROI/注释、批处理，以实现高内容筛选和显微镜工作流程。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# OMERO 集成

## 概述

OMERO 是一个用于管理、可视化和分析显微镜图像和元数据的开源平台。通过 Python API 访问图像、检索数据集、分析像素、管理 ROI 和注释，以实现高内容筛选和显微镜工作流程。

## 何时使用此技能

此技能应在以下情况下使用：
- 使用 OMERO Python API (omero-py)访问显微镜数据
- 检索图像、数据集、项目或筛选数据以编程方式
- 分析像素数据并创建派生图像
- 在显微镜图像上创建或管理 ROI（感兴趣区域）
- 向 OMERO 对象添加注释、标签或元数据
- 在 OMERO 表中存储测量结果
- 创建用于批处理的服务器端脚本
- 执行高内涵筛选分析

## 核心能力

该技能涵盖八个主要能力领域。每个内容都详细记录在引用/目录中：

### 1. 连接和会话管理
* *文件**：`references/connection.md`

E 建立与 OMERO 服务器的安全连接、管理会话、处理身份验证以及使用组上下文。将此用于初始设置和连接模式。

* *常见场景：**
- 使用凭据连接到 OMERO 服务器
- 使用现有会话 ID
- 在组上下文之间切换
- 使用上下文管理器管理连接生命周期

### 2. 数据访问和检索
* *文件**：`references/data_access.md`

导航OMERO的分层数据结构（项目→数据集→图像）和筛选数据（屏幕→板→孔）。检索对象、按属性查询、访问元数据。

* *常见场景：**
- 列出用户的所有项目和数据集
- 按ID或数据集检索图像
- 访问筛选板数据
- 使用过滤器查询对象

### 3.元数据和注释
* *文件**：`references/metadata.md`

创建和管理注释，包括标签、键值对、文件附件和注释。将注释链接到图像、数据集或其他对象。

* *常见场景：**
- 向图像添加标签
- 将分析结果附加为文件
- 创建自定义键值元数据
- 按命名空间查询注释

### 4. 图像处理和渲染
* *文件**： `references/image_processing.md`

以 NumPy 数组的形式访问原始像素数据，操作渲染设置，创建派生图像并管理物理尺寸。

* *常见场景：**
- 提取像素数据进行计算分析
- 生成缩略图
- 创建最大强度投影
- 修改通道渲染设置

### 5. 感兴趣区域 (ROI)
* *文件**：`references/rois.md`

 创建、检索和分析具有各种形状（矩形、椭圆形、多边形、蒙版、点、线）的 ROI。从 ROI 区域提取强度统计数据。

* *常见场景：**
- 在图像上绘制矩形 ROI
- 创建用于分割的多边形蒙版
- 分析 ROI 内的像素强度
- 导出 ROI 坐标

### 6. OMERO表
* *文件**：`references/tables.md`

存储和查询与OMERO对象关联的结构化表格数据。对于分析结果、测量和元数据很有用。

* *常见场景：**
- 存储图像的定量测量结果
- 创建具有多个列类型的表
- 带条件查询表数据
- 将表链接到特定图像或数据集

### 7. 脚本和批处理操作
* *文件**：`references/scripts.md`

创建在服务器端运行的OMERO.脚本，以进行批处理、自动化工作流程以及与OMERO客户端的集成。

* *常见场景：**
- 批量处理多个图像
- 创建自动化分析管道
- 生成跨数据集的汇总统计信息
- 以自定义格式导出数据

### 8. 高级功能
* *文件**：`references/advanced.md`

 涵盖权限、文件集、跨组

* *常见场景：**
- 处理组权限
- 访问原始导入的文件
- 执行跨组查询
- 通过回调删除对象

## 安装

```bash
uv pip install omero-py
```

* *要求：**
- Python 3.7+
- Zeroc Ice 3.6+
- 访问 OMERO 服务器（主机、端口、凭据）

## 快速入门

基本连接模式：

```python
from omero.gateway import BlitzGateway

# Connect to OMERO server
conn = BlitzGateway(username, password, host=host, port=port)
connected = conn.connect()

if connected:
    # Perform operations
    for project in conn.listProjects():
        print(project.getName())

    # Always close connection
    conn.close()
else:
    print("Connection failed")
```

* *带有上下文管理器的推荐模式：**

```python
from omero.gateway import BlitzGateway

with BlitzGateway(username, password, host=host, port=port) as conn:
    # Connection automatically managed
    for project in conn.listProjects():
        print(project.getName())
    # Automatically closed on exit
```

## 选择正确的功能

* *对于数据探索：**
- 从`references/connection.md`开始建立连接
- 使用`references/data_access.md`导航层次结构
- 检查`references/metadata.md`以获取注释详细信息

* *用于图像分析：**
- 使用`references/image_processing.md`进行像素数据访问
- 使用`references/rois.md`进行基于区域的分析
- 使用`references/tables.md`存储结果

* *用于自动化：**
- 使用`references/scripts.md`进行服务器端处理
- 使用`references/data_access.md`进行批量数据检索

* *用于高级操作：**
- 使用`references/advanced.md` 的权限和删除
- 检查 `references/connection.md` 的跨组查询

## 常用工作流程

### 工作流程 1：检索和分析图像

1. 连接到OMERO服务器（`references/connection.md`）
2. 导航到数据集 (`references/data_access.md`)
3. 从数据集 (`references/data_access.md`)
4 检索图像。以 NumPy 数组 (`references/image_processing.md`)
5 的形式访问像素数据。执行分析
6. 将结果存储为表或文件注释（`references/tables.md` 或 `references/metadata.md`）

### 工作流程 2：批量 ROI 分析

1. 连接OMERO服务器
2. 检索具有现有 ROI 的图像 (`references/rois.md`)
3. 对于每个图像，获取 ROI 形状
4. 提取 ROI 内的像素强度 (`references/rois.md`)
5. 将测量值存储在 OMERO 表 (`references/tables.md`)

### 工作流程 3：创建分析脚本

1. 设计分析工作流程
2. 使用OMERO.scripts框架(`references/scripts.md`)
3. 通过脚本参数
4访问数据。批量处理图像
5. 生成输出（新图像、表格、文件）

## 错误处理

始终将OMERO操作包装在try- except块中并确保连接正确关闭：

```python
from omero.gateway import BlitzGateway
import traceback

try:
    conn = BlitzGateway(username, password, host=host, port=port)
    if not conn.connect():
        raise Exception("Connection failed")

    # Perform operations

except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
finally:
    if conn:
        conn.close()
```

## 其他资源

- **官方文档**： https://omero.readthedocs.io/en/stable/developers/Python.html
- **BlitzGateway API**： https://omero.readthedocs.io/en/stable/developers/Python.html#omero-blitzgateway
- **OMERO 模型**： https://omero.readthedocs.io/en/stable/developers/Model.html
- **社区论坛**：https://forum.image.sc/tag/omero

## 注释

- OMERO 使用基于组的权限（READ-ONLY、READ-ANNOTATE、READ-WRITE）
- OMERO 中的图像进行组织分层：项目 > 数据集 > Image
- 筛选数据使用：Screen > Plate > Well > WellSample > Image
- 始终关闭与空闲服务器资源的连接
- 使用上下文管理器进行自动资源管理
- 像素数据作为 NumPy 数组返回用于分析
