---
name: ginkgo-cloud-lab
description: 在 Ginkgo Bioworks 云实验室 (cloud.ginkgo.bio)上提交和管理协议，这是一个基于 Web 的界面，用于在可重新配置自动化推车 (RAC)上自主执行实验室。当用户想要运行无细胞蛋白质表达（验证或优化）、生成荧光像素艺术或与 Ginkgo Cloud Lab 服务交互时使用。涵盖协议选择、输入准备、定价和订购工作流程。
---

# Ginkgo 云实验室

## 概述

Ginkgo 云实验室 (https://cloud.ginkgo.bio)提供对 Ginkgo Bioworks 自主实验室基础设施的远程访问。协议在可重新配置自动化推车 (RAC)上执行 - 具有机械臂、磁悬浮样品运输和涵盖 70 多种仪器的工业级软件的模块化单元。

 该平台还包括 **EstiMate**，这是一种 AI 代理，它接受人类语言协议描述，并返回超出列出协议的自定义工作流程的可行性评估和定价。

## 可用协议

### 1. 无细胞蛋白表达验证

使用重构的大肠杆菌 CFPS 进行快速 go/no-go 表达筛选。提交 FASTA 序列（最多 1800 bp）并通过虚拟凝胶图像接收表达确认、基线滴度 (mg/L)和初始纯度。

- **价格：** 39 美元/样品 | **周转时间：** 5-10 天 | **状态：** 已认证 
- **详细信息：** 请参见 [references/cell-free- Protein-express-validation.md](references/cell-free- Protein-express-validation.md)

### 2. 无细胞蛋白表达优化 

DoE 基于每个蛋白多达 24 个条件的优化（裂解物、温度、分子伴侣、二硫键）增强子、辅助因子）。专为难以表达的蛋白和膜蛋白而设计。

- **价格：** 199 美元/样品 | **周转时间：** 6-11 天 | **状态：** 已认证
- **详细信息：** 参见 [references/cell-free- Protein-express-optimization.md](references/cell-free- Protein-express-optimization.md)

### 3. 荧光像素艺术生成

将像素艺术图像（48x48 至 96x96 px，PNG/SVG）转换为通过声学分配使用多达 11 种大肠杆菌菌株制作荧光细菌图稿。以高分辨率 UV 照片形式提供。

- **价格：** 25 美元/盘 | **周转时间：** 5-7 天 | **状态：** Beta
- **详细信息：** 请参阅 [references/luminous-pixel-art- Generation.md](references/luminous-pixel-art- Generation.md)

## 一般订购工作流程

1. 在 https://cloud.ginkgo.bio/protocols
2 选择协议。配置参数（样品/蛋白质、重复、板的数量）
3. 上传输入文件（用于蛋白质协议的 FASTA，用于像素艺术的 PNG/SVG）
4. 在“其他详细信息”字段中添加任何特殊要求
5. 提交并接收可行性报告和报价

对于上面未列出的协议，请使用 **EstiMate** 聊天以简单的语言描述自定义协议并接收兼容性评估和定价。

## 身份验证

访问 Ginkgo 云实验室，网址为 https://cloud.ginkgo.bio。可能需要创建帐户或机构访问权限。请通过 cloud@ginkgo.bio 联系 Ginkgo 了解访问问题。

## 关键基础设施

- **RAC（可重构自动化推车）：** 具有高精度手臂和磁悬浮运输的模块化机器人单元
- **Catalyst 软件：** 协议编排、调度、参数化和实时监控
- **70+ 集成仪器：** 示例准备、液体处理、分析读数、存储、孵化
- **星云：** Ginkgo 位于波士顿的自主实验室设施，MA
