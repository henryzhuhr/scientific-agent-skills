---
name: rowan
description: Rowan 是一个具有 Python API 的云原生分子建模和药物化学工作流程平台。用于 pKa 和 macropKa 预测、构象异构体和互变异构体集成、对接和类似物对接、蛋白质-配体共折叠、MSA 生成、分子动力学、渗透性、描述符工作流程以及相关的小分子或蛋白质建模任务。非常适合程序化批量筛选、多步骤化学管道以及需要维护本地 HPC/GPU 基础设施的工作流程。
license: Proprietary (API key required)
compatibility: Python 3.12+, API key required
metadata:
  skill-author: Rowan Science
  trigger-keywords: ["pKa prediction", "molecular docking", "conformer search", "chemistry workflow", "drug discovery", "SMILES", "protein structure", "batch molecular modeling", "cloud chemistry"]
---

# Rowan：云原生分子建模和药物设计工作流程

## 概述

Rowan 是一个用于分子模拟、药物化学和基于结构的设计的云原生工作流程平台。其 Python API 为小分子建模、属性预测、对接、分子动力学和 AI 结构工作流程提供了统一的接口。

 当您想要以编程方式运行药物化学或分子设计工作流程而无需维护本地 HPC 基础设施、GPU 配置或一组单独的建模工具时，请使用 Rowan。 Rowan 处理所有基础设施、结果管理和计算缩放。

## 何时使用 Rowan

* *Rowan 非常适合：**

- 量子化学、半经验方法或神经网络势
- 批量属性预测（pKa、描述符、渗透性、溶解度）
- 构象异构体和互变异构体整体生成
- 对接工作流程（单配体、类似物系列、位姿细化）
- 蛋白质-配体共折叠和 MSA 生成
- 多步骤化学流程（例如互变异构体搜索→对接→位姿分析）
- 您需要一致、可扩展的基础设施的批量药物化学活动

* *Rowan 不适合：**
- 简单的分子 I/O（直接使用 RDKit）
- 高频 *ab initio* 量子化学或相对论计算

## 访问和定价model

Rowan 使用基于信用的使用模型。所有用户（包括免费层用户）都可以创建 API 密钥并使用 Python API。

### 免费层访问

- 访问所有 Rowan 核心工作流程
- 每周 20 个积分
- 500 个注册积分

### 定价和积分消耗

根据计算类型消耗积分：

- **CPU**：每分钟1个积分
- **GPU**：每分钟3个积分
- **H100/H200 GPU**：每分钟7个积分

购买的积分按每个积分定价，并在购买后一年内有效。

### 典型成本估算

|工作流程|典型运行时间 |预计学分|注释 |
|----------|----------------|--------------------|-------|
|描述符| <1 分钟 | 0.5–2 |重量轻，有利于分流|
| pKa（单转变）| 2–5 分钟 | 2-5 | 2-5取决于分子大小|
| MacropKa (pH 0–14) | 5–15 分钟 | 5–15 |采样范围更广，成本更高|
|符合者搜索| 3–10 分钟 | 3–10 |合奏质量很重要|
|互变异构体搜索 | 2–5 分钟 | 2-5 | 2-5杂环系统|
|对接（单配体）| 5–20 分钟 | 5–20 |取决于口袋大小、精致度|
|模拟对接系列（10-50 个配体）| 30–120 分钟 | 30–100+ |共享参考系|
| MSA 一代 | 5–30 分钟 | 5–30 |取决于序列长度|
|蛋白质-配体共折叠| 15–60 分钟 | 20–50+ | AI结构预测，GPU密集型|

## 快速入门

```bash
uv pip install rowan-python
```

```python
import rowan
rowan.api_key = "your_api_key_here"  # or set ROWAN_API_KEY env var

# Submit a descriptors workflow — completes in under a minute
wf = rowan.submit_descriptors_workflow("CC(=O)Oc1ccccc1C(=O)O", name="aspirin")
result = wf.result()

print(result.descriptors['MW'])    # 180.16
print(result.descriptors['SLogP']) # 1.19
print(result.descriptors['TPSA'])  # 59.44
```

如果打印没有错误，则说明设置正确。

## 安装

```bash
uv pip install rowan-python
# or: pip install rowan-python
```

## 用户和webhook管理

### 身份验证

通过环境变量设置API密钥（推荐）：

```bash
export ROWAN_API_KEY="your_api_key_here"
```

或者直接在中设置Python:

```python
import rowan
rowan.api_key = "your_api_key_here"
```

验证身份验证:

```python
import rowan
user = rowan.whoami()  # Returns user info if authenticated
print(f"User: {user.email}")
print(f"Credits available: {user.credits_available_string}")
```

### Webhook机密管理

对于webhook签名验证，通过您的用户管理机密帐户：

