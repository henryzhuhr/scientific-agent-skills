# AI 辅助策展参考

使用 AI 视觉分析进行单元策展的指南，灵感来自 SpikeAgent 的方法。

## 概述

AI 辅助策展使用视觉语言模型来分析尖峰排序可视化，
 提供类似于人类策展人的专家级质量评估。

### 工作流程

```
Traditional:  Metrics → Threshold → Labels
AI-Enhanced:  Metrics → AI Visual Analysis → Confidence Score → Labels
```

## Claude 代码集成

在 Claude 代码中使用此技能时，Claude 可以直接分析波形图，无需 API 设置。简单地说：

1. 生成单位报告或绘图
2. 请克劳德分析可视化
3. Claude 将提供专家级的管理决策

Claude 代码中的示例工作流程：
```python
# Generate plots for a unit
npa.plot_unit_summary(analyzer, unit_id=0, output='unit_0_summary.png')

# Then ask Claude: "Please analyze this unit's waveforms and autocorrelogram
# to determine if it's a well-isolated single unit, multi-unit activity, or noise"
```

Claude 可以评估：
- 波形一致性和形状
- 自相关图的不应期违规
- 幅度稳定性time
- 整体单元隔离质量

## 快速入门

### 生成单元报告

```python
import neuropixels_analysis as npa

# Create visual report for a unit
report = npa.generate_unit_report(analyzer, unit_id=0, output_dir='reports/')

# Report includes:
# - Waveforms, templates, autocorrelogram
# - Amplitudes over time, ISI histogram
# - Quality metrics summary
# - Base64 encoded image for API
```

### AI可视化分析

```python
from anthropic import Anthropic

# Setup API client
client = Anthropic()

# Analyze single unit
result = npa.analyze_unit_visually(
    analyzer,
    unit_id=0,
    api_client=client,
    model='claude-opus-4.5',
    task='quality_assessment'
)

print(f"Classification: {result['classification']}")
print(f"Reasoning: {result['reasoning']}")
```

### 批量分析

```python
# Analyze all units
results = npa.batch_visual_curation(
    analyzer,
    api_client=client,
    output_dir='ai_curation/',
    progress_callback=lambda i, n: print(f"Progress: {i}/{n}")
)

# Get labels
ai_labels = {uid: r['classification'] for uid, r in results.items()}
```

## 交互式策展会议

用于人工智能辅助下的人机交互策展：

```python
# Create session
session = npa.CurationSession.create(
    analyzer,
    output_dir='curation_session/',
    sort_by_confidence=True  # Show uncertain units first
)

# Process units
while True:
    unit = session.current_unit()
    if unit is None:
        break

    print(f"Unit {unit.unit_id}:")
    print(f"  Auto: {unit.auto_classification} (conf: {unit.confidence:.2f})")

    # Generate report
    report = npa.generate_unit_report(analyzer, unit.unit_id)

    # Get AI opinion
    ai_result = npa.analyze_unit_visually(analyzer, unit.unit_id, api_client=client)
    session.set_ai_classification(unit.unit_id, ai_result['classification'])

    # Human decision
    decision = input("Decision (good/mua/noise/skip): ")
    if decision != 'skip':
        session.set_decision(unit.unit_id, decision)

    session.next_unit()

# Export results
labels = session.get_final_labels()
session.export_decisions('final_curation.csv')
```

## 分析任务

### 质量评估（默认）

分析波形形状、不应期、幅度稳定性。

```python
result = npa.analyze_unit_visually(analyzer, uid, task='quality_assessment')
# Returns: 'good', 'mua', or 'noise'
```

### 合并候选检测

确定是否应合并两个单元。

```python
result = npa.analyze_unit_visually(analyzer, uid, task='merge_candidate')
# Returns: 'merge' or 'keep_separate'
```

### 漂移评估

E评估记录中的运动/漂移。

```python
result = npa.analyze_unit_visually(analyzer, uid, task='drift_assessment')
# Returns drift magnitude and correction recommendation
```

## 自定义提示

创建自定义分析提示：

