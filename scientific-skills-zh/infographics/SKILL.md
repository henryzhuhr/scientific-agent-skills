---
name: infographics
description: "使用 Nano Banana Pro AI 和智能迭代细化创建专业的信息图表。使用 Gemini 3 Pro 进行质量审核。集成 research-lookup 和网络搜索以获取准确的数据。支持 10 种信息图表类型、8 种行业样式和色盲安全调色板。"
allowed-tools: Read Write Edit Bash
---

# 信息图表

## 概述

信息图表是信息、数据或知识的可视化表示，旨在快速、清晰地呈现复杂内容。 **此技能使用 Nano Banana Pro AI 进行信息图生成，并结合 Gemini 3 Pro 质量审查和 Perplexity Sonar 进行研究。**

* *工作原理：**
- （可选）**研究阶段**：使用 Perplexity Sonar 收集准确的事实和统计数据
- 用自然语言描述您的信息图
- Nano Banana Pro 生成出版物质量的信息图自动
- **Gemini 3 Pro 根据文档类型阈值审查质量**
- **智能迭代**：仅在质量低于阈值时重新生成
- 在几分钟内即可实现专业级输出
- 无需设计技能

* *按文档类型划分的质量阈值：**
|文件类型 |门槛|描述 |
|-------------|------------|------------|
|营销| 8.5/10 |营销材料 - 必须引人注目 |
|报告| 8.0/10 |商业报告-专业品质|
|介绍| 7.5/10 |幻灯片、演讲 - 清晰且引人入胜 |
|社会| 7.0/10 |社交媒体内容|
|内部| 7.0/10 |内部使用|
|草稿| 6.5/10 |工作草案|
|默认 | 7.5/10 |通用 |

* *只需描述您想要的内容，Nano Banana Pro 即可创建它。**

## 快速入门

通过简单描述即可生成任何信息图：

```bash
# Generate a list infographic (default threshold 7.5/10)
python skills/infographics/scripts/generate_infographic.py \
  "5 benefits of regular exercise" \
  -o figures/exercise_benefits.png --type list

# Generate for marketing (highest threshold: 8.5/10)
python skills/infographics/scripts/generate_infographic.py \
  "Product features comparison" \
  -o figures/product_comparison.png --type comparison --doc-type marketing

# Generate with corporate style
python skills/infographics/scripts/generate_infographic.py \
  "Company milestones 2010-2025" \
  -o figures/timeline.png --type timeline --style corporate

# Generate with colorblind-safe palette
python skills/infographics/scripts/generate_infographic.py \
  "Heart disease statistics worldwide" \
  -o figures/health_stats.png --type statistical --palette wong

# Generate WITH RESEARCH for accurate, up-to-date data
python skills/infographics/scripts/generate_infographic.py \
  "Global AI market size and growth projections" \
  -o figures/ai_market.png --type statistical --research
```

* *幕后发生的事情：**
1. **（可选）研究**：困惑声纳收集准确的事实、统计数据和数据
2. **第一代**：Nano Banana Pro 根据设计最佳实践 
3 创建初始信息图。 **评论 1**：**Gemini 3 Pro** 根据文档类型阈值 
4 评估质量。 **决策**：如果质量 >= 阈值 → **完成**（不再需要迭代！）
5. **如果低于阈值**：根据批评改进提示，重新生成
6. **重复**：直到质量达到阈值或达到最大迭代次数

* *智能迭代的好处：**
- ✅ 如果第一代足够好，则节省 API 调用
- ✅ 营销材料的更高质量标准
- ✅ 草稿/内部使用的周转速度更快
- ✅ 每次使用的适当质量案例

* *输出**：版本化图像加上详细的审核日志，其中包含质量分数、评论和早期停止信息。

## 何时使用此技能

在以下情况下使用**信息图表**技能：
- 以可视化格式呈现数据或统计数据
- 为项目里程碑或项目创建时间线可视化历史
- 解释流程、工作流程或分步指南
- 并排比较选项、产品或概念
- 以引人入胜的视觉格式总结关键点
- 创建地理或基于地图的数据可视化
- 构建层次结构或组织图表
- 设计社交媒体内容或营销材料

