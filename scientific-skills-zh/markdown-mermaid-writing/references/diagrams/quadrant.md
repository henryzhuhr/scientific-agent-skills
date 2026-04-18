<!-- 来源：https://github.com/SuperiorByteWorks-LLC/agent-project |许可证：Apache-2.0 |作者：Clayton Young / Superior Byte Works, LLC (Boreal Bytes) -->

# 象限图

> **返回[样式指南](../mermaid_style_guide.md)** — 首先阅读样式指南以了解表情符号、颜色和可访问性规则。

* *语法关键字：** `quadrantChart`
* *最适合：**优先级矩阵、风险评估、两轴比较、努力/影响分析
* *何时不使用：**基于时间的数据（使用 [Gantt](gantt.md)或 [XY Chart](xy_chart.md)）、简单排名（使用表格）

> ⚠️ **辅助功能：**象限图**不**支持`accTitle`/`accDescr`。始终将描述性的_斜体_ Markdown 段落直接放在代码块上方。

- --

## 示例图

_按所需工作量与业务影响绘制工程计划的优先级矩阵，帮助团队决定下一步要构建什么：_

```mermaid
quadrantChart
    title 🎯 Engineering Priority Matrix
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Do First
    quadrant-2 Plan Carefully
    quadrant-3 Reconsider
    quadrant-4 Quick Wins
    Upgrade auth library: [0.3, 0.9]
    Migrate to new DB: [0.9, 0.8]
    Fix typos in docs: [0.1, 0.2]
    Add dark mode: [0.4, 0.6]
    Rewrite legacy API: [0.95, 0.95]
    Update CI cache: [0.15, 0.5]
    Add unit tests: [0.5, 0.7]
```

- --

## 提示

- 使用 `Low X --> High X` 格式标记轴
- 使用 **可操作** 标签命名所有四个象限
- 将项目绘制为 `Name: [x, y]`，值为 0.0–1.0
- 限制为 **5–10 个项目** — 更多会变得混乱
- 象限编号：1=右上、2=左上、3=左下、4=右下
- **始终**与屏幕阅读器上面的 Markdown 文本描述配对

- --

## 模板

_两个轴的描述以及象限位置意思是：_

```mermaid
quadrantChart
    title 🎯 Your Matrix Title
    x-axis Low X Axis --> High X Axis
    y-axis Low Y Axis --> High Y Axis
    quadrant-1 High Both
    quadrant-2 High Y Only
    quadrant-3 Low Both
    quadrant-4 High X Only
    Item A: [0.3, 0.8]
    Item B: [0.7, 0.6]
    Item C: [0.2, 0.3]
```
