---
name: glycoengineering
description: 分析和设计蛋白质糖基化。扫描 N-糖基化序列 (N-X-S/T)的序列，预测 O-糖基化热点，并访问精选的 glycoengineering 工具（NetOGlyc、GlycoShield、GlycoWorkbench）。用于糖蛋白工程、治疗性抗体优化和疫苗设计。
license: Unknown
metadata:
    skill-author: Kuan-lin Huang
---

# 糖工程

## 概述

糖基化是最常见、最复杂的蛋白质翻译后修饰 (PTM)，影响超过 50% 的人类蛋白质。聚糖调节蛋白质折叠、稳定性、免疫识别、受体相互作用和治疗性蛋白质的药代动力学。 Glycoengineering 涉及合理修饰糖基化模式，以提高治疗效果、稳定性或免疫逃避。

* *两种主要糖基化类型：**
- **N-糖基化**：连接到序列子 N-X-[S/T]中的天冬酰胺 (N)，其中 X ≠ 脯氨酸；发生在 ER/Golgi
- **O-糖基化**：连接丝氨酸 (S)或苏氨酸 (T)；没有严格的共识主题；主要是 GalNAc 起始

## 何时使用此技能

在以下情况下使用此技能：

- **抗体工程**：优化 Fc 糖基化以增强 ADCC、CDC 或降低免疫原性
- **治疗性蛋白质设计**：识别影响半衰期、稳定性或免疫原性的糖基化位点
- **疫苗抗原设计**：工程聚糖屏蔽将免疫反应集中在保守表位
- **生物仿制药表征**：比较参考和生物仿制药之间的聚糖模式
- **药物靶标分析**：糖基化是否会影响受体的靶标结合？
- **蛋白质稳定性**：N-聚糖通常稳定蛋白质；识别稳定突变位点

## N-糖基化序列分析

### 扫描 N-糖基化位点

N-糖基化发生在序列子 **N-X-[S/T]** 处，其中 X ≠ Proline.

```python
import re
from typing import List, Tuple

def find_n_glycosylation_sequons(sequence: str) -> List[dict]:
    """
    Scan a protein sequence for canonical N-linked glycosylation sequons.
    Motif: N-X-[S/T], where X ≠ Proline.

    Args:
        sequence: Single-letter amino acid sequence

    Returns:
        List of dicts with position (1-based), motif, and context
    """
    seq = sequence.upper()
    results = []
    i = 0
    while i <= len(seq) - 3:
        triplet = seq[i:i+3]
        if triplet[0] == 'N' and triplet[1] != 'P' and triplet[2] in {'S', 'T'}:
            context = seq[max(0, i-3):i+6]  # ±3 residue context
            results.append({
                'position': i + 1,   # 1-based
                'motif': triplet,
                'context': context,
                'sequon_type': 'NXS' if triplet[2] == 'S' else 'NXT'
            })
            i += 3
        else:
            i += 1
    return results

def summarize_glycosylation_sites(sequence: str, protein_name: str = "") -> str:
    """Generate a research log summary of N-glycosylation sites."""
    sequons = find_n_glycosylation_sequons(sequence)

    lines = [f"# N-Glycosylation Sequon Analysis: {protein_name or 'Protein'}"]
    lines.append(f"Sequence length: {len(sequence)}")
    lines.append(f"Total N-glycosylation sequons: {len(sequons)}")

    if sequons:
        lines.append(f"\nN-X-S sites: {sum(1 for s in sequons if s['sequon_type'] == 'NXS')}")
        lines.append(f"N-X-T sites: {sum(1 for s in sequons if s['sequon_type'] == 'NXT')}")
        lines.append(f"\nSite details:")
        for s in sequons:
            lines.append(f"  Position {s['position']}: {s['motif']} (context: ...{s['context']}...)")
    else:
        lines.append("No canonical N-glycosylation sequons detected.")

    return "\n".join(lines)

# Example: IgG1 Fc region
fc_sequence = "APELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK"
print(summarize_glycosylation_sites(fc_sequence, "IgG1 Fc"))
```

### 突变 N-糖基化位点

