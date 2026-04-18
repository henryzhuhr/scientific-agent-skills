# 导出格式

## BibTeX

```python
zot.add_parameters(format='bibtex')
bibtex_db = zot.top(limit=50)
# Returns a bibtexparser BibDatabase object

# Access entries as list of dicts
entries = bibtex_db.entries
for entry in entries:
    print(entry.get('title'), entry.get('author'))

# Write to .bib file
import bibtexparser
with open('library.bib', 'w') as f:
    bibtexparser.dump(bibtex_db, f)
```

## CSL-JSON

```python
zot.add_parameters(content='csljson', limit=50)
csl_items = zot.items()
# Returns a list of dicts in CSL-JSON format
```

## 参考书目 HTML（格式化引文）

```python
# APA style bibliography
zot.add_parameters(content='bib', style='apa')
bib_entries = zot.items(limit=50)
# Returns list of HTML <div> strings

for entry in bib_entries:
    print(entry)  # e.g. '<div>Smith, J. (2024). Title. <i>Journal</i>...</div>'
```

* *注意**： `format='bib'` 删除 `limit` 参数。 API 强制执行最多 150 个项目。

### 可用的引文样式

从 [Zotero 样式存储库](https://www.zotero.org/styles)传递任何有效的 CSL 样式名称：
- `'apa'`
- `'chicago-author-date'`
- `'chicago-note-bibliography'`
- `'mla'`
- `'vancouver'`
- `'ieee'`
- `'harvard-cite-them-right'`
- `'nature'`

## 正文引用

```python
zot.add_parameters(content='citation', style='apa')
citations = zot.items(limit=50)
# Returns list of HTML <span> elements: ['<span>(Smith, 2024)</span>', ...]
```

## 其他格式

将`content`设置为任何Zotero导出格式：

|格式| `content`值|返回|
|--------------------|----------------|---------|
| BibTeX | `'bibtex'` |通过 `format='bibtex'` |
| CSL-JSON | `'csljson'` |字典列表 |
| RIS | `'ris'` | unicode 字符串列表 |
| RDF（都柏林核心）| `'rdf_dc'` | unicode 字符串列表 |
|佐特罗 RDF | `'rdf_zotero'` | unicode 字符串列表 |
| BibLaTeX | `'biblatex'` | unicode 字符串列表 |
|维基百科引文模板| `'wikipedia'` | unicode 字符串列表 |

* *注意**：使用 `content` 导出格式时，必须提供 `limit` 参数。不支持同时检索多个格式。

```python
# Export as RIS
zot.add_parameters(content='ris', limit=50)
ris_data = zot.items()
with open('library.ris', 'w', encoding='utf-8') as f:
    f.write('\n'.join(ris_data))
```

## 仅密钥

```python
# Get item keys as a newline-delimited string
zot.add_parameters(format='keys')
keys_str = zot.items()
keys = keys_str.strip().split('\n')
```

## 版本信息（用于同步）

```python
# Dict of {key: version} for all items
zot.add_parameters(format='versions')
versions = zot.items()
```
