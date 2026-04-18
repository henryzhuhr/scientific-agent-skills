# LabArchives API 参考

## API 结构

所有 LabArchives API 调用都遵循以下 URL 模式：

```
https://<base_url>/api/<api_class>/<api_method>?<authentication_parameters>&<method_parameters>
```

## 区域 API 端点

|地区 |基本网址|
|--------|----------|
|美国/国际 | `https://api.labarchives.com/api` |
|澳大利亚 | `https://auapi.labarchives.com/api` |
|英国 | `https://ukapi.labarchives.com/api` |

## 身份验证

所有 API 调用都需要身份验证参数：

- `access_key_id`：由 LabArchives 管理员提供
- `access_password`：由 LabArchives 管理员提供
- 某些特定功能可能需要其他用户特定凭据操作

## API类和方法

### 用户API类

#### `users/user_access_info`

检索用户ID和笔记本访问信息。

* *参数：**
- `login_or_email`（必填）：用户的电子邮件地址或登录名用户名
- `password`（必需）：用户的外部应用程序密码（不是常规登录密码）

* *返回：** XML或JSON响应包含：
- 用户ID（uid）
- 具有ID的可访问笔记本列表（nbid）
- 帐户状态和权限

* *示例：**
```python
params = {
    'login_or_email': 'researcher@university.edu',
    'password': 'external_app_password'
}
response = client.make_call('users', 'user_access_info', params=params)
```

#### `users/user_info_via_id`

通过用户ID检索详细的用户信息。

* *参数：**
- `uid`（必填）：从以下位置获取的用户ID user_access_info

* *返回：** 用户个人资料信息包括：
- 姓名和电子邮件
- 帐户创建日期
- 机构隶属关系
- 角色和权限
- 存储配额和用法

* *示例：**
```python
params = {'uid': '12345'}
response = client.make_call('users', 'user_info_via_id', params=params)
```

### Notebooks API 类

#### `notebooks/notebook_backup`

下载完整的笔记本数据，包括条目、附件和metadata.

* *参数：**
- `uid`（必填）：用户ID
- `nbid`（必填）：笔记本ID
- `json`（可选，默认：false）：以JSON格式返回数据，而不是XML
- `no_attachments`（可选，默认：false）：从备份中排除附件

* *返回：**
- 当`no_attachments=false`时：包含所有笔记本数据的7z压缩存档
- 当`no_attachments=true`时：带有条目内容的XML或JSON结构化数据

* *文件格式：**
返回的存档包括：
- HTML格式的条目文本内容
- 文件原始格式的附件
- 带有时间戳、作者和版本历史记录的元数据 XML 文件
- 评论线程和注释

* *示例：**
```python
# Full backup with attachments
params = {
    'uid': '12345',
    'nbid': '67890',
    'json': 'false',
    'no_attachments': 'false'
}
response = client.make_call('notebooks', 'notebook_backup', params=params)

# Write to file
with open('notebook_backup.7z', 'wb') as f:
    f.write(response.content)
```

```python
# Metadata only backup (JSON format, no attachments)
params = {
    'uid': '12345',
    'nbid': '67890',
    'json': 'true',
    'no_attachments': 'true'
}
response = client.make_call('notebooks', 'notebook_backup', params=params)
import json
notebook_data = json.loads(response.content)
```

#### `notebooks/list_notebooks`

检索用户可访问的所有笔记本（方法名称可能因 API 版本而异）。

* *参数：**
- `uid`（必填）：用户 ID

* *返回：** 具有以下内容的笔记本列表：
- 笔记本 ID (nbid)
- 笔记本名称
- 创建和修改日期
- 访问级别（所有者、编辑者、查看者）
- 成员计数

### 条目 API 类

#### `entries/create_entry`

在notebook.

* *参数：**
- `uid`（必填）：用户ID
- `nbid`（必填）：笔记本ID
- `title`（必填）：条目标题
- `content` （可选）：HTML格式的参赛内容
- `date` （可选）：参赛日期（默认为当前日期）

* *返回：**参赛ID和创建确认

* *示例：**
```python
params = {
    'uid': '12345',
    'nbid': '67890',
    'title': 'Experiment 2025-10-20',
    'content': '<p>Conducted PCR amplification of target gene...</p>',
    'date': '2025-10-20'
}
response = client.make_call('entries', 'create_entry', params=params)
```

#### `entries/create_comment`

向现有条目添加评论。

* *参数：**
- `uid`（必填）：用户ID
- `nbid`（必填）：笔记本ID
- `entry_id` （必需）：目标条目 ID
- `comment` （必需）：注释文本（支持 HTML）

