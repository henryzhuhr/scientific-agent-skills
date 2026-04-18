# 聚糖数据库和资源参考

## 主要数据库

### GlyTouCan
- **URL**：https://glytoucan.org/
- **内容**：聚糖结构的唯一登录号 (GTC ID)
- **用途**：跨数据库的标准化聚糖识别
- **格式**：GlycoCT、WURCS、IUPAC

```python
import requests

def lookup_glytoucan(glytoucan_id: str) -> dict:
    """Fetch glycan details from GlyTouCan."""
    url = f"https://api.glytoucan.org/glycan/{glytoucan_id}"
    response = requests.get(url, headers={"Accept": "application/json"})
    return response.json() if response.ok else {}
```

### GlyConnect
- **URL**：https://glyconnect.expasy.org/
- **内容**：具有位点特异性聚糖谱的蛋白质糖基化数据库
- **集成**：链接 UniProt 蛋白质经实验验证的糖基化
- **使用**：查找目标蛋白的已知糖基化

```python
import requests

def get_glycoprotein_info(uniprot_id: str) -> dict:
    """Get glycosylation data for a protein from GlyConnect."""
    base_url = "https://glyconnect.expasy.org/api"
    response = requests.get(f"{base_url}/proteins/uniprot/{uniprot_id}")
    return response.json() if response.ok else {}

def get_glycan_compositions(glyconnect_protein_id: int) -> list:
    """Get all glycan compositions for a GlyConnect protein entry."""
    base_url = "https://glyconnect.expasy.org/api"
    response = requests.get(f"{base_url}/compositions/protein/{glyconnect_protein_id}")
    return response.json().get("data", []) if response.ok else []
```

### UniCarbKB
- **URL**：https://unicarbkb.org/
- **内容**：利用生物技术精心策划的聚糖结构context
- **特征**：组织/细胞类型特异性聚糖数据、质谱数据

### KEGG Glycan
- **URL**：https://www.genome.jp/kegg/glycan/
- **内容**：KEGG 格式的聚糖结构，生物合成通路
- **整合**：链接至聚糖生物合成的KEGG PATHWAY图谱

### CAZy（碳水化合物活性酶）
- **URL**：http://www.cazy.org/
- **内容**：构建、破坏和修饰聚糖的酶
- **用途**：识别 glycoengineering 应用的酶

## 预测服务器

### NetNGlyc 1.0
- **URL**：https://services.healthtech.dtu.dk/services/NetNGlyc-1.0/
- **方法**：N-糖基化位点的神经网络预测
- **输入**：蛋白质FASTA序列
- **输出**：每个天冬酰胺的概率得分；阈值 ~0.5

### NetOGlyc 4.0
- **URL**：https://services.healthtech.dtu.dk/services/NetOGlyc-4.0/
- **方法**：O-GalNAc 糖基化预测的神经网络
- **输入**：蛋白质 FASTA序列
- **输出**：每个丝氨酸/苏氨酸的概率；阈值~0.5

### GlycoMine（机器学习）
- N-、O- 和 C-糖基化的机器学习预测器
- 多种聚糖类型：N-GlcNAc、O-GalNAc、O-GlcNAc、O-Man、O-Fuc、O-Glc、C-Man

### SymLink（糖基化位点和序列子）预测器）
- 物种特异性 N-糖基化预测
- 比简单序列子扫描更具体

## 质谱糖蛋白组学工具

### Byonic（蛋白质指标）
- 从 MS2 谱图进行糖肽从头鉴定
- 综合聚糖数据库
- 位点特异性糖型分配

### 吉祥物聚糖分析
- 聚糖特异性搜索参数
- 自下而上糖蛋白组学的常用

### GlycoWorkbench
- **URL**： https://www.eurocarbdb.org/project/gluworkbench
- 聚糖结构绘图和质量计算
- 聚糖碎片离子的MS/MS 谱注释

### Skyline
- 糖肽的靶向定量
- 与聚糖数据库集成

## 聚糖命名系统

### 牛津表示法（对于 N 聚糖）
将复杂的 N 聚糖编码为文本字符串：
```
G0F   = Core-fucosylated, biantennary, no galactose
G1F   = Core-fucosylated, one galactose
G2F   = Core-fucosylated, two galactoses
G2FS1 = Core-fucosylated, two galactoses, one sialic acid
G2FS2 = Core-fucosylated, two galactoses, two sialic acids
M5    = High mannose 5 (Man5GlcNAc2)
M9    = High mannose 9 (Man9GlcNAc2)
```

### 聚糖符号命名法 (SNFG)
的标准彩色符号出版物：
- 蓝色圆圈=葡萄糖
- 绿色圆圈=甘露糖
- 黄色圆圈=半乳糖
- 蓝色方块=N-乙酰葡糖胺
- 黄色方块=N-乙酰半乳糖胺
- 紫色菱形=N-乙酰神经氨酸（唾液酸）
- 红色三角形 = 岩藻糖

## 治疗性糖蛋白和关键糖基化位点

|治疗 |目标|关键糖基化|功能 |
|-------------|--------|--------------------|---------|
| IgG1 抗体 |各种| N297（FC）| ADCC/CDC效应器功能|
|促红细胞生成素 | EPOR | N24、N38、N83、O-聚糖 |药代动力学|
|依那西普 |肿瘤坏死因子 | N420 (IgG1 Fc) |半条命|
| tPA（阿替普酶）|纤维蛋白 | N117、N184、N448 |纤维蛋白结合|
|因子 VIII |大众汽车 | 25 N-糖基位点 |清仓|

## 批量分析示例

```python
from glycoengineering_tools import find_n_glycosylation_sequons, predict_o_glycosylation_hotspots
import pandas as pd

def analyze_glycosylation_landscape(sequences_dict: dict) -> pd.DataFrame:
    """
    Batch analysis of glycosylation for multiple proteins.

    Args:
        sequences_dict: {protein_name: sequence}

    Returns:
        DataFrame with glycosylation summary per protein
    """
    results = []
    for name, seq in sequences_dict.items():
        n_sites = find_n_glycosylation_sequons(seq)
        o_sites = predict_o_glycosylation_hotspots(seq)

        results.append({
            'protein': name,
            'length': len(seq),
            'n_glycosites': len(n_sites),
            'o_glyco_hotspots': len(o_sites),
            'n_glyco_density': len(n_sites) / len(seq) * 100,
            'n_glyco_positions': [s['position'] for s in n_sites]
        })

    return pd.DataFrame(results)
```
