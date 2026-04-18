# ML 会议写作风格指南

NeurIPS、ICML、ICLR、CVPR、ECCV、ICCV 等主要机器学习和计算机视觉会议的综合写作指南。

* *最后更新**：2024

- --

## 概述

ML 会议优先考虑 **新颖性**、**严谨的实证评估**，以及**再现性**。论文的评估标准是明确的贡献、强有力的基线、全面的消融和对局限性的诚实讨论。

### 关键理念

> “展示而不是告诉——你的实验应该证明你的主张，而不仅仅是你的散文。”

* *主要目标**：通过严格的实验验证新方法来推进最先进的技术。

- --

## 受众和语气

### 目标读者

- ML 研究人员和实践者
- 特定子领域的专家
- 熟悉最新文献
- 期望技术深度和精度

### 语气特征

|特点|描述|
|-------------|--------------|
| **技术** |方法论细节密集 |
| **精确** |术语准确，无歧义|
| **经验** |有实验支持的主张|
| **直接** |明确贡献贡献|
| **诚实** |承认限制 |

### Voice

- **第一人称复数（“我们”）**：“我们建议...”“我们的方法...”
- **主动语态**：“我们引入一种新颖的架构...”
- **自信但谨慎**：强有力的主张需要强有力的证据

- --

## 摘要

### 风格要求

- **密集且注重数字**
- **150-250 个字**（因场地而异）
- **前期关键结果**：包括具体指标
- **流畅的段落**（非结构化）

### 摘要结构

1. **问题**（1句话）：你正在解决什么问题？
2. **现有工作的局限性**（1句话）：为什么当前方法达不到
3. **你的方法**（1-2句话）：你的方法是什么？
4. **关键结果**（2-3 句话）：基准测试中的具体数字
5. **意义**（可选，1句话）：为什么这很重要

### 摘要示例（NeurIPS 风格）

```
Transformers have achieved remarkable success in sequence modeling but 
suffer from quadratic computational complexity, limiting their application 
to long sequences. We introduce FlashAttention-2, an IO-aware exact 
attention algorithm that achieves 2x speedup over FlashAttention and up 
to 9x speedup over standard attention on sequences up to 16K tokens. Our 
key insight is to reduce memory reads/writes by tiling and recomputation, 
achieving optimal IO complexity. On the Long Range Arena benchmark, 
FlashAttention-2 enables training with 8x longer sequences while matching 
standard attention accuracy. Combined with sequence parallelism, we train 
GPT-style models on sequences of 64K tokens at near-linear cost. We 
release optimized CUDA kernels achieving 80% of theoretical peak FLOPS 
on A100 GPUs. Code is available at [anonymous URL].
```

### 摘要 Don'ts

❌“我们为 X 提出了一种新颖的方法”（模糊，没有结果）
❌“我们的方法优于基线”（没有具体）数字）
❌“这是一个重要的问题”（不言而喻的说法）

✅ 包括具体指标：“达到 94.5% 的准确率，提高 3.2%”
✅ 包括规模：“在 1M 样本上”或“16K 令牌序列”
✅ 包括比较：“比以前快 2 倍” SOTA"

- --

## 简介

### 结构（2-3 页）

ML 介绍具有独特的结构，带有 **编号的贡献**。

### 逐段指南

* *第 1 段：问题动机**
- 为什么是这个问题重要吗？
- 有哪些应用？
- 设置技术挑战

```
"Large language models have demonstrated remarkable capabilities in 
natural language understanding and generation. However, their quadratic 
attention complexity presents a fundamental bottleneck for processing 
long documents, multi-turn conversations, and reasoning over extended 
contexts. As models scale to billions of parameters and context lengths 
extend to tens of thousands of tokens, efficient attention mechanisms 
become critical for practical deployment."
```

* *第 2 段：现有方法的局限性**
- 存在哪些方法？
- 为什么它们不足？
- 技术限制分析

```
"Prior work has addressed this through sparse attention patterns, 
linear attention approximations, and low-rank factorizations. While 
these methods reduce theoretical complexity, they often sacrifice 
accuracy, require specialized hardware, or introduce approximation 
errors that compound in deep networks. Exact attention remains 
preferable when computational resources permit."
```

