# 命令行界面

pyzotero CLI 连接到您的**本地 Zotero 安装**（不是远程 API）。它需要运行本地 Zotero 桌面应用程序。

## 安装

```bash
uv add "pyzotero[cli]"
# or run without installing:
uvx --from "pyzotero[cli]" pyzotero search -q "your query"
```

## 搜索

```bash
# Search titles and metadata
pyzotero search -q "machine learning"

# Full-text search (includes PDF content)
pyzotero search -q "climate change" --fulltext

# Filter by item type
pyzotero search -q "methodology" --itemtype journalArticle --itemtype book

# Filter by tags (AND logic)
pyzotero search -q "evolution" --tag "reviewed" --tag "high-priority"

# Search within a collection
pyzotero search --collection ABC123 -q "test"

# Paginate results
pyzotero search -q "deep learning" --limit 20 --offset 40

# Output as JSON (for machine processing)
pyzotero search -q "protein" --json
```

## 获取单个项目

```bash
# Get a single item by key
pyzotero item ABC123

# Get as JSON
pyzotero item ABC123 --json

# Get child items (attachments, notes)
pyzotero children ABC123 --json

# Get multiple items at once (up to 50)
pyzotero subset ABC123 DEF456 GHI789 --json
```

## 集合 &标签

```bash
# List all collections
pyzotero listcollections

# List all tags
pyzotero tags

# Tags in a specific collection
pyzotero tags --collection ABC123
```

## 全文内容

```bash
# Get full-text content of an attachment
pyzotero fulltext ABC123
```

## 项目类型

```bash
# List all available item types
pyzotero itemtypes
```

## DOI Index

```bash
# Get complete DOI-to-key mapping (useful for caching)
pyzotero doiindex > doi_cache.json
# Returns JSON: {"10.1038/s41592-024-02233-6": {"key": "ABC123", "doi": "..."}}
```

## 输出格式

默认情况下，CLI 输出人类可读的文本，包括标题、作者、日期、出版物、卷、问题、DOI、URL 和 PDF 附件路径。

 使用 `--json` 进行结构化 JSON 输出，适合通过管道传输到其他内容tools.

## 搜索行为注释

- 默认搜索仅涵盖顶级项目标题和元数据字段
- `--fulltext` 将搜索扩展到 PDF 内容；结果显示父书目项目（不是原始附件）
- 多个`--tag`标志使用AND逻辑
- 多个`--itemtype`标志使用OR逻辑
