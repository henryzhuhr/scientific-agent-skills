# 编写 API 方法

## 创建项目

在创建项目之前始终使用 `item_template()` 获取有效模板。

```python
# Get a template for a specific item type
template = zot.item_template('journalArticle')

# Fill in fields
template['title'] = 'Deep Learning for Genomics'
template['date'] = '2024'
template['publicationTitle'] = 'Nature Methods'
template['volume'] = '21'
template['DOI'] = '10.1038/s41592-024-02233-6'
template['creators'] = [
    {'creatorType': 'author', 'firstName': 'Jane', 'lastName': 'Doe'},
    {'creatorType': 'author', 'firstName': 'John', 'lastName': 'Smith'},
]

# Validate fields before creating (raises InvalidItemFields if invalid)
zot.check_items([template])

# Create the item
resp = zot.create_items([template])
# resp: {'success': {'0': 'NEWITEMKEY'}, 'failed': {}, 'unchanged': {}}
new_key = resp['success']['0']
```

### 一次创建多个项目

```python
templates = []
for data in paper_data_list:
    t = zot.item_template('journalArticle')
    t['title'] = data['title']
    t['DOI'] = data['doi']
    templates.append(t)

resp = zot.create_items(templates)
```

### 创建子项项目

```python
# Create a note as a child of an existing item
note_template = zot.item_template('note')
note_template['note'] = '<p>My annotation here</p>'
zot.create_items([note_template], parentid='PARENTKEY')
```

## 更新项目

```python
# Retrieve, modify, update
item = zot.item('ITEMKEY')
item['data']['title'] = 'Updated Title'
item['data']['abstractNote'] = 'New abstract text.'
success = zot.update_item(item)  # returns True or raises error

# Update many items at once (auto-chunked at 50)
items = zot.items(limit=10)
for item in items:
    item['data']['extra'] += '\nProcessed'
zot.update_items(items)
```

## 删除项目

```python
# Must retrieve item first (version field is required)
item = zot.item('ITEMKEY')
zot.delete_item([item])

# Delete multiple items
items = zot.items(tag='to-delete')
zot.delete_item(items)
```

## 项目类型和字段

```python
# All available item types
item_types = zot.item_types()
# [{'itemType': 'artwork', 'localized': 'Artwork'}, ...]

# All available fields
fields = zot.item_fields()

# Valid fields for a specific item type
journal_fields = zot.item_type_fields('journalArticle')

# Valid creator types for an item type
creator_types = zot.item_creator_types('journalArticle')
# [{'creatorType': 'author', 'localized': 'Author'}, ...]

# All localised creator field names
creator_fields = zot.creator_fields()

# Attachment link modes (needed for attachment templates)
link_modes = zot.item_attachment_link_modes()

# Template for an attachment
attach_template = zot.item_template('attachment', linkmode='imported_file')
```

## 乐观锁定

使用`last_modified`来防止覆盖并发更改：

```python
# Only update if library version matches
zot.update_item(item, last_modified=4025)
# Raises an error if the server version differs
```

## 注释

- `create_items()`每个最多接受50个项目打电话；如果需要，可批量处理。
- `update_items()` 自动分块 50 个项目。
- 如果传递给 `create_items()` 的字典包含与现有项目匹配的 `key`，它将被更新而不是创建。
- 始终在 `create_items()` 之前调用 `check_items()` 来捕获字段早期错误。