```python
def eliminate_glycosite(sequence: str, position: int, replacement: str = "Q") -> str:
    """
    Eliminate an N-glycosylation site by substituting Asn → Gln (conservative).

    Args:
        sequence: Protein sequence
        position: 1-based position of the Asn to mutate
        replacement: Amino acid to substitute (default Q = Gln; similar size, not glycosylated)

    Returns:
        Mutated sequence
    """
    seq = list(sequence.upper())
    idx = position - 1
    assert seq[idx] == 'N', f"Position {position} is '{seq[idx]}', not 'N'"
    seq[idx] = replacement.upper()
    return ''.join(seq)

def add_glycosite(sequence: str, position: int, flanking_context: str = "S") -> str:
    """
    Introduce an N-glycosylation site by mutating a residue to Asn,
    and ensuring X ≠ Pro and +2 = S/T.

    Args:
        position: 1-based position to introduce Asn
        flanking_context: 'S' or 'T' at position+2 (if modification needed)
    """
    seq = list(sequence.upper())
    idx = position - 1

    # Mutate to Asn
    seq[idx] = 'N'

    # Ensure X+1 != Pro (mutate to Ala if needed)
    if idx + 1 < len(seq) and seq[idx + 1] == 'P':
        seq[idx + 1] = 'A'

    # Ensure X+2 = S or T
    if idx + 2 < len(seq) and seq[idx + 2] not in ('S', 'T'):
        seq[idx + 2] = flanking_context

    return ''.join(seq)
```

## O-糖基化分析

### 启发式 O-糖基化热点预测

```python
def predict_o_glycosylation_hotspots(
    sequence: str,
    window: int = 7,
    min_st_fraction: float = 0.4,
    disallow_proline_next: bool = True
) -> List[dict]:
    """
    Heuristic O-glycosylation hotspot scoring based on local S/T density.
    Not a substitute for NetOGlyc; use as fast baseline.

    Rules:
    - O-GalNAc glycosylation clusters on Ser/Thr-rich segments
    - Flag Ser/Thr residues in windows enriched for S/T
    - Avoid S/T immediately followed by Pro (TP/SP motifs inhibit GalNAc-T)

    Args:
        window: Odd window size for local S/T density
        min_st_fraction: Minimum fraction of S/T in window to flag site
    """
    if window % 2 == 0:
        window = 7
    seq = sequence.upper()
    half = window // 2
    candidates = []

    for i, aa in enumerate(seq):
        if aa not in ('S', 'T'):
            continue
        if disallow_proline_next and i + 1 < len(seq) and seq[i+1] == 'P':
            continue

        start = max(0, i - half)
        end = min(len(seq), i + half + 1)
        segment = seq[start:end]
        st_count = sum(1 for c in segment if c in ('S', 'T'))
        frac = st_count / len(segment)

        if frac >= min_st_fraction:
            candidates.append({
                'position': i + 1,
                'residue': aa,
                'st_fraction': round(frac, 3),
                'window': f"{start+1}-{end}",
                'segment': segment
            })

    return candidates
```

## 外部Glycoengineering工具

### 1. NetOGlyc 4.0（O-糖基化预测）

用于高精度 O-GalNAc 位点预测的 Web 服务：
- **URL**：https://services.healthtech.dtu.dk/services/NetOGlyc-4.0/
- **输入**：FASTA 蛋白质序列
- **输出**：每个残基 O-糖基化概率分数
- **方法**：经过训练的神经网络在经过实验验证的 O-GalNAc 位点上

```python
import requests

def submit_netoglycv4(fasta_sequence: str) -> str:
    """
    Submit sequence to NetOGlyc 4.0 web service.
    Returns the job URL for result retrieval.

    Note: This uses the DTU Health Tech web service. Results take ~1-5 min.
    """
    url = "https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi"
    # NetOGlyc submission (parameters may vary with web service version)
    # Recommend using the web interface directly for most use cases
    print("Submit sequence at: https://services.healthtech.dtu.dk/services/NetOGlyc-4.0/")
    return url

# Also: NetNGlyc for N-glycosylation prediction
# URL: https://services.healthtech.dtu.dk/services/NetNGlyc-1.0/
```

### 2. GlycoShield-MD（聚糖屏蔽分析）

GlycoShield-MD 分析聚糖在 MD 模拟过程中如何屏蔽蛋白质表面：
- **URL**： https://gitlab.mpcdf.mpg.de/dioscuri-biophysicals/glycoshield-md/
- **使用**：在MD轨迹上映射蛋白质表面上的聚糖屏蔽
- **输出**：每个残基屏蔽分数，可视化

```bash
# Installation
pip install glycoshield

# Basic usage: analyze glycan shielding from glycosylated protein MD trajectory
glycoshield \
    --topology glycoprotein.pdb \
    --trajectory glycoprotein.xtc \
    --glycan_resnames BGLCNA FUC \
    --output shielding_analysis/
```

