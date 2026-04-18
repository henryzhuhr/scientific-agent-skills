# DiffDock 工作流程和示例

本文档提供常见 DiffDock 任务的实用工作流程和使用示例。

## 安装和设置

### Conda 安装（推荐）

```bash
# Clone repository
git clone https://github.com/gcorso/DiffDock.git
cd DiffDock

# Create conda environment
conda env create --file environment.yml
conda activate diffdock
```

### Docker安装

```bash
# Pull Docker image
docker pull rbgcsail/diffdock

# Run container with GPU support
docker run -it --gpus all --entrypoint /bin/bash rbgcsail/diffdock

# Inside container, activate environment
micromamba activate diffdock
```

### 第一次运行
第一次执行预先计算SO(2)和SO(3)查找表，需要几分钟。后续运行立即开始。

## 工作流程 1：单一蛋白质-配体对接

### 使用 PDB 文件和 SMILES 字符串

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_path examples/protein.pdb \
  --ligand "COc1ccc(C(=O)Nc2ccccc2)cc1" \
  --out_dir results/single_docking/
```

* *输出结构**：
```
results/single_docking/
├── index_0_rank_1.sdf       # Top-ranked prediction
├── index_0_rank_2.sdf       # Second-ranked prediction
├── ...
├── index_0_rank_10.sdf      # 10th prediction (if samples_per_complex=10)
└── confidence_scores.txt    # Scores for all predictions
```

### 使用配体结构文件

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_path protein.pdb \
  --ligand ligand.sdf \
  --out_dir results/ligand_file/
```

* *支持的配体格式**：SDF、MOL2或RDKit可读的任何格式

## 工作流程2：蛋白质序列到结构对接

### 使用ESMFold进行蛋白质折叠

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_sequence "MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK" \
  --ligand "CC(C)Cc1ccc(cc1)C(C)C(=O)O" \
  --out_dir results/sequence_docking/
