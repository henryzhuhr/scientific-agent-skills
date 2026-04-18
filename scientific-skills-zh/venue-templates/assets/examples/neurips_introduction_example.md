# NeurIPS/ICML 介绍示例

这个示例展示了独特的 ML 会议介绍结构，具有编号贡献和技术精度。

- --

## 完整介绍示例

* *论文主题**：高效长上下文变压器

- --

### 第 1 段：问题动机

```
Large language models (LLMs) have demonstrated remarkable capabilities in 
natural language understanding, code generation, and reasoning tasks [1, 2, 3]. 
These capabilities scale with both model size and context length—longer 
contexts enable processing of entire documents, multi-turn conversations, 
and complex reasoning chains that span many steps [4, 5]. However, the 
standard Transformer attention mechanism [6] has O(N²) time and memory 
complexity with respect to sequence length N, creating a fundamental 
bottleneck for processing long sequences. For a context window of 100K 
tokens, computing full attention requires 10 billion scalar operations 
and 40 GB of memory for the attention matrix alone, making training and 
inference prohibitively expensive on current hardware.
```

* *关键特性**：
- 说明为什么这很重要（LLM能力）
- 连接到扩展（更长的上下文=更好的性能）
- 具体数字（O（N²），100K代币，100亿次操作，40 GB)
- 建立可信度的引用

- --

### 第 2 段：现有方法的局限性

```
Prior work has addressed attention efficiency through three main approaches. 
Sparse attention patterns [7, 8, 9] reduce complexity to O(N√N) or O(N log N) 
by restricting attention to local windows, fixed stride patterns, or learned 
sparse masks. Linear attention approximations [10, 11, 12] reformulate 
attention using kernel feature maps that enable O(N) computation, but 
sacrifice the ability to model arbitrary pairwise interactions. Low-rank 
factorizations [13, 14] approximate the attention matrix as a product of 
smaller matrices, achieving efficiency at the cost of expressivity. While 
these methods reduce theoretical complexity, they introduce approximation 
errors that compound in deep networks, often resulting in 2-5% accuracy 
degradation on long-range modeling benchmarks [15]. Perhaps more importantly, 
they fundamentally change the attention mechanism, making it difficult to 
apply advances in standard attention (e.g., rotary positional embeddings, 
grouped-query attention) to efficient variants.
```

* *关键特征**：
- 先前工作的有组织的分类
- 规定的复杂性每种方法
- 明确识别局限性
- 量化缺点（2-5% 退化）
- 识别更深层次的问题（与进步不兼容）

- --

### 第3 段：您的方法（高级）

```
We take a different approach: rather than approximating attention, we 
accelerate exact attention by optimizing memory access patterns. Our key 
observation is that on modern GPUs, attention is bottlenecked by memory 
bandwidth, not compute. Reading and writing the N × N attention matrix to 
and from GPU high-bandwidth memory (HBM) dominates runtime, while the GPU's 
tensor cores remain underutilized. We propose LongFlash, an IO-aware exact 
attention algorithm that computes attention block-by-block in fast on-chip 
SRAM, never materializing the full attention matrix in HBM. By carefully 
orchestrating the tiling pattern and fusing the softmax computation with 
matrix multiplications, LongFlash reduces HBM accesses from O(N²) to 
O(N²d/M) where d is the head dimension and M is the SRAM size, achieving 
asymptotically optimal IO complexity.
```

* *关键特征**：
- 与先前工作的明显区别（“不同方法”）
- 明确阐述关键见解
- 技术机制解释
- 量化复杂性改进
- 方法名称介绍了

- --

### 第4段：贡献（关键）

