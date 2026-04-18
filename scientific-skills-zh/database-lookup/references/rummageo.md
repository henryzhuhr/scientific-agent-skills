# RummaGEO（GEO基因集富集搜索）

## 基本URL
```
https://rummageo.com/
```

## 授权
无需授权。

## 关键端点

|端点|方法|描述 |
|----------|--------|-------------|
| `/api/enrich` |发布 |提交基因集以针对 GEO 签名进行富集 |
| `/api/table` |获取 |索引 GEO 签名的分页表 |

## 示例调用
```bash
curl -X POST "https://rummageo.com/api/enrich" \
  -H "Content-Type: application/json" \
  -d '{"genes": ["BRCA1","TP53","EGFR","MYC","PTEN"]}'
```

## 响应格式
JSON。具有重叠统计数据、p 值、源研究链接的匹配 GEO 签名的排名列表。

## 注意 
POST 端点 — 通过 shell 使用 `curl`，而不是 WebFetch。

## 速率限制
没有发布的限制。专为交互式/编程使用而设计。
