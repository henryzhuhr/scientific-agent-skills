---
name: adaptyv
author: "K-Dense, Inc."
description: "如何使用 Adaptyv Bio Foundry API 和 Python SDK 进行蛋白质实验设计、提交和结果检索。每当用户提及 Adaptyv、Foundry API、蛋白质结合测定、蛋白质筛选实验、BLI/SPR 测定、热稳定性测定或想要提交蛋白质序列进行实验表征时，请使用此技能。当代码导入“adaptyv”、“adaptyv_sdk”或“FoundryClient”或引用“foundry-api-public.adaptyvbio.com”时也会触发。"
---

# Adaptyv Bio Foundry API

Adaptyv Bio 是一个云实验室，可将蛋白质序列转化为实验数据。用户通过API或UI提交氨基酸序列； Adaptyv 的自动化实验室运行测定（结合、热稳定性、表达、荧光）并在大约 21 天内提供结果。

## 快速入门

* *基本 URL：** `https://foundry-api-public.adaptyvbio.com/api/v1`

  * *身份验证：** `Authorization` 标头中的承载令牌。代币从 [foundry.adaptyvbio.com](https://foundry.adaptyvbio.com/) sidebar.

 获取编写代码时，请始终从环境变量 `ADAPTYV_API_KEY` 或 `.env` 文件中读取 API 密钥 - 切勿硬编码令牌。首先检查项目根目录下是否有`.env`文件；如果存在，请使用 `python-dotenv` 之类的库来加载它。 

```bash
export FOUNDRY_API_TOKEN="abs0_..."
curl https://foundry-api-public.adaptyvbio.com/api/v1/targets?limit=3 \
  -H "Authorization: Bearer $FOUNDRY_API_TOKEN"
```

 除 `GET /openapi.json` 之外的每个请求都需要身份验证。将令牌存储在环境变量或 `.env` 文件中 - 切勿将它们提交到源代码管理。

## Python SDK

Install：`uv add adaptyv-sdk`（如果不存在 `pyproject.toml`，则回退到 `uv pip install adaptyv-sdk`）

* *环境变量**（在shell或`.env`文件中设置）：
```bash
ADAPTYV_API_KEY=your_api_key
ADAPTYV_API_URL=https://foundry-api-public.adaptyvbio.com/api/v1
```

### 装饰器模式

```python
from adaptyv import lab

@lab.experiment(target="PD-L1", experiment_type="screening", method="bli")
def design_binders():
    return {"design_a": "MVKVGVNG...", "design_b": "MKVLVAG..."}

result = design_binders()
print(f"Experiment: {result.experiment_url}")
```

### 客户端模式

```python
from adaptyv import FoundryClient

client = FoundryClient(api_key="...", base_url="https://foundry-api-public.adaptyvbio.com/api/v1")

# Browse targets
targets = client.targets.list(search="EGFR", selfservice_only=True)

# Estimate cost
estimate = client.experiments.cost_estimate({
    "experiment_spec": {
        "experiment_type": "screening",
        "method": "bli",
        "target_id": "target-uuid",
        "sequences": {"seq1": "EVQLVESGGGLVQ..."},
        "n_replicates": 3
    }
})

# Create and submit
exp = client.experiments.create({...})
client.experiments.submit(exp.experiment_id)

# Later: retrieve results
results = client.experiments.get_results(exp.experiment_id)
```

## 实验类型

|类型 |方法|措施|需要目标 |
|---|---|---|---|
| `affinity` | `bli` 或 `spr` | KD、kon、koff 动力学 |是 |
| `screening` | `bli` 或 `spr` |是/否绑定 |是 |
| `thermostability` | — |熔化温度（Tm）|否|
| `expression` | — |表达产量|否|
| `fluorescence` | — |荧光强度|否 |

## 实验生命周期

```
Draft → WaitingForConfirmation → QuoteSent → WaitingForMaterials → InQueue → InProduction → DataAnalysis → InReview → Done
```

|状态 |谁在行动 |描述 |
|---|---|---|
| `Draft` |你|可编辑，无成本承诺|
| `WaitingForConfirmation` | Adaptyv |审核中，报价准备中|
| `QuoteSent` |你|审核并确认报价|
| `WaitingForMaterials` | Adaptyv |基因片段和靶点排序|
| `InQueue` | Adaptyv |材料到达，排队等待实验室|
| `InProduction` | Adaptyv |检测运行|
| `DataAnalysis` | Adaptyv |原始数据处理和QC |
| `InReview` | Adaptyv |最终验证|
| `Done` |你|结果可用|
| `Canceled` |要么 |专家立即取消 |

实验轨道上的 `results_status` 字段：`none`、`partial` 或 `all`.

## 常见工作流程

### 1. 提交绑定屏幕（步骤步骤）

```python
# 1. Find a target
targets = client.targets.list(search="EGFR", selfservice_only=True)
target_id = targets.items[0].id

# 2. Preview cost
estimate = client.experiments.cost_estimate({
    "experiment_spec": {
        "experiment_type": "screening",
        "method": "bli",
        "target_id": target_id,
        "sequences": {"seq1": "EVQLVESGGGLVQ...", "seq2": "MKVLVAG..."},
        "n_replicates": 3
    }
})

# 3. Create experiment (starts as Draft)
exp = client.experiments.create({
    "name": "EGFR binder screen batch 1",
    "experiment_spec": {
        "experiment_type": "screening",
        "method": "bli",
        "target_id": target_id,
        "sequences": {"seq1": "EVQLVESGGGLVQ...", "seq2": "MKVLVAG..."},
        "n_replicates": 3
    }
})

# 4. Submit for review
client.experiments.submit(exp.experiment_id)

# 5. Poll or use webhooks until Done
# 6. Retrieve results
results = client.experiments.get_results(exp.experiment_id)
```

### 2.自动化管道（跳过草稿+自动接受报价）

```python
exp = client.experiments.create({
    "name": "Auto pipeline run",
    "experiment_spec": {...},
    "skip_draft": True,
    "auto_accept_quote": True,
    "webhook_url": "https://my-server.com/webhook"
})
# Webhook fires on each status transition; poll or wait for Done
```

### 3.使用Webhooks

创建实验时传递`webhook_url`。 Adaptyv 在每次状态转换时使用实验 ID、先前状态和新状态 POST 到该 URL。

## 序列

- 简单格式：`{"seq1": "EVQLVESGGGLVQPGGSLRLSCAAS"}`
  - 丰富格式：`{"seq1": {"aa_string": "EVQLVESGGGLVQ...", "control": false, "metadata": {"type": "scfv"}}}`
  - 多链：使用冒号分隔符 — `"MVLS:EVQL"`
  - 有效氨基酸：A、C、D、E、F、G、H、I、K、L、M、N、P、Q、R、S、T、V、W、Y （不区分大小写，存储大写）
- 序列只能添加到 `Draft` 状态的实验

## 过滤、排序和分页

所有列表端点都支持分页（`limit` 1-100，默认 50；`offset`）、搜索（名称上的自由文本）字段），并排序。

* *过滤**通过`filter`查询参数使用s-表达式语法：
- 比较：`eq(field,value)`、`neq`、`gt`、`gte`、`lt`、`lte`、 `contains(field,substring)`
- 范围/设置：`between(field,lo,hi)`、`in(field,v1,v2,...)`
- 逻辑：`and(expr1,expr2,...)`、`or(...)`、`not(expr)`
- 空：`is_null(field)`、 `is_not_null(field)`
- JSONB：`at(field,key)` — 例如，`eq(at(metadata,score),42)`
- 演员：`float()`、`int()`、`text()`、`timestamp()`、 `date()`

* *排序**使用`asc(field)`或`desc(field)`，逗号分隔（最多8个）：
```
sort=desc(created_at),asc(name)
```

* *示例：** `filter=and(gte(created_at,2026-01-01),eq(status,done))`

## 错误处理

所有错误返回：
```json
{
  "error": "Human-readable description",
  "request_id": "req_019462a4-b1c2-7def-8901-23456789abcd"
}
```
`request_id` 也在 `x-request-id` 响应标头中 - 联系支持人员时将其包括在内。

## 令牌管理

令牌使用基于 Biscuit 的加密衰减。您可以通过 `POST /tokens/attenuate` 创建按组织、资源类型、操作（读取/创建/更新）和过期范围划分的受限令牌。撤销令牌 (`POST /tokens/revoke`)会撤销它及其所有后代。

## 详细 API 参考

有关具有请求/响应模式的所有 32 个端点的完整列表，请阅读 `references/api-endpoints.md`.
