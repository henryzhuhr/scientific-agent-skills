# JASPAR（转录因子结合配置文件）

## 基本 URL
```
https://jaspar.elixir.no/api/v1/
```

## Auth
无需验证。

## 关键端点

|端点|描述 |
|----------|-------------|
| `/matrix/` |列出所有 TF 结合配置文件 |
| `/matrix/{matrix_id}/` |特定配置文件（例如 CTCF 的 MA0139.1）|
| `/matrix/?tax_id={id}&collection=CORE` |按品种过滤 + 收藏 |
| `/matrix/{id}/?format=jaspar` | JASPAR 格式的配置文件|
| `/matrix/{id}/?format=meme` | MEME 格式的简介 |
| `/matrix/{id}/?format=transfac` | TRANSFAC 格式的配置文件 |
| `/taxon/` |列出分类群 |
| `/collection/` |列出集合（CORE、CNE 等）|

## 过滤器参数
- `tax_id` — NCBI 分类 ID（人类为 9606）
- `collection` — CORE、CNE、PHYLOFACTS 等。
- `tf_class` — TF 结构类
- `name` — TF 名称搜索
- `page`, `page_size` — 分页

## 调用示例
```
# Get CTCF binding profile
https://jaspar.elixir.no/api/v1/matrix/MA0139.1/

# Human CORE TF profiles
https://jaspar.elixir.no/api/v1/matrix/?tax_id=9606&collection=CORE&page_size=10

# Get profile in MEME format
https://jaspar.elixir.no/api/v1/matrix/MA0139.1/?format=meme
```

## 响应格式
JSON。配置文件包括：`matrix_id`、`name`、`pfm`（位置频率矩阵为 A/C/G/T 字典）、`sequence_logo` URL、`species`、`class`、`family`.

## API文档
Swagger，位于 https://jaspar.elixir.no/api/v1/docs/

## 速率限制
没有发布的限制。讲道理吧。
