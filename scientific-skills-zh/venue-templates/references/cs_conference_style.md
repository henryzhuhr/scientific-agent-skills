# CS会议写作风格指南

ACL、EMNLP、NAACL（NLP）、CHI、CSCW（HCI）、SIGKDD、WWW、SIGIR（数据挖掘/IR）等主要CS会议的综合写作指南。

* *最后更新**：2024

- --

## 概述

CS会议跨越具有不同写作文化的不同子领域。本指南涵盖了 NLP、HCI 和数据挖掘/IR 场所，每个场所都有独特的期望和评估标准。

- --

# 第 1 部分：NLP 会议（ACL、EMNLP、NAACL）

## NLP 写作哲学

> “在标准基准上获得强有力的实证结果，并进行富有洞察力的分析。”

NLP 论文平衡实证严谨性和语言洞察力。人工评估与自动指标一起变得越来越重要。

## 受众和语气

### 目标读者
- NLP研究人员和计算语言学家
- 熟悉变压器架构、标准基准
- 期望可重复的结果和错误分析

### 语气特点
|特点|描述|
|-------------|--------------|
| **以任务为中心** |明确的问题定义|
| **以基准为导向** |强调的标准数据集|
| **分析丰富** |误差分析、定性示例|
| **可重复** |完整实现细节 |

## 摘要（NLP 风格）

### 结构
- **任务/问题**（1 句话）
- **先前工作的限制**（1 句）
- **你的方法**（1-2 句）
- **基准测试结果**（2句子）
- **分析结果**（可选，1句话）

### 摘要示例

```
Coreference resolution remains challenging for pronouns with distant or 
ambiguous antecedents. Prior neural approaches struggle with these 
difficult cases due to limited context modeling. We introduce 
LongContext-Coref, a retrieval-augmented coreference model that 
dynamically retrieves relevant context from document history. On the 
OntoNotes 5.0 benchmark, LongContext-Coref achieves 83.4 F1, improving 
over the previous state-of-the-art by 1.2 points. On the challenging 
WinoBias dataset, we reduce gender bias by 34% while maintaining 
accuracy. Qualitative analysis reveals that our model successfully 
resolves pronouns requiring world knowledge, a known weakness of 
prior approaches.
```

## NLP论文结构

```
├── Introduction
│   ├── Task motivation
│   ├── Prior work limitations
│   ├── Your contribution
│   └── Contribution bullets
├── Related Work
├── Method
│   ├── Problem formulation
│   ├── Model architecture
│   └── Training procedure
├── Experiments
│   ├── Datasets (with statistics)
│   ├── Baselines
│   ├── Main results
│   ├── Analysis
│   │   ├── Error analysis
│   │   ├── Ablation study
│   │   └── Qualitative examples
│   └── Human evaluation (if applicable)
├── Discussion / Limitations
└── Conclusion
```

## NLP特定要求

### 数据集
- 使用**标准基准**：GLUE、SQuAD、CoNLL、OntoNotes
- 报告**数据集统计**：训练/开发/测试大小
- **数据预处理**：记录所有步骤

### 评估指标
- **适合任务的指标**：F1、BLEU、ROUGE、准确性
- **统计显着性**：配对引导程序、p 值
- **多次运行**：报告种子之间的平均值±标准差

### 人类评估
越来越期望生成任务：
- **注释者详细信息**：数量、资格、协议
- **评估协议**：指南、接口、付款
- **注释者间协议**：Cohen 的 κ 或 Krippendorff 的 α

### 人类评估示例表

```
Table 3: Human Evaluation Results (100 samples, 3 annotators)
─────────────────────────────────────────────────────────────
Method        | Fluency | Coherence | Factuality | Overall
─────────────────────────────────────────────────────────────
Baseline      |   3.8   |    3.2    |    3.5     |   3.5
GPT-3.5       |   4.2   |    4.0    |    3.7     |   4.0
Our Method    |   4.4   |    4.3    |    4.1     |   4.3
─────────────────────────────────────────────────────────────
Inter-annotator κ = 0.72. Scale: 1-5 (higher is better).
```

## ACL 具体注释

- **ARR（ACL 滚动审核）**：跨 ACL 场地的共享审核系统
- **负责任的 NLP 检查表**：道德、限制、风险
- **长（8 页）与短（4 页）页）**：不同的期望
- **研究结果论文**：较低层接受轨迹

- --

# 第2部分：HCI会议（CHI、CSCW、UIST）

## HCI写作哲学

> “技术服务于人类——首先了解用户，然后设计和设计评估。”

HCI 论文从根本上来说是 **以用户为中心**。仅靠技术新颖性是不够的； 

## 受众和语气

### 目标读者
- HCI 研究人员和从业者
- UX 设计师和产品开发人员
- 跨学科（CS、心理学、设计、社会科学）