```python
import rowan

# Get your current webhook secret (returns None if none exists)
secret = rowan.get_webhook_secret()
if secret is None:
    secret = rowan.create_webhook_secret()
print(f"Secret key: {secret.secret}")

# Rotate your secret (invalidates old, creates new)
# Use this periodically for security
new_secret = rowan.rotate_webhook_secret()
print(f"New secret created (old secret disabled): {new_secret.secret}")

# Verify incoming webhook signatures
is_valid = rowan.verify_webhook_secret(
    request_body=b"...",           # Raw request body (bytes)
    signature="X-Rowan-Signature", # From request header
    secret=secret.secret
)
```

## 分子输入格式

Rowan 接受以下格式的分子：

- **SMILES**（首选）：`"CCO"`、`"c1ccccc1O"`
- **SMARTS 模式**（对于某些工作流程）：子集用于子结构匹配的 SMARTS
- **InChI**（如果您的 API 版本支持）：`"InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3"`

 如果无法解析分子，API 将验证输入并引发 `rowan.ValidationError`。始终使用规范化的 SMILES 来实现再现性。

* *提示：** 在提交之前使用 RDKit 验证 SMILES：

```python
from rdkit import Chem
smiles = "CCO"
mol = Chem.MolFromSmiles(smiles)
if mol is None:
    raise ValueError(f"Invalid SMILES: {smiles}")
```

## 核心使用模式

大多数 Rowan 任务遵循相同的三步模式：

1. **提交**工作流程
2. **等待**完成（带有可选流）
3. **使用便利属性检索**类型化结果

```python
import rowan

# 1. Submit — use the specific workflow function (not the generic submit_workflow)
workflow = rowan.submit_descriptors_workflow(
    "CC(=O)Oc1ccccc1C(=O)O",
    name="aspirin descriptors",
)

# 2. & 3. Wait and retrieve
result = workflow.result()  # Blocks until done (default: wait=True, poll_interval=5)
print(result.data)              # Raw dict
print(result.descriptors['MW']) # 180.16 — use result.descriptors dict, not result.molecular_weight
```

对于长时间运行的工作流程，请使用流式传输：

```python
for partial in workflow.stream_result(poll_interval=5):
    print(f"Progress: {partial.complete}%")
    print(partial.data)
```

### result()与stream_result()

|图案|使用时间 |持续时间 |
|---------|----------|----------|
| `result()` |可以等待完整结果| <5 分钟（典型值）|
| `stream_result()` |您想要进度反馈或需要早期部分结果 | >5 分钟，或交互使用 |

* *指南：** 使用 `result()` 作为描述符、pKa。使用 `stream_result()` 进行符合搜索、对接、共折叠。

## 使用结果

Rowan 的 API 包括具有便捷属性的 **类型化工作流程结果对象**。

### 使用类型化属性和 .data

结果有两种访问模式：

1. **便利属性**（首先推荐）：`result.descriptors`、`result.best_pose`、`result.conformer_energies`
2. **原始后备**：`result.data` — 来自 API

 的原始字典示例：

```python
result = rowan.submit_descriptors_workflow(
    "CCO",
    name="ethanol",
).result()

# Convenience property (returns dict of all descriptors):
print(result.descriptors['MW'])   # 46.042
print(result.descriptors['SLogP'])  # -0.001
print(result.descriptors['TPSA'])   # 57.96

# Raw data fallback (descriptors are nested under 'descriptors' key):
print(result.data['descriptors'])
# {'MW': 46.042, 'SLogP': -0.001, 'TPSA': 57.96, 'nHBDon': 1.0, 'nHBAcc': 1.0, ...}
```

* *注意：**`DescriptorsResult` **不**具有 `molecular_weight` 属性。描述符键使用短名称（`MW`、`SLogP`、`nHBDon`）而不是详细名称。

### 缓存失效

一些结果属性是延迟加载的（例如，构象几何、蛋白质结构）。要刷新：

```python
result.clear_cache()
new_structures = result.conformer_molecules  # Refetched
```

## 项目、文件夹和组织

对于重要的活动，请使用项目和文件夹来保持工作井井有条。

### 项目

```python
import rowan

# Create a project
project = rowan.create_project(name="CDK2 lead optimization")
rowan.set_project("CDK2 lead optimization")

# All subsequent workflows go into this project
wf = rowan.submit_descriptors_workflow("CCO", name="test compound")

# Retrieve later
project = rowan.retrieve_project("CDK2 lead optimization")
workflows = rowan.list_workflows(project=project, size=50)
```

### 文件夹

```python
# Create a hierarchical folder structure
folder = rowan.create_folder(name="docking/batch_1/screening")

wf = rowan.submit_docking_workflow(
    # ... docking params ...
    folder=folder,
    name="compound_001",
)

# List workflows in a folder
results = rowan.list_workflows(folder=folder)
```

## 工作流程决策树

### pKa与MacropKa

* *在以下情况下使用微观pKa：**

- 您需要单个可电离基团的 pKa
- 您对酸碱转变和质子化热力学感兴趣
- 该分子具有一两个可电离位点
- 速度至关重要（更快，更少的学分）