* *使用scientific-schematics代替：**
- 技术流程图和电路图
- 生物途径和分子图
- 神经网络架构图
- CONSORT/PRISMA方法图

- --

## 研究集成

### 自动数据采集（`--research`）

创建需要准确、最新数据的信息图表时，请使用 `--research` 标志使用 **Perplexity Sonar Pro** 自动收集事实和统计数据。

```bash
# Research and generate statistical infographic
python skills/infographics/scripts/generate_infographic.py \
  "Global renewable energy adoption rates by country" \
  -o figures/renewable_energy.png --type statistical --research

# Research for timeline infographic
python skills/infographics/scripts/generate_infographic.py \
  "History of artificial intelligence breakthroughs" \
  -o figures/ai_history.png --type timeline --research

# Research for comparison infographic
python skills/infographics/scripts/generate_infographic.py \
  "Electric vehicles vs hydrogen vehicles comparison" \
  -o figures/ev_hydrogen.png --type comparison --research
```

### 研究提供什么

自动研究阶段：

1. **收集关键事实**：有关主题 
2 的 5-8 个相关事实和统计数据。 **提供上下文**：准确表示的背景信息
3. **查找数据点**：具体数字、百分比和日期
4. **引用来源**：提及主要研究或来源
5. **优先考虑新近度**：重点关注 2023-2026 年信息

### 何时使用研究

* *启用研究 (`--research`)：**
- 需要准确数字的统计信息图表
- 市场数据、行业统计或趋势
- 科学或医学信息
- 当前事件或最新进展
- 准确性至关重要的任何主题

* *跳过研究：**
- 简单概念信息图
- 内部流程文档
- 在提示中提供所有数据的主题
- 速度关键生成

### 研究输出

启用研究后，会创建其他文件：
- `{name}_research.json` - 原始研究数据和来源
- 研究内容自动合并到信息图表提示中

- --

## 信息图表类型

### 1.统计/数据驱动 (`--type statistical`)

最适合：呈现数字、百分比、调查结果和定量数据。

* *关键元素：** 图表（条形图、饼图、折线图、圆环图）、大数字标注、数据比较、趋势

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Global internet usage 2025: 5.5 billion users (68% of population), \
   Asia Pacific 53%, Europe 15%, Americas 20%, Africa 12%" \
  -o figures/internet_stats.png --type statistical --style technology
```

- --

### 2. 时间线 (`--type timeline`)

最适合：历史事件、项目里程碑、公司历史、概念演变。

* *关键元素：** 时间流程、日期标记、事件节点、连接lines.

```bash
python skills/infographics/scripts/generate_infographic.py \
  "History of AI: 1950 Turing Test, 1956 Dartmouth Conference, \
   1997 Deep Blue, 2016 AlphaGo, 2022 ChatGPT" \
  -o figures/ai_history.png --type timeline --style technology
```

- --

### 3. 流程/操作方法 (`--type process`)

最适合：分步说明、工作流程、程序、教程。

* *关键元素：**编号步骤、方向箭头、操作图标、清晰的流程。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "How to start a podcast: 1. Choose your niche, 2. Plan content, \
   3. Set up equipment, 4. Record episodes, 5. Publish and promote" \
  -o figures/podcast_process.png --type process --style marketing
```

- --

### 4. 比较 (`--type comparison`)

最适合：产品比较、优缺点、之前/之后，选项评估。

* *关键元素：**并排布局、匹配类别、检查/交叉指标。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Electric vs Gas Cars: Fuel cost (lower vs higher), \
   Maintenance (less vs more), Range (improving vs established)" \
  -o figures/ev_comparison.png --type comparison --style nature
```

- --

### 5. 列表/信息 (`--type list`)

最适合：提示、事实、要点、摘要、快速参考

* *关键元素：** 编号或项目符号点、图标、清晰的层次结构。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "7 Habits of Highly Effective People: Be Proactive, \
   Begin with End in Mind, Put First Things First, Think Win-Win, \
   Seek First to Understand, Synergize, Sharpen the Saw" \
  -o figures/habits.png --type list --style corporate
```

- --

### 6. 地理 (`--type geographic`)

最适合：区域数据、人口统计、基于位置的统计、全球trend.