* *第3段：您的方法（高级）**
- 您的主要见解是什么？
- 您的方法在概念上如何工作？
- 为什么应该这样做成功？

```
"We observe that the primary bottleneck in attention is not computation 
but rather memory bandwidth—reading and writing the large N×N attention 
matrix dominates runtime on modern GPUs. We propose FlashAttention-2, 
which eliminates this bottleneck through a novel tiling strategy that 
computes attention block-by-block without materializing the full matrix."
```

* *第 4 段：贡献列表（关键）**

这是 ML 会议的**强制性且独特的**：

```
Our contributions are as follows:

• We propose FlashAttention-2, an IO-aware exact attention algorithm 
  that achieves optimal memory complexity O(N²d/M) where M is GPU 
  SRAM size.

• We provide theoretical analysis showing that our algorithm achieves 
  2-4x fewer HBM accesses than FlashAttention on typical GPU 
  configurations.

• We demonstrate 2x speedup over FlashAttention and up to 9x over 
  standard PyTorch attention across sequence lengths from 256 to 64K 
  tokens.

• We show that FlashAttention-2 enables training with 8x longer 
  contexts on the same hardware, unlocking new capabilities for 
  long-range modeling.

• We release optimized CUDA kernels and PyTorch bindings at 
  [anonymous URL].
```

### 贡献项目符号指南

|良好的贡献项目符号 |不良贡献项目符号 |
|----------------------------------------|------------------------|
|具体、可量化|模糊的说法|
|独立 |需要阅读论文才能理解|
|各有特色|重叠子弹|
|强调新颖性|陈述明显事实 |

### 相关工作安排

- **简介**：简要定位（1-2 段）
- **单独部分**：详细比较（在最后或结论之前）
- **附录**：篇幅有限的扩展讨论

- --

## 方法

### 结构（2-3页）

```
METHOD
├── Problem Formulation
├── Method Overview / Architecture
├── Key Technical Components
│   ├── Component 1 (with equations)
│   ├── Component 2 (with equations)
│   └── Component 3 (with equations)
├── Theoretical Analysis (if applicable)
└── Implementation Details
```

### 数学符号

- **定义所有符号**：“让X ∈ ℝ^{N×d}表示输入序列...”
- **一致符号**：相同符号表示相同事物通篇
- **重要方程的编号**：稍后按编号引用

### 算法伪代码

包括清晰的伪代码以实现可重复性：

```
Algorithm 1: FlashAttention-2 Forward Pass
─────────────────────────────────────────
Input: Q, K, V ∈ ℝ^{N×d}, block size B_r, B_c
Output: O ∈ ℝ^{N×d}

1:  Divide Q into T_r = ⌈N/B_r⌉ blocks
2:  Divide K, V into T_c = ⌈N/B_c⌉ blocks
3:  Initialize O = 0, ℓ = 0, m = -∞
4:  for i = 1 to T_r do
5:    Load Q_i from HBM to SRAM
6:    for j = 1 to T_c do
7:      Load K_j, V_j from HBM to SRAM
8:      Compute S_ij = Q_i K_j^T
9:      Update running max and sum
10:     Update O_i incrementally
11:   end for
12:   Write O_i to HBM
13: end for
14: return O
```

### 架构图

- **清晰，出版质量数字**
- **标记所有组件**
- **用箭头显示数据流**
- **使用一致的视觉语言**

- --

## 实验

### 结构（2-3）页）

```
EXPERIMENTS
├── Experimental Setup
│   ├── Datasets and Benchmarks
│   ├── Baselines
│   ├── Implementation Details
│   └── Evaluation Metrics
├── Main Results
│   └── Table/Figure with primary comparisons
├── Ablation Studies
│   └── Component-wise analysis
├── Analysis
│   ├── Scaling behavior
│   ├── Qualitative examples
│   └── Error analysis
└── Computational Efficiency
```

### 数据集和基准

- **使用标准基准**：建立可比性
- **报告数据集统计信息**：大小、分割、预处理
- **证明非标准选择**：如果使用自定义数据，请解释为什么

