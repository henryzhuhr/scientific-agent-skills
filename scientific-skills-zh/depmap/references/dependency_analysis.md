# DepMap 依赖性分析指南

## 了解 Chronos 分数

Chronos 是用于从 CRISPR 筛选数据计算基因依赖性分数的当前 (v5+)算法。它解决了系统偏差，包括：
- 拷贝数效应（由于 DNA 切割，高拷贝基因显得至关重要）
- 引导 RNA 效率变化 
- 细胞系生长速率

### 分数解释

|分数范围|解读 |
|------------------------|----------------|
| > 0 |被敲除后可能会促进生长（一些噪音）|
| 0 至 -0.3 |非必需：健身效果极小|
| -0.3 至 -0.5 |轻度依赖|
| -0.5 至 -1.0 |显着依赖性|
| <-1.0 |强依赖性（共同必需范围）|
| ≈ −1.0 |泛必需基因（例如蛋白酶体亚基）的中位数 |

### 常见必需基因（对照）

几乎所有细胞系中必需的基因（得分 ~−1 至 −2）：
- 核糖体蛋白：RPL...、RPS...
- 蛋白酶体：PSMA...、 PSMB...
- 剪接体：SNRPD1、SNRNP70
- DNA 复制：MCM2、PCNA
- 转录：POLR2A、TAF...

 这些可用作屏幕质量的阳性对照。

### 非必需控制

适应度影响可忽略不计的基因（得分〜0）：
- 非表达基因（组织特异性）
- 安全港位点

## 选择性评估

以确定依赖性是否为癌症选择性：

```python
import pandas as pd
import numpy as np

def compute_selectivity(gene_effect_df, target_gene, cancer_lineage):
    """Compute selectivity score for a cancer lineage."""
    scores = gene_effect_df[target_gene].dropna()

    # Get cell line metadata
    from depmap_utils import load_cell_line_info
    cell_info = load_cell_line_info()
    scores_df = scores.reset_index()
    scores_df.columns = ["DepMap_ID", "score"]
    scores_df = scores_df.merge(cell_info[["DepMap_ID", "lineage"]])

    cancer_scores = scores_df[scores_df["lineage"] == cancer_lineage]["score"]
    other_scores = scores_df[scores_df["lineage"] != cancer_lineage]["score"]

    # Selectivity: lower mean in cancer lineage vs others
    selectivity = other_scores.mean() - cancer_scores.mean()
    return {
        "target_gene": target_gene,
        "cancer_lineage": cancer_lineage,
        "cancer_mean": cancer_scores.mean(),
        "other_mean": other_scores.mean(),
        "selectivity_score": selectivity,
        "n_cancer": len(cancer_scores),
        "fraction_dependent": (cancer_scores < -0.5).mean()
    }
```

## CRISPR 数据集版本

|数据集 |描述 |推荐|
|------|--------------|----------|
| `CRISPRGeneEffect` |时间校正基因效应|是（当前）|
| `Achilles_gene_effect` |较旧的 CERES 算法 |仅旧版|
| `RNAi_merged` | DEMETER2 RNAi |用于交叉验证 |

## 质量指标

DepMap 报告每个屏幕的质量控制指标：
- **偏度**：泛必需基因应显示负偏度
- **AUC**：泛必需与非必需对照的 ROC 下面积

 良好屏幕：偏度 < -1，AUC > 0.85

## 癌症谱系代码

`sample_info.csv`中`lineage`字段的常用值：

|血统 |描述 |
|---------|-------------|
| `lung` |肺癌|
| `breast` |乳腺癌|
| `colorectal` |结直肠癌|
| `brain_cancer` |脑癌（GBM等）|
| `leukemia` |白血病|
| `lymphoma` |淋巴瘤|
| `prostate` |前列腺癌|
| `ovarian` |卵巢癌|
| `pancreatic` |胰腺癌|
| `skin` |黑色素瘤及其他皮肤|
| `liver` |肝癌|
| `kidney` |肾癌 |

## 合成致死率分析

```python
import pandas as pd
import numpy as np
from scipy import stats

def find_synthetic_lethal(gene_effect_df, mutation_df, biomarker_gene,
                           fdr_threshold=0.1):
    """
    Find synthetic lethal partners for a loss-of-function mutation.

    For each gene, tests if cell lines mutant in biomarker_gene
    are more dependent on that gene vs. WT lines.
    """
    if biomarker_gene not in mutation_df.columns:
        return pd.DataFrame()

    # Get mutant vs WT cell lines
    common = gene_effect_df.index.intersection(mutation_df.index)
    is_mutant = mutation_df.loc[common, biomarker_gene] == 1

    mutant_lines = common[is_mutant]
    wt_lines = common[~is_mutant]

    results = []
    for gene in gene_effect_df.columns:
        mut_scores = gene_effect_df.loc[mutant_lines, gene].dropna()
        wt_scores = gene_effect_df.loc[wt_lines, gene].dropna()

        if len(mut_scores) < 5 or len(wt_scores) < 10:
            continue

        stat, pval = stats.mannwhitneyu(mut_scores, wt_scores, alternative='less')
        results.append({
            "gene": gene,
            "mean_mutant": mut_scores.mean(),
            "mean_wt": wt_scores.mean(),
            "effect_size": wt_scores.mean() - mut_scores.mean(),
            "pval": pval,
            "n_mutant": len(mut_scores),
            "n_wt": len(wt_scores)
        })

    df = pd.DataFrame(results)
    # FDR correction
    from scipy.stats import false_discovery_control
    df["qval"] = false_discovery_control(df["pval"], method="bh")
    df = df[df["qval"] < fdr_threshold].sort_values("effect_size", ascending=False)
    return df
```

## 药物敏感性 (PRISM)

DepMap 还包含来自 PRISM 测定的化合物敏感性数据：

```python
import pandas as pd

def load_prism_data(filepath="primary-screen-replicate-collapsed-logfold-change.csv"):
    """
    Load PRISM drug sensitivity data.
    Rows = cell lines, Columns = compounds (broad_id::name::dose)
    Values = log2 fold change (more negative = more sensitive)
    """
    return pd.read_csv(filepath, index_col=0)

# Available datasets:
# primary-screen: 4,518 compounds at single dose
# secondary-screen: ~8,000 compounds at multiple doses (AUC available)
```
