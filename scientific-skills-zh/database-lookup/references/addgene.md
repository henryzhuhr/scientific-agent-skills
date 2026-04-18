# Addgene（质粒存储库）

## 基本 URL
```
https://www.addgene.org/api/
```

## 需要 Auth
API 密钥。在 addgene.org 注册并请求 API 访问。
传递为：`Authorization: Token <your_api_key>`

从 `.env` 加载为 `ADDGENE_API_KEY`.

## 关键端点

|端点|描述 |
|----------|--------------|
| `/plasmids/{addgene_id}/` |通过 ID |
| 获取质粒详细信息`/plasmids/search/?q={query}` |按关键字搜索质粒|
| `/depositors/{id}/` |存款人信息|
| `/articles/{id}/` |相关出版物 |

## 调用示例
```
# Get plasmid details (e.g., pSpCas9)
GET https://www.addgene.org/api/plasmids/12260/
Authorization: Token YOUR_KEY

# Search plasmids
GET https://www.addgene.org/api/plasmids/search/?q=GFP
Authorization: Token YOUR_KEY
```

## 响应格式
JSON，包含质粒名称、骨架、插入片段、抗性标记、存放者、序列、出版物。

## 速率限制
没有发布的限制。合理使用预期。
