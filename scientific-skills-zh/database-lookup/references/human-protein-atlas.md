# 人类蛋白质图谱 (HPA)

## 基本 URL
```
https://www.proteinatlas.org
```

## Auth
无需 API 密钥。

## 关键端点

|目的| URL 模式 |
|---|---|
| Ensembl ID 的基因数据 | `/{ENSEMBL_ID}.json` |
|按符号显示的基因数据 | `/{GENE_NAME}.json` |
|搜索 (JSON) | `/search/{QUERY}?format=json` |
|搜索 (XML) | `/search/{QUERY}?format=xml` |

## 调用示例

```
# Gene data by Ensembl ID
https://www.proteinatlas.org/ENSG00000141510.json

# Gene data by symbol
https://www.proteinatlas.org/TP53.json

# Search
https://www.proteinatlas.org/search/TP53?format=json
```

## 响应格式（JSON，基因端点）
```json
{
  "Gene": "TP53",
  "Gene synonym": ["p53", "LFS1"],
  "Ensembl": "ENSG00000141510",
  "Gene description": "tumor protein p53",
  "Uniprot": ["P04637"],
  "Chromosome": "17",
  "Protein class": ["Transcription factors"],
  "RNA tissue specificity": "Low tissue specificity",
  "Subcellular location": ["Nucleoplasm"],
  "Pathology prognostics": [...]
}
```

## 批量下载
对于大规模工作，请使用来自的 TSV 文件https://www. Proteinatlas.org/about/download:
- `normal_tissue.tsv` — IHC 组织表达
- `rna_tissue_consensus.tsv` — RNA 共识
- `subcellular_location.tsv`
- `pathology.tsv` — 癌症预后

## 率限制
没有公布的限制。讲道理。对于大型查询，更喜欢批量下载。
