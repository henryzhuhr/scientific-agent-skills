# 保存的搜索

## 检索保存的搜索

```python
# Get all saved search metadata (not results)
searches = zot.searches()
# Returns list of dicts with name, key, conditions, version

for search in searches:
    print(search['data']['name'], search['data']['key'])
```

* *注意**：无法通过 API 检索保存的搜索*结果*（截至 2025 年）。仅返回元数据。

## 创建保存的搜索

每个条件字典必须具有`condition`，`operator`和`value`：

```python
conditions = [
    {
        'condition': 'title',
        'operator': 'contains',
        'value': 'machine learning'
    }
]
zot.saved_search('ML Papers', conditions)
```

### 多个条件（AND逻辑)

```python
conditions = [
    {'condition': 'itemType', 'operator': 'is', 'value': 'journalArticle'},
    {'condition': 'tag', 'operator': 'is', 'value': 'unread'},
    {'condition': 'date', 'operator': 'isAfter', 'value': '2023-01-01'},
]
zot.saved_search('Recent Unread Articles', conditions)
```

## 删除已保存的搜索

```python
# Get search keys first
searches = zot.searches()
keys = [s['data']['key'] for s in searches if s['data']['name'] == 'Old Search']
zot.delete_saved_search(keys)
```

## 发现有效的运算符和条件

```python
# All available operators
operators = zot.show_operators()

# All available conditions
conditions = zot.show_conditions()

# Operators valid for a specific condition
title_operators = zot.show_condition_operators('title')
# e.g. ['is', 'isNot', 'contains', 'doesNotContain', 'beginsWith']
```

## 常见条件/运算符组合

|状况 |常用运算符|
|---------|-----------------|
| `title` | `contains`、`doesNotContain`、`is`、`beginsWith` |
| `tag` | `is`、`isNot` |
| `itemType` | `is`、`isNot` |
| `date` | `isBefore`、`isAfter`、`is` |
| `creator` | `contains`、`is` |
| `publicationTitle` | `contains`、`is` |
| `year` | `is`、`isBefore`、`isAfter` |
| `collection` | `is`、`isNot` |
| `fulltextContent` | `contains` |