```

* *用例**：
- PDB中不可用的蛋白质结构
- 建模突变或变体
- 从头蛋白质设计验证

* *注意**：ESMFold折叠增加了计算时间（30秒-5分钟，具体取决于序列） length)

## 工作流程 3：批量处理多个复合体

### 准备 CSV 文件

使用所需列创建 `complexes.csv`：

```csv
complex_name,protein_path,ligand_description,protein_sequence
complex1,proteins/protein1.pdb,CC(=O)Oc1ccccc1C(=O)O,
complex2,,COc1ccc(C#N)cc1,MSKGEELFTGVVPILVELDGDVNGHKF...
complex3,proteins/protein3.pdb,ligands/ligand3.sdf,
```

* *列说明**：
- `complex_name`： complex
- `protein_path`：PDB 文件的路径（如果使用序列则留空）
- `ligand_description`：配体文件的 SMILES 字符串或路径
- `protein_sequence`：氨基酸序列（如果使用 PDB 则留空）

### 运行批处理对接

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv complexes.csv \
  --out_dir results/batch_predictions/ \
  --batch_size 10
```

* *输出结构**：
```
results/batch_predictions/
├── complex1/
│   ├── rank_1.sdf
│   ├── rank_2.sdf
│   └── ...
├── complex2/
│   ├── rank_1.sdf
│   └── ...
└── complex3/
    └── ...
```

## 工作流程4：高通量虚拟筛选

### 筛选大配体的设置文库

```python
# generate_screening_csv.py
import pandas as pd

# Load ligand library
ligands = pd.read_csv("ligand_library.csv")  # Contains SMILES

# Create DiffDock input
screening_data = {
    "complex_name": [f"screen_{i}" for i in range(len(ligands))],
    "protein_path": ["target_protein.pdb"] * len(ligands),
    "ligand_description": ligands["smiles"].tolist(),
    "protein_sequence": [""] * len(ligands)
}

df = pd.DataFrame(screening_data)
df.to_csv("screening_input.csv", index=False)
```

### 运行筛选

```bash
# Pre-compute ESM embeddings for faster screening
python datasets/esm_embedding_preparation.py \
  --protein_ligand_csv screening_input.csv \
  --out_file protein_embeddings.pt

# Run docking with pre-computed embeddings
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv screening_input.csv \
  --esm_embeddings_path protein_embeddings.pt \
  --out_dir results/virtual_screening/ \
  --batch_size 32
```

### 后处理：提取热门命中

```python
# analyze_screening_results.py
import os
import pandas as pd

results = []
results_dir = "results/virtual_screening/"

for complex_dir in os.listdir(results_dir):
    confidence_file = os.path.join(results_dir, complex_dir, "confidence_scores.txt")
    if os.path.exists(confidence_file):
        with open(confidence_file) as f:
            scores = [float(line.strip()) for line in f]
            top_score = max(scores)
            results.append({"complex": complex_dir, "top_confidence": top_score})

# Sort by confidence
df = pd.DataFrame(results)
df_sorted = df.sort_values("top_confidence", ascending=False)

# Get top 100 hits
top_hits = df_sorted.head(100)
top_hits.to_csv("top_hits.csv", index=False)
```

## 工作流程 5：与蛋白质的集成对接灵活性

### 准备蛋白质整体

```python
# For proteins with known flexibility, use multiple conformations
# Example: Using MD snapshots or crystal structures

# create_ensemble_csv.py
import pandas as pd

conformations = [
    "protein_conf1.pdb",
    "protein_conf2.pdb",
    "protein_conf3.pdb",
    "protein_conf4.pdb"
]

ligand = "CC(C)Cc1ccc(cc1)C(C)C(=O)O"

data = {
    "complex_name": [f"ensemble_{i}" for i in range(len(conformations))],
    "protein_path": conformations,
    "ligand_description": [ligand] * len(conformations),
    "protein_sequence": [""] * len(conformations)
}

pd.DataFrame(data).to_csv("ensemble_input.csv", index=False)
```

### 运行整体对接

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv ensemble_input.csv \
  --out_dir results/ensemble_docking/ \
  --samples_per_complex 20  # More samples per conformation
```

## 工作流程 6：与下游分析集成

### 示例：DiffDock + GNINA 重新评分

```bash
# 1. Run DiffDock
python -m inference \
  --config default_inference_args.yaml \
  --protein_path protein.pdb \
  --ligand "CC(=O)OC1=CC=CC=C1C(=O)O" \
  --out_dir results/diffdock_poses/ \
  --save_visualisation

# 2. Rescore with GNINA
for pose in results/diffdock_poses/*.sdf; do
    gnina -r protein.pdb -l "$pose" --score_only -o "${pose%.sdf}_gnina.sdf"
done
```

### 示例：DiffDock + OpenMM Energy最小化

```python
# minimize_poses.py
from openmm import app, LangevinIntegrator, Platform
from openmm.app import ForceField, Modeller, PDBFile
from rdkit import Chem
import os

# Load protein
protein = PDBFile('protein.pdb')
forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

# Process each DiffDock pose
pose_dir = 'results/diffdock_poses/'
for pose_file in os.listdir(pose_dir):
    if pose_file.endswith('.sdf'):
        # Load ligand
        mol = Chem.SDMolSupplier(os.path.join(pose_dir, pose_file))[0]

        # Combine protein + ligand
        modeller = Modeller(protein.topology, protein.positions)
        # ... add ligand to modeller ...

        # Create system and minimize
        system = forcefield.createSystem(modeller.topology)
        integrator = LangevinIntegrator(300, 1.0, 0.002)
        simulation = app.Simulation(modeller.topology, system, integrator)
        simulation.minimizeEnergy(maxIterations=1000)

        # Save minimized structure
        positions = simulation.context.getState(getPositions=True).getPositions()
        PDBFile.writeFile(simulation.topology, positions,
                         open(f"minimized_{pose_file}.pdb", 'w'))
```

## 工作流程 7：使用图形界面

### 启动 Web 界面

```bash
python app/main.py
```

### 访问界面
在 Web 浏览器中导航到 `http://localhost:7860`

### 功能
- 上传蛋白质PDB或输入序列
- 输入配体SMILES或上传结构
- 通过GUI调整推理参数
- 交互式可视化结果
- 直接下载预测

### 在线替代
使用拥抱面部空间演示，无需本地安装：
- URL：https://huggingface.co/spaces/reginabarzilaygroup/DiffDock-Web

## 高级配置

### 自定义推理设置

创建自定义YAML配置：

```yaml
# custom_inference.yaml
# Model settings
model_dir: ./workdir/v1.1/score_model
confidence_model_dir: ./workdir/v1.1/confidence_model

# Sampling parameters
samples_per_complex: 20  # More samples for better coverage
inference_steps: 25      # More steps for accuracy

# Temperature adjustments (increase for more diversity)
temp_sampling_tr: 1.3
temp_sampling_rot: 2.2
temp_sampling_tor: 7.5

# Output
save_visualisation: true
```

使用自定义配置：

```bash
python -m inference \
  --config custom_inference.yaml \
  --protein_path protein.pdb \
  --ligand "CC(=O)OC1=CC=CC=C1C(=O)O" \
  --out_dir results/custom_config/
```

## 常见问题故障排除

### 问题：内存不足错误

* *解决方案**：减小批量大小
```bash
python -m inference ... --batch_size 2
```

### 问题：速度慢性能

* *解决方案**：确保GPU使用
```python
import torch
print(torch.cuda.is_available())  # Should return True
```

### 问题：大型配体的预测不佳

* *解决方案**：增加采样多样性
```bash
python -m inference ... --samples_per_complex 40 --temp_sampling_tor 9.0
```

### 问题：具有许多的蛋白质链

* *解决方案**：限制链或隔离结合位点
```bash
python -m inference ... --chain_cutoff 4
```

或预处理PDB以仅包含相关链。

## 最佳实践总结

1. **开始简单**：在批量处理之前用单一复合体进行测试
2. **GPU 必备**：使用 GPU 获得合理的性能
3. **多个样本**：生成 10-40 个样本以实现稳健的预测 
4. **验证结果**：使用分子可视化和补充评分
5. **考虑置信度**：使用置信度分数进行初始排名，而不是最终决策
6. **迭代参数**：调整特定系统的温度/步骤
7. **预计算嵌入**：用于重复使用相同的蛋白质
8. **组合工具**：与评分函数和能量最小化集成
