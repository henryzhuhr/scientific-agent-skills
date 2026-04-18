# ClinicalTrials.gov (v2 API)

## 基本 URL
```
https://clinicaltrials.gov/api/v2/
```

## Auth
无需 API 密钥。完全公开。

## 关键终点

### 搜索研究
```
GET /studies
```

 关键参数：
- `query.cond` — 状况/疾病（例如 `breast cancer`）
- `query.intr` — 干预/治疗（例如 `pembrolizumab`）
- `query.term` — 一般搜索词
- `query.spons` — 赞助商
- `query.id` — NCT ID
- `filter.overallStatus` — 以竖线分隔： `RECRUITING|COMPLETED|ACTIVE_NOT_RECRUITING|...`
- `filter.phase` — `PHASE1|PHASE2|PHASE3|PHASE4|NA`
- `filter.geo` — `distance(lat,lon,dist)` `distance(38.89,-77.03,50mi)`
- `fields` — 以逗号分隔的字段列表，以减少有效负载
- `sort` — 例如`LastUpdatePostDate:desc`
- `pageSize` — 每页结果（默认 10 个，最多 1000 个）
- `pageToken` — 下一页的光标（来自 `nextPageToken` 响应）
- `countTotal=true` — 包括总数count

示例 — 招募 3 期乳腺癌试验：
```
/studies?query.cond=breast+cancer&filter.overallStatus=RECRUITING&filter.phase=PHASE3&pageSize=5&countTotal=true
```

 响应结构：
```json
{
  "totalCount": 1234,
  "studies": [
    {
      "protocolSection": {
        "identificationModule": {"nctId": "NCT05123456", "briefTitle": "..."},
        "statusModule": {"overallStatus": "RECRUITING"},
        "designModule": {"phases": ["PHASE3"], "enrollmentInfo": {"count": 500}},
        "conditionsModule": {"conditions": ["Breast Cancer"]},
        "eligibilityModule": {"minimumAge": "18 Years", "sex": "ALL"}
      }
    }
  ],
  "nextPageToken": "CAYQAg"
}
```

### NCT ID 的单一研究
```
GET /studies/{nctId}
```
示例： `/studies/NCT05123456`

### 研究计数
```
GET /stats/size?query.cond={condition}&filter.overallStatus=RECRUITING
```

### 字段元数据
```
GET /studies/metadata
```

## 分页
通过 `pageToken` 使用基于游标的分页（不是数字）偏移量）。在第一次请求时包含 `countTotal=true` 以获取总计。

## 速率限制
No API 密钥。保持合理——每秒几个请求。批量：https://clinicaltrials.gov/AllAPIJSON.zip
