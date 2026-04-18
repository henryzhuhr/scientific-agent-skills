# 数据丰富

Enrich: $ARGUMENTS

## 开始之前

通知用户丰富可能需要几分钟，具体取决于请求的行数和字段数。

## 步骤 1：开始丰富

使用以下命令模式之一（替换用户的实际数据）：

用于内联数据：

```bash
parallel-cli enrich run --data '[{"company": "Google"}, {"company": "Microsoft"}]' --intent "CEO name and founding year" --target "output.json" --no-wait --json
```

对于 CSV 文件：

```bash
parallel-cli enrich run --source-type csv --source "input.csv" --target "/tmp/output.json" --source-columns '[{"name": "company", "description": "Company name"}]' --intent "CEO name and founding year" --no-wait --json
```

如果这是您知道 `interaction_id` 的先前研究或丰富任务的**后续**，请添加上下文链接：

```bash
parallel-cli enrich run --data '...' --intent "..." --target "output.json" --no-wait --json --previous-interaction-id "$INTERACTION_ID"
```

通过跨请求链接 `interaction_id` 值，每个后续操作都会自动具有先前轮次的完整上下文 - 因此您可以丰富早期研究中发现的实体，而无需重述已发现的内容。

 * *重要：** 始终包含 `--no-wait`，以便命令立即返回，而不是立即返回blocking.

解析输出以提取`taskgroup_id`、`interaction_id`和监控URL。立即告诉用户：
- 丰富化已启动
- 他们可以跟踪进度的监控 URL

 告诉他们可以将轮询步骤置于后台以在运行时继续工作。

## 步骤 2：轮询结果

根据丰富任务选择一个简短的描述性文件名（例如，`companies-ceos`、`startups-funding`）。使用带连字符的小写字母，无空格。

```bash
parallel-cli enrich poll "$TASKGROUP_ID" --timeout 540 --json --output "$FILENAME.json"
```

`enrich run` 上的 `--target` 标志不会延续到投票中 — 您必须在此处传递 `--output` 才能保存结果。始终使用 `--json` 获取结构化 JSON 输出。

重要：
 - 使用 `--timeout 540`（9 分钟）保持在工具执行限制内

### 如果轮询超时

大型数据集的丰富可能需要超过 9 分钟的时间。如果投票未完成就退出：
1. 告诉用户浓缩仍在服务器端运行
2. 重新运行相同的`parallel-cli enrich poll`命令继续等待

## 响应格式

* *第 1 步之后：** 共享监控 URL（用于跟踪进度）。

  * *第 2 步之后：**
1. 报告行数丰富
2. 预览输出 JSON
3 的前几行。告诉用户输出 JSON 文件的完整路径 (`$FILENAME.json`)
4. 共享 `interaction_id` 并告诉用户他们可以提出基于此丰富的后续问题

完成后不要重新共享监控 URL — 结果位于输出文件中。

* *记住 `interaction_id`** — 如果用户提出与此丰富相关的后续问题，请在下一次研究或丰富中将其用作 `--previous-interaction-id`命令.
