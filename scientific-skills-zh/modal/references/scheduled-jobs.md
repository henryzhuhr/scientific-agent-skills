# Modal 计划作业

## 概述

Modal 支持按计划自动运行函数，可以使用 cron 语法或固定间隔。使用 `modal deploy` 部署计划函数，它们在云端无人值守地运行。

## 计划类型

### modal.Cron

标准 cron 语法 — 跨部署稳定：

```python
import modal

app = modal.App("scheduled-tasks")

# Daily at 9 AM UTC
@app.function(schedule=modal.Cron("0 9 * * *"))
def daily_report():
    generate_and_send_report()

# Every Monday at midnight
@app.function(schedule=modal.Cron("0 0 * * 1"))
def weekly_cleanup():
    cleanup_old_data()

# Every 15 minutes
@app.function(schedule=modal.Cron("*/15 * * * *"))
def frequent_check():
    check_system_health()
```

#### Cron 语法参考

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sun=0)
│ │ │ │ │
* * * * *
```

|图案|含义 |
|---------|---------|
| `0 9 * * *` |世界标准时间 (UTC)每日上午 9:00 |
| `0 */6 * * *` |每 6 小时 |
| `*/30 * * * *` |每30分钟一班|
| `0 0 * * 1` |每周一午夜|
| `0 0 1 * *` |每个月的第一天|
| `0 9 * * 1-5` |工作日上午 9 点 |

### modal.Period

固定间隔 — 每次部署时重置：

```python
# Every 5 hours
@app.function(schedule=modal.Period(hours=5))
def periodic_sync():
    sync_data()

# Every 30 minutes
@app.function(schedule=modal.Period(minutes=30))
def poll_updates():
    check_for_updates()

# Every day
@app.function(schedule=modal.Period(days=1))
def daily_task():
    ...
```

`modal.Period` 在每次部署时重置其计时器。如果您需要不随部署而变化的计划，请使用 `modal.Cron`.

## 部署计划功能

计划仅在部署时激活：

```bash
modal deploy script.py
```

`modal run` 和 `modal serve` 不会激活Schedules.

## 监控

- 在 Modal 仪表板的 **应用程序** 部分中查看计划的运行
- 每次运行都会显示其状态、持续时间和日志
- 使用仪表板上的 **“立即运行”** 按钮手动触发

## 管理

- 计划不能已暂停 — 删除计划并重新部署以停止
- 要更改计划，请更新 `schedule` 参数并重新部署`schedule`- 要完全停止，请删除 `schedule` 参数或运行 `modal app stop <name>`

## 常见模式

### ETL管道

```python
@app.function(
    schedule=modal.Cron("0 2 * * *"),  # 2 AM UTC daily
    secrets=[modal.Secret.from_name("db-creds")],
    timeout=7200,
)
def etl_pipeline():
    import os
    data = extract(os.environ["SOURCE_DB_URL"])
    transformed = transform(data)
    load(transformed, os.environ["DEST_DB_URL"])
```

### 模型再训练

```python
@app.function(
    schedule=modal.Cron("0 0 * * 0"),  # Weekly on Sunday
    gpu="H100",
    volumes={"/data": data_vol, "/models": model_vol},
    timeout=86400,
)
def retrain():
    model = train_on_latest_data("/data/training/")
    torch.save(model.state_dict(), "/models/latest.pt")
```

### 运行状况检查

```python
@app.function(
    schedule=modal.Period(minutes=5),
    secrets=[modal.Secret.from_name("slack-webhook")],
)
def health_check():
    import os, requests
    status = check_all_services()
    if not status["healthy"]:
        requests.post(os.environ["SLACK_URL"], json={"text": f"Alert: {status}"})
```
