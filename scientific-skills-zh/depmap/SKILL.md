---
name: depmap
description: 查询癌症依赖性图谱 (DepMap)以获取癌细胞系基因依赖性评分 (CRISPR Chronos)、药物敏感性数据和基因效应概况。用于识别癌症特定的脆弱性、合成致死相互作用以及验证肿瘤药物靶点。
license: CC-BY-4.0
metadata:
    skill-author: Kuan-lin Huang
---

# DepMap — 癌症依赖性图谱 

## 概述

癌症依赖性图谱 (DepMap)项目由布罗德研究所 (Broad Institute)运行，利用全基因组 CRISPR 敲除筛选 (DepMap CRISPR)、RNA 干扰 (RNAi)和化合物敏感性测定，系统地表征数百种癌细胞系的遗传依赖性（棱镜）。 DepMap 数据对于以下方面至关重要：
- 识别哪些基因对于特定癌症类型至关重要 
- 寻找癌症选择性依赖性（治疗靶点）
- 验证肿瘤药物靶标
- 发现合成致死相互作用

* *关键资源：**
- DepMap Portal：https://depmap.org/portal/
- DepMap 数据下载：https://depmap.org/portal/download/all/
- Python 包：`depmap`（或通过 API/downloads 访问）
- API： https://depmap.org/portal/api/

## 何时使用此技能

在以下情况下使用 DepMap：

- **目标验证**：是否具有特定突变（例如 KRAS 突变）的癌细胞系中生存所必需的基因？
- **生物标志物发现**：哪些基因组特征预测对敲除的敏感性
- **合成致死性**：查找当另一个基因突变/删除时选择性必需的基因
- **药物敏感性**：哪些细胞系特征可以预测对化合物的反应？
- **泛癌必需性**：基因是在所有癌症类型中广泛必需的（不良靶标）还是选择性必需的？
- **相关性分析**：哪些基因对具有相关的依赖性特征（同本质）？

## 核心概念

### 依赖性评分

|分数 |范围 |含义 |
|-------|--------|---------|
| **Chronos** (CRISPR) | ~ -3 到 0+ |越消极=越重要。共同的基本阈值：-1。泛必需基因 ~−1 至 −2 |
| **RNAi DEMETER2** | ~ -3 到 0+ |与 Chronos |
| 类似的规模**基因效应** |归一化 |归一化的时间； −1 = 常见必需基因的中位效应 |

* *关键阈值：**
- Chronos ≤ -0.5：可能依赖 
- Chronos ≤ -1：强烈依赖（常见必需范围）

### 细胞系注释

每个细胞系具有：
- `DepMap_ID`：唯一标识符（例如，`ACH-000001`）
- `cell_line_name`：人类可读的名称
- `primary_disease`：癌症类型
- `lineage`：广泛的组织谱系
- `lineage_subtype`：特定subtype

## 核心功能

### 1. DepMap API

```python
import requests
import pandas as pd

BASE_URL = "https://depmap.org/portal/api"

def depmap_get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
```

### 2. 基因依赖性评分

```python
def get_gene_dependency(gene_symbol, dataset="Chronos_Combined"):
    """Get CRISPR dependency scores for a gene across all cell lines."""
    url = f"{BASE_URL}/gene"
    params = {
        "gene_id": gene_symbol,
        "dataset": dataset
    }
    response = requests.get(url, params=params)
    return response.json()

# Alternatively, use the /data endpoint:
def get_dependencies_slice(gene_symbol, dataset_name="CRISPRGeneEffect"):
    """Get a gene's dependency slice from a dataset."""
    url = f"{BASE_URL}/data/gene_dependency"
    params = {"gene_name": gene_symbol, "dataset_name": dataset_name}
    response = requests.get(url, params=params)
    data = response.json()
    return data
```

### 3. 基于下载的分析（推荐用于大型查询）

对于大规模分析，下载DepMap数据文件并在本地分析：

