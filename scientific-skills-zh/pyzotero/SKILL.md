---
name: pyzotero
description: 使用 pyzotero Python 客户端与 Zotero 参考管理库进行交互。通过 Zotero Web API v3 检索、创建、更新和删除项目、集合、标签和附件。以编程方式使用 Zotero 图书馆、管理书目参考、导出引文、搜索图书馆内容、上传 PDF 附件或构建与 Zotero 集成的研究自动化工作流程时，请使用此技能。
allowed-tools: Read Write Edit Bash
license: MIT License
metadata:
    skill-author: K-Dense Inc.
---

# Pyzotero

Pyzotero 是 [Zotero API v3](https://www.zotero.org/support/dev/web_api/v3/start)的 Python 包装器。使用它以编程方式管理 Zotero 库：读取项目和集合、创建和更新参考、上传附件、管理标签和导出引文。

## 身份验证设置

* *所需凭据** — 从 https://www.zotero.org/settings/keys:
- **用户 ID**：显示为“您在 API 调用中使用的用户 ID”
- **API密钥**：在 https://www.zotero.org/settings/keys/new
 创建 - **库 ID**：对于组库，组 URL 中 `/groups/` 后面的整数

将凭据存储在环境变量或 `.env` 文件中：
```
ZOTERO_LIBRARY_ID=your_user_id
ZOTERO_API_KEY=your_api_key
ZOTERO_LIBRARY_TYPE=user  # or "group"
```

查看[references/authentication.md](references/authentication.md)了解完整设置详细信息。

## 安装

```bash
uv add pyzotero
# or with CLI support:
uv add "pyzotero[cli]"
```

## 快速入门

```python
from pyzotero import Zotero

zot = Zotero(library_id='123456', library_type='user', api_key='ABC1234XYZ')

# Retrieve top-level items (returns 100 by default)
items = zot.top(limit=10)
for item in items:
    print(item['data']['title'], item['data']['itemType'])

# Search by keyword
results = zot.items(q='machine learning', limit=20)

# Retrieve all items (use everything() for complete results)
all_items = zot.everything(zot.items())
```

## 核心概念

- A `Zotero` 实例绑定到单个库（用户或组）。所有方法都在该库上运行。
- 项目数据位于 `item['data']` 中。访问 `item['data']['title']`、`item['data']['creators']`.
- Pyzotero 等字段默认返回 100 个项目（API 默认值为 25）。使用 `zot.everything(zot.items())` 获取所有项目。
- 写入方法成功时返回 `True` 或引发 `ZoteroError`.

## 参考文件

|文件 |目录|
|------|----------|
| [参考文献/认证.md](参考文献/认证.md) |凭证、库类型、本地模式 |
| [参考文献/read-api.md](参考文献/read-api.md) |检索项目、集合、标签、组 |
| [参考文献/search-params.md](参考文献/search-params.md) |过滤、排序、搜索参数|
| [参考文献/write-api.md](参考文献/write-api.md) |创建、更新、删除项目|
| [参考文献/collections.md](参考文献/collections.md) |集合CRUD操作|
| [参考文献/tags.md](参考文献/tags.md) |标签检索与管理|
| [参考文献/文件附件.md](参考文献/文件附件.md) |文件检索和附件上传|
| [参考文献/exports.md](参考文献/exports.md) | BibTeX、CSL-JSON、参考书目导出|
| [参考文献/分页.md](参考文献/分页.md) | follow()、everything()、生成器 |
| [参考文献/全文.md](参考文献/全文.md) |全文内容索引与检索|
| [参考文献/saved-searches.md](参考文献/saved-searches.md) |保存搜索管理|
| [参考文献/cli.md](参考文献/cli.md) |命令行界面使用|
| [参考文献/错误处理.md](参考文献/错误处理.md) |错误和异常处理 |

## 常见模式

### 获取和修改项目
```python
item = zot.item('ITEMKEY')
item['data']['title'] = 'New Title'
zot.update_item(item)
```

### 从模板创建项目
```python
template = zot.item_template('journalArticle')
template['title'] = 'My Paper'
template['creators'][0] = {'creatorType': 'author', 'firstName': 'Jane', 'lastName': 'Doe'}
zot.create_items([template])
```

### 导出为BibTeX
```python
zot.add_parameters(format='bibtex')
bibtex = zot.top(limit=50)
# bibtex is a bibtexparser BibDatabase object
print(bibtex.entries)
```

### 本地模式（只读，无需API密钥）
```python
zot = Zotero(library_id='123456', library_type='user', local=True)
items = zot.items()
```
