# arXiv API

arXiv 是物理、数学、计算机科学、定量生物学、定量金融、统计学、电气工程和经济学的预印本服务器。

* *重要：** arXiv API 返回 **Atom XML**，而不是 JSON。没有 JSON 选项。

## 基本 URL

```
https://export.arxiv.org/api/query
```

## 身份验证

不需要。完全公开。

## 查询参数

```
GET https://export.arxiv.org/api/query?search_query={query}&start={n}&max_results={n}
```

|参数|必填 |默认|描述 |
|-----------|---------|---------|-------------|
| `search_query` |是* | --|使用字段前缀 + 布尔运算符 |
| 进行搜索`id_list` |是* | --|以逗号分隔的 arXiv ID（例如，`2103.15348,2005.14165`）|
| `start` |没有 | 0 |分页偏移量（从0开始）|
| `max_results` |没有 | 10 | 10每个请求的结果（最多 2000 个；绝对最大 30000）|
| `sortBy` |没有 | `relevance` | `relevance`、`lastUpdatedDate`、`submittedDate` |
| `sortOrder` |没有 | `descending` | `ascending` 或 `descending` |

* 必须至少提供 `search_query` 或 `id_list` 之一。它们可以组合（交集）。

## 搜索字段前缀

|前缀|搜索 |
|--------|----------|
| `ti:` |标题|
| `au:` |作者|
| `abs:` |摘要|
| `co:` |评论|
| `jr:` |期刊参考|
| `cat:` |学科类别|
| `rn:` |报告编号|
| `all:` |所有字段 |

## 布尔运算符

- `AND` -- 两个条件
- `OR` -- 任一条件
- `ANDNOT` -- 排除
- 用于分组的括号（URL 编码为`%28` / `%29`)
- 引用短语（URL 编码为 `%22`）

## 示例查询

* *搜索所有字段：**
```
https://export.arxiv.org/api/query?search_query=all:transformer+attention&max_results=5
```

* *作者+类别：**
```
https://export.arxiv.org/api/query?search_query=au:hinton+AND+cat:cs.LG&max_results=10
```

* *标题搜索：**
```
https://export.arxiv.org/api/query?search_query=ti:%22attention+is+all+you+need%22
```

* *作者ID:**
```
https://export.arxiv.org/api/query?id_list=2103.15348
```

* *多个 ID:**
```
https://export.arxiv.org/api/query?id_list=2103.15348,2005.14165,1706.03762
```

* *日期范围:**
```
https://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+submittedDate:[202401010000+TO+202412312359]
```

## 响应格式 (Atom XML)

```xml
<feed xmlns="http://www.w3.org/2005/Atom">
  <opensearch:totalResults>1234</opensearch:totalResults>
  <opensearch:startIndex>0</opensearch:startIndex>
  <opensearch:itemsPerPage>10</opensearch:itemsPerPage>

  <entry>
    <id>http://arxiv.org/abs/1706.03762v7</id>
    <title>Attention Is All You Need</title>
    <summary>The dominant sequence transduction models are based on...</summary>
    <published>2017-06-12T17:57:34Z</published>
    <updated>2023-08-02T00:00:12Z</updated>
    <author><name>Ashish Vaswani</name></author>
    <author><name>Noam Shazeer</name></author>
    <!-- more authors -->
    <category term="cs.CL" scheme="http://arxiv.org/schemas/atom"/>
    <arxiv:primary_category term="cs.CL"/>
    <link rel="alternate" href="http://arxiv.org/abs/1706.03762v7"/>
    <link rel="related" type="application/pdf" href="http://arxiv.org/pdf/1706.03762v7"/>
    <arxiv:doi>10.48550/arXiv.1706.03762</arxiv:doi>
    <arxiv:comment>15 pages, 5 figures</arxiv:comment>
    <arxiv:journal_ref>Advances in Neural Information Processing Systems 30 (NIPS 2017)</arxiv:journal_ref>
  </entry>
</feed>
```

### 每个条目的关键 XML 元素

|元素|描述 |
|---------|--------------|
| `<id>` | arXiv 网址：`http://arxiv.org/abs/{id}` |
| `<title>` |论文标题|
| `<summary>` |摘要|
| `<published>` |原始提交日期 (ISO 8601) |
| `<updated>` |最新版本日期|
| `<author><name>` |每位作者一份 |
| `<category term="...">` |学科类别|
| `<arxiv:primary_category>` |一级分类|
| `<link rel="alternate">` |摘要页面网址|
| `<link rel="related" title="pdf">` | PDF 网址 |
| `<arxiv:doi>` | DOI（如果可用）|
| `<arxiv:comment>` |作者评论|
| `<arxiv:journal_ref>` |期刊参考 |

## 解析提示

由于 arXiv 返回 XML，您需要解析它。使用 `curl`，您可以通过管道输出并提取您需要的内容。 XML 命名空间为 `http://www.w3.org/2005/Atom`，arXiv 扩展位于 `http://arxiv.org/schemas/atom`.

 对于实际提取，关键数据位于 `<entry>` 元素中。每个条目的 `<id>` 都包含 URL 路径中的 arXiv ID。

## 常见类别

|类别 |领域 |
|----------|--------|
| `cs.AI` |人工智能|
| `cs.CL` |计算与语言（NLP）|
| `cs.CV` |计算机视觉|
| `cs.LG` |机器学习|
| `stat.ML` |机器学习（统计）|
| `q-bio` |定量生物学|
| `physics` |物理（所有子类别）|
| `math` |数学（所有子类别）|
| `econ` |经济学|
| `eess` |电气工程与系统科学 |

 完整列表：https://arxiv.org/category_taxonomy

## 速率限制

- **每 3 秒 1 个请求**（硬限制）
- 一次单个连接
- 搜索结果每天缓存 -- 相同的查询不会在 24 小时内显示新结果
- 对于批量数据，请改用 OAI-PMH 接口
