# 错误处理

## 异常类型

Pyzotero 针对 API 错误引发 `ZoteroError` 子类。从`pyzotero.zotero_errors`导入：

```python
from pyzotero import zotero_errors
```

常见异常：

|例外 |原因 |
|-----------|--------|
| `UserNotAuthorised` | API 密钥无效或缺失 |
| `HTTPError` |一般 HTTP 错误 |
| `ParamNotPassed` |缺少必需参数 |
| `CallDoesNotExist` |库类型 |
| 的 API 方法无效`ResourceNotFound` |未找到物品/收藏钥匙|
| `Conflict` |版本冲突（乐观锁）|
| `PreConditionFailed` | `If-Unmodified-Since-Version` 检查失败 |
| `TooManyItems` |批次超过 50 件限制 |
| `TooManyRequests` |超出 API 速率限制 |
| `InvalidItemFields` |项目字典包含未知字段 |

## 基本错误处理

```python
from pyzotero import Zotero
from pyzotero import zotero_errors

zot = Zotero('123456', 'user', 'APIKEY')

try:
    item = zot.item('BADKEY')
except zotero_errors.ResourceNotFound:
    print('Item not found')
except zotero_errors.UserNotAuthorised:
    print('Invalid API key')
except Exception as e:
    print(f'Unexpected error: {e}')
    if hasattr(e, '__cause__'):
        print(f'Caused by: {e.__cause__}')
```

## 版本冲突处理

```python
try:
    zot.update_item(item)
except zotero_errors.PreConditionFailed:
    # Item was modified since you retrieved it — re-fetch and retry
    fresh_item = zot.item(item['data']['key'])
    fresh_item['data']['title'] = new_title
    zot.update_item(fresh_item)
```

## 检查无效字段

```python
from pyzotero import zotero_errors

template = zot.item_template('journalArticle')
template['badField'] = 'bad value'

try:
    zot.check_items([template])
except zotero_errors.InvalidItemFields as e:
    print(f'Invalid fields: {e}')
    # Fix fields before calling create_items
```

## 速率限制

Zotero API 速率限制请求。如果您收到 `TooManyRequests`:

```python
import time
from pyzotero import zotero_errors

def safe_request(func, *args, **kwargs):
    retries = 3
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except zotero_errors.TooManyRequests:
            wait = 2 ** attempt
            print(f'Rate limited, waiting {wait}s...')
            time.sleep(wait)
    raise RuntimeError('Max retries exceeded')

items = safe_request(zot.items, limit=100)
```

## 访问底层错误

```python
try:
    zot.item('BADKEY')
except Exception as e:
    print(e.__cause__)    # original HTTP error
    print(e.__context__)  # exception context
```
