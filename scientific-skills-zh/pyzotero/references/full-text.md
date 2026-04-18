# 全文内容

Pyzotero可以检索和设置附件项目的全文索引内容。

## 检索全文内容

```python
# Get full-text content for a specific attachment item
data = zot.fulltext_item('ATTACHMENTKEY')
# Returns:
# {
#   "content": "Full text of the document...",
#   "indexedPages": 50,
#   "totalPages": 50
# }
# For text docs: indexedChars/totalChars instead of pages

text = data['content']
coverage = data['indexedPages'] / data['totalPages']
```

## 查找具有新全文内容的项目

```python
# Get item keys with full-text updated since a library version
new_fulltext = zot.new_fulltext(since='1085')
# Returns dict: {'KEY1': 1090, 'KEY2': 1095, ...}
# Values are the library version at which full-text was indexed
```

## 设置全文内容

```python
# Set full-text for a PDF attachment
payload = {
    'content': 'The full text content of the document.',
    'indexedPages': 50,
    'totalPages': 50
}
zot.set_fulltext('ATTACHMENTKEY', payload)

# For text documents use indexedChars/totalChars
payload = {
    'content': 'Full text here.',
    'indexedChars': 15000,
    'totalChars': 15000
}
zot.set_fulltext('ATTACHMENTKEY', payload)
```

## 通过 CLI 进行全文搜索

CLI 提供跨本地索引 PDF 的全文搜索：

```bash
# Search full-text content
pyzotero search -q "CRISPR gene editing" --fulltext

# Output as JSON (retrieves parent bibliographic items for attachments)
pyzotero search -q "climate tipping points" --fulltext --json
```

## 在 API 中搜索 (qmode=everything)

```python
# Search in titles/creators + full-text content
results = zot.items(q='protein folding', qmode='everything', limit=20)
```