* * 在以下情况下使用 MacropKa：**

- 您需要在生理相关范围内实现 pH 依赖性行为（例如，0–14）
- 您需要在 pH 值范围内聚合电荷和质子化态群体 
- 该分子具有多个具有耦合质子化的电离基团 
- 您需要下游特性，例如不同 pH 值下的水溶性 

* *示例决策：**

```text
Phenol (pKa ~10): Use microscopic pKa
Amine (pKa ~9–10): Use microscopic pKa
Multi-ionizable drug (N, O, acidic group): Use macropKa
ADME assessment across GI pH: Use macropKa
```

### 构象搜索与互变异构体搜索

* *在以下情况下使用构象搜索：**

- 已知单一互变异构形式
- 您需要多样化的 3D 整体进行对接、MD 或 SAR分析
- 可旋转键主导化学空间

* *在以下情况下使用互变异构体搜索：**

- 互变异构平衡不确定（例如杂环、酮-烯醇系统）
- 您需要对所有相关的质子化异构体进行建模
- 下游计算（对接，pKa）取决于互变异构形式

* *组合工作流程：**

```python
# Step 1: Find best tautomer
taut_wf = rowan.submit_tautomer_search_workflow(
    initial_molecule="O=c1[nH]ccnc1",
    name="imidazole tautomers",
)
best_taut = taut_wf.result().best_tautomer

# Step 2: Generate conformers from best tautomer
conf_wf = rowan.submit_conformer_search_workflow(
    initial_molecule=best_taut,
    name="imidazole conformers",
)
```

### 对接与模拟对接与共折叠

|工作流程|使用时间 |输入 |输出|
|----------|---------|--------|--------|
|对接|单配体，已知口袋|蛋白质 + 微笑 + 口袋坐标 |姿势、得分、dG |
|模拟对接 | 5–100+ 相关化合物 |蛋白质 + SMILES 列表 + 参考配体 |所有姿势，参考对齐|
|蛋白质-配体共折叠|序列+配体，无晶体结构 |蛋白质序列+微笑| ML 预测的绑定复合体 |

## 常见工作流类别

### 1. 描述符

A 批量分类、SAR 或探索性脚本的轻量级入口点。

```python
wf = rowan.submit_descriptors_workflow(
    "CC(=O)Oc1ccccc1C(=O)O",  # positional arg, accepts SMILES string
    name="aspirin descriptors",
)

result = wf.result()
print(result.descriptors['MW'])    # 180.16
print(result.descriptors['SLogP']) # 1.19
print(result.descriptors['TPSA'])  # 59.44
print(result.data['descriptors'])
# {'MW': 180.16, 'SLogP': 1.19, 'TPSA': 59.44, 'nHBDon': 1.0, 'nHBAcc': 4.0, ...}
```

* *常见描述符键：**

|关键|描述 |典型药物范围 |
|-----|--------------|--------------------|
| `MW` |分子量 (Da) | <500（利宾斯基）|
| `SLogP` |计算的 LogP（亲脂性）| -2 至 +5 |
| `TPSA` |拓扑极表面积 (Å²) |口服生物利用度<140 |
| `nHBDon` | H 型键供体数量 | ≤5（利平斯基）|
| `nHBAcc` | H-键受体计数 | ≤10（利宾斯基）|
| `nRot` |可旋转键数 |口服药物<10 |
| `nRing` |环数| — |
| `nHeavyAtom` |重原子计数 | — |
| `FilterItLogS` |估计水溶性 (LogS) | >-4 首选 |
| `Lipinski` | Lipinski Ro5 通过 (1.0)或失败 (0.0) | — |

结果包含数百个附加分子描述符（BCUT、GETAWAY、WHIM 等）；通过 `result.descriptors['key']`.

### 访问任何内容 2. 微观 pKa

用于特定结构的质子化态能量学和酸/碱行为。

 有两种方法可用：

|方法|输入 |速度|封面|使用时 |
|--------|--------|--------|--------|------------|
| `chemprop_nevolianis2025` |微笑字符串|快|仅去质子化（阴离子共轭碱） |仅酸性基团；快速筛选|
| `starling` |微笑字符串|快|酸+碱（完全质子化/去质子化）|大多数药物样分子；首选 SMILES 方法 |
| `aimnet2_wagen2024`（默认）| 3D 分子对象 |速度更慢，准确度更高 |酸+碱|您已拥有 3D 结构（例如，来自构象异构体搜索）|

```python
# Fast path: SMILES input with full acid+base coverage (use starling method when available)
wf = rowan.submit_pka_workflow(
    initial_molecule="c1ccccc1O",       # phenol SMILES; param is initial_molecule, not initial_smiles
    method="starling",   # fast SMILES method, covers acid+base; chemprop_nevolianis2025 is deprotonation-only
    name="phenol pKa",
)

result = wf.result()
print(result.strongest_acid)    # 9.81 (pKa of the most acidic site)
print(result.conjugate_bases)   # list of {pka, smiles, atom_index, ...} per deprotonatable site
```

