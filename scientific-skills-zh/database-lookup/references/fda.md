# OpenFDA API

## 基本 URL
```
https://api.fda.gov
```

## Auth
可选的免费 API 密钥（不带时为 40 请求/分钟，带时为 240 请求/分钟）。在 https://open.fda.gov/apis/authentication/
 注册密码为：`?api_key=YOUR_KEY`

## 关键端点

|端点|描述 |
|----------|--------------|
| `/drug/event.json` |药物不良事件（FAERS）|
| `/drug/label.json` |药品标签 (SPL) |
| `/drug/ndc.json` | NDC目录|
| `/drug/drugsfda.json` |药品@FDA（批准）|
| `/drug/enforcement.json` |药品召回|
| `/device/event.json` |器械不良事件|
| `/device/510k.json` | 510(k)间隙 |
| `/food/event.json` |食品不良事件|
| `/food/enforcement.json` |食品执法 |

## 查询参数

- `search` — 使用 OpenFDA 语法进行查询
- `count` — 计算字段的唯一值
- `limit` — 每个请求的结果（最多 1000）
- `skip` — 分页偏移量（最大 25000）

### 搜索语法
- 字段搜索：`field:"value"`
- AND：`field1:value1+AND+field2:value2`
- 或：`field1:value1+OR+field2:value2`
- 日期范围： `field:[20230101+TO+20231231]`
- 通配符：`field:aspir*`
- OpenFDA 协调字段使用 `openfda.` 前缀

## 调用示例

```
# Adverse events for aspirin
/drug/event.json?search=patient.drug.openfda.brand_name:"aspirin"&limit=5

# Top adverse reactions for a drug
/drug/event.json?search=patient.drug.openfda.generic_name:"metformin"&count=patient.reaction.reactionmeddrapt.exact

# Drug labels by generic name
/drug/label.json?search=openfda.generic_name:"ibuprofen"&limit=3

# Drug recalls in date range
/drug/enforcement.json?search=report_date:[20230101+TO+20231231]&limit=10

# Serious adverse events only
/drug/event.json?search=patient.drug.openfda.brand_name:"warfarin"+AND+serious:1&limit=10
```

## 速率限制
|等级 |请求/分钟 |请求/天 |
|-----|-------------|------------|
|没有 API 密钥 | 40| 1,000 |
|带有 API 密钥（免费）| 240 | 240 120,000 |
