# OMIM（人类在线孟德尔遗传）API 参考

## 基本 URL
```
https://api.omim.org/api
```

## 身份验证
* *需要 API 密钥。** 在 https://omim.org/api 请求（免费用于学术/非商业用途）。
- 作为查询参数传递： `?apiKey=YOUR_API_KEY`
- 所有请求都需要密钥；未经身份验证的请求将被拒绝。

## 速率限制
未公开详细记录。根据服务条款合理使用。

## 响应格式
JSON（使用 `&format=json`）或 XML（默认）。对于 JSON 响应，始终附加 `&format=json`。

## 关键端点

### 1. 条目查找（按 MIM 编号）
```
GET https://api.omim.org/api/entry?mimNumber={mim_number}&apiKey={key}&format=json
```
 示例：
```
GET https://api.omim.org/api/entry?mimNumber=141900&apiKey=YOUR_KEY&format=json
```
 返回包含标题、文本、基因图谱、等位基因变体的条目， references.

### 2. 包含特定 Includes 的条目
```
GET https://api.omim.org/api/entry?mimNumber=141900&include=text&include=allelicVariantList&include=geneMap&apiKey={key}&format=json
```
包含选项：`text`、`clinicalSynopsis`、`geneMap`、`allelicVariantList`、`referenceList`、`existFlags`、 `externalLinks`.

### 3. 搜索条目
```
GET https://api.omim.org/api/entry/search?search={query}&apiKey={key}&format=json
```
示例 — 搜索“马凡综合征”：
```
GET https://api.omim.org/api/entry/search?search=marfan+syndrome&apiKey=YOUR_KEY&format=json&start=0&limit=10
```

### 4. 使用过滤器搜索
```
GET https://api.omim.org/api/entry/search?search={query}&filter=gene&apiKey={key}&format=json
```
过滤器选项： `gene`、`phenotype`、`clinical_synopsis` 等

### 5. 基因图谱查找
```
GET https://api.omim.org/api/geneMap?chromosome={chrom}&apiKey={key}&format=json
```
示例：
```
GET https://api.omim.org/api/geneMap?chromosome=17&apiKey=YOUR_KEY&format=json&start=0&limit=10
```

### 6. 基因图谱查找搜索
```
GET https://api.omim.org/api/geneMap/search?search={query}&apiKey={key}&format=json
```

### 7. 临床概要搜索
```
GET https://api.omim.org/api/clinicalSynopsis/search?search={query}&apiKey={key}&format=json
```

## 响应结构
```json
{
  "omim": {
    "version": "1.0",
    "entryList": [
      {
        "entry": {
          "mimNumber": 141900,
          "status": "live",
          "titles": {
            "preferredTitle": "HEMOGLOBIN S; HBS",
            "alternativeTitles": "SICKLE CELL ANEMIA"
          },
          "textSectionList": [...],
          "geneMap": {
            "chromosome": "11",
            "cytoLocation": "11p15.4",
            "geneSymbols": "HBB"
          }
        }
      }
    ]
  }
}
```

## 分页
使用`start` 和 `limit` 查询参数：
```
&start=0&limit=20
```

## MIM 编号类型
- **星号 (*)**：基因
- **加号 (+)**：具有已知表型的基因
- **数字符号(#)**：表型（分子基础已知）
- **百分比 (%)**：表型（分子基础未知）
- **空**：其他条目类型

## 注释
- OMIM 数据受版权保护； API 访问免费供学术使用，但需要注册。
- API 不支持批量下载；使用具有单独协议的 OMIM 下载页面。
- 将 MIM 编号与 ClinVar、NCBI Gene 和 HPO 交叉引用以进行综合疾病分析。
