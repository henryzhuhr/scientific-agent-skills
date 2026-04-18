# 搜索和请求参数

参数可以直接传递给任何读取API调用，或者使用`add_parameters()`.

```python
# Inline parameters (valid for one call only)
results = zot.items(q='climate change', limit=50, sort='date', direction='desc')

# Set globally (overridden by inline params on the next call)
zot.add_parameters(limit=50, sort='dateAdded')
results = zot.items()
```

## 可用参数

|进行全局设置参数|类型 |描述|
|-----------|------|-------------|
| `q` | STR |快速搜索 - 默认标题和创建者字段 |
| `qmode` | STR | `'titleCreatorYear'`（默认）或 `'everything'`（全文）|
| `itemType` | STR |按项目类型过滤。请参阅运算符的搜索语法 |
| `tag` |字符串或列表|按标签过滤。多个标签 = AND 逻辑 |
| `since` |整数 |仅返回在此库版本之后修改的对象 |
| `sort` | STR |排序字段（见下文）|
| `direction` | STR | `'asc'` 或 `'desc'` |
| `limit` |整数 | 1–100，或 `None` |
| `start` |整数 |结果集的偏移量 |
| `format` | STR |响应格式（参见exports.md）|
| `itemKey` | STR |逗号分隔的项目键（最多 50 个）|
| `content` | STR | `'bib'`、`'html'`、`'citation'` 或导出格式 |
| `style` | STR | CSL样式名称（与`content='bib'`一起使用）|
| `linkwrap` | STR | `'1'` 在参考书目输出中将 URL 包装在 `<a>` 标签中 |

## 排序字段

`dateAdded`、`dateModified`、`title`、`creator`、`type`、 `date`、`publisher`、
`publicationTitle`、`journalAbbreviation`、`language`、`accessDate`、
`libraryCatalog`、`callNumber`、`rights`、 `addedBy`, `numItems`, `tags`

## 标签搜索语法

```python
# Single tag
zot.items(tag='machine learning')

# Multiple tags — AND logic (items must have all tags)
zot.items(tag=['climate', 'adaptation'])

# OR logic (items with any tag)
zot.items(tag='climate OR adaptation')

# Exclude a tag
zot.items(tag='-retracted')
```

## 项目类型过滤

```python
# Single type
zot.items(itemType='journalArticle')

# OR multiple types
zot.items(itemType='journalArticle || book')

# Exclude a type
zot.items(itemType='-note')
```

常见项目类型：`journalArticle`、`book`、`bookSection`、`conferencePaper`、
`thesis`、`report`、`dataset`、 `preprint`、`note`、`attachment`、`webpage`、`webpage`、
`patent`、`statute`、`case`、`hearing`、`interview`、`letter`、 `manuscript`,
`map`, `artwork`, `audioRecording`, `videoRecording`, `podcast`, `film`,
`radioBroadcast`, `tvBroadcast`, `presentation`、`encyclopediaArticle`、
`dictionaryEntry`、`forumPost`、`blogPost`、`instantMessage`、`email`、
`document`、`computerProgram`、 `bill`、`newspaperArticle`、`magazineArticle`

## 示例

```python
# Recent journal articles matching query, sorted by date
zot.items(q='CRISPR', itemType='journalArticle', sort='date', direction='desc', limit=20)

# Items added since a known library version
zot.items(since=4000)

# Items with a specific tag, offset for pagination
zot.items(tag='to-read', limit=25, start=25)

# Full-text search
zot.items(q='gene editing', qmode='everything', limit=10)
```
