# DailyMed（NIH/NLM 药物标签）

## 基本 URL
```
https://dailymed.nlm.nih.gov/dailymed/services/
```

## Auth
无需 API 密钥。

## 关键端点

|端点|描述 |
|----------|-------------|
| `v2/spls.json?drug_name={name}` |按名称搜索药品标签|
| `v2/spls/{setid}.json` |通过SetID |
|获取标签元数据`v2/spls/{setid}/ndcs.json` |标签的 NDC 代码 |
| `v2/spls/{setid}/media.json` |标签的图像/媒体 |
| `v2/drugnames.json?drug_name={prefix}` |药品名称自动填写|
| `v2/drugclasses.json?drug_class_name={name}` |按药理类别搜索|
| `v2/rxcuis.json?drug_name={name}` |药物的 RxNorm CUI |
| `v2/ndc/{ndc_code}/spls.json` |按 NDC 代码查找标签 |

## `/v2/spls.json`
- `drug_class` — 药理学类别的附加过滤器
- `labeler` — 制造商名称
- `page` / `pagesize` — 分页（最大100)

## 调用示例

```
# Search metformin labels
https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=metformin

# Drug name autocomplete
https://dailymed.nlm.nih.gov/dailymed/services/v2/drugnames.json?drug_name=ator

# Search by pharmacologic class
https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_class=HMG-CoA+Reductase+Inhibitor

# Full label XML (SPL content with sections)
https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}/packaging.xml
```

## 响应格式
```json
{
  "metadata": {
    "total_elements": 12,
    "elements_per_page": 10,
    "current_page": 1,
    "total_pages": 2
  },
  "data": [
    {
      "published_date": "2024-01-15",
      "title": "METFORMIN HYDROCHLORIDE tablet",
      "setid": "b03f295f-..."
    }
  ]
}
```

## 速率限制
没有发布的限制。讲道理吧。
