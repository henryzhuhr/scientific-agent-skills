# 标签管理

## 检索标签

```python
# All tags in the library
tags = zot.tags()
# Returns list of strings: ['climate change', 'machine learning', ...]

# Tags for a specific item
item_tags = zot.item_tags('ITEMKEY')

# Tags in a specific collection
col_tags = zot.collection_tags('COLKEY')

# Filter tags by prefix (e.g. all tags starting with 'bio')
filtered = zot.tags(q='bio')
```

## 为商品添加标签

```python
# Add one or more tags to an item (retrieves item first)
item = zot.item('ITEMKEY')
updated = zot.add_tags(item, 'tag1', 'tag2', 'tag3')

# Add a list of tags
tag_list = ['reviewed', 'high-priority', '2024']
updated = zot.add_tags(item, *tag_list)
```

## 删除标签

```python
# Delete specific tags from the library
zot.delete_tags('old-tag', 'unused-tag')

# Delete a list of tags
tags_to_remove = ['deprecated', 'temp']
zot.delete_tags(*tags_to_remove)
```

## 搜索商品Tag

```python
# Items with a single tag
items = zot.items(tag='machine learning')

# Items with multiple tags (AND logic)
items = zot.items(tag=['climate', 'adaptation'])

# Items with any of these tags (OR logic)
items = zot.items(tag='climate OR sea level')

# Items NOT having a tag
items = zot.items(tag='-retracted')
```

## 批量标签操作

```python
# Add a tag to all items in a collection
items = zot.everything(zot.collection_items('COLKEY'))
for item in items:
    zot.add_tags(item, 'collection-reviewed')

# Find all items with a specific tag and retag them
old_tag_items = zot.everything(zot.items(tag='old-name'))
for item in old_tag_items:
    # Add new tag
    item['data']['tags'].append({'tag': 'new-name'})
    # Remove old tag
    item['data']['tags'] = [t for t in item['data']['tags'] if t['tag'] != 'old-name']
zot.update_items(old_tag_items)
```

## 标签类型

Zotero 在 `tag['type']` 中存储了两种标签类型：
- `0` — 用户添加的标签（默认）
- `1` — 自动导入的标签（来自书目数据库）

```python
item = zot.item('ITEMKEY')
for tag in item['data']['tags']:
    print(tag['tag'], tag.get('type', 0))
```