* *关键元素：**地图可视化、颜色编码、数据叠加、图例。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Renewable energy adoption by region: Iceland 100%, Norway 98%, \
   Germany 50%, USA 22%, India 20%" \
  -o figures/renewable_map.png --type geographic --style nature
```

- --

### 7. 分层/金字塔 (`--type hierarchical`)

最适合：组织结构、优先级、重要性排名。

* *关键元素：**金字塔或树结构、不同的级别、大小级数。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Maslow's Hierarchy: Physiological, Safety, Love/Belonging, \
   Esteem, Self-Actualization" \
  -o figures/maslow.png --type hierarchical --style education
```

- --

### 8. 解剖/视觉隐喻 (`--type anatomical`)

最适合：使用熟悉的视觉解释复杂系统隐喻。

* *关键元素：** 中心隐喻图像、标记部分、连接线。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Business as a human body: Brain=Leadership, Heart=Culture, \
   Arms=Sales, Legs=Operations, Skeleton=Systems" \
  -o figures/business_body.png --type anatomical --style corporate
```

- --

### 9. 简历/专业 (`--type resume`)

最适合：个人品牌、简历、作品集亮点、专业成就。

* *关键要素：** 照片区域、技能可视化、时间轴、联系信息。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "UX Designer resume: Skills - User Research 95%, Wireframing 90%, \
   Prototyping 85%. Experience - 2020-2022 Junior, 2022-2025 Senior" \
  -o figures/resume.png --type resume --style technology
```

- --

### 10. 社交媒体 (`--type social`)

最适合：Instagram、LinkedIn、Twitter/X 帖子、可共享图形。

* *关键元素：** 粗体标题、最小文本、最大影响力、鲜艳的色彩。

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Save Water, Save Life: 2.2 billion people lack safe drinking water. \
   Tips: shorter showers, fix leaks, full loads only" \
  -o figures/water_social.png --type social --style marketing
```

- --

## 样式预设

### 行业样式 (`--style`)

|风格|颜色 |最适合 |
|-------|--------|---------|
| `corporate` |海军蓝、钢蓝色、金色|商业报告、财务|
| `healthcare` |医用蓝、青色、浅青色|医疗、保健|
| `technology` |科技蓝、石板色、紫罗兰 |软件、数据、人工智能|
| `nature` |森林绿、薄荷绿、土棕色|环保、有机|
| `education` |学院蓝、浅蓝、珊瑚色|学习、学术|
| `marketing` |珊瑚色、青色、黄色 |社交媒体、活动 |
| `finance` |海军蓝、金色、绿色/红色 |投资、银行|
| `nonprofit` |暖橙色、鼠尾草色、沙色 |社会事业、慈善机构 |

```bash
# Corporate style
python skills/infographics/scripts/generate_infographic.py \
  "Q4 Results" -o q4.png --type statistical --style corporate

# Healthcare style
python skills/infographics/scripts/generate_infographic.py \
  "Patient Journey" -o journey.png --type process --style healthcare
```

- --

## 色盲安全调色板

### 可用调色板 (`--palette`)

|调色板|颜色 |描述 |
|---------|--------|-------------|
| `wong` |橙色、天蓝色、绿色、蓝色、朱红色 |最广泛推荐|
| `ibm` |群青、靛蓝、品红、橙色、金色 | IBM 的无障碍调色板 |
| `tol` | 12 色扩展调色板 |对于许多类别 |

```bash
# Wong's colorblind-safe palette
python skills/infographics/scripts/generate_infographic.py \
  "Survey results by category" -o survey.png --type statistical --palette wong
