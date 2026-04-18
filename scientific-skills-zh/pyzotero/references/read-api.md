# 读取 API 方法

## 检索项目

```python
# All items in library (100 per call by default)
items = zot.items()

# Top-level items only (excludes attachments/notes that are children)
top = zot.top(limit=25)

# A specific item by key
item = zot.item('ITEMKEY')

# Multiple specific items (up to 50 per call)
subset = zot.get_subset(['KEY1', 'KEY2', 'KEY3'])

# Items from trash
trash = zot.trash()

# Deleted items (requires 'since' parameter)
deleted = zot.deleted(since=1000)

# Items from "My Publications"
pubs = zot.publications()  # user libraries only

# Count all items
count = zot.count_items()

# Count top-level items
n = zot.num_items()
```

## 项目数据结构

项目以字典形式返回。数据位于 `item['data']`:

```python
item = zot.item('VDNIEAPH')[0]
title = item['data']['title']
item_type = item['data']['itemType']
creators = item['data']['creators']
tags = item['data']['tags']
key = item['data']['key']
version = item['data']['version']
collections = item['data']['collections']
doi = item['data'].get('DOI', '')
```

## 子项

```python
# Get child items (notes, attachments) of a parent
children = zot.children('PARENTKEY')
```

## 检索集合

```python
# All collections (including subcollections)
collections = zot.collections()

# Top-level collections only
top_collections = zot.collections_top()

# A specific collection
collection = zot.collection('COLLECTIONKEY')

# Sub-collections of a collection
sub = zot.collections_sub('COLLECTIONKEY')

# All collections and sub-collections in a flat list
all_cols = zot.all_collections()
# Or from a specific collection down:
all_cols = zot.all_collections('COLLECTIONKEY')

# Items in a specific collection (not sub-collections)
col_items = zot.collection_items('COLLECTIONKEY')

# Top-level items in a specific collection
col_top = zot.collection_items_top('COLLECTIONKEY')

# Count items in a collection
n = zot.num_collectionitems('COLLECTIONKEY')
```

## 检索标签

```python
# All tags in the library
tags = zot.tags()

# Tags from a specific item
item_tags = zot.item_tags('ITEMKEY')

# Tags in a collection
col_tags = zot.collection_tags('COLLECTIONKEY')
```

## 检索组

```python
groups = zot.groups()
# Returns list of group libraries accessible to current key
```

## 版本信息

```python
# Last modified version of the library
version = zot.last_modified_version()

# Item versions dict {key: version}
item_versions = zot.item_versions()

# Collection versions dict {key: version}
col_versions = zot.collection_versions()

# Changes since a known version (for syncing)
changed_items = zot.item_versions(since=1000)
```

## 库设置

```python
settings = zot.settings()
# Returns synced settings (feeds, PDF reading progress, etc.)
# Use 'since' to get only changes:
new_settings = zot.settings(since=500)
```

## 已保存搜索

```python
searches = zot.searches()
# Retrieves saved search metadata (not results)
```