### 语气特点
|特点|描述|
|-------------|-------------|
| **以用户为中心** |关注人，而不是技术 |
| **了解设计** |植根于设计思维|
| **经验** |用户研究提供证据 |
| **反光** |考虑更广泛的影响 |

## HCI 摘要

### 关注用户和影响

```
Video calling has become essential for remote collaboration, yet 
current interfaces poorly support the peripheral awareness that makes 
in-person work effective. Through formative interviews with 24 remote 
workers, we identified three key challenges: difficulty gauging 
colleague availability, lack of ambient presence cues, and interruption 
anxiety. We designed AmbientOffice, a peripheral display system that 
conveys teammate presence through subtle ambient visualizations. In a 
two-week deployment study with 18 participants across three distributed 
teams, AmbientOffice increased spontaneous collaboration by 40% and 
reduced perceived isolation (p<0.01). Participants valued the system's 
non-intrusive nature and reported feeling more connected to remote 
colleagues. We discuss implications for designing ambient awareness 
systems and the tension between visibility and privacy in remote work.
```

## HCI 论文结构

### 通过设计/系统论文进行研究

```
├── Introduction
│   ├── Problem in human terms
│   ├── Why technology can help
│   └── Contribution summary
├── Related Work
│   ├── Domain background
│   ├── Prior systems
│   └── Theoretical frameworks
├── Formative Work (often)
│   ├── Interviews / observations
│   └── Design requirements
├── System Design
│   ├── Design rationale
│   ├── Implementation
│   └── Interface walkthrough
├── Evaluation
│   ├── Study design
│   ├── Participants
│   ├── Procedure
│   ├── Findings (quant + qual)
│   └── Limitations
├── Discussion
│   ├── Design implications
│   ├── Generalizability
│   └── Future work
└── Conclusion
```

### 定性/访谈研究

```
├── Introduction
├── Related Work
├── Methods
│   ├── Participants
│   ├── Procedure
│   ├── Data collection
│   └── Analysis method (thematic, grounded theory, etc.)
├── Findings
│   ├── Theme 1 (with quotes)
│   ├── Theme 2 (with quotes)
│   └── Theme 3 (with quotes)
├── Discussion
│   ├── Implications for design
│   ├── Implications for research
│   └── Limitations
└── Conclusion
```

## HCI 特定要求

### 参与者报告
- **人口统计**：年龄、性别、相关经验
- **招聘**：招募方式和地点
- **报酬**：付款金额和类型
- **IRB 批准**：道德委员会声明

### 调查结果中的引用
使用直接引用来接地结果：
```
Participants valued the ambient nature of the display. As P7 described: 
"It's like having a window to my teammate's office. I don't need to 
actively check it, but I know they're there." This passive awareness 
reduced the barrier to initiating contact.
```

### 设计影响部分
将结果转化为可操作的指导：
```
**Implication 1: Support peripheral awareness without demanding attention.**
Ambient displays should be visible in peripheral vision but not require 
active monitoring. Designers should consider calm technology principles.

**Implication 2: Balance visibility with privacy.**
Users want to share presence but fear surveillance. Systems should 
provide granular controls and make visibility mutual.
```

## CHI-特定注释

- **贡献类型**：经验、工件、方法论、理论
- **ACM 格式**：带有 `sigchi` 选项的 `acmart` 文档类
- **辅助功能**：替代文本，预期包含语言
- **贡献声明**：需要每个作者的贡献

- --

# 第 3 部分：数据挖掘和 IR（SIGKDD， WWW, SIGIR)

## 数据挖掘写作哲学

> “具有实际影响力的现实世界数据的可扩展方法。”

数据挖掘论文强调**可扩展性**、**现实世界适用性**和**可靠的实验方法**。

## 受众和语气

### 目标读者
- 数据科学家和机器学习工程师
- 行业研究人员
- 应用机器学习从业者

### 语气特征
|特点|描述|
|-------------|-------------|
| **可扩展** |处理大型数据集|
| **实用** |实际应用|
| **可重复** |数据集和代码共享|
| **工业** |有价值的行业数据集 |

## KDD 摘要

### 强调规模和应用

```
Fraud detection in e-commerce requires processing millions of 
transactions in real-time while adapting to evolving attack patterns. 
We present FraudShield, a graph neural network framework for real-time 
fraud detection that scales to billion-edge transaction graphs. Unlike 
prior methods that require full graph access, FraudShield uses 
incremental updates with O(1) inference cost per transaction. On a 
proprietary dataset of 2.3 billion transactions from a major e-commerce 
platform, FraudShield achieves 94.2% precision at 80% recall, 
outperforming production baselines by 12%. The system has been deployed 
at [Company], processing 50K transactions per second and preventing 
an estimated $400M in annual fraud losses. We release an anonymized 
benchmark dataset and code.
```

