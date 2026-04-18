# 分页: follow(), everything(), Generators

Pyzotero 默认返回 100 个项目。使用这些方法检索更多内容。

## everything() — 检索所有结果

获取所有项目的最简单方法：

```python
# All items in the library
all_items = zot.everything(zot.items())

# All top-level items
all_top = zot.everything(zot.top())

# All items in a collection
all_col = zot.everything(zot.collection_items('COLKEY'))

# All items matching a search
all_results = zot.everything(zot.items(q='machine learning', itemType='journalArticle'))
```

`everything()` 适用于所有可返回多个项目的 Read API 调用。

## follow() — 顺序分页

```python
# Retrieve items in batches, manually advancing the page
first_batch = zot.top(limit=25)
second_batch = zot.follow()   # next 25 items
third_batch = zot.follow()    # next 25 items
```

* *警告**：当没有更多可用项目时，`follow()` 会引发 `StopIteration`。在像 `zot.item()`.

## iterfollow() — Generator

```python
# Create a generator over follow()
first = zot.top(limit=10)
lazy = zot.iterfollow()

# Retrieve subsequent pages
second = next(lazy)
third = next(lazy)
```

## makeiter() — Generator over Any Method

```python
# Create a generator directly from a method call
gen = zot.makeiter(zot.top(limit=25))

page1 = next(gen)  # first 25 items
page2 = next(gen)  # next 25 items
# Raises StopIteration when exhausted
```

## 手动启动/限制这样的单项调用后无效分页

```python
page_size = 50
offset = 0

while True:
    batch = zot.items(limit=page_size, start=offset)
    if not batch:
        break
    # process batch
    for item in batch:
        process(item)
    offset += page_size
```

## 性能说明

- `everything()`顺序进行多个API调用；大型库可能需要时间。
- 对于包含数千个项目的库，使用 `since=version` 仅检索更改的项目（对于同步工作流程有用）。
- 所有 `follow()`、`everything()` 和 `makeiter()` 仅对返回多个项目的方法有效。