### 3. GlycoWorkbench（聚糖结构绘图/分析）

- **URL**：https://www.eurocarbdb.org/project/glycoworkbench
- **用途**：绘制聚糖结构、计算质量、注释 MS 谱
- **格式**：GlycoCT、IUPAC 缩合聚糖表示法

### 4. GlyConnect（聚糖-蛋白质）数据库）

- **URL**：https://glyconnect.expasy.org/
- **用途**：查找经过实验验证的糖蛋白和糖基化位点
- **查询**：通过蛋白质（UniProt ID）、聚糖结构或组织

```python
import requests

def query_glyconnect(uniprot_id: str) -> dict:
    """Query GlyConnect for glycosylation data for a protein."""
    url = f"https://glyconnect.expasy.org/api/proteins/uniprot/{uniprot_id}"
    response = requests.get(url, headers={"Accept": "application/json"})
    if response.status_code == 200:
        return response.json()
    return {}

# Example: query EGFR glycosylation
egfr_glyco = query_glyconnect("P00533")
```

### 5. UniCarbKB（聚糖结构数据库）

- **URL**：https://unicarbkb.org/
- **使用**：浏览聚糖结构，按质量或组成搜索
- **格式**：GlycoCT 或 IUPAC 表示法

## 关键 Glycoengineering 策略

### 用于治疗性抗体

|目标|战略|注释 |
|------|---------|--------|
|增强 ADCC | Fc Asn297 的去岩藻糖基化 |无岩藻糖基化 IgG1 与 FcγRIIIa 的结合能力提高约 50 倍 |
|降低免疫原性 |去除非人类聚糖 |消除 α-Gal、NGNA 表位 |
|提高 PK 半衰期 |唾液酸化 |唾液酸化聚糖延长半衰期 |
|减少炎症 |过度唾液酸化 | IVIG抗炎机制|
|创建聚糖盾|添加 N-糖基化位点到表面 |掩盖易受攻击的表位（疫苗设计）|

### 使用的常见突变

|突变|效果|
|----------|--------|
| N297A/Q (IgG1) | N297A/Q (IgG1) |去除 Fc 糖基化（无糖基）|
| N297D (IgG1) |去除 Fc 糖基化 |
| S298A/E333A/K334A |增加 FcγRIIIa 结合 |
| F243L (IgG1) |增加去岩藻糖基化 |
| T299A |删除 Fc 糖基化 |

## 聚糖表示法

#### IUPAC 简写表示法（单糖缩写）

|符号|全名 |型号 |
|--------|------------|------|
|葡萄糖|葡萄糖 |己糖|
| GlcNAc | N-乙酰氨基葡萄糖| HexNAc |
|男人|甘露糖|己糖|
|加尔 |半乳糖 |己糖|
|福克 |岩藻糖 |脱氧己糖|
| Neu5Ac | N-乙酰神经氨酸（唾液酸） |唾液酸|
|半乳糖胺 | N-乙酰半乳糖胺 | HexNAc |

### 复杂的 N-聚糖结构

```
Typical complex biantennary N-glycan:
Neu5Ac-Gal-GlcNAc-Man\
                       Man-GlcNAc-GlcNAc-[Asn]
Neu5Ac-Gal-GlcNAc-Man/
(±Core Fuc at innermost GlcNAc)
```

## 最佳实践

- **在实验验证之前从 NetNGlyc/NetOGlyc** 开始进行计算预测
- **使用质谱验证**：糖蛋白组学（Byonic、Mascot）位点特异性聚糖分析
- **考虑位点背景**：并非所有预测的序列子实际上都是糖基化的（可及性、细胞类型、蛋白质构象）
- **对于抗体**：Fc N297 聚糖至关重要 - 始终首先表征该位点
- **使用 GlyConnect** 检查您感兴趣的蛋白质是否已通过实验验证糖基化数据

## 其他资源

- **GlyTouCan**（聚糖结构存储库）：https://glytoucan.org/
- **GlyConnect**：https://glyconnect.expasy.org/
- **CFG 功能性糖组学**：http://www.featureglycomics.org/
- **DTU 健康技术服务器**（NetNGlyc、 NetOGlyc）：https://services.healthtech.dtu.dk/
- **GlycoWorkbench**：https://glycoworkbench.software.informer.com/
- **评论**：Apweiler R 等人。 (1999) Biochim 生物物理学法。 PMID：10564035
- **治疗 glycoengineering 评论**：Jefferis R (2009) Nature Reviews Drug Discovery。 PMID：19448661