```python
import pandas as pd
import requests, os

def download_depmap_data(url, output_path):
    """Download a DepMap data file."""
    response = requests.get(url, stream=True)
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

# DepMap 24Q4 data files (update version as needed)
FILES = {
    "crispr_gene_effect": "https://figshare.com/ndownloader/files/...",
    # OR download from: https://depmap.org/portal/download/all/
    # Files available:
    # CRISPRGeneEffect.csv - Chronos gene effect scores
    # OmicsExpressionProteinCodingGenesTPMLogp1.csv - mRNA expression
    # OmicsSomaticMutationsMatrixDamaging.csv - mutation binary matrix
    # OmicsCNGene.csv - copy number
    # sample_info.csv - cell line metadata
}

def load_depmap_gene_effect(filepath="CRISPRGeneEffect.csv"):
    """
    Load DepMap CRISPR gene effect matrix.
    Rows = cell lines (DepMap_ID), Columns = genes (Symbol (EntrezID))
    """
    df = pd.read_csv(filepath, index_col=0)
    # Rename columns to gene symbols only
    df.columns = [col.split(" ")[0] for col in df.columns]
    return df

def load_cell_line_info(filepath="sample_info.csv"):
    """Load cell line metadata."""
    return pd.read_csv(filepath)
```

### 4.识别选择性依赖性

```python
import numpy as np
import pandas as pd

def find_selective_dependencies(gene_effect_df, cell_line_info, target_gene,
                                 cancer_type=None, threshold=-0.5):
    """Find cell lines selectively dependent on a gene."""

    # Get scores for target gene
    if target_gene not in gene_effect_df.columns:
        return None

    scores = gene_effect_df[target_gene].dropna()
    dependent = scores[scores <= threshold]

    # Add cell line info
    result = pd.DataFrame({
        "DepMap_ID": dependent.index,
        "gene_effect": dependent.values
    }).merge(cell_line_info[["DepMap_ID", "cell_line_name", "primary_disease", "lineage"]])

    if cancer_type:
        result = result[result["primary_disease"].str.contains(cancer_type, case=False, na=False)]

    return result.sort_values("gene_effect")

# Example usage (after loading data)
# df_effect = load_depmap_gene_effect("CRISPRGeneEffect.csv")
# cell_info = load_cell_line_info("sample_info.csv")
# deps = find_selective_dependencies(df_effect, cell_info, "KRAS", cancer_type="Lung")
```

### 5.生物标志物分析（基因效应与基因效应）突变）

```python
import pandas as pd
from scipy import stats

def biomarker_analysis(gene_effect_df, mutation_df, target_gene, biomarker_gene):
    """
    Test if mutation in biomarker_gene predicts dependency on target_gene.

    Args:
        gene_effect_df: CRISPR gene effect DataFrame
        mutation_df: Binary mutation DataFrame (1 = mutated)
        target_gene: Gene to assess dependency of
        biomarker_gene: Gene whose mutation may predict dependency
    """
    if target_gene not in gene_effect_df.columns or biomarker_gene not in mutation_df.columns:
        return None

    # Align cell lines
    common_lines = gene_effect_df.index.intersection(mutation_df.index)
    scores = gene_effect_df.loc[common_lines, target_gene].dropna()
    mutations = mutation_df.loc[scores.index, biomarker_gene]

    mutated = scores[mutations == 1]
    wt = scores[mutations == 0]

    stat, pval = stats.mannwhitneyu(mutated, wt, alternative='less')

    return {
        "target_gene": target_gene,
        "biomarker_gene": biomarker_gene,
        "n_mutated": len(mutated),
        "n_wt": len(wt),
        "mean_effect_mutated": mutated.mean(),
        "mean_effect_wt": wt.mean(),
        "pval": pval,
        "significant": pval < 0.05
    }
```

### 6. 共本质分析

