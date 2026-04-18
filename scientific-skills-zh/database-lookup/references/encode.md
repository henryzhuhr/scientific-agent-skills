# ENCODE（DNA 元素百科全书）

## 基本 URL
```
https://www.encodeproject.org
```

## Auth
无需身份验证。附加 `?format=json` 或设置 `Accept: application/json`.

## 每个门户 URL 在使用正确标头请求时都会返回 JSON。

## 关键端点

|端点|描述 |
|----------|--------------|
| `/search/?type=Experiment&format=json` |搜索实验|
| `/experiments/{accession}/?format=json` |具体实验|
| `/files/{accession}/?format=json` |文件元数据|
| `/biosamples/{accession}/?format=json` |生物样本信息|
| `/annotations/?format=json` |搜索注释 |

## 搜索参数
- `type` — 实验、文件、生物样本、注释等。 
- `assay_title` — ChIP-seq、RNA-seq、ATAC-seq 等。 CTCF, H3K27ac)
- `biosample_ontology.term_name` — 单元格类型
- `limit` — 每页结果
- `field` — 要返回的特定字段

## 示例调用
```
# ChIP-seq experiments for CTCF
https://www.encodeproject.org/search/?type=Experiment&assay_title=ChIP-seq&target.label=CTCF&format=json&limit=5

# Specific experiment
https://www.encodeproject.org/experiments/ENCSR000AAA/?format=json

# Files for an experiment
https://www.encodeproject.org/search/?type=File&dataset=/experiments/ENCSR000AAA/&format=json
```

## 响应格式
JSON-LD。搜索：`@graph`数组+`total`+`facets`。使用`frame=object`或`frame=embedded`来控制深度。

## 速率限制
没有公布的限制。使用`limit=`和`field=`来减少有效负载。