### 3. MacropKa

用于在一定范围内的 pH 依赖性质子化行为。

```python
wf = rowan.submit_macropka_workflow(
    initial_smiles="CN1CCN(CC1)C2=NC=NC3=CC=CC=C32",  # imidazole
    min_pH=0,
    max_pH=14,
    min_charge=-2,  # default
    max_charge=2,   # default
    compute_aqueous_solubility=True,  # default
    name="imidazole macropKa",
)

result = wf.result()
print(result.pka_values)               # list of pKa values
print(result.logd_by_ph)               # dict of {pH: logD}
print(result.aqueous_solubility_by_ph) # dict of {pH: solubility}
print(result.isoelectric_point)        # isoelectric point
print(result.data)
# {'pKa_values': [...], 'logD_by_pH': {...}, 'aqueous_solubility_by_pH': {...}, ...}
```

### 4. 构象异构体搜索

用于当集成质量很重要时的3D集成生成。

```python
wf = rowan.submit_conformer_search_workflow(
    initial_molecule="CCOC(=O)N1CCC(CC1)Oc1ncnc2ccccc12",
    num_conformers=50,  # Optional: override default
    name="conformer search",
)

result = wf.result()
print(result.conformer_energies)  # [0.0, 1.2, 2.5, ...]
print(result.conformer_molecules)  # List of 3D molecules
print(result.best_conformer)  # Lowest-energy conformer
```

### 5.互变异构体搜索

用于互变异构体状态影响下游建模的杂环和系统。

```python
wf = rowan.submit_tautomer_search_workflow(
    initial_molecule="O=c1[nH]ccnc1",  # or keto tautomer
    name="imidazolone tautomers",
)

result = wf.result()
print(result.best_tautomer)  # Most stable SMILES string
print(result.tautomers)      # List of tautomeric SMILES
print(result.molecules)      # List of molecule objects
```

### 6. 对接

用于蛋白质配体对接，具有可选的位姿细化和构象异构体生成。

```python
# Upload protein once, reuse in multiple workflows
protein = rowan.upload_protein(
    name="CDK2",
    file_path="cdk2.pdb",
)

# Define binding pocket
pocket = {
    "center": [10.5, 24.2, 31.8],
    "size": [18.0, 18.0, 18.0],
}

# Submit docking
wf = rowan.submit_docking_workflow(
    protein=protein,
    pocket=pocket,
    initial_molecule="CCNc1ncc(c(Nc2ccc(F)cc2)n1)-c1cccnc1",
    do_pose_refinement=True,
    do_conformer_search=True,
    name="lead docking",
)

result = wf.result()
print(result.scores)  # Docking scores (kcal/mol)
print(result.best_pose)  # Mol object with 3D coordinates
print(result.data)  # Raw result dict
```

* *蛋白质制备提示：**

- PDB文件应该相当干净（除非有意，否则除去水/杂原子）
- 在对接系列中使用相同的蛋白质对象一致性
- 如果您有PDB ID，请使用`rowan.create_protein_from_pdb_id()`代替

### 7.模拟对接

用于将化合物系列放入共享绑定上下文中。

```python
# Analogue series (e.g., SAR campaign)
analogues = [
    "CCNc1ncc(c(Nc2ccc(F)cc2)n1)-c1cccnc1",    # reference
    "CCNc1ncc(c(Nc2ccc(Cl)cc2)n1)-c1cccnc1",   # chloro
    "CCNc1ncc(c(Nc2ccc(OC)cc2)n1)-c1cccnc1",   # methoxy
    "CCNc1ncc(c(Nc2cc(C)c(F)cc2)n1)-c1cccnc1", # methyl, fluoro
]

wf = rowan.submit_analogue_docking_workflow(
    analogues=analogues,
    initial_molecule=analogues[0],  # Reference ligand
    protein=protein,
    pocket=pocket,
    name="SAR series docking",
)

result = wf.result()
print(result.analogue_scores)  # List of scores for each analogue
print(result.best_poses)  # List of poses
```

### 8.MSA生成

用于多序列比对（对于下游共折叠有用）。

```python
wf = rowan.submit_msa_workflow(
    initial_protein_sequences=[
        "MENFQKVEKIGEGTYGVVYKARNKLTGEVVALKKIRLDTETEGVP"
    ],
    output_formats=["colabfold", "chai", "boltz"],
    name="target MSA",
)

result = wf.result()
result.download_files()  # Downloads alignments to disk
```

### 9. 蛋白质-配体共折叠

用于在没有晶体结构可用时基于 AI 的结合复合物预测。

