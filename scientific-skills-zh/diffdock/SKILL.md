---
name: diffdock
description: 基于扩散的分子对接。通过 PDB/SMILES、置信度评分、虚拟筛选预测蛋白质-配体结合姿势，以进行基于结构的药物设计。不适用于亲和力预测。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# DiffDock：使用扩散模型进行分子对接

## 概述

DiffDock 是一种基于扩散的深度学习工具，用于分子对接，可预测小分子配体与蛋白质靶标的 3D 结合姿势。它代表了最先进的计算对接，对于基于结构的药物发现和化学生物学至关重要。

* *核心功能：**
- 使用深度学习高精度预测配体结合姿势
- 支持蛋白质结构（PDB文件）或序列（通过ESMFold）
- 处理单个复合物或批量虚拟筛选活动
- 生成置信度分数以评估预测可靠性
- 处理不同的配体输入（SMILES、SDF、MOL2）

* *关键区别：** DiffDock 预测**结合姿势**（3D 结构）和**置信度**（预测确定性），而不是结合亲和力（ΔG、Kd）。始终与评分函数（GNINA、MM/GBSA）结合进行亲和力评估。

## 何时使用此技能

此技能应在以下情况下使用：

- “将此配体与蛋白质对接”或“预测结合姿势”
- “运行分子对接”或“执行蛋白质-配体对接”
- “虚拟”筛选”或“筛选化合物库”
- “该分子在哪里结合？”或“预测结合位点”
- 基于结构的药物设计或先导优化任务
- 涉及PDB 文件+SMILES 字符串或配体结构的任务
- 多个蛋白质-配体对的批量对接

## 安装和环境设置

### 检查环境状态

在继续之前DiffDock 任务，验证环境设置：

```bash
# Use the provided setup checker
python scripts/setup_check.py
```

此脚本验证 Python 版本、PyTorch with CUDA、PyTorch Geometric、RDKit、ESM 和其他依赖项。

### 安装选项

* *选项 1：Conda（推荐）**
```bash
git clone https://github.com/gcorso/DiffDock.git
cd DiffDock
conda env create --file environment.yml
conda activate diffdock
```

* *选项 2：Docker**
```bash
docker pull rbgcsail/diffdock
docker run -it --gpus all --entrypoint /bin/bash rbgcsail/diffdock
micromamba activate diffdock
```

* *重要说明：**
- GPU 强烈推荐（10-100 倍于 CPU 的加速）
- 首次运行预计算 SO(2)/SO(3)查找表（约 2-5 分钟）
- 如果不存在，模型检查点（约 500MB）会自动下载

## 核心工作流程

### 工作流程 1：单一蛋白质-配体对接

* *用例：** 将一种配体与一种蛋白质靶标对接

* *输入要求：**
- 蛋白质：PDB文件或氨基酸序列
- 配体：SMILES字符串或结构文件（SDF/MOL2）

* *命令：**
```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_path protein.pdb \
  --ligand "CC(=O)Oc1ccccc1C(=O)O" \
  --out_dir results/single_docking/
```

* *替代（蛋白质序列）：**
```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_sequence "MSKGEELFTGVVPILVELDGDVNGHKF..." \
  --ligand ligand.sdf \
  --out_dir results/sequence_docking/
```

* *输出结构：**
```
results/single_docking/
├── rank_1.sdf          # Top-ranked pose
├── rank_2.sdf          # Second-ranked pose
├── ...
├── rank_10.sdf         # 10th pose (default: 10 samples)
└── confidence_scores.txt
```

### 工作流程 2：批量处理多个复合物

* *用例：**将多个配体与蛋白质对接，虚拟筛选活动

* *步骤 1：准备批量 CSV**

 使用提供的脚本创建或验证批量输入：

```bash
# Create template
python scripts/prepare_batch_csv.py --create --output batch_input.csv

# Validate existing CSV
python scripts/prepare_batch_csv.py my_input.csv --validate
```

* *CSV 格式：**
```csv
complex_name,protein_path,ligand_description,protein_sequence
complex1,protein1.pdb,CC(=O)Oc1ccccc1C(=O)O,
complex2,,COc1ccc(C#N)cc1,MSKGEELFT...
complex3,protein3.pdb,ligand3.sdf,
```

* *必需列：**
- `complex_name`：唯一标识符
- `protein_path`：PDB文件路径（如果使用序列则留空）
- `ligand_description`：SMILES字符串或配体文件路径
- `protein_sequence`：氨基酸序列（如果使用PDB则留空）

* *步骤2：运行批处理对接**

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv batch_input.csv \
  --out_dir results/batch/ \
  --batch_size 10
```

* *用于大型虚拟筛选（>100种化合物）：**

预计算蛋白质嵌入以加快处理速度：
```bash
# Pre-compute embeddings
python datasets/esm_embedding_preparation.py \
  --protein_ligand_csv screening_input.csv \
  --out_file protein_embeddings.pt

# Run with pre-computed embeddings
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv screening_input.csv \
  --esm_embeddings_path protein_embeddings.pt \
  --out_dir results/screening/
