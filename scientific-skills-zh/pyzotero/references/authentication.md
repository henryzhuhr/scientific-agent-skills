# 身份验证和设置

## 凭证

从 https://www.zotero.org/settings/keys:

| 获取资质证书 |哪里可以找到 |
|------------|---------------|
| **用户ID** | “您在 API 调用中使用的用户 ID”部分 |
| **API 密钥** |在 /settings/keys/new |
| 创建新密钥**群组图书馆 ID** |组URL中`/groups/`后的整数（例如`https://www.zotero.org/groups/169947`）|

## 环境变量

存储在`.env`中或在shell中导出：
```
ZOTERO_LIBRARY_ID=436
ZOTERO_API_KEY=ABC1234XYZ
ZOTERO_LIBRARY_TYPE=user
```

载入Python:
```python
import os
from dotenv import load_dotenv
from pyzotero import Zotero

load_dotenv()

zot = Zotero(
    library_id=os.environ['ZOTERO_LIBRARY_ID'],
    library_type=os.environ['ZOTERO_LIBRARY_TYPE'],
    api_key=os.environ['ZOTERO_API_KEY']
)
```

## 库类型

```python
# Personal library
zot = Zotero('436', 'user', 'ABC1234XYZ')

# Group library
zot = Zotero('169947', 'group', 'ABC1234XYZ')
```

* *重要**：`Zotero` 实例绑定到单个库。要访问多个库，请创建多个实例。

## 本地模式（只读）

连接到本地 Zotero 安装，无需 API 密钥。只支持读请求。

```python
zot = Zotero(library_id='436', library_type='user', local=True)
items = zot.items(limit=10)  # reads from local Zotero
```

## 可选参数

```python
zot = Zotero(
    library_id='436',
    library_type='user',
    api_key='ABC1234XYZ',
    preserve_json_order=True,   # use OrderedDict for JSON responses
    locale='en-US',             # localise field names (e.g. 'fr-FR' for French)
)
```

## 密钥权限

检查当前API密钥可以访问的内容：
```python
info = zot.key_info()
# Returns dict with user info and group access permissions
```

检查可访问组：
```python
groups = zot.groups()
# Returns list of group libraries accessible to the current key
```

## API 密钥范围

在 https://www.zotero.org/settings/keys/new 创建 API 密钥时，选择适当的权限：
- **只读**：用于检索项目和集合
- **写入访问**：用于创建、更新和删除items
- **注释访问**：在读/写操作中包含注释
- **文件访问**：上传附件所需