```python
wf = rowan.submit_protein_cofolding_workflow(
    initial_protein_sequences=[
        "MENFQKVEKIGEGTYGVVYKARNKLTGEVVALKKIRLDTETEGVP"
    ],
    initial_smiles_list=[
        "CCNc1ncc(c(Nc2ccc(F)cc2)n1)-c1cccnc1"
    ],
    name="protein-ligand cofolding",
)

result = wf.result()
print(result.predictions)  # List of predicted structures
print(result.messages)  # Model metadata/warnings

predicted_structure = result.get_predicted_structure()
predicted_structure.write("predicted_complex.pdb")
```

## 所有支持的工作流程类型

全部工作流程遵循相同的提交→等待→检索模式并支持网络钩子和项目/文件夹组织。

### 核心分子建模工作流程

|工作流程|功能|何时使用 |
|----------|---------|------------|
|描述符| `submit_descriptors_workflow` |首过分类：MW、LogP、TPSA、HBA/HBD、Lipinski 过滤器 |
| pKa| `submit_pka_workflow` |单一可电离基团；需要质子化热力学|
|宏普卡 | `submit_macropka_workflow` |多电离药物； pH 依赖性电荷/LogD/溶解度 |
|符合者搜索 | `submit_conformer_search_workflow` |用于对接、MD 或 SAR 的 3D 整体；已知互变异构体|
|互变异构体搜索 | `submit_tautomer_search_workflow` |杂环、酮-烯醇；不确定的互变异构形式|
|溶解度| `submit_solubility_workflow` |水或溶剂特定溶解度预测|
|膜渗透率| `submit_membrane_permeability_workflow` | Caco-2、PAMPA、BBB、血浆通透性|
| ADMET | `submit_admet_workflow` |广泛的药物相似性和 ADMET 属性扫描 |

### 基于结构的设计工作流程

|工作流程|功能|何时使用 |
|----------|---------|------------|
|对接| `submit_docking_workflow` |单配体，已知结合口袋|
|模拟坞站 | `submit_analogue_docking_workflow` |共享口袋中的 SAR 系列（5-100 多种化合物）|
|批量对接| `submit_batch_docking_workflow` |快速文库筛选；大型复合套装|
|蛋白质医学博士 | `submit_protein_md_workflow` |长时标动态；构象采样|
|姿势分析医学博士 | `submit_pose_analysis_md_workflow` |对接姿势的 MD 细化 |
|蛋白质共折叠| `submit_protein_cofolding_workflow` |无晶体结构； AI 预测的结合复合物 |
|蛋白质粘合剂设计| `submit_protein_binder_design_workflow` |针对蛋白质靶点从头生成结合剂 |

### 高级计算化学

|工作流程|功能|何时使用 |
|----------|---------|------------|
|基本计算| `submit_basic_calculation_workflow` | QM/ML几何优化或单点能量|
|电子特性| `submit_electronic_properties_workflow` |偶极子，部分电荷，HOMO-LUMO，ESP |
|溴二苯醚 | `submit_bde_workflow` |键解离能；代谢软点预测|
|氧化还原电位| `submit_redox_potential_workflow` |氧化/还原电位|
|自旋态| `submit_spin_states_workflow` |有机金属/自由基的自旋态能量排序 |
|应变| `submit_strain_workflow` |相对于全局最小值的构象应变|
|扫描| `submit_scan_workflow` | PES扫描；扭转型材|
|多级优化| `submit_multistage_opt_workflow` |跨理论层次的渐进优化 |

### 反应化学

|工作流程|功能|何时使用 |
|----------|---------|------------|
|双端 TS 搜索 | `submit_double_ended_ts_search_workflow` |两个已知结构之间的过渡态|
|互联网RC | `submit_irc_workflow` |确认TS连接；固有反应坐标 |

### 高级属性

|工作流程|功能|何时使用 |
|----------|---------|------------|
|核磁共振| `submit_nmr_workflow` |用于结构验证的预测 1H/13C 化学位移 |
|离子淌度| `submit_ion_mobility_workflow` |用于 MS 方法开发的碰撞截面 (CCS) |
|氢键强度| `submit_hydrogen_bond_basicity_workflow` |配方/溶解度的氢键供体/受体强度|
|福井| `submit_fukui_workflow` |亲电/亲核攻击的位点反应指数|
|交互能量分解| `submit_interaction_energy_decomposition_workflow` |片段级相互作用分析|

### 结合自由能

|工作流程|功能|何时使用|
|----------|---------|------------|
| RBFE/FEP | `submit_relative_binding_free_energy_perturbation_workflow` |同属系列的相对ΔΔG |
| RBFE 图 | `submit_rbfe_graph_workflow` |构建和优化 RBFE 扰动网络 |

### 序列和结构生物学

|工作流程|功能|何时使用|
|----------|---------|------------|
| MSA | `submit_msa_workflow` |用于共折叠的多序列比对（ColabFold、Chai、Boltz）|
|溶剂依赖性顺应器| `submit_solvent_dependent_conformers_workflow` |溶剂感知的符合异构体集合|

## 批量提交和检索