### 基线

* *对于接受至关重要。**包括：
- **最近的SOTA**：不仅仅是旧方法
- **公平比较**：相同的计算预算，超参数调整
- **消融版本**：没有关键组件的方法
- **强大的基线**：不要挑选弱竞争对手

### 主要结果表

清晰、全面的格式：

```
Table 1: Results on Long Range Arena Benchmark (accuracy %)
──────────────────────────────────────────────────────────
Method          | ListOps | Text  | Retrieval | Image | Path  | Avg
──────────────────────────────────────────────────────────
Transformer     |  36.4   | 64.3  |   57.5    | 42.4  | 71.4  | 54.4
Performer       |  18.0   | 65.4  |   53.8    | 42.8  | 77.1  | 51.4
Linear Attn     |  16.1   | 65.9  |   53.1    | 42.3  | 75.3  | 50.5
FlashAttention  |  37.1   | 64.5  |   57.8    | 42.7  | 71.2  | 54.7
FlashAttn-2     |  37.4   | 64.7  |   58.2    | 42.9  | 71.8  | 55.0
──────────────────────────────────────────────────────────
```

### 消融研究（强制）

显示您的重要内容方法：

```
Table 2: Ablation Study on FlashAttention-2 Components
──────────────────────────────────────────────────────
Variant                              | Speedup | Memory
──────────────────────────────────────────────────────
Full FlashAttention-2                |   2.0x  |  1.0x
  - without sequence parallelism     |   1.7x  |  1.0x
  - without recomputation            |   1.3x  |  2.4x
  - without block tiling             |   1.0x  |  4.0x
FlashAttention-1 (baseline)          |   1.0x  |  1.0x
──────────────────────────────────────────────────────
```

### 消融应该显示什么

- **每个组件都很重要**：删除它会损害性能
- **设计选择合理**：为什么采用这种架构/超参数？
- **故障模式**：方法何时不起作用？
- **敏感性分析**：超参数的鲁棒性

- --

## 相关工作

### 放置选项

1. **介绍后**：简历论文中常见
2. **结论之前**：常见于 NeurIPS/ICML
3. **附录**：当空间紧张时

### 写作风格

- **按主题组织**：不按时间顺序
- **定位你的作品**：你与每一行工作有何不同
- **公平描述**：不要歪曲以前的作品
- **最近引用**：包括2023-2024 年论文

### 示例结构

```
**Efficient Attention Mechanisms.** Prior work on efficient attention 
falls into three categories: sparse patterns (Beltagy et al., 2020; 
Zaheer et al., 2020), linear approximations (Katharopoulos et al., 2020; 
Choromanski et al., 2021), and low-rank factorizations (Wang et al., 
2020). Our work differs in that we focus on IO-efficient exact 
attention rather than approximations.

**Memory-Efficient Training.** Gradient checkpointing (Chen et al., 2016) 
and activation recomputation (Korthikanti et al., 2022) reduce memory 
by trading compute. We adopt similar ideas but apply them within the 
attention operator itself.
```

- --

## 限制部分

### 为什么重要

* *NeurIPS、ICML、ICLR 越来越需要**。诚实的限制：
- 展示科学成熟度
- 指导未来工作
- 防止过度销售

### 包含什么

1. **方法限制**：什么时候失败？
2. **实验限制**：什么没有测试？
3. **范围限制**：什么超出了范围？
4. **计算限制**：资源要求

### 示例限制部分

```
**Limitations.** While FlashAttention-2 provides substantial speedups, 
several limitations remain. First, our implementation is optimized for 
NVIDIA GPUs and does not support AMD or other hardware. Second, the 
speedup is most pronounced for medium to long sequences; for very short 
sequences (<256 tokens), the overhead of our kernel launch dominates. 
Third, we focus on dense attention; extending our approach to sparse 
attention patterns remains future work. Finally, our theoretical 
analysis assumes specific GPU memory hierarchy parameters that may not 
hold for future hardware generations.
```

- --

## 再现性

### 再现性检查表 (NeurIPS/ICML)

大多数 ML 会议都需要再现性检查表覆盖：