```python
import pandas as pd

def co_essentiality(gene_effect_df, target_gene, top_n=20):
    """Find genes with most correlated dependency profiles (co-essential partners)."""
    if target_gene not in gene_effect_df.columns:
        return None

    target_scores = gene_effect_df[target_gene].dropna()

    correlations = {}
    for gene in gene_effect_df.columns:
        if gene == target_gene:
            continue
        other_scores = gene_effect_df[gene].dropna()
        common = target_scores.index.intersection(other_scores.index)
        if len(common) < 50:
            continue
        r = target_scores[common].corr(other_scores[common])
        if not pd.isna(r):
            correlations[gene] = r

    corr_series = pd.Series(correlations).sort_values(ascending=False)
    return corr_series.head(top_n)

# Co-essential genes often share biological complexes or pathways
```

## 查询工作流程

### 工作流程1：癌症类型的目标验证

1. 下载`CRISPRGeneEffect.csv`和`sample_info.csv`
2. 按癌症类型 
3 筛选细胞系。计算癌症中目标基因相对于所有其他基因的平均基因效应
4. 计算选择性：对您的癌症类型的依赖性有多具体？
5. 将突变、表达或 CNA 数据作为生物标志物进行交叉引用

### 工作流程 2：合成致死率筛查

1. 鉴定感兴趣基因突变/缺失的细胞系（例如 BRCA1 突变体）
2. 计算突变体与 WT 系 
3 中所有基因的基因效应得分。鉴定突变系（合成致死伙伴）
4 中更为重要的基因。按选择性和效应大小过滤

### 工作流程 3：化合物敏感性分析

1. 下载 PRISM 复合灵敏度数据 (`primary-screen-replicate-treatment-info.csv`)
2. 将化合物 AUC/log2（倍数变化）与基因组特征 
3 相关联。识别化合物敏感性的预测生物标志物

## DepMap 数据文件参考

|文件 |描述 |
|------|--------------|
| `CRISPRGeneEffect.csv` | CRISPR Chronos 基因效应（主要依赖性数据）|
| `CRISPRGeneEffectUnscaled.csv` |未缩放的 CRISPR 分数 |
| `RNAi_merged.csv` | DEMETER2 RNAi 依赖性 |
| `sample_info.csv` |细胞系元数据（谱系、疾病等）|
| `OmicsExpressionProteinCodingGenesTPMLogp1.csv` | mRNA 表达 |
| `OmicsSomaticMutationsMatrixDamaging.csv` |破坏性体细胞突变（二元）|
| `OmicsCNGene.csv` |每个基因的拷贝数|
| `PRISM_Repurposing_Primary_Screens_Data.csv` |药物敏感性（重新利用库） |

从以下位置下载所有文件：https://depmap.org/portal/download/all/

## 最佳实践

- **使用 Chronos 分数**（不是 DEMETER2）进行当前 CRISPR 分析 - 更好地控制切割效率
- **区分泛必需与癌症选择性**：目标基因低方差（在所有细胞系中都是必需的）是较差的药物靶标
- **用表达数据进行验证**：无论实际功能如何，细胞系中未表达的基因都将评分为非必需基因
- **使用 DepMap ID** 进行细胞系识别 - cell_line_name 可能不明确
- **考虑拷贝数**：扩增的基因可能由于以下原因而显得必需拷贝数效应（垃圾 DNA 假设）
- **多重测试校正**：计算全基因组生物标志物关联时，应用 FDR 校正

## 其他资源

- **DepMap 门户**：https://depmap.org/portal/
- **数据下载**：https://depmap.org/portal/download/all/
- **DepMap 论文**：Behan FM 等人。 （2019）自然。 PMID：30971826
- **Chronos 论文**：Dempster JM 等人。 （2021）自然方法。 PMID：34349281
- **GitHub**：https://github.com/broadinstitute/depmap-portal
- **Figshare**：https://figshare.com/articles/dataset/DepMap_24Q4_Public/27993966