```

### 工作流程3：分析结果

之后对接完成，分析置信度分数并对预测进行排名：

```bash
# Analyze all results
python scripts/analyze_results.py results/batch/

# Show top 5 per complex
python scripts/analyze_results.py results/batch/ --top 5

# Filter by confidence threshold
python scripts/analyze_results.py results/batch/ --threshold 0.0

# Export to CSV
python scripts/analyze_results.py results/batch/ --export summary.csv

# Show top 20 predictions across all complexes
python scripts/analyze_results.py results/batch/ --best 20
```

分析脚本：
- 解析所有预测的置信度分数
- 分类为高 (>0)、中等（-1.5 到 0）或低 (<-1.5)
- 对预测进行排名在复合物内部和之间
- 生成统计摘要
- 将结果导出到CSV以进行下游分析

## 置信度分数解释

* *理解分数：**

|分数范围|置信度 |解读 |
|------------------------|--------------------------------|----------------|
| **> 0** |高|预测力强，可能准确 |
| **-1.5 至 0** |中等|合理预测，认真验证|
| **< -1.5** |低|预测不确定，需要验证 |

* *重要说明：**
1. **置信度≠亲和力**：高置信度意味着模型对结构的确定性，而不是强结合
2. **上下文很重要**：调整预期：
  - 大配体（> 500 Da）：预期置信度较低
  - 多个蛋白质链：可能会降低置信度
  - 新蛋白质家族：可能表现不佳
3. **多个样本**：查看前 3-5 个预测，寻找共识

* *详细指导：** 使用读取工具读取 `references/confidence_and_limitations.md`

## 参数自定义

### 使用自定义配置

创建特定用途的自定义配置案例：

```bash
# Copy template
cp assets/custom_inference_config.yaml my_config.yaml

# Edit parameters (see template for presets)
# Then run with custom config
python -m inference \
  --config my_config.yaml \
  --protein_ligand_csv input.csv \
  --out_dir results/
```

### 调整的关键参数

* *采样密度：**
- `samples_per_complex: 10` → 对于困难案例增加到 20-40
- 更多样本 = 更好的覆盖范围，但更长的运行时间

* *推理步骤：**
- `inference_steps: 20` → 增加到 25-30，以获得更高的精度
- 更多步骤 = 可能质量更好，但速度更慢

* *温度参数（控制多样性）：**
- `temp_sampling_tor: 7.04` → 增加柔性配体 (8-10)
- `temp_sampling_tor: 7.04` → 刚性配体减少 (5-6)
- 更高的温度 = 更多样化的姿势

* *模板中可用的预设：**
1. 高精度：更多样本+步骤，更低温度
2. 快速筛选：样本更少，速度更快
3. 柔性配体：提高扭转温度
4. 刚性配体：降低扭转温度

* *完整参数参考：**使用读取工具读取`references/parameters_reference.md`

## 高级技术

### 集成对接（蛋白质灵活性）

对于具有已知灵活性的蛋白质，对接至多个构象：

```python
# Create ensemble CSV
import pandas as pd

conformations = ["conf1.pdb", "conf2.pdb", "conf3.pdb"]
ligand = "CC(=O)Oc1ccccc1C(=O)O"

data = {
    "complex_name": [f"ensemble_{i}" for i in range(len(conformations))],
    "protein_path": conformations,
    "ligand_description": [ligand] * len(conformations),
    "protein_sequence": [""] * len(conformations)
}

pd.DataFrame(data).to_csv("ensemble_input.csv", index=False)
```

 以增加的采样运行对接：
```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv ensemble_input.csv \
  --samples_per_complex 20 \
  --out_dir results/ensemble/
