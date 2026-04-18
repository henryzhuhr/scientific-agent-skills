# 工作空间 API

## 概述

protocols.io 中的工作空间通过组织协议、管理成员和控制访问权限来实现团队协作。工作区 API 允许您列出工作区、管理成员资格以及访问工作区特定的协议。

## 基本 URL

所有工作区端点都使用基本 URL：`https://protocols.io/api/v3`

## 工作区操作

### 列出用户工作区

检索经过身份验证的用户有权访问的所有工作区to.

* *端点：** `GET /workspaces`

* *查询参数：**
- `page_size`：每页结果数（默认：10，最大：50）
- `page_id`：分页页码（从0开始）

* *响应包括：**
- 工作空间 ID 和名称
- 工作空间类型（个人、群组、机构）
- 成员计数
- 访问级别（所有者、管理员、成员、查看者）
- 创建日期

* *示例请求：**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/workspaces"
```

### 获取工作空间详细信息

检索特定工作空间的详细信息。

* *端点：** `GET /workspaces/{workspace_id}`

* *路径参数：**
- `workspace_id`：工作空间唯一标识符

* *响应包括：**
- 完整工作区元数据
- 包含角色的成员列表
- 工作区设置和权限
- 协议计数和类别

## 工作区成员资格

### 列出工作区成员

检索某个成员的所有成员workspace.

* *端点：** `GET /workspaces/{workspace_id}/members`

* *查询参数：**
- `page_size`：每页结果数
- `page_id`：分页页码

* *响应包括：**
- 成员名称和电子邮件
- 角色（所有者、管理员、成员、查看者）
- 加入日期
- 活动状态

### 请求工作空间访问

请求加入工作空间。

* *端点：** `POST /workspaces/{workspace_id}/join-request`

* *请求正文：**
- `message`（可选）：向工作区管理员发送的消息，解释请求

* *请求示例：**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am collaborating with Dr. Smith on the CRISPR project and would like to access the shared protocols."
  }' \
  "https://protocols.io/api/v3/workspaces/12345/join-request"
```

### 加入公共工作区

无需批准即可直接加入公共工作区。

* *端点：** `POST /workspaces/{workspace_id}/join`

* *注意**：仅适用于配置为允许公共加入的工作区

## 工作区协议

### 列出工作区协议

检索工作区中的所有协议。

* *端点：** `GET /workspaces/{workspace_id}/protocols`

* *查询参数：**
- `filter`：过滤协议
  - `all`：工作区中的所有协议
  - `own`：仅您创建的协议
  - `shared`：共享的协议和你一起
- `key`：搜索关键词
- `order_field`：排序字段（`activity`、`created_on`、`modified_on`、`name`）
- `order_dir`：排序方向(`desc`, `asc`)
- `page_size`：每页结果数
- `page_id`：分页页码
- `content_format`：内容格式（`json`， `html`、`markdown`)

* *示例请求：**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/workspaces/12345/protocols?filter=all&order_field=modified_on&order_dir=desc"
```

### 在工作空间中创建协议

在特定工作空间中创建新协议。

* *端点：** `POST /workspaces/{workspace_id}/protocols`

* *请求体**：与标准协议创建参数相同（参见protocols_api.md）

* *注意**：协议将在工作空间内创建并继承工作空间权限

## 工作空间类型和权限

### 工作空间类型

1. **个人工作空间**
  - 个人用户的默认工作空间
  - 默认私有
  - 可以共享特定协议

2. **组工作空间**
  - 团队协作工作空间
  - 所有成员的共享访问权限
  - 基于角色的权限

3. **机构工作空间**
  - 组织范围的工作空间
  - 通常包括品牌
  - 集中协议管理

### 权限级别

1. **所有者**
  - 完全工作区控制
  - 管理成员和权限
  - 删除工作区

2. **管理员**
  - 管理协议和成员
  - 配置工作区设置
  - 无法删除工作区

3. **成员**
  - 创建和编辑协议
  - 查看所有工作区协议
  - 评论和协作

4. **查看者**
  - 仅查看访问
  - 可以对协议进行评论
  - 无法创建或编辑

## 常见用例

### 1. 实验室协议存储库

在共享工作区中组织实验室协议：

1. 创建或加入实验室工作区：`GET /workspaces`
2. 列出现有协议：`GET /workspaces/{id}/protocols`
3. 创建新协议：`POST /workspaces/{id}/protocols`
4. 邀请实验室成员：共享工作区邀请
5. 按类别或标签组织

### 2. 协作协议开发

与团队成员一起开发协议：

1. 确定目标工作空间：`GET /workspaces`
2. 在工作区
3 中创建协议草案。通过workspace
4自动与团队成员共享。通过评论收集反馈
5. 迭代并发布最终版本

### 3. 跨机构协作

与外部协作者合作：

1. 创建或识别共享工作区
2. 请求访问：`POST /workspaces/{id}/join-request`
3. 一旦获得批准，即可访问共享协议
4. 贡献新协议或更新
5. 在个人工作空间中维护机构协议副本

### 4.协议迁移

在工作空间之间移动协议：

1. 列出源工作区协议：`GET /workspaces/{source_id}/protocols`
2. 对于每个协议，检索完整的详细信息
3. 在目标工作区中创建协议：`POST /workspaces/{target_id}/protocols`
4. 复制所有步骤和元数据
5. 更新参考资料和链接

### 5. 工作区审计

审查工作区活动和内容：

1. 列出所有工作区：`GET /workspaces`
2. 对于每个工作区，获取成员列表
3. 检索带有活动日期 
4 的协议列表。识别不活动或过时的协议
5. 生成活动报告

## 工作空间管理最佳实践

1. **组织**
  - 使用一致的命名约定
  - 按项目或类别标记协议
  - 维护工作区目录或索引

2. **访问控制**
  - 定期查看成员列表
  - 分配适当的权限级别
  - 删除不活动的成员

3. **协议标准**
  - 建立工作区范围的协议模板
  - 定义所需的元数据字段
  - 实施质量审核流程

4. **协作**
  - 向成员传达工作区指南
  - 鼓励协议文档
  - 促进知识共享

5. **备份和存档**
  - 定期导出工作区协议
  - 维护协议版本历史记录
  - 存档已完成的项目

## 组织和工作空间

组织是可以包含多个工作空间的更高级别实体。

### 导出组织数据

* *端点：** `GET /organizations/{org_id}/export`

* *用例**：批量导出所有协议和工作区数据以用于机构存档或备份

## 通知和活动

工作区活动可能会触发通知：

- 添加到工作区的新协议
- 团队的协议更新成员
- 关于工作区协议的新评论
- 成员加入或离开工作区
- 权限更改

在帐户设置中配置通知首选项。

## 错误处理

常见错误响应：

- `400 Bad Request`：工作区ID无效或参数
- `401 Unauthorized`：缺少或无效的访问令牌
- `403 Forbidden`：工作区权限不足
- `404 Not Found`：找不到工作区或无法访问
- `429 Too Many Requests`：超出速率限制

## 集成注意事项

集成工作区功能时：

1. **缓存工作区列表**：避免重复工作区列表调用
2. **尊重权限**：在尝试操作之前检查用户的角色
3. **处理加入请求**：实施工作区访问批准的工作流程
4. **定期同步**：定期更新本地工作区数据
5. **支持离线访问**：离线工作的缓存协议，重连时同步