```
Our contributions are as follows:

• We propose LongFlash, an IO-aware exact attention algorithm that achieves 
  2-4× speedup over FlashAttention [16] and up to 9× over standard PyTorch 
  attention on sequences from 1K to 128K tokens (Section 3).

• We provide theoretical analysis proving that LongFlash achieves optimal 
  IO complexity of O(N²d/M) among all algorithms that compute exact 
  attention, and analyze the regime where our algorithm provides maximum 
  benefit (Section 3.3).

• We introduce sequence parallelism techniques that enable LongFlash to 
  scale to sequences of 1M+ tokens across multiple GPUs with near-linear 
  weak scaling efficiency (Section 4).

• We demonstrate that LongFlash enables training with 8× longer contexts 
  on the same hardware: we train a 7B parameter model on 128K token 
  contexts using the same memory that previously limited us to 16K tokens 
  (Section 5).

• We release optimized CUDA kernels achieving 80% of theoretical peak 
  FLOPS on A100 and H100 GPUs, along with PyTorch and JAX bindings, at 
  [anonymous URL] (Section 6).
```

* *关键功能**：
- 编号/项目符号格式
- 每个贡献都是具体和量化的
- 每个贡献的部分参考声明
- 方法论和经验贡献
- 提到的代码发布
- 独立的项目符号（每个单独有意义）

- --

## 替代开头段落

### 对于方法论文

```
Scalable optimization algorithms are fundamental to modern machine learning. 
Stochastic gradient descent (SGD) and its variants [1, 2, 3] have enabled 
training of models with billions of parameters on massive datasets. However, 
these first-order methods exhibit slow convergence on ill-conditioned 
problems, often requiring thousands of iterations to converge on tasks 
where second-order methods would converge in tens of iterations [4, 5].
```

#### 应用论文

```
Drug discovery is a costly and time-consuming process, with the average new 
drug requiring 10-15 years and $2.6 billion to develop [1]. Machine learning 
offers the potential to accelerate this process by predicting molecular 
properties, identifying promising candidates, and optimizing lead compounds 
computationally [2, 3]. Recent successes in protein structure prediction [4] 
and molecular generation [5] have demonstrated that deep learning can 
capture complex chemical patterns, raising hopes for ML-driven drug discovery.
```

### 理论论文

```
Understanding why deep neural networks generalize well despite having more 
parameters than training examples remains one of the central puzzles of 
modern machine learning [1, 2]. Classical statistical learning theory 
predicts that such overparameterized models should overfit dramatically, 
yet in practice, large networks trained with SGD achieve excellent test 
accuracy [3]. This gap between theory and practice has motivated a rich 
literature on implicit regularization [4], neural tangent kernels [5], 
and feature learning [6], but a complete theoretical picture remains elusive.
```

- --

## 贡献项目符号模板

### 新方法

```
• We propose [Method Name], a novel [type of method] that [key innovation] 
  achieving [performance improvement] over [baseline] on [benchmark].
```

### 理论分析

```
• We prove that [statement], providing the first [type of result] for 
  [problem setting]. This resolves an open question from [prior work].
```

### 实证研究

```
• We conduct a comprehensive evaluation of [N] methods across [M] datasets, 
  revealing that [key finding] and identifying [failure mode/best practice].
```

### 代码/数据发布

```
• We release [resource name], a [description] containing [scale/scope], 
  available at [URL]. This enables [future work/reproducibility].
```

- --

## 要避免的常见错误

### 模糊贡献

❌ **不好**：
```
• We propose a novel method for attention
• We show our method is better than baselines
• We provide theoretical analysis
```

✅ **好**：
```
• We propose LongFlash, achieving 2-4× speedup over FlashAttention
• We prove LongFlash achieves optimal O(N²d/M) IO complexity
• We enable 8× longer context training on fixed hardware budget
```

### 缺少量化

❌ **差**：“我们的方法显着优于之前的工作”
✅ **好**：“我们的方法在 GLUE 上提高了 3.2% 的准确度，在 SuperGLUE 上提高了 4.1%”

### 重叠子弹

❌ **差**：
```
• We propose a new attention mechanism
• We introduce LongFlash attention
• Our novel attention approach...
```
（这三个都说同样的事情）次）

### 埋藏贡献

❌ **差**：贡献项目符号在第2页末尾
✅ **好**：贡献项目符号在第1页末尾清晰可见

- --

## 另请参阅

- `ml_conference_style.md` - 综合ML会议指南
- `venue_writing_styles.md` - 跨场馆风格对比