```

### 与评分函数集成

DiffDock 生成姿势；与其他工具结合进行亲和力：

* *GNINA（快速神经网络评分）：**
```bash
for pose in results/*.sdf; do
    gnina -r protein.pdb -l "$pose" --score_only
done
```

* *MM/GBSA（更准确，更慢）：**
能量最小化后使用AmberTools MMPBSA.py或gmx_MMPBSA

* *自由能量计算（最准确）：**
使用OpenMM + OpenFE或GROMACS进行FEP/TI计算

* *推荐工作流程：**
1. DiffDock → 生成具有置信度分数 
2 的姿势。目视检查 → 检查结构合理性
3. GNINA 或 MM/GBSA → 按亲和力重新评分和排名
4. 实验验证 → 生化检测

## 限制和范围

* *DiffDock 设计用于：**
- 小分子配体（通常为 100-1000 Da）
- 类药物有机化合物
- 小肽（<20）残基）
- 单链或多链蛋白质

* *DiffDock 不适用于：**
- 大生物分子（蛋白质-蛋白质对接）→ 使用 DiffDock-PP 或 AlphaFold-Multimer
- 大肽（> 20 个残基）→ 使用替代方法
- 共价对接→使用专门的共价对接工具
- 结合亲和力预测→与评分功能结合
- 膜蛋白→未经专门训练，谨慎使用

* *完整限制：**使用读取工具读取`references/confidence_and_limitations.md`

## 故障排除

### 常见问题

* *问题：所有预测的置信度较低**
- 原因：大/不寻常的配体、不明确的结合位点、蛋白质灵活性
- 解决方案：增加`samples_per_complex`（20-40），尝试集成对接，验证蛋白质结构

* *问题：内存不足错误**
- 原因：GPU内存不足以满足批量大小
- 解决方案：减少`--batch_size 2`或一次处理更少的复合体

* *问题：性能缓慢**
- 原因：在CPU而不是GPU上运行
- 解决方案：使用`python -c "import torch; print(torch.cuda.is_available())"`验证CUDA，使用GPU

* *问题：不切实际的结合姿势**
- 原因：蛋白质制备不良，配体太大，结合位点错误
- 解决方案：检查蛋白质是否有缺失的残基，去除远Waters，请考虑指定绑定站点

* *问题：“找不到模块”错误**
- 原因：缺少依赖项或环境错误
- 解决方案：运行`python scripts/setup_check.py`来诊断

### 性能优化

* *最佳结果：**
1. 使用GPU（实际使用必备）
2. 预先计算 ESM 嵌入以重复使用蛋白质 
3. 一起批量处理多个复合物
4. 从默认参数开始，然后根据需要进行调整
5. 验证蛋白质结构（解决缺失残基）
6. 对配体使用规范的 SMILES

## 图形用户界面

对于交互式使用，启动 Web 界面：

```bash
python app/main.py
# Navigate to http://localhost:7860
```

 或无需安装即可使用在线演示：
- https://huggingface.co/spaces/reginabarzilaygroup/DiffDock-Web

## 资源

### 帮助程序脚本 (`scripts/`)

* *`prepare_batch_csv.py`**：创建和验证批量输入 CSV 文件
- 使用示例创建模板条目
- 验证文件路径和 SMILES 字符串
- 检查所需的列和格式问题

* *`analyze_results.py`**：分析置信度得分和排名预测
- 解析单次或批量运行的结果
- 生成统计摘要
- 导出到 CSV 以供下游使用分析
- 识别复合体中的最高预测

* *`setup_check.py`**：验证DiffDock环境设置
- 检查Python版本和依赖项
- 验证PyTorch和CUDA可用性
- 测试RDKit和PyTorch几何安装
- 如果需要，提供安装说明

### 参考文档(`references/`)

* *`parameters_reference.md`**：完整的参数文档
- 所有命令行选项和配置参数
- 默认值和可接受的范围
- 用于控制多样性的温度参数
- 模型检查点位置和版本标志

用户需要时阅读此文件：
- 详细参数解释
- 针对特定系统的微调指南
- 替代采样策略

* *`confidence_and_limitations.md`**：置信度得分解释和工具限制
- 详细置信度得分解释
- 何时信任预测
- DiffDock 的范围和限制
- 与互补集成工具
- 预测质量故障排除

在用户需要时阅读此文件：
- 帮助解释置信度分数
- 了解何时不使用DiffDock
- 与其他工具结合使用的指南
- 验证策略

* *`workflows_examples.md`**：全面的工作流程示例
- 详细的安装说明
- 所有工作流程的分步示例
- 高级集成模式
- 常见问题故障排除
- 最佳实践和优化提示

用户时阅读此文件需要：
- 带代码的完整工作流程示例
- 与 GNINA、OpenMM 或其他工具集成
- 虚拟筛选工作流程
- 集成对接程序

### 资产 (`assets/`)

* *`batch_template.csv`**：模板批处理
- 带有所需列的预格式化CSV
- 显示不同输入类型的示例条目
- 准备使用实际数据进行自定义

* *`custom_inference_config.yaml`**：配置模板
- 带有所有参数的带注释的YAML
- 四种常用的预设配置案例
- 详细注释解释每个参数
- 准备定制和使用

## 最佳实践

1. **在开始大型作业
2之前，请务必使用`setup_check.py`验证环境**。 **使用 `prepare_batch_csv.py` 验证批量 CSV** 以尽早发现错误
3. **从默认值开始**，然后根据系统特定需求调整参数
4. **生成多个样本** (10-40)以实现稳健的预测
5. 在下游分析之前对顶部姿势进行**目视检查**
6. **结合评分**功能进行亲和力评估
7. **使用置信度分数**进行初始排名，而不是最终决定
8. **虚拟筛选活动的预计算嵌入**
9. **文档参数**用于再现性
10. **尽可能通过实验验证结果**

## 引用

当使用DiffDock时，引用适当的论文：

* *DiffDock-L（当前默认模型）：**
```
Stärk et al. (2024) "DiffDock-L: Improving Molecular Docking with Diffusion Models"
arXiv:2402.18396
```

* *原始DiffDock:**
```
Corso et al. (2023) "DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking"
ICLR 2023, arXiv:2210.01776
```

## 其他资源

- **GitHub 存储库**：https://github.com/gcorso/DiffDock
- **在线演示**： https://huggingface.co/spaces/reginabarzilaygroup/DiffDock-Web
- **DiffDock-L论文**：https://arxiv.org/abs/2402.18396
- **原始论文**：https://arxiv.org/abs/2210.01776
