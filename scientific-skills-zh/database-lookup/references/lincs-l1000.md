# LINCS L1000 (Clue.io) API 参考

## 概述
LINCS L1000 数据集可通过线索.io.

## 的 **连接映射 (CMap) API** 访问（在线索.io 免费注册）
- 通过标头传递：`user_key: YOUR_API_KEY`

## 关键端点

|端点|描述 |
|---|---|
| `GET /perts` |查询扰动因素（化合物、基因敲低、过度表达）|
| `GET /genes` |查询基因（L1000标志+推断）|
| `GET /cells` |查询L1000使用的细胞系|
| `GET /sigs` |查询连接签名|
| `GET /profiles` |访问表达谱（5 级 z 分数）|
| `GET /pcls` |扰动类 |

## 查询参数
所有端点都支持使用环回式 JSON 的 `filter` 参数：
- `where` — 过滤条件
- `fields` — 选择特定字段
- `limit` / `skip` — 分页

## 调用示例

```bash
# Search for a compound perturbagen by name
curl -H "user_key: YOUR_API_KEY" \
  "https://api.clue.io/api/perts?filter={\"where\":{\"pert_iname\":\"vorinostat\"}}"

# Get landmark genes
curl -H "user_key: YOUR_API_KEY" \
  "https://api.clue.io/api/genes?filter={\"where\":{\"is_lm\":true},\"limit\":10}"

# Query cell lines
curl -H "user_key: YOUR_API_KEY" \
  "https://api.clue.io/api/cells?filter={\"where\":{\"cell_iname\":\"MCF7\"}}"

# Get connectivity signatures for a compound
curl -H "user_key: YOUR_API_KEY" \
  "https://api.clue.io/api/sigs?filter={\"where\":{\"pert_iname\":\"vorinostat\"},\"limit\":5}"
```

## 响应格式
JSON。示例（扰动）：
```json
[
  {
    "pert_id": "BRD-K81418486",
    "pert_iname": "vorinostat",
    "pert_type": "trt_cp",
    "moa": ["HDAC inhibitor"],
    "target": ["HDAC1","HDAC2","HDAC3","HDAC6"]
  }
]
```

## 速率限制
- 免费层：中等速率限制（确切数字未公开记录）
- 可通过clue.io 数据门户单独提供批量数据下载