对于库或类似物系列，使用特定的工作流程功能循环提交。通用 `rowan.batch_submit_workflow()` 和 `rowan.submit_workflow()` 函数当前从 API 返回 422 错误 - 请改用命名函数（`submit_descriptors_workflow`、`submit_pka_workflow` 等）。

### 提交批次

```python
smileses = ["CCO", "CC(=O)O", "c1ccccc1O"]
names = ["ethanol", "acetic acid", "phenol"]

workflows = [
    rowan.submit_descriptors_workflow(smi, name=name)
    for smi, name in zip(smileses, names)
]

print(f"Submitted {len(workflows)} workflows")
```

### 轮询批次状态

```python
statuses = rowan.batch_poll_status([wf.uuid for wf in workflows])
# Returns aggregate counts — not per-UUID:
# {'queued': 0, 'running': 1, 'complete': 2, 'failed': 0, 'total': 3, ...}

if statuses["complete"] == statuses["total"]:
    print("All workflows done")
elif statuses["failed"] > 0:
    print(f"{statuses['failed']} workflows failed")
```

### 检索和收集结果

```python
results = []
for wf in workflows:
    try:
        result = wf.result()
        results.append(result.data)
    except rowan.WorkflowError as e:
        print(f"Workflow {wf.uuid} failed: {e}")

# Optionally aggregate into DataFrame
import pandas as pd
df = pd.DataFrame(results)
```

### 非阻塞/触发和检查模式

对于您不想保持流程打开的长时间运行的工作流程，请提交工作流程，保存其UUID，并稍后在单独的流程中检查。

* *会话 1 — 提交并保存 UUID：**

```python
import rowan, json

rowan.api_key = "..."
smileses = ["CCO", "CC(=O)O", "c1ccccc1O"]

workflows = [
    rowan.submit_descriptors_workflow(smi, name=f"compound_{i}")
    for i, smi in enumerate(smileses)
]

# Save UUIDs to disk (or a database)
uuids = [wf.uuid for wf in workflows]
with open("workflow_uuids.json", "w") as f:
    json.dump(uuids, f)

print("Submitted. Check back later.")
```

* *会话 2 — 检查状态并在准备就绪时收集结果：**

```python
import rowan, json

rowan.api_key = "..."

with open("workflow_uuids.json") as f:
    uuids = json.load(f)

results = []
for uuid in uuids:
    wf = rowan.retrieve_workflow(uuid)
    if wf.done():
        result = wf.result(wait=False)
        results.append({"uuid": uuid, "data": result.data})
    else:
        print(f"{uuid}: still running ({wf.status})")

print(f"Collected {len(results)} completed results")
```

## Webhooks 和异步工作流程

对于长时间运行的活动或当您不想保持流程处于活动状态时，请使用 Webhooks 在工作流程发生时通知您的后端完成.

### 设置 webhooks

每个工作流提交函数都接受一个 `webhook_url` 参数：

```python
wf = rowan.submit_docking_workflow(
    protein=protein,
    pocket=pocket,
    initial_molecule="CCO",
    webhook_url="https://myserver.com/rowan_callback",
    name="docking with webhook",
)

print(f"Workflow submitted. Result will be POSTed to webhook when complete.")
```

Webhook URL 可以传递到任何特定的工作流函数（`submit_docking_workflow()`、`submit_pka_workflow()`、`submit_descriptors_workflow()`、等）。

### Webhook 身份验证与机密

Rowan 支持 Webhook 签名验证以确保请求是真实的。您需要：

1. **创建或检索 Webhook 密钥：**

```python
import rowan

# Create a new webhook secret
secret = rowan.create_webhook_secret()
print(f"Your webhook secret: {secret.secret}")

# Or retrieve an existing secret
secret = rowan.get_webhook_secret()

# Rotate your secret (invalidates old one, creates new)
new_secret = rowan.rotate_webhook_secret()
```

2. **验证传入的 Webhook 请求：**

```python
import rowan
import hmac
import json

def verify_webhook(request_body: bytes, signature: str, secret: str) -> bool:
    """Verify the HMAC-SHA256 signature of a webhook request."""
    return rowan.verify_webhook_secret(request_body, signature, secret)
```

### Webhook 负载和签名

当工作流程完成时，Rowan 将 JSON 负载发送到您的 Webhook URL，其标头为：

```text
X-Rowan-Signature: <HMAC-SHA256 signature>
```

请求正文包含完整的工作流程结果：

```json
{
  "workflow_uuid": "wf_12345abc",
  "workflow_type": "docking",
  "workflow_name": "lead docking",
  "status": "COMPLETED_OK",
  "created_at": "2025-04-01T12:00:00Z",
  "completed_at": "2025-04-01T12:15:30Z",
  "data": {
    "scores": [-8.2, -8.0, -7.9],
    "best_pose": {...},
    "metadata": {...}
  }
}
```

### 具有签名验证功能的示例 Webhook 处理程序 (FastAPI)