## KDD 论文结构

```
├── Introduction
│   ├── Problem and impact
│   ├── Technical challenges
│   ├── Your approach
│   └── Contributions
├── Related Work
├── Preliminaries
│   ├── Problem definition
│   └── Notation
├── Method
│   ├── Overview
│   ├── Technical components
│   └── Complexity analysis
├── Experiments
│   ├── Datasets (with scale statistics)
│   ├── Baselines
│   ├── Main results
│   ├── Scalability experiments
│   ├── Ablation study
│   └── Case study / deployment
└── Conclusion
```

## KDD 特定要求

### 可扩展性
- **数据集大小**：报告节点、边、样本的数量
- **运行时分析**：挂钟时间比较
- **复杂性**：规定的时间和空间复杂性
- **缩放实验**：显示性能与数据大小

### 工业部署
- **案例研究**：真实部署故事
- **A/B 测试**：在线评估结果（如果适用）
- **生产指标**：业务影响（如果可共享）

### 可扩展性示例表

```
Table 4: Scalability Comparison (runtime in seconds)
──────────────────────────────────────────────────────
Dataset     | Nodes  | Edges  | GCN   | GraphSAGE | Ours
──────────────────────────────────────────────────────
Cora        |  2.7K  |  5.4K  |  0.3  |    0.2    |  0.1
Citeseer    |  3.3K  |  4.7K  |  0.4  |    0.3    |  0.1
PubMed      | 19.7K  | 44.3K  |  1.2  |    0.8    |  0.3
ogbn-arxiv  | 169K   | 1.17M  |  8.4  |    4.2    |  1.6
ogbn-papers | 111M   | 1.6B   |  OOM  |   OOM     | 42.3
──────────────────────────────────────────────────────
```

- --

# 第4部分：CS场馆的通用元素

## 写作质量

### 清晰度
- **每句话一个想法**
- **使用前定义术语**
- **使用一致符号**

### 精度
- **精确数字**：“23.4％”而不是“大约20％”
- **明确声明**：除非必要，否则避免对冲
- **具体比较**：命名基线

## 贡献项目符号

在所有CS中使用场地：
```
Our contributions are:
• We identify [problem/insight]
• We propose [method name] that [key innovation]
• We demonstrate [results] on [benchmarks]
• We release [code/data] at [URL]
```

## 再现性标准

所有 CS 场地越来越期望：
- **代码可用性**：GitHub 链接（匿名审核）
- **数据可用性**：公共数据集或发布计划
- **完整超参数**：培训详细信息已完成
- **随机种子**：复制的精确值

## 道德和更广泛的影响

### NLP (ACL/EMNLP)
- **限制部分**：必需
- **负责任的NLP清单**：道德考虑
- **偏差分析**：对于影响人的模型

### HCI (CHI)
- **IRB/道德批准**：人类受试者需要
- **知情同意**：描述的程序
- **隐私考虑**：数据处理

### KDD/WWW
- **社会影响**：考虑误用可能性
- **隐私保护**：针对敏感数据
- **公平分析**：适用时

- --

## 场地比较表

|方面| ACL/EMNLP |气| KDD/WWW |西格 |
|--------|------------|-----|---------|--------|
| **焦点** | NLP 任务 |用户研究|可扩展的机器学习 |红外/搜索|
| **评估** |基准+人类|用户研究|大型展览 |数据集|
| **理论重量** |中等|低|中等|中等|
| **行业价值** |高|中等|非常高|高|
| **页数限制** | 8 长/4 短 | 10 + 参考文献 | 9 + 参考文献 | 10 + 参考文献 |
| **评论风格** |到达目的地 |直接|直接|直接 |

- --

## 提交前清单

### 所有 CS 场地 
- [ ]明确的贡献声明
- [ ]强大的基线
- [ ]再现性信息完整
- [ ]正确的场地template
- [ ]匿名（如果双盲）

### NLP-Specific
- [ ]标准基准测试结果
- [ ]包含错误分析
- [ ]人类评估（用于生成）
- [ ]负责任的NLP检查清单

### HCI 特定
- [ ] IRB 批准说明
- [ ]参与者人口统计
- [ ]结果中直接引用
- [ ]设计含义

### 数据挖掘特定
- [ ]可扩展性实验
- [ ]数据集大小统计
- [ ]运行时比较
- [ ]复杂性分析

- --

## 另请参阅

- `venue_writing_styles.md` - Master 风格概述
- `ml_conference_style.md` - NeurIPS/ICML 风格指南
- `conferences_formatting.md` - 技术格式要求
- `reviewer_expectations.md` - CS 审阅者寻求什么
