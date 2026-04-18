# AlphaFold DB（预测的蛋白质结构）

## 基本 URL
```
https://alphafold.ebi.ac.uk/api/
```

## Auth
无需身份验证。

## 关键端点

|端点|描述 |
|----------|-------------|
| `/prediction/{uniprot_accession}` |按 UniProt ID 预测元数据 |

## 结构文件 URL（直接下载）
```
https://alphafold.ebi.ac.uk/files/AF-{UNIPROT}-F1-model_v4.pdb
https://alphafold.ebi.ac.uk/files/AF-{UNIPROT}-F1-model_v4.cif
https://alphafold.ebi.ac.uk/files/AF-{UNIPROT}-F1-predicted_aligned_error_v4.json
```

## 示例调用
```
# Get prediction metadata for EGFR
https://alphafold.ebi.ac.uk/api/prediction/P00533

# Download PDB structure
https://alphafold.ebi.ac.uk/files/AF-P00533-F1-model_v4.pdb

# Download PAE (predicted aligned error)
https://alphafold.ebi.ac.uk/files/AF-P00533-F1-predicted_aligned_error_v4.json
```

## 元数据的响应格式
JSON。用于结构的 PDB/mmCIF。 PAE 作为 JSON 矩阵。

## 速率限制
没有严格的限制。使用FTP/Cloud进行批量下载（~200M+结构）。