```

- --

## 智能迭代细化

### 工作原理

```
┌─────────────────────────────────────────────────────┐
│  1. Generate infographic with Nano Banana Pro       │
│                    ↓                                │
│  2. Review quality with Gemini 3 Pro                │
│                    ↓                                │
│  3. Score >= threshold?                             │
│       YES → DONE! (early stop)                      │
│       NO  → Improve prompt, go to step 1            │
│                    ↓                                │
│  4. Repeat until quality met OR max iterations      │
└─────────────────────────────────────────────────────┘
```

### 质量审核标准

Gemini 3 Pro 对每个类别进行评估信息图：

1. **视觉层次和布局**（0-2分）
  - 清晰的视觉层次
  - 逻辑阅读流程
  - 平衡的构图

2. **排版和可读性**（0-2 分）
  - 可读文本
  - 粗体标题
  - 无重叠

3. **数据可视化**（0-2分）
  - 突出的数字
  - 清晰的图表/图标
  - 正确的标签

4. **颜色和辅助功能**（0-2 分）
  - 专业色彩
  - 足够的对比度
  - 色盲友好

5. **总体影响**（0-2分）
  - 专业外观
  - 无视觉缺陷
  - 实现沟通目标

### 评论日志

每一代都会生成一个 JSON 审核日志：
```json
{
  "user_prompt": "5 benefits of exercise...",
  "infographic_type": "list",
  "style": "healthcare",
  "doc_type": "marketing",
  "quality_threshold": 8.5,
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/exercise_v1.png",
      "score": 8.7,
      "needs_improvement": false,
      "critique": "SCORE: 8.7\nSTRENGTHS:..."
    }
  ],
  "final_score": 8.7,
  "early_stop": true,
  "early_stop_reason": "Quality score 8.7 meets threshold 8.5"
}
```

- --

## 命令行参考

```bash
python skills/infographics/scripts/generate_infographic.py [OPTIONS] PROMPT

Arguments:
  PROMPT                    Description of the infographic content

Options:
  -o, --output PATH         Output file path (required)
  -t, --type TYPE           Infographic type preset
  -s, --style STYLE         Industry style preset
  -p, --palette PALETTE     Colorblind-safe palette
  -b, --background COLOR    Background color (default: white)
  --doc-type TYPE           Document type for quality threshold
  --iterations N            Maximum refinement iterations (default: 3)
  --api-key KEY             OpenRouter API key
  -v, --verbose             Verbose output
  --list-options            List all available options
```

### 列出所有选项

```bash
python skills/infographics/scripts/generate_infographic.py --list-options
```

- --

## 配置

### API密钥设置

设置您的OpenRouter API密钥：
```bash
export OPENROUTER_API_KEY='your_api_key_here'
```

在以下位置获取API密钥：https://openrouter.ai/keys

- --

## 提示工程提示

### 具体说明内容

✓ **好的提示**（具体、详细）：
```
"5 benefits of meditation: reduces stress, improves focus, 
better sleep, lower blood pressure, emotional balance"
```

✗ **避免含糊提示**：
```
"meditation infographic"
```

### 包含数据点

✓ **好**：
```
"Market growth from $10B (2020) to $45B (2025), CAGR 35%"
```

✗ **模糊**：
```
"market is growing"
```

### 指定视觉元素

✓ **好**：
```
"Timeline showing 5 milestones with icons for each event"
```

- --

## 参考文件

有关详细指导，请加载这些参考文件：

- **`references/infographic_types.md`**：适用于所有 10 多种类型的扩展模板
- **`references/design_principles.md`**：视觉层次结构、布局、排版
- **`references/color_palettes.md`**：完整调色板规范

- --

## 故障排除

### 常见问题

* *问题**：信息图表中的文本不可读
- **解决办法**：减少文字内容；使用--type指定布局类型

* *问题**：颜色冲突或无法访问
- **解决方案**：使用`--palette wong`作为色盲安全颜色

* *问题**：质量得分太低
- **解决方案**：使用`--iterations 3`增加迭代；使用更具体的提示

* *问题**：生成了错误的信息图表类型
- **解决方案**：始终指定`--type`标志以获得一致的结果

- --

## 与其他技能集成

此技能与：

- 协同工作**scientific-schematics**：用于技术图表和流程图
- **market-research-reports**：用于业务报告的信息图表
- **scientific-slides**：用于演示的信息图表元素
- **generate-image**：用于非信息图表视觉效果内容

- --

## 快速参考清单

生成之前：
- [ ]清晰、具体的内容描述
- [ ]选择信息图表类型 (`--type`)
- [ ]适合受众的样式 (`--style`)
- [ ]指定输出路径 (`-o`)
- [ ] API 密钥配置

生成后：
- [ ]审核生成的图像
- [ ]检查评分的审核日志
- [ ]如果需要，使用更具体的提示重新生成

- --

 使用此技能，利用 Nano Banana Pro AI 的智能品质，创建专业、易于访问且视觉上引人注目的信息图表评论.