```python
from fastapi import FastAPI, Request, HTTPException
import rowan
import json

app = FastAPI()
_ws = rowan.get_webhook_secret() or rowan.create_webhook_secret()
webhook_secret = _ws.secret

@app.post("/rowan_callback")
async def handle_rowan_webhook(request: Request):
    # Get request body and signature
    body = await request.body()
    signature = request.headers.get("X-Rowan-Signature")

    if not signature:
        raise HTTPException(status_code=400, detail="Missing X-Rowan-Signature header")

    # Verify signature
    if not rowan.verify_webhook_secret(body, signature, webhook_secret):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    # Parse and process
    payload = json.loads(body)
    wf_uuid = payload["workflow_uuid"]
    status = payload["status"]

    if status == "COMPLETED_OK":
        print(f"Workflow {wf_uuid} succeeded!")
        result_data = payload["data"]
        # Process result, update database, trigger next workflow, etc.
    elif status == "FAILED":
        print(f"Workflow {wf_uuid} failed!")
        # Handle failure

    # Respond quickly to prevent retries
    return {"status": "received"}
```

### Webhook 最佳实践

- **始终使用 `rowan.verify_webhook_secret()` 验证签名**，以确保请求来自Rowan
- **快速响应**（< 5 秒）；将繁重的处理卸载到异步任务或后台作业
- **实现幂等性**：工作流程可以重试；使用 `workflow_uuid`
 优雅地处理重复的有效负载 - **记录所有事件**以进行调试和审计跟踪
 - **用于长期活动**：webhooks 具有 50 多个工作流程；对于小型作业，使用 `result()` 进行轮询更简单
- **定期轮换机密** 使用 `rowan.rotate_webhook_secret()` 确保安全
- **返回 2xx 状态** 以确认接收； Rowan 可能会重试 5xx 错误

## 蛋白质实用程序

### 上传蛋白质

```python
# From local PDB file
protein = rowan.upload_protein(
    name="egfr_kinase_domain",
    file_path="egfr_kinase.pdb",
)

# From PDB database
protein_from_pdb = rowan.create_protein_from_pdb_id(
    name="CDK2 (1M17)",
    code="1M17",
)

# Retrieve previously uploaded protein
protein = rowan.retrieve_protein("protein-uuid")

# List all proteins
my_proteins = rowan.list_proteins()
```

### 蛋白质制备指南

- **文件格式**：PDB、mmCIF（Rowan自动检测）
- **水分子**：Rowan通常保留相关水；如果需要的话，预先除去大量水
- **杂原子**：通常保留辅因子、离子和结合的配体；上传前删除不需要的杂原子
- **多链蛋白质**：完全支持
- **分辨率**：适用于NMR结构、同源模型和冷冻电镜；质量对于下游预测很重要
- **验证**：Rowan 验证 PDB 语法；严重畸形的文件可能会被拒绝

## 端到端示例：先导优化活动

此示例演示了优化命中化合物的实际工作流程：

```python
import rowan
import pandas as pd

# 1. Create a project and folder for organization
project = rowan.create_project(name="CDK2 Hit Optimization")
rowan.set_project("CDK2 Hit Optimization")
folder = rowan.create_folder(name="round_1_tautomers_and_pka")

# 2. Load hit compound and analogues
hit = "CCNc1ncc(c(Nc2ccc(F)cc2)n1)-c1cccnc1"  # Known hit
analogues = [
    "CCNc1ncc(c(Nc2ccccc2)n1)-c1cccnc1",      # Remove F
    "CCNc1ncc(c(Nc2ccc(Cl)cc2)n1)-c1cccnc1",  # Cl instead of F
    "CCC(C)Nc1ncc(c(Nc2ccc(F)cc2)n1)-c1cccnc1",  # Propyl instead of ethyl
]

# 3. Determine best tautomers (just in case)
print("Searching tautomeric forms...")
taut_workflows = [
    rowan.submit_tautomer_search_workflow(
        smi, name=f"analog_{i}", folder=folder,
    )
    for i, smi in enumerate(analogues)
]

best_tautomers = []
for wf in taut_workflows:
    result = wf.result()
    best_tautomers.append(result.best_tautomer)

# 4. Predict pKa and basic properties for all analogues
print("Predicting pKa and properties...")
pka_workflows = [
    rowan.submit_pka_workflow(
        smi, method="chemprop_nevolianis2025", name=f"pka_{i}", folder=folder,
    )
    for i, smi in enumerate(best_tautomers)
]

descriptor_workflows = [
    rowan.submit_descriptors_workflow(smi, name=f"desc_{i}", folder=folder)
    for i, smi in enumerate(best_tautomers)
]

# 5. Collect results
pka_results = []
for wf in pka_workflows:
    try:
        result = wf.result()
        pka_results.append({
            "compound": wf.name,
            "pka": result.strongest_acid,  # pKa of the strongest acid site
            "uuid": wf.uuid,
        })
    except rowan.WorkflowError as e:
        print(f"pKa prediction failed for {wf.name}: {e}")

descriptor_results = []
for wf in descriptor_workflows:
    try:
        result = wf.result()
        desc = result.descriptors
        descriptor_results.append({
            "compound": wf.name,
            "mw": desc.get("MW"),
            "logp": desc.get("SLogP"),
            "hba": desc.get("nHBAcc"),
            "hbd": desc.get("nHBDon"),
            "uuid": wf.uuid,
        })
    except rowan.WorkflowError as e:
        print(f"Descriptor calculation failed for {wf.name}: {e}")

# 6. Merge and summarize
df_pka = pd.DataFrame(pka_results)
df_desc = pd.DataFrame(descriptor_results)
df = df_pka.merge(df_desc, on="compound", how="outer")

print("\n=== Preliminary SAR ===")
print(df.to_string())

# 7. Select promising compound for docking
# compound names are "pka_0", "pka_1", etc. — extract index to look up SMILES
top_idx = int(df.loc[df["pka"].idxmin(), "compound"].split("_")[1])
top_smiles = best_tautomers[top_idx]

print(f"\nProceeding with docking: {top_smiles}")

# 8. Docking campaign
protein = rowan.create_protein_from_pdb_id(name="CDK2_1CKP", code="1CKP")
pocket = {"center": [10.5, 24.2, 31.8], "size": [18.0, 18.0, 18.0]}

docking_wf = rowan.submit_docking_workflow(
    protein=protein,
    pocket=pocket,
    initial_molecule=top_smiles,
    do_pose_refinement=True,
    name=f"docking_{top_compound}",
)

dock_result = docking_wf.result()
print(f"\nDocking score: {dock_result.scores[0]:.2f} kcal/mol")
print(f"Best pose saved to: best_pose.pdb")
dock_result.best_pose.write("best_pose.pdb")
```