- [ ]代码可用性
- [ ]数据集可用性
- [ ]指定超参数
- [ ]报告随机种子
- [ ]规定计算要求
- [ ]报告运行次数和方差
- [ ]统计显着性检验

### 报告内容

* *超参数**：
```
"We train with Adam (β₁=0.9, β₂=0.999, ε=1e-8) and learning rate 3e-4 
with linear warmup over 1000 steps and cosine decay. Batch size is 256 
across 8 A100 GPUs. We train for 100K steps (approximately 24 hours)."
```

* *随机种子**：
```
"All experiments are averaged over 3 random seeds (0, 1, 2) with 
standard deviation reported in parentheses."
```

* *计算**：
```
"Experiments were conducted on 8 NVIDIA A100-80GB GPUs. Total training 
time was approximately 500 GPU-hours."
```

- --

## 人物

### 人物质量

- **首选矢量图形**：PDF、SVG
- **光栅高分辨率**：300+ dpi
- **以出版物尺寸可读**：以实际列宽进行测试
- **色盲可访问**：除了颜色之外还使用图案

### 常见图形类型

1. **架构图**：直观地展示你的方法
2. **性能图**：学习曲线，缩放行为
3. **比较表**：主要结果
4. **消融数字**：组件贡献
5. **定性示例**：输入/输出样本

### 图说明

独立的说明说明：
- 显示的内容
- 如何阅读该图
- 关键要点

- --

## 参考文献

### 引文样式

- **编号[1]** 或**作者年份（Smith 等人，2023）**
- 检查场地特定要求
- 始终保持一致

### 参考指南

- **引用最近的工作**：预计 2022-2024 年论文
- **不要过度引用自己**：引起偏见问题
- **适当引用 arxiv**：可用时使用已发布的版本
- **包括所有相关的先前工作**：缺少引用会损害审查

- --

## 特定地点注释

### NeurIPS

- **8 页** 主要 + 无限附录/参考文献
- **有时需要更广泛的影响**部分
- **再现性检查表** 强制
- 提交开放评审，公开评论

### ICML

- **8页**主+无限附录/参考文献
- 强调**理论+实验**
- 鼓励再现性声明

### ICLR

- **8 页** 主（相机就绪可以超过）
- OpenReview 与 **公众评论和讨论**
- 作者回复期为交互式
- 强烈强调**新颖性和洞察力** 

### CVPR/ICCV/ECCV

- **8 页** 主要包括参考文献
- **补充视频** 鼓励
- 高度重视**视觉结果**
- 基准性能关键

- --

## 常见错误

1. **弱基线**：未与最近的 SOTA
2 进行比较。 **缺少消融**：未显示组件贡献
3. **夸大其词**：当您部分解决 X
4 时，“我们解决了 X”。 **模糊的贡献**：“我们提出了一种新颖的方法”
5. **再现性差**：缺少超参数，种子
6. **模板错误**：使用去年的样式文件
7. **匿名违规**：盲审中暴露身份
8. **缺少限制**：不承认故障模式

- --

## 反驳提示

ML会议有作者回复期。提示：
- **首先解决关键问题**：优先考虑关键问题
- **运行请求的实验**：及时可行时
- **简洁**：审稿人阅读许多反驳
- **保持专业**：即使有不公平的评论
- **参考具体行**：“如所述L127..."

- --

## 提交前清单

### 内容
- [ ]明确问题动机
- [ ]显式贡献列表
- [ ]完整方法描述
- [ ]综合实验
- [ ]包括强基线
- [ ]存在消融研究
- [ ]承认局限性

### 技术
- [ ]正确的场地风格文件（当年）
- [ ]匿名（没有作者姓名，无法识别） URL)
- [ ]遵守页面限制
- [ ]参考文献完整
- [ ]补充组织

### 再现性
- [ ]列出的超参数
- [ ]指定随机种子
- [ ]计算要求所述
- [ ]已注明代码/数据可用性
- [ ]已完成再现性检查表

- --

## 另请参阅

- `venue_writing_styles.md` - 主样式概述
- `conferences_formatting.md` - 技术格式要求
- `reviewer_expectations.md` - ML 审阅者寻求什么
