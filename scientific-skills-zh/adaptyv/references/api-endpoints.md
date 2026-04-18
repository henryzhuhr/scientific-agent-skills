# Adaptyv Bio Foundry API — 完整端点参考

基本 URL：`https://foundry-api-public.adaptyvbio.com/api/v1`
OpenAPI 规范：`GET /openapi.json`

## 目录

- [实验](#experiments)
- [序列](#sequences)
- [结果](#results)
- [目标](#targets)
- [引号](#quotes)
- [令牌](#tokens)
- [更新](#updates)
- [反馈](#feedback)

- --

## 实验

### POST /experiments — 创建实验

创建一个新实验。默认以`Draft`状态启动。

* *请求体：**

|领域 |类型 |必填 |描述 |
|---|---|---|---|
| `name` |字符串|是的 |人类可读的名称 |
| `experiment_spec` |实验规格|是的 |实验定义（见下文）|
| `skip_draft` |布尔 |否（默认 false）|绕过Draft，直接进入WaitingForConfirmation |
| `auto_accept_quote` |布尔 |否（默认 false）|自动接受报价并创建发票|
| `webhook_url` |字符串/空 |没有 |状态更改 POST 通知的 URL |

* *ExperimentSpec:**

|领域 |类型 |必填 |描述 |
|---|---|---|---|
| `experiment_type` |字符串|是的 | `affinity`、`screening`、`thermostability`、`fluorescence` 或 `expression` |
| `method` |字符串|绑定类型必需 | `bli` 或 `spr` |
| `target_id` | uuid|绑定类型必需 |目录中的目标 UUID |
| `sequences` |对象|是的 |名称映射→氨基酸字符串或丰富对象|
| `n_replicates` |整数 |推荐（默认3）|技术重复（最少 1 次）|
| `antigen_concentrations` |数字[] |否（仅限亲和力）|默认为 `[1000.0, 316.2, 100.0, 31.6, 0.0]` nM |
| `parameters` |对象|没有 |实验特定设置 |

* *实验类型的现场要求：**

|领域 |亲和力|放映|热稳定性 |荧光|表达式 |
|---|---|---|---|---|---|
| `experiment_type` |必填|必填|必填|必填|必填|
| `method` |必填|必填| — | — | — |
| `target_id` |必填|必填| — | — | — |
| `sequences` |必填|必填|必填|必填|必填|
| `n_replicates` |推荐|推荐|可选 |可选 |可选|
| `antigen_concentrations` |可选 | — | — | — | — |

* *响应（201）：**

|领域 |类型 |描述 |
|---|---|---|
| `experiment_id` |字符串|新实验UUID |
| `error` |字符串/空 |验证失败时出现错误消息|
| `stripe_hosted_invoice_url` |字符串/空 | `auto_accept_quote` 创建发票时出现 |
| `stripe_invoice_id` |字符串/空 | Stripe 发票 ID |

* *状态代码：** 201、400、401、403、404

- --

### GET /experiments — 列出实验

列出调用者可访问的实验，按创建日期排序（最新的在前）。

* *查询参数：** `limit`、`offset`、`filter`、`search`、`sort`

* *响应项：**

|领域 |类型 |描述 |
|---|---|---|
| `id` | uuid|唯一标识符|
| `code` |字符串|例如，“EXP-2024-001”|
| `name` |字符串/空 |人类可读的名称 |
| `status` |实验状态 |当前生命周期状态|
| `experiment_type` |实验类型 |亲和力/筛选/热稳定性/荧光/表达|
| `results_status` |结果状态 |无/部分/全部|
| `created_at` |日期时间 | ISO 8601 |
| `experiment_url` |字符串| Foundry 门户的 URL |
| `stripe_invoice_url` |字符串/空 |发票网址 |
| `stripe_quote_url` |字符串/空 |引用 URL |

* *状态代码：** 200, 401

- --

### GET /experiments/{experiment_id} — 获取实验

返回单个实验的完整元数据。

* *路径参数：** `experiment_id`（uuid）

* *响应：**

|领域 |类型 |描述 |
|---|---|---|
| `id` | uuid|唯一标识符|
| `code` |字符串|实验代码|
| `status` |实验状态 |目前状态|
| `experiment_spec` |实验规格|完整实验定义|
| `results_status` |结果状态 |无/部分/全部|
| `created_at` |日期时间 | ISO 8601 |
| `experiment_url` |字符串|门户网址|
| `costs` |对象|成本细分 |

* *状态代码：** 200、401、404、500

- --

### PATCH /experiments/{experiment_id} — 更新实验

修改现有实验。实验草稿允许完全编辑；生成报价后，只有 `name`、`description` 和 `webhook_url` 是可编辑的。

* *路径参数：** `experiment_id` (uuid)

* *请求正文：** 所有字段都是可选的 — 仅更新提供的字段。

  * *状态代码：** 200、400、401、404、409

- --

### POST /experiments/{experiment_id}/submit — 提交实验

提交实验草稿以供审核。从 `Draft` 升级到 `WaitingForConfirmation`.

* *路径参数：** `experiment_id`（uuid）

* *响应：**

|领域 |类型 |描述 |
|---|---|---|
| `experiment_id` |字符串|实验 UUID |

* *状态代码：** 200, 401, 403, 404, 409, 500

- --

### POST /experiments/cost-estimate — 估算成本

在不创建实验的情况下计算成本。

* *请求主体：**
```json
{
  "experiment_spec": {
    "experiment_type": "screening",
    "method": "bli",
    "target_id": "...",
    "sequences": {"seq1": "MKTL..."},
    "n_replicates": 3
  }
}
```

* *响应：**

|领域 |类型 |描述 |
|---|---|---|
| `pricing_version` |字符串|例如，“v1_2026-01-20”|
| `assay` |对象|具有基本定价和重复定价的每种类型成本 |
| `materials` |对象|目标材料成本（结合实验）|
| `total_cents` |整数 |总价以美元计 |

所有价格均不含增值税；开票时计算的税费。没有自助定价的目标返回不完整的估算值。

* *状态代码：** 200、400、401

- --

### GET /experiments/{experiment_id}/quote — 获取报价

返回报价元数据（总计、货币、状态、到期时间）。

* *路径参数：** `experiment_id`（uuid）

* *响应：**

|领域 |类型 |描述 |
|---|---|---|
| `experiment_id` |字符串|实验UUID |
| `stripe_quote_url` |字符串|条纹报价网址|
| `amount_total` | int64 |最小货币单位合计 |
| `amount_subtotal` | int64 |小计|
| `currency` |字符串| ISO 货币代码（例如“usd”）|
| `status` |字符串|报价状态|
| `expires_at` |日期时间/空 |到期时间 |

* *状态代码：** 200、401、403、404、500

- --

### GET /experiments/{experiment_id}/quote/pdf — 获取报价 PDF

以 PDF 文件形式返回报价(`application/pdf`).

* *路径参数：** `experiment_id` (uuid)

* *状态代码：** 200, 401, 403, 404, 500

- --

### POST /experiments/{experiment_id}/quote/confirm — 接受报价（通过实验）

接受 Stripe 报价，创建草稿发票，转换到 `WaitingForMaterials`.

* *路径参数：** `experiment_id` (uuid)

* *请求正文：**

|领域 |类型 |必填 |描述 |
|---|---|---|---|
| `purchase_order_number` |字符串/空 |没有 |供您记录的采购订单号 |
| `notes` |字符串/空 |没有 |保留 |

* *回复：**

|领域 |类型 |描述 |
|---|---|---|
| `id` |字符串|报价ID |
| `status` | StripeQuote 状态 |新状态|
| `hosted_invoice_url` |字符串/空 |条纹支付网址|
| `invoice_id` |字符串/空 |生成的发票 ID |

* *状态代码：** 200、401、403、404、409

- --

### GET /experiments/{experiment_id}/invoice — 获取发票

返回发票元数据，包括托管付款 URL。

* *路径param:** `experiment_id` (uuid)

* *状态代码:** 200, 401, 403, 404, 500

- --

### GET /experiments/{experiment_id}/results — 列出实验结果

返回所有分析结果一个具体的实验。

* *路径参数：** `experiment_id` (uuid)
  * *查询参数：** `limit`、`offset`、`filter`、`sort`

  * *状态码：** 200、400、401、403、 404

- --

### GET /experiments/{experiment_id}/sequences — 列出实验序列

返回特定实验的所有序列，最新的先排序。

* *路径参数：** `experiment_id` (uuid)
* *查询参数：** `limit`、`offset`、`search`、`sort`

* *状态代码：** 200、400、401、403、404

- --

### GET /experiments/{experiment_id}/updates —列出实验更新

返回一个实验的更新，最旧的第一个。类型：`status_change`、`progress`、`error`.

* *路径参数：** `experiment_id` (uuid)
* *查询参数：** `limit`、`offset`、 `filter`、`sort`

过滤器示例：`filter=eq(type,status_change)`

- --

## 序列

### GET /sequences — 列表序列

返回所有实验的序列，最新的先排序。

* *查询参数：** `limit`、`offset`、`search`、`sort`、`experiment_id`（按实验 UUID 过滤）

* *响应项：**

|领域 |类型 |描述 |
|---|---|---|
| `id` | uuid|唯一标识符|
| `name` |字符串/空 |可选名称|
| `aa_preview` |字符串/空 |截断预览（前 50 个字符）|
| `length` | int32 |氨基酸序列长度|
| `experiment_id` | uuid|亲子实验|
| `experiment_code` |字符串|人类可读的实验代码 |
| `is_control` |布尔 |这是否是一个控件|
| `created_at` |日期时间 |创建时间戳 |

* *状态代码：** 200, 401

- --

### GET /sequences/{sequence_id} — 获取序列

返回完整详细信息，包括完整的氨基酸字符串。

* *路径参数：** `sequence_id` (uuid)

* *回复：**

|领域 |类型 |描述 |
|---|---|---|
| `id` | uuid|唯一标识符|
| `aa_string` |字符串/空 |完整氨基酸序列|
| `length` | int32 |氨基酸长度|
| `is_control` |布尔 |控制标志|
| `metadata` |对象|序列级注释|
| `experiment` |对象|亲实验参考|
| `created_at` |日期时间 |创建时间戳 |

* *状态代码：** 200、401、403、404、500

- --

### POST /sequences — 将序列添加到实验

将序列附加到由其人类可读代码标识的 **草稿** 实验。

* *请求机身：**

|领域 |类型 |必填 |描述 |
|---|---|---|---|
| `experiment_code` |字符串|是的 |例如，“PROJ-001”|
| `sequences` |数组|是的 |序列条目数组 |

* *每个序列条目：**

|领域 |类型 |必填 |描述 |
|---|---|---|---|
| `aa_string` |字符串|是的 |氨基酸序列|
| `name` |字符串|没有 |人类可读的名称 |
| `control` |布尔 |没有 |这是否是一个控件|
| `metadata` |对象|没有 |注释 |

* *响应 (201):**

|领域 |类型 |描述 |
|---|---|---|
| `added_count` | int32 |添加的序列数|
| `experiment_id` |字符串|实验UUID |
| `experiment_code` |字符串|实验代码|
| `sequence_ids` |数组|已添加序列的ID |

* *状态码：** 201, 400, 404, 409（实验不在草稿中），500

- --

## 结果

### GET /results — 列出结果

列出已完成的分析结果，从新排序。当 `results_status` 到达 `partial` 或 `all`.

 时出现结果**查询参数：** `limit`、`offset`、`filter`、`search`、`sort`

* *响应项：**

|领域 |类型 |描述 |
|---|---|---|
| `id` | uuid|结果标识符|
| `title` |字符串|人类可读的标题 |
| `experiment_id` | uuid|相关实验|
| `result_type` |字符串|例如，“亲和力”、“热稳定性”|
| `summary` |数组|主要结果（特定类型，见下文）|
| `metadata` |对象|扩展元数据（例如仪器信息）|
| `data_package_url` |字符串/空 |原始数据包下载地址|
| `created_at` |日期时间 |结果生成时|

* *AffinityResult 摘要字段：** `kd_mean`、`kd_std`、`kon_mean`、`kon_log_std`、`koff_mean`、`koff_std`、`replicates`（包含每个重复 `kd` 的数组， `kon`、`koff`、`binding_strength`、`kon_method`、`koff_method`、`replicate` 索引）、`sequence`、`target_id`

* *热稳定性结果汇总字段：** Tm 值和熔解曲线

* *状态代码：** 200, 401

- --

### GET /results/{result_id} — 获取结果

返回详细结果数据，包括完整摘要数组。

* *路径参数：** `result_id` (uuid)

* *状态代码：** 200、401、403、404、500

- --

## Targets

### GET /targets — 列出目标

列出可用于实验的经过验证的抗原。

* *查询参数：**

|参数|类型 |描述 |
|---|---|---|
| `limit` |整数 |最大项目数（1-100，默认 50）|
| `offset` |整数 |跳过计数|
| `search` |字符串|产品名称自由文本搜索 |
| `sort` |字符串|排序表达式 |
| `selfservice_only` |布尔 |仅适用于自助定价 |
| `show_conjugated` |布尔 |包括缀合目标（默认：仅未缀合）|
| `detailed` |布尔 |使用富集数据填充 `details` 块 |

* *响应项：**

|领域 |类型 |描述 |
|---|---|---|
| `id` | uuid|目标UUID（用作`experiment_spec.target_id`）|
| `name` |字符串|目标名称|
| `vendor_name` |字符串|供应商名称|
| `catalog_number` |字符串|供应商目录/SKU 编号 |
| `url` |字符串|目标网址|
| `pricing` |对象/空 |自助定价（空=需要自定义报价）|
| `details` |对象/空 |富集数据（基因名称、结构、序列、生物活性）|

* *状态代码：** 200、401

- --

### GET /targets/{target_id} — 获取目标

返回单个目标的目录记录。

* *路径参数：** `target_id` (uuid)

* *状态代码：** 200、400、401、403、404、500

- --

### POST /targets/request-custom — 提交自定义目标请求

提交新的自定义目标以供工作人员审核。必须至少提供`sequence`或`pdb_id`之一。

* *请求正文：**

|领域 |类型 |必填 |描述 |
|---|---|---|---|
| `name` |字符串|是的 |显示名称 |
| `product_id` |字符串|是的 |在组织内必须是唯一的 |
| `sequence` |字符串/空 |至少一个 |氨基酸序列 |
| `pdb_id` |字符串/空 |至少一个 | PDB 标识符 |
| `pdb_file` |字符串/空 |没有 | PDB文件内容|
| `molecular_weight` |数字/空 |没有 |重量（kDa）|
| `note` |字符串/空 |没有 |附加说明 |

* *状态代码：** 201、400、401、403、500

- --

### GET /targets/request-custom — 列出自定义目标请求

返回您组织的自定义目标请求，按最新顺序排序。

* *查询参数：** `limit`、`offset`、`filter`、`sort`

过滤器示例：`filter=eq(status,pending_review)`

- --

### GET /targets/request-custom/{request_id} — 获取自定义目标请求

* *路径参数：** `request_id` (uuid)

  * *响应：**

|领域 |类型 |描述 |
|---|---|---|
| `id` | uuid|请求标识符|
| `name` |字符串|目标名称|
| `product_id` |字符串|您的产品ID |
| `status` |字符串|例如，“pending_review”|
| `material_id` |字符串/空 |如果获得批准，则链接目录 ID |
| `molecular_weight` |数字/空 |重量（kDa）|
| `note` |字符串/空 |用户须知|
| `created_at` |日期时间 |创建|
| `updated_at` |日期时间 |最后更新 |

* *状态代码：** 200, 401, 403, 404, 500

- --

## Quotes

### GET /quotes — 列表报价

返回呼叫者组织的所有报价。

* *查询参数：** `limit`、`offset`、`filter`、`sort`

* *回复项：**

|领域 |类型 |描述 |
|---|---|---|
| `id` |字符串|报价标识符|
| `quote_number` |字符串|人类可读的报价编号|
| `organization_id` | uuid|组织|
| `amount_cents` |整数 |金额以分为单位 |
| `currency` |字符串| ISO 4217 代码 |
| `status` | StripeQuote 状态 |报价状态|
| `valid_until` |日期时间 |到期|
| `created_at` |日期时间 |创建时间戳 |

- --

### GET /quotes/{quote_id} — 获取报价

返回包含分项定价的完整报价文档。

* *路径参数：** `quote_id`（字符串，例如， "qt_1Abc2DefGhi")

* *响应：**

|领域 |类型 |描述 |
|---|---|---|
| `id` |字符串|报价标识符|
| `quote_number` |字符串|参考编号|
| `organization_id` | uuid|组织|
| `organization_name` |字符串|组织名称|
| `line_items` |数组|明细定价|
| `subtotal_cents` |整数 |以分为单位的小计 |
| `tax_cents` |整数 |税费以分为单位|
| `total_cents` |整数 |总计（美分）|
| `currency` |字符串| ISO 4217 |
| `status` | StripeQuote 状态 |目前状态|
| `valid_until` |日期时间 |过期|
| `notes` |字符串|特别定价信息|
| `terms_and_conditions` |字符串|条款|
| `stripe_quote_url` |字符串|条纹网址 |
| `created_at` |日期时间 |已创建 |

* *状态代码：** 200、401、403、404、500

- --

### POST /quotes/{quote_id}/confirm — 接受报价

完成报价，创建草稿发票，将实验推进到 `WaitingForMaterials`.

* *路径参数：** `quote_id`（字符串）

* *请求正文：**

|领域 |类型 |必填 |描述 |
|---|---|---|---|
| `purchase_order_number` |字符串/空 |没有 |订单号|
| `notes` |字符串/空 |没有 |保留 |

* *响应：** `id`、`status`、`hosted_invoice_url`、`invoice_id`

* *状态码：** 200、403、404、409、 500

- --

### POST /quotes/{quote_id}/reject — 拒绝报价

取消报价；链接的实验恢复为 `Draft`.

* *路径参数：** `quote_id`（字符串）

* *请求正文：**

|领域 |类型 |必填 |描述 |
|---|---|---|---|
| `reason` |报价拒绝原因 |是的 |主要原因|
| `feedback` |字符串/空 |没有 |附加反馈 |

* *回复：** `id`、`status`（已取消）

* *状态代码：** 200、403、404、409、500

- --

## Tokens

### GET /tokens — 列出 token

返回调用者拥有的所有令牌（根和衰减）。

* *查询参数：** `limit`、`offset`

* *响应项目：**

|领域 |类型 |描述 |
|---|---|---|
| `id` |字符串|代币标识符|
| `name` |字符串|人类可读标签|
| `kind` |字符串| “根”或“减弱”|
| `created_at` |日期时间 |创建|
| `expires_at` |日期时间/空 |过期（空=无过期）|
| `revoked_at` |日期时间/空 |撤销时间戳|
| `parent_token_id` |字符串/空 |父级（根为空）|
| `root_token_id` |字符串/空 |推导树根|
| `attenuation_spec` |对象/空 |限制（对于 root 为空）|

- --

### POST /tokens/attenuate — 衰减令牌

使用 Biscuit 加密衰减创建现有令牌的受限版本。

* *请求正文：**

|领域 |类型 |必填 |描述 |
|---|---|---|---|
| `token` |字符串|是的 |现有代币（`abs0_{slug}{biscuit_base64}`）|
| `attenuation` |衰减规格 |是的 |适用限制|
| `name` |字符串|是的 |人类可读标签|
| `attenuated_parent_token_id` | uuid/空 |没有 |链式衰减的父 ID |

* *限制类型：** 组织、资源（实验/结果）、操作（读取/创建/更新）、过期

* *响应 (201)：** `id`（数据库 ID）、`token`（新衰减令牌字符串）

* *状态代码：** 201, 400, 401, 403

- --

### POST /tokens/revoke — 撤销令牌和谱系

撤销调用令牌的根和所有减弱的后代。幂等.

* *响应：**

|领域 |类型 |描述 |
|---|---|---|
| `token_id` |字符串|根令牌 ID 已撤销 |
| `revoked_at` |日期时间 |撤销时间戳|
| `children_revoked` | int64 |新撤销的子令牌 |

* *状态代码：** 200、403、404

- --

## 更新

### GET /updates — 列表更新

返回实验更新源（最新的在前）：状态更改、进度、错误。

* *查询参数：** `limit`、`offset`、`filter`、`sort`

* *过滤器示例：**
- `filter=eq(experiment_id,<uuid>)`
- `filter=in(experiment_id,uuid1,uuid2)`
- `filter=eq(type,status_change)`

* *回复项：**

|领域 |类型 |描述 |
|---|---|---|
| `id` |字符串|更新标识符|
| `experiment_id` | uuid|相关实验|
| `experiment_code` |字符串|人类可读代码|
| `name` |字符串|更新说明|
| `timestamp` |日期时间 |更新时 |

- --

## 反馈

### POST /feedback/submit — 提交反馈

用于错误报告、功能请求或一般反馈。

* *请求正文：**

|领域 |类型 |必填 |描述 |
|---|---|---|---|
| `request_uuid` | uuid|是的 |来自有问题的 API 请求的 UUID |
| `feedback_type` |反馈类型 |是的 | `feature_request`、`feedback` 或 `bug_report` |
| `title` |字符串/空 |没有 |短标题|
| `json_body` |对象/空 |至少一个 |结构化错误详细信息 |
| `human_note` |字符串/空 |至少一个 |自由格式描述 |

* *响应 (201):** `reference`（反馈参考）、`message`（确认）

* *状态代码：** 201、400、401、500
