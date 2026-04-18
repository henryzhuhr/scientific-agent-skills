# KEGG REST API

## 基本 URL
```
https://rest.kegg.jp
```

## Auth
无需 API 密钥。免费供学术使用。商业用途需要许可证。

## 重要提示：KEGG 返回制表符分隔的文本和平面文件格式，而不是 JSON。

## 关键操作（基于 URL 路径，无查询参数）

| URL 模式 |描述 |
|-------------|--------------|
| `/list/{database}` |列出所有条目 |
| `/list/{database}/{organism}` |列出有机体的条目 |
| `/get/{dbentries}` |获取条目数据（平面文件）|
| `/get/{dbentries}/image` |路径图像（PNG）|
| `/get/{dbentries}/kgml` |路径为 KGML XML |
| `/find/{database}/{query}` |按关键字搜索 |
| `/find/{database}/{query}/formula` |按分子式搜索|
| `/find/{database}/{value}/exact_mass` |按精确质量搜索 |
| `/link/{target_db}/{source_db}` |查找数据库之间的链接条目|
| `/link/{target_db}/{dbentries}` |特定 ID 的链接 |
| `/conv/{target_db}/{dbentries}` |交叉引用ID转换|
| `/ddi/{dbentries}` |药物间相互作用 |

## 数据库代码

|代码|数据库|示例 ID |
|------|---------|------------|
| `pathway` |途径| `hsa00010` |
| `compound` |化合物| `C00001` |
| `drug` |药品 | `D00001` |
| `enzyme` |酶 | `ec:1.1.1.1` |
| `genes`/`hsa` |基因| `hsa:10458` |
| `disease` |疾病 | `H00001` |
| `reaction` |反应 | `R00001` |
| `ko` | KO 直向同源物 | `K00001` |

## 调用示例

```
# List human pathways
https://rest.kegg.jp/list/pathway/hsa

# Get pathway entry
https://rest.kegg.jp/get/hsa00010

# Search compounds by name
https://rest.kegg.jp/find/compound/aspirin

# Search by molecular formula
https://rest.kegg.jp/find/compound/C9H8O4/formula

# Find pathways for a gene
https://rest.kegg.jp/link/pathway/hsa:10458

# Find diseases for a gene
https://rest.kegg.jp/link/disease/hsa:672

# Convert KEGG to PubChem IDs
https://rest.kegg.jp/conv/pubchem/C00001

# Get multiple entries (max 10, joined with +)
https://rest.kegg.jp/get/C00001+C00002+C00003

# Drug-drug interactions
https://rest.kegg.jp/ddi/D00564+D00110
```

## 响应格式
用于列表/查找/链接/转换的制表符分隔文本。 get 的平面文件文本。 **不支持 JSON。**

## 速率限制
没有发布的限制。保持每秒几个请求。使用 `+`，每个 `/get` 最多可批量处理 10 个 ID。如果请求太多，可能会返回 HTTP 403。