* *返回：** 注释 ID 和时间戳

#### `entries/create_part`

将组件/部分添加到条目（例如，文本部分、表格、图片）.

* *参数：**
- `uid`（必填）：用户 ID
- `nbid`（必填）：笔记本 ID
- `entry_id`（必填）：目标条目 ID
- `part_type`（必填）：部件类型（文本、表格、图片等）
- `content`（必填）：适当格式的零件内容

* *返回：**零件ID和创建确认

#### `entries/upload_attachment`

将文件附件上传到条目。

* *参数：**
- `uid`（必填）：用户 ID
- `nbid`（必填）：笔记本 ID
- `entry_id`（必填）：目标条目 ID
- `file`（必填）：文件数据（multipart/form-data）
- `filename`（必填）：原始文件名

* *返回：**附件ID和上传确认

* *使用请求库的示例：**
```python
import requests

url = f'{api_url}/entries/upload_attachment'
files = {'file': open('/path/to/data.csv', 'rb')}
params = {
    'uid': '12345',
    'nbid': '67890',
    'entry_id': '11111',
    'filename': 'data.csv',
    'access_key_id': access_key_id,
    'access_password': access_password
}
response = requests.post(url, files=files, data=params)
```

### 站点报告API类

仅限企业的机构报告和报告功能Analytics.

#### `site_reports/detailed_usage_report`

生成机构的综合使用统计数据。

* *参数：**
- `start_date`（必填）：报告开始日期（YYYY-MM-DD）
- `end_date`（必填）：报告结束日期 (YYYY-MM-DD)
- `format`（可选）：输出格式（csv、json、xml）

* *返回：** 使用指标包括：
- 用户登录频率
- 条目创建计数
- 存储利用率
- 协作统计
- 基于时间的活动模式

#### `site_reports/detailed_notebook_report`

生成机构中所有笔记本的详细报告。

* *参数：**
- `include_settings`（可选，默认：false）：包括笔记本设置
- `include_members`（可选，默认值：false）：包括成员列表

* *返回：** 笔记本清单包含：
- 笔记本名称和 ID
- 所有者信息
- 创建和上次修改日期
- 成员计数和访问级别
- 存储size
- 设置（如果需要）

#### `site_reports/pdf_offline_generation_report`

出于合规性和审核目的跟踪 PDF 导出。

* *参数：**
- `start_date`（必填）：报告开始日期
- `end_date`（必填）：报告结束日期

* *返回：** 导出活动日志：
- 生成 PDF 的用户
- 导出的笔记本和条目
- 导出timestamp
- IP 地址

### 实用程序 API 类

#### `utilities/institutional_login_urls`

检索用于 SSO 集成的机构登录 URL。

* *参数：** 不需要（使用访问密钥身份验证）

* *返回：** 机构登录列表端点

## 响应格式

### XML 响应示例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<response>
    <uid>12345</uid>
    <email>researcher@university.edu</email>
    <notebooks>
        <notebook>
            <nbid>67890</nbid>
            <name>Lab Notebook 2025</name>
            <role>owner</role>
        </notebook>
    </notebooks>
</response>
```

### JSON 响应示例

```json
{
    "uid": "12345",
    "email": "researcher@university.edu",
    "notebooks": [
        {
            "nbid": "67890",
            "name": "Lab Notebook 2025",
            "role": "owner"
        }
    ]
}
```

## 错误代码

|代码|留言 |意义|解决方案|
|------|---------|---------|----------|
| 401 | 401未经授权 |凭证无效 |验证 access_key_id 和 access_password |
| 403 | 403禁止 |权限不足|检查用户角色和笔记本访问权限 |
| 404 | 404未找到 |资源不存在 |验证 uid、nbid 或 entry_id 是否正确 |
| 429 | 429太多请求 |超出速率限制 |实施指数退避|
| 500 | 500内部服务器错误 |服务器端问题 |重试请求或联系支持 |

## 速率限制

LabArchives 实施速率限制以确保服务稳定性：

- **推荐：** 每个 API 密钥每分钟最多 60 个请求
- **突发限额：** 可以容忍最多 100 个请求的短突发
- **最佳实践：** 实施批量操作请求之间有 1-2 秒的延迟

## API 版本控制

LabArchives API 向后兼容。添加新方法不会破坏现有的实现。监控 LabArchives 公告以了解新功能。

## 支持和文档

对于 API 访问请求、技术问题或功能请求：
- 电子邮件：support@labarchives.com
- 包括您的机构名称和特定用例以获得更快的帮助