```python
from neuropixels_analysis.ai_curation import create_curation_prompt

# Get base prompt
prompt = create_curation_prompt(
    task='quality_assessment',
    additional_context='Focus on waveform amplitude consistency'
)

# Or fully custom
custom_prompt = """
Analyze this unit and determine if it represents a fast-spiking interneuron.

Look for:
1. Narrow waveform (peak-to-trough < 0.5ms)
2. High firing rate
3. Regular ISI distribution

Classify as: FSI (fast-spiking interneuron) or OTHER
"""

result = npa.analyze_unit_visually(
    analyzer, uid,
    api_client=client,
    custom_prompt=custom_prompt
)
```

## 将AI与指标相结合

最佳实践：使用AI 和定量指标：

```python
def hybrid_curation(analyzer, metrics, api_client):
    """Combine metrics and AI for robust curation."""
    labels = {}

    for unit_id in metrics.index:
        row = metrics.loc[unit_id]

        # High confidence from metrics alone
        if row['snr'] > 10 and row['isi_violations_ratio'] < 0.001:
            labels[unit_id] = 'good'
            continue

        if row['snr'] < 1.5:
            labels[unit_id] = 'noise'
            continue

        # Uncertain cases: use AI
        result = npa.analyze_unit_visually(
            analyzer, unit_id, api_client=api_client
        )
        labels[unit_id] = result['classification']

    return labels
```

## 会话管理

### 恢复会话

```python
# Resume interrupted session
session = npa.CurationSession.load('curation_session/20250101_120000/')

# Check progress
summary = session.get_summary()
print(f"Progress: {summary['progress_pct']:.1f}%")
print(f"Remaining: {summary['remaining']} units")

# Continue from where we left off
unit = session.current_unit()
```

### 导航会话

```python
# Go to specific unit
session.go_to_unit(42)

# Previous/next
session.prev_unit()
session.next_unit()

# Update decision
session.set_decision(42, 'good', notes='Clear refractory period')
```

### 导出结果

```python
# Get final labels (priority: human > AI > auto)
labels = session.get_final_labels()

# Export detailed results
df = session.export_decisions('curation_results.csv')

# Summary
summary = session.get_summary()
print(f"Good: {summary['decisions'].get('good', 0)}")
print(f"MUA: {summary['decisions'].get('mua', 0)}")
print(f"Noise: {summary['decisions'].get('noise', 0)}")
```

## 可视化报告组件

生成的报告包括6个面板：

|面板|内容 |寻找什么|
|------|----------|------------------|
|波形 |单个尖峰波形 |稠度、形状|
|模板|平均值±标准差|洁净负峰，生理形态|
|自相关图 |尖峰计时 | 0ms处的间隙（不应期）|
|振幅|振幅随时间变化|稳定、无漂移|
| ISI 直方图 |尖峰间间隔 |耐火间隙 < 1.5ms |
|指标|质量数字 | SNR、ISI 违规、存在 |

## API 支持

当前支持的 API：

|供应商|客户|型号示例|
|----------|--------|----------------|
|人择 | `anthropic.Anthropic()` |克劳德-opus-4.5 |
|开放人工智能 | `openai.OpenAI()` | gpt-4-vision-预览 |
|谷歌 | `google.generativeai` | gemini-pro-vision |

### 人类示例

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")
result = npa.analyze_unit_visually(analyzer, uid, api_client=client)
```

### OpenAI 示例

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")
result = npa.analyze_unit_visually(
    analyzer, uid,
    api_client=client,
    model='gpt-4-vision-preview'
)
```

## 最佳实践

1. **在不确定的情况下使用 AI** - 不要将 API 调用浪费在明显的好/噪音单元 
2 上。 **与指标相结合** - 人工智能应该补充而不是取代定量措施
3. **人类监督** - 审查人工智能决策，尤其是重要分析
4. **保存会话** - 始终使用 CurationSession 来跟踪决策
5. **文档推理** - 使用注释字段记录决策理由

## 成本优化

```python
# Only use AI for uncertain units
uncertain_units = metrics.query("""
    snr > 2 and snr < 8 and
    isi_violations_ratio > 0.001 and isi_violations_ratio < 0.1
""").index.tolist()

# Batch process only these
results = npa.batch_visual_curation(
    analyzer,
    unit_ids=uncertain_units,
    api_client=client
)
```

## 参考资料

- [SpikeAgent](https://github.com/SpikeAgent/SpikeAgent) - AI驱动的秒杀排序助手
- [Anthropic Vision API](https://docs.anthropic.com/en/docs/vision)
- [GPT-4 Vision](https://platform.openai.com/docs/guides/vision)