## 错误处理和故障排除

### 常见错误和解决方案

```python
import rowan

# Error 1: Invalid SMILES
try:
    wf = rowan.submit_descriptors_workflow("CCCC(CC", name="bad smiles")  # Invalid
except rowan.ValidationError as e:
    print(f"Invalid SMILES: {e}")
    # Solution: Use RDKit to validate before submission
    from rdkit import Chem
    smi = Chem.MolToSmiles(Chem.MolFromSmiles(smi))

# Error 2: API key not set
try:
    wf = rowan.submit_descriptors_workflow("CCO")
except rowan.AuthenticationError:
    print("API key not found. Set ROWAN_API_KEY env var or call rowan.api_key = '...'")

# Error 3: Insufficient credits
try:
    wf = rowan.submit_protein_cofolding_workflow(...)
except rowan.InsufficientCreditsError as e:
    print(f"Not enough credits: {e}. Purchase more or reduce job size.")

# Error 4: Workflow failed (bad molecule, etc.)
try:
    wf = rowan.submit_docking_workflow(...)
    result = wf.result()
except rowan.WorkflowError as e:
    print(f"Workflow failed: {e}")
    # Check wf.status for details
    print(f"Status: {wf.status}")

# Error 5: Workflow not yet done — poll manually
result = wf.result(wait=True, poll_interval=5)  # waits and polls every 5s
# Or check status without blocking:
if not wf.done():
    print("Workflow still running. Call wf.result() again later.")
```

### 调试技巧

- **检查工作流程状态**：`wf.status`，检查`wf.done()`，或调用`wf.get_status()`
- **检查原始结果**：`result.data`而不是方便属性
- **重新运行失败的工作流程**：保存UUID并使用`rowan.retrieve_workflow(uuid)`
重试- **预先验证分子**：在批量提交之前使用RDKit或Chemaxon

## 推荐的使用模式

- **优先使用 Rowan 原生工作流程**，而不是存在低级程序集
- **使用项目和文件夹**进行任何重要的活动（>5 个工作流程）
- **使用 `result()` 阻止直到完成**（默认：`wait=True, poll_interval=5`）
- **首先使用类型化结果属性**，回退到`.data` 用于未映射的字段
- **对化合物库或类似物系列使用批量提交**
- **用于多步骤化学活动的链工作流程**：
  - `pKa → macropKa → permeability`（ADME 评估）
  - `tautomer search → docking → pose-analysis MD`（姿势细化）
  - `MSA generation → protein-ligand cofolding`（AI 结构预测）
- **使用 webhooks** 进行长期运行的活动（> 50 个工作流程）或异步管道
- **使用流式**进行大型整合器/对接搜索的交互式反馈

## 总结

当您的工作流程需要云执行分子设计任务时，尤其是当您需要时，请使用 Rowan一个统一的 API 和跨小分子建模、蛋白质、对接、ADME 预测和 ML 结构生成的一致结果处理。

Rowan 是一个分子设计工作流程平台，而不仅仅是一个远程化学引擎。它可以处理基础设施扩展、结果持久性和多步骤管道编排，以便您可以专注于科学。
