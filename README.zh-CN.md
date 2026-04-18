# Scientific Agent Skills

[English](README.md) | 中文

> **🔔 Claude Scientific Skills 现已更名为 Scientific Agent Skills。** 技能不变，兼容性更广，现在可用于任何支持开放 [Agent Skills](https://agentskills.io/) 标准的 AI 代理，而不再局限于 Claude。

> **全新发布：[K-Dense BYOK](https://github.com/K-Dense-AI/k-dense-byok)** — 一款免费、开源、可在桌面运行的 AI 协作科研助手，由 Scientific Agent Skills 提供支持。你可以自带 API 密钥，从 40+ 模型中自由选择，并获得一个完整的研究工作区，包含网页搜索、文件处理、100+ 科学数据库，以及本仓库全部 133 项技能的访问能力。你的数据保留在本地电脑中，如需处理重负载任务，也可选用 [Modal](https://modal.com/) 扩展到云端计算。[点此开始。](https://github.com/K-Dense-AI/k-dense-byok)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![Skills](https://img.shields.io/badge/Skills-133-brightgreen.svg)](#whats-included)
[![Databases](https://img.shields.io/badge/Databases-100%2B-orange.svg)](#whats-included)
[![Agent Skills](https://img.shields.io/badge/Standard-Agent_Skills-blueviolet.svg)](https://agentskills.io/)
[![Works with](https://img.shields.io/badge/Works_with-Cursor_|_Claude_Code_|_Codex-blue.svg)](#getting-started)
[![X](https://img.shields.io/badge/Follow_on_X-%40k__dense__ai-000000?logo=x)](https://x.com/k_dense_ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-K--Dense_Inc.-0A66C2?logo=linkedin)](https://www.linkedin.com/company/k-dense-inc)
[![YouTube](https://img.shields.io/badge/YouTube-K--Dense_Inc.-FF0000?logo=youtube)](https://www.youtube.com/@K-Dense-Inc)

这是一套由 [K-Dense](https://k-dense.ai) 创建的、覆盖 **133 个即开即用的科研与研究技能** 的完整合集，适用于任何支持开放 [Agent Skills](https://agentskills.io/) 标准的 AI 代理。内容涵盖癌症基因组学、药物靶点结合、分子动力学、RNA velocity、地理空间科学、时间序列预测、78+ 科学数据库等多个方向。可与 **Cursor、Claude Code、Codex 等** 配合使用，把你的 AI 代理变成能够跨生物学、化学、医学等领域执行复杂多步骤科研流程的研究助手。

仓库中的规范英文技能源目录位于 `scientific-skills/`。同时还维护了一个简体中文镜像 `scientific-skills-zh/`，保持相同的目录和文件名、翻译后的 Markdown 内容，以及独立生成的中文安全报告 `SECURITY.zh.md`。

---

这些技能让你的 AI 代理能够无缝使用多个科学领域中的专业库、数据库与工具。虽然代理本身也可以自行使用任意 Python 包或 API，但这些显式定义的技能提供了经过整理的文档与示例，能让它在下列工作流中表现得更强、更稳定：

- 🧬 生物信息学与基因组学 - 序列分析、单细胞 RNA-seq、基因调控网络、变异注释、系统发育分析
- 🧪 化学信息学与药物发现 - 分子性质预测、虚拟筛选、ADMET 分析、分子对接、先导优化
- 🔬 蛋白质组学与质谱 - LC-MS/MS 处理、肽段鉴定、谱图匹配、蛋白定量
- 🏥 临床研究与精准医疗 - 临床试验、药物基因组学、变异解读、药物安全、临床决策支持、治疗规划
- 🧠 医疗 AI 与临床机器学习 - EHR 分析、生理信号处理、医学影像、临床预测模型
- 🖼️ 医学影像与数字病理 - DICOM 处理、全切片图像分析、计算病理、放射学工作流
- 🤖 机器学习与 AI - 深度学习、强化学习、时间序列分析、模型可解释性、贝叶斯方法
- 🔮 材料科学与化学 - 晶体结构分析、相图、代谢建模、计算化学
- 🌌 物理与天文学 - 天文数据分析、坐标变换、宇宙学计算、符号数学、物理计算
- ⚙️ 工程与仿真 - 离散事件仿真、多目标优化、代谢工程、系统建模、过程优化
- 📊 数据分析与可视化 - 统计分析、网络分析、时间序列、出版级图形、大规模数据处理、EDA
- 🌍 地理空间科学与遥感 - 卫星影像处理、GIS 分析、空间统计、地形分析、地球观测机器学习
- 🧪 实验室自动化 - 液体处理协议、实验设备控制、工作流自动化、LIMS 集成
- 📚 科学传播 - 文献综述、同行评审、科学写作、文档处理、海报、幻灯片、示意图、引文管理
- 🔬 多组学与系统生物学 - 多模态数据整合、通路分析、网络生物学、系统层面的洞察
- 🧬 蛋白工程与设计 - 蛋白语言模型、结构预测、序列设计、功能注释
- 🎓 研究方法学 - 假设生成、科学头脑风暴、批判性思维、基金申请、学者评估

**把你的 AI 编码代理变成桌面上的“AI 科学家”！**

> ⭐ **如果你觉得这个仓库有用**，欢迎点个 Star。这能帮助更多人发现这些工具，也能鼓励我们持续维护并扩展这套技能集合。

> 🎬 **第一次接触 Scientific Agent Skills？** 可以观看我们的 [Scientific Agent Skills 快速上手视频](https://youtu.be/ZxbnDaD_FVg)。

---

<a id="whats-included"></a>

## 📦 包含内容

本仓库提供 **133 项科研与研究技能**，按以下类别组织：

- **100+ 科学与金融数据库** - 统一的 Database Lookup 技能可直接访问 78 个公共数据库（包括 PubChem、ChEMBL、UniProt、COSMIC、ClinicalTrials.gov、FRED、USPTO 等），并额外提供 DepMap、Imaging Data Commons、PrimeKG、U.S. Treasury Fiscal Data 等专用技能。BioServices（约 40 个生物信息服务）、BioPython（通过 Entrez 访问 38 个 NCBI 子数据库）和 gget（20+ 基因组数据库）等多数据库包进一步扩展了覆盖范围
- **70+ 个优化过的 Python 包技能** - 为 RDKit、Scanpy、PyTorch Lightning、scikit-learn、BioPython、pyzotero、BioServices、PennyLane、Qiskit、OpenMM、MDAnalysis、scVelo、TimesFM 等提供显式定义的技能，附带整理好的文档、示例与最佳实践。注意：代理可以编写并使用 *任何* Python 包，而不只限于这些；这些技能只是为所列包提供更强、更可靠的支持
- **9 项科研集成技能** - 为 Benchling、DNAnexus、LatchBio、OMERO、Protocols.io、Open Notebook 等平台提供显式定义的技能。同样，代理并不受限于这些平台，Python 能访问到的任何 API 或平台都可以使用；这里只是预先优化并写好文档的路径
- **30+ 分析与沟通工具** - 覆盖文献综述、科学写作、同行评审、文档处理、海报、幻灯片、示意图、信息图、Mermaid 图等
- **10+ 研究与临床工具** - 包括假设生成、基金申请、临床决策支持、治疗方案、法规合规、情景分析

每项技能都包含：

- ✅ 完整文档（`SKILL.md`）
- ✅ 实用代码示例
- ✅ 使用场景与最佳实践
- ✅ 集成指南
- ✅ 参考资料

---

## 📋 目录

- [包含内容](#whats-included)
- [为什么使用它？](#why-use-this)
- [快速开始](#getting-started)
- [安全免责声明](#security-disclaimer)
- [支持开源社区](#support-the-open-source-community)
- [前置要求](#prerequisites)
- [快速示例](#quick-examples)
- [使用场景](#use-cases)
- [可用技能](#available-skills)
- [贡献指南](#contributing)
- [故障排查](#troubleshooting)
- [常见问题](#faq)
- [支持](#support)
- [加入社区](#join-our-community)
- [引用方式](#citation)
- [许可证](#license)

---

<a id="why-use-this"></a>

## 🚀 为什么使用它？

### ⚡ **加速你的科研工作**

- **节省数天工作量** - 省去查 API 文档和搭建集成环境的时间
- **可用于生产的代码** - 提供经过测试和验证、符合科研最佳实践的示例
- **多步骤工作流** - 用一条提示词即可执行复杂流程

### 🎯 **覆盖全面**

- **133 项技能** - 覆盖主要科研领域的广泛能力
- **100+ 数据库** - 通过 database-lookup 统一访问 78+ 数据库，并包含专用数据访问技能，以及 BioServices、BioPython、gget 等多数据库包
- **70+ 个优化过的 Python 包技能** - 包括 RDKit、Scanpy、PyTorch Lightning、scikit-learn、BioServices、PennyLane、Qiskit、OpenMM、scVelo、TimesFM 等（代理可使用任意 Python 包；这些是预先文档化、表现更稳定的路径）

### 🔧 **易于集成**

- **配置简单** - 把技能复制到技能目录后即可开始使用
- **自动发现** - 你的代理会自动找到并使用相关技能
- **文档完善** - 每项技能都带有示例、使用场景和最佳实践

### 🌟 **持续维护与支持**

- **持续更新** - 由 K-Dense 团队持续维护和扩展
- **社区驱动** - 开源项目，欢迎社区积极贡献
- **可用于企业** - 对高级需求提供商业支持

---

<a id="getting-started"></a>

## 🎯 快速开始

使用一条命令安装 Scientific Agent Skills：

```bash
npx skills add K-Dense-AI/scientific-agent-skills
```

这是在 **所有平台** 上安装 Agent Skills 的官方标准方式，适用于 **Claude Code、Claude Cowork、Codex、Gemini CLI、Cursor**，以及其他任何支持开放 [Agent Skills](https://agentskills.io/) 标准的代理。

**就这么简单！** 你的 AI 代理会自动发现这些技能，并在与科研任务相关时使用它们。你也可以在提示词中直接提到某个技能名称来手动调用。

---

<a id="security-disclaimer"></a>

## ⚠️ 安全免责声明

> **技能可以执行代码，并影响你的编码代理行为。安装前请自行审查。**

Agent Skills 很强大，它们可以指示 AI 代理运行任意代码、安装软件包、发起网络请求，并修改你系统上的文件。恶意技能或编写不当的技能，都有可能把你的编码代理引导到有害行为上。

我们非常重视安全。所有贡献都会经过审核流程，而且我们会对本仓库中的每项技能运行基于 LLM 的安全扫描（通过 [Cisco AI Defense Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner)）。但作为一个规模较小、同时还在接收越来越多社区贡献的团队，我们无法保证每项技能都对所有潜在风险做过穷尽式审查。

**最终，由你负责审查自己安装的技能，并决定信任哪些内容。**

我们建议你：

- **不要一次性全部安装。** 只安装你实际工作中需要的技能。当所有技能都由 K-Dense 创建并维护时，安装完整集合是合理的；但现在仓库已包含许多社区贡献的技能，我们未必能像自研技能那样做同等深度的审查。
- **安装前先阅读 `SKILL.md`。** 每项技能的文档都会说明它做什么、使用哪些软件包、会连接哪些外部服务。如果看起来有可疑之处，就不要安装。
- **查看贡献历史。** 由 K-Dense（`K-Dense-AI`）编写的技能都经过了我们的内部审查流程。社区贡献的技能也经过了我们尽力而为的检查，但受限于资源，不能等同于全面保证。
- **自行运行安全扫描。** 在安装第三方技能前，先在本地扫描：

  ```bash
  uv pip install cisco-ai-skill-scanner
  skill-scanner scan /path/to/skill --use-behavioral
  ```

- **报告任何可疑情况。** 如果你发现某项技能可疑或行为异常，请立即[提交 issue](https://github.com/K-Dense-AI/scientific-agent-skills/issues)，我们会调查。

所有技能大约按周进行一次扫描，英文结果见 [SECURITY.md](SECURITY.md)，中文镜像结果见 [SECURITY.zh.md](SECURITY.zh.md)。只要发现安全缺口，我们就会尽量尽快处理。

---

<a id="support-the-open-source-community"></a>

## ❤️ 支持开源社区

Scientific Agent Skills 建立在 **50+ 个卓越开源项目** 的基础上，这些项目由全球各地的开发者和研究社区持续维护。Biopython、Scanpy、RDKit、scikit-learn、PyTorch Lightning 等项目，都是这些技能背后的关键支撑。

**如果你觉得这个仓库有价值，欢迎支持那些让它成为可能的项目：**

- ⭐ 在 GitHub 上为它们点 Star
- 💰 通过 GitHub Sponsors 或 NumFOCUS 赞助维护者
- 📝 在你的论文中引用这些项目
- 💻 贡献代码、文档或 bug 报告

👉 **[查看完整支持项目列表](docs/open-source-sponsors.zh-CN.md)**

---

<a id="prerequisites"></a>

## ⚙️ 前置要求

- **Python**：3.11+（推荐 3.12+ 以获得最佳兼容性）
- **uv**：Python 包管理器（安装技能依赖所必需）
- **客户端**：任何支持 [Agent Skills](https://agentskills.io/) 标准的代理（Cursor、Claude Code、Gemini CLI、Codex 等）
- **系统**：macOS、Linux，或带 WSL2 的 Windows
- **依赖**：由各技能自动处理（具体要求请查看对应 `SKILL.md`）

### 安装 uv

这些技能使用 `uv` 作为安装 Python 依赖的包管理器。请按你的操作系统选择安装方式：

**macOS 和 Linux：**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows：**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**替代方案（通过 pip）：**

```bash
pip install uv
```

安装后，可通过以下命令验证是否生效：

```bash
uv --version
```

更多安装选项和细节，请参阅 [uv 官方文档](https://docs.astral.sh/uv/)。

---

<a id="quick-examples"></a>

## 💡 快速示例

安装好这些技能后，你就可以要求 AI 代理执行复杂的多步骤科研工作流。以下是一些示例提示词：

### 🧪 药物发现流程

**目标**：寻找用于肺癌治疗的新型 EGFR 抑制剂

**提示词**：

```
尽可能使用你可以访问的可用技能。查询 ChEMBL 中的 EGFR 抑制剂（IC50 < 50nM），用 RDKit 分析构效关系，
使用 datamol 生成改良类似物，基于 AlphaFold 的 EGFR 结构用 DiffDock 进行虚拟筛选，
在 PubMed 中检索耐药机制，检查 COSMIC 里的突变，并生成可视化结果和综合报告。
```

**使用技能**：ChEMBL、RDKit、datamol、DiffDock、AlphaFold DB、PubMed、COSMIC、scientific visualization

*需要云端 GPU 和最终可直接用于发表的报告？[在 K-Dense Web 免费运行此流程。](https://k-dense.ai)*

---

### 🔬 单细胞 RNA-seq 分析

**目标**：结合公共数据整合的 10X Genomics 数据综合分析

**提示词**：

```
尽可能使用你可以访问的可用技能。用 Scanpy 加载 10X 数据集，执行 QC 和 doublet 去除，
与 Cellxgene Census 数据整合，使用 NCBI Gene markers 识别细胞类型，用 PyDESeq2 进行差异表达分析，
通过 Arboreto 推断基因调控网络，经 Reactome/KEGG 做通路富集，并用 Open Targets 识别治疗靶点。
```

**使用技能**：Scanpy、Cellxgene Census、NCBI Gene、PyDESeq2、Arboreto、Reactome、KEGG、Open Targets

*想要免配置的云端执行和可分享的输出？[免费试用 K-Dense Web。](https://k-dense.ai)*

---

### 🧬 多组学生物标志物发现

**目标**：整合 RNA-seq、蛋白质组学和代谢组学以预测患者结局

**提示词**：

```
尽可能使用你可以访问的可用技能。用 PyDESeq2 分析 RNA-seq，用 pyOpenMS 处理质谱数据，
整合来自 HMDB/Metabolomics Workbench 的代谢物，把蛋白映射到通路（UniProt/KEGG），通过 STRING 寻找相互作用，
用 statsmodels 关联不同组学层，用 scikit-learn 构建预测模型，并在 ClinicalTrials.gov 搜索相关试验。
```

**使用技能**：PyDESeq2、pyOpenMS、HMDB、Metabolomics Workbench、UniProt、KEGG、STRING、statsmodels、scikit-learn、ClinicalTrials.gov

*这条流程计算量较大。[可在 K-Dense Web 上配合云 GPU 运行，免费开始。](https://k-dense.ai)*

---

### 🎯 虚拟筛选项目

**目标**：发现作用于蛋白-蛋白相互作用的变构调节剂

**提示词**：

```
尽可能使用你可以访问的可用技能。获取 AlphaFold 结构，用 BioPython 识别相互作用界面，
在 ZINC 中搜索变构候选（MW 300-500，logP 2-4），用 RDKit 过滤，使用 DiffDock 对接，
通过 DeepChem 排序，检查 PubChem 供应商信息，搜索 USPTO 专利，并用 MedChem/molfeat 优化先导化合物。
```

**使用技能**：AlphaFold DB、BioPython、ZINC、RDKit、DiffDock、DeepChem、PubChem、USPTO、MedChem、molfeat

*跳过本地 GPU 瓶颈。[在 K-Dense Web 免费运行虚拟筛选。](https://k-dense.ai)*

---

### 🏥 临床变异解读

**目标**：分析 VCF 文件，用于遗传性肿瘤风险评估

**提示词**：

```
尽可能使用你可以访问的可用技能。使用 pysam 解析 VCF，用 Ensembl VEP 注释变异，查询 ClinVar 获取致病性，
检查 COSMIC 的肿瘤突变，从 NCBI Gene 获取基因信息，用 UniProt 分析蛋白影响，
在 PubMed 检索病例报告，查看 ClinPGx 的药物基因组学信息，借助文档处理工具生成临床报告，
并在 ClinicalTrials.gov 中查找匹配的临床试验。
```

**使用技能**：pysam、Ensembl、ClinVar、COSMIC、NCBI Gene、UniProt、PubMed、ClinPGx、Document Skills、ClinicalTrials.gov

*需要最终交付的是一份精致的临床报告，而不仅是代码？[K-Dense Web 能生成可直接发表的结果，免费试用。](https://k-dense.ai)*

---

### 🌐 系统生物学网络分析

**目标**：分析 RNA-seq 数据中的基因调控网络

**提示词**：

```
尽可能使用你可以访问的可用技能。查询 NCBI Gene 获取注释，从 UniProt 拉取序列，通过 STRING 识别相互作用，
映射到 Reactome/KEGG 通路，使用 Torch Geometric 分析拓扑结构，借助 Arboreto 重建 GRN，
用 Open Targets 评估可成药性，使用 PyMC 建模，进行网络可视化，并在 GEO 中搜索相似模式。
```

**使用技能**：NCBI Gene、UniProt、STRING、Reactome、KEGG、Torch Geometric、Arboreto、Open Targets、PyMC、GEO

*想要零配置、端到端、可分享的输出？[免费试用 K-Dense Web。](https://k-dense.ai)*

> 📖 **想看更多示例？** 请查看 [docs/examples.md](docs/examples.md)，其中包含面向各科研领域的完整工作流示例和详细用例。

---

## 🚀 想跳过环境配置，直接开始做科研？

**下面这些情况你是否很熟悉？**

- 花在环境配置上的时间比真正分析还多
- 你的工作流需要本地机器没有的 GPU
- 你需要的是可以直接分享、可直接发表的图表或报告，而不是一段脚本
- 你想立刻运行复杂的多步骤流程，而不是先去啃包文档

如果是，**[K-Dense Web](https://k-dense.ai)** 就是为你准备的。它是完整的 AI 协作科研平台：包含本仓库中的全部能力，再加上云 GPU、200+ 技能，以及可直接放进论文或演示文稿中的输出。零配置即可开始。

| 功能 | 本仓库 | K-Dense Web |
|---------|-----------|-------------|
| 科学技能 | 133 项技能 | **200+ 项技能**（独家） |
| 配置 | 手动安装 | **零配置，开箱即用** |
| 计算资源 | 你的本地机器 | **自带云 GPU 和 HPC** |
| 工作流 | 提示词和代码 | **端到端科研流程** |
| 输出 | 代码和分析 | **可直接发表的图表、报告和论文** |
| 集成 | 本地工具 | **实验室系统、ELN 和云存储** |

> *“K-Dense Web 让我在一个下午内就从原始测序数据走到了图表初稿。过去要花三天做环境配置和写脚本的工作，现在直接就能跑通。”*
> **计算生物学家，药物发现领域**

> ### 💰 赠送 50 美元免费额度，无需信用卡
>
> 几分钟内即可开始运行真实科研工作流。
>
> **[免费试用 K-Dense Web](https://k-dense.ai)**

*[k-dense.ai](https://k-dense.ai) | [查看完整对比](https://k-dense.ai/blog/k-dense-web-vs-scientific-agent-skills)*

---

<a id="use-cases"></a>

## 🔬 使用场景

### 🧪 药物发现与药物化学

- **虚拟筛选**：针对蛋白靶点，从 PubChem/ZINC 中筛选数百万化合物
- **先导优化**：使用 RDKit 分析构效关系，借助 datamol 生成类似物
- **ADMET 预测**：用 DeepChem 预测吸收、分布、代谢、排泄和毒性
- **分子对接**：使用 DiffDock 预测结合构象和亲和力
- **生物活性挖掘**：从 ChEMBL 查询已知抑制剂并分析 SAR 模式

### 🧬 生物信息学与基因组学

- **序列分析**：用 BioPython 和 pysam 处理 DNA/RNA/蛋白序列
- **单细胞分析**：使用 Scanpy 分析 10X Genomics 数据，识别细胞类型，并用 Arboreto 推断 GRN
- **变异注释**：通过 Ensembl VEP 注释 VCF 文件，并在 ClinVar 中查询致病性
- **变异数据库管理**：使用 TileDB-VCF 构建可扩展的 VCF 数据库，支持样本增量写入、人群规模查询和压缩存储基因组变异数据
- **基因发现**：查询 NCBI Gene、UniProt 和 Ensembl 以获取全面的基因信息
- **网络分析**：通过 STRING 识别蛋白互作，并映射到 KEGG、Reactome 等通路

### 🏥 临床研究与精准医疗

- **临床试验**：在 ClinicalTrials.gov 搜索相关研究并分析入组标准
- **变异解读**：结合 ClinVar、COSMIC 和 ClinPGx 进行变异注释和药物基因组学分析
- **药物安全**：查询 FDA 数据库中的不良事件、药物相互作用和召回信息
- **精准治疗**：将患者变异与靶向疗法和临床试验进行匹配

### 🔬 多组学与系统生物学

- **多组学整合**：组合 RNA-seq、蛋白质组学与代谢组学数据
- **通路分析**：对差异表达基因进行 KEGG/Reactome 通路富集
- **网络生物学**：重建基因调控网络，识别枢纽基因
- **生物标志物发现**：整合多组学层级来预测患者结局

### 📊 数据分析与可视化

- **统计分析**：执行假设检验、功效分析和实验设计
- **出版级图形**：使用 matplotlib 和 seaborn 创建适合发表的可视化图像
- **网络可视化**：使用 NetworkX 展示生物网络
- **报告生成**：用 Document Skills 生成完整 PDF 报告

### 🧪 实验室自动化

- **协议设计**：为自动化液体处理创建 Opentrons 协议
- **LIMS 集成**：与 Benchling 和 LabArchives 集成做数据管理
- **工作流自动化**：自动化多步骤实验室流程

---

<a id="available-skills"></a>

## 📚 可用技能

本仓库包含 **133 项科研与研究技能**，覆盖多个领域。每项技能都提供完整文档、代码示例和与科研库、数据库及工具协作时的最佳实践。

### 技能类别

> **说明：** 下列 Python 包技能和集成技能都是*显式定义*的技能，也就是附带文档、示例和最佳实践、能带来更强更稳定表现的优化路径。它们不是能力上限：代理仍可安装并使用*任何* Python 包，或调用*任何* API，即使没有对应专用技能。这里列出的技能只是让常见工作流更快、更可靠。

#### 🧬 **生物信息学与基因组学**（21+ 项技能）

- 序列分析：BioPython、pysam、scikit-bio、BioServices
- 单细胞分析：Scanpy、AnnData、scvi-tools、scVelo（RNA velocity）、Arboreto、Cellxgene Census
- 基因组工具：gget、geniml、gtars、deepTools、FlowIO、Polars-Bio、Zarr、TileDB-VCF
- 差异表达：PyDESeq2
- 系统发育学：ETE Toolkit、Phylogenetics（MAFFT、IQ-TREE 2、FastTree）

#### 🧪 **化学信息学与药物发现**（10+ 项技能）

- 分子处理：RDKit、Datamol、Molfeat
- 深度学习：DeepChem、TorchDrug
- 对接与筛选：DiffDock
- 分子动力学：OpenMM + MDAnalysis（MD 模拟与轨迹分析）
- 云端量子化学：Rowan（pKa、docking、cofolding）
- 成药性评估：MedChem
- 基准测试：PyTDC

#### 🔬 **蛋白质组学与质谱**（2 项技能）

- 谱图处理：matchms、pyOpenMS

#### 🏥 **临床研究与精准医疗**（8+ 项技能）

- 临床数据库：通过 Database Lookup 访问（ClinicalTrials.gov、ClinVar、ClinPGx、COSMIC、FDA、cBioPortal、Monarch 等）
- 癌症基因组学：DepMap（癌症依赖性评分、药物敏感性）
- 癌症影像：Imaging Data Commons（通过 idc-index 访问 NCI 放射和病理数据集）
- 医疗 AI：PyHealth、NeuroKit2、Clinical Decision Support
- 临床文档：Clinical Reports、Treatment Plans

#### 🖼️ **医学影像与数字病理**（3 项技能）

- DICOM 处理：pydicom
- 全切片影像：histolab、PathML

#### 🧠 **神经科学与电生理**（1 项技能）

- 神经记录：Neuropixels-Analysis（细胞外 spike、硅探针、spike sorting）

#### 🤖 **机器学习与 AI**（16+ 项技能）

- 深度学习：PyTorch Lightning、Transformers、Stable Baselines3、PufferLib
- 经典机器学习：scikit-learn、scikit-survival、SHAP
- 时间序列：aeon、TimesFM（Google 的单变量预测零样本基础模型）
- 贝叶斯方法：PyMC
- 优化：PyMOO
- 图机器学习：Torch Geometric
- 降维：UMAP-learn
- 统计建模：statsmodels

#### 🔮 **材料科学、化学与物理**（7 项技能）

- 材料：Pymatgen
- 代谢建模：COBRApy
- 天文学：Astropy
- 量子计算：Cirq、PennyLane、Qiskit、QuTiP

#### ⚙️ **工程与仿真**（4 项技能）

- 数值计算：MATLAB/Octave
- 计算流体力学：FluidSim
- 离散事件仿真：SimPy
- 符号数学：SymPy

#### 📊 **数据分析与可视化**（16+ 项技能）

- 可视化：Matplotlib、Seaborn、Scientific Visualization
- 地理空间分析：GeoPandas、GeoMaster（遥感、GIS、卫星影像、空间 ML、500+ 示例）
- 数据处理：Dask、Polars、Vaex
- 网络分析：NetworkX
- 文档处理：Document Skills（PDF、DOCX、PPTX、XLSX）
- 信息图：Infographics（AI 驱动的专业信息图创建）
- 图表：Markdown & Mermaid Writing（默认采用文本化图表作为文档标准）
- 探索性数据分析：EDA 工作流
- 统计分析：Statistical Analysis 工作流

#### 🧪 **实验室自动化**（4 项技能）

- 液体处理：PyLabRobot
- 云实验室：Ginkgo Cloud Lab（无细胞蛋白表达、基于自主 RAC 基础设施的荧光像素艺术）
- 协议管理：Protocols.io
- LIMS 集成：Benchling、LabArchives

#### 🔬 **多组学与系统生物学**（4+ 项技能）

- 通路分析：通过 Database Lookup 访问（KEGG、Reactome、STRING）以及 PrimeKG
- 多组学：HypoGeniC
- 数据管理：LaminDB

#### 🧬 **蛋白工程与设计**（3 项技能）

- 蛋白语言模型：ESM
- 糖工程：Glycoengineering（N/O-糖基化预测、治疗性抗体优化）
- 云端实验平台：Adaptyv（自动化蛋白测试与验证）

#### 📚 **科学传播**（20+ 项技能）

- 文献：Paper Lookup（PubMed、PMC、bioRxiv、medRxiv、arXiv、OpenAlex、Crossref、Semantic Scholar、CORE、Unpaywall）、Literature Review
- 高级论文搜索：BGPT Paper Search（每篇论文 25+ 个结构化字段，包括方法、结果、样本量、质量评分，来源于全文而非摘要）
- 网页搜索：Parallel Web（带引用的综合总结）
- 研究笔记：Open Notebook（自托管 NotebookLM 替代方案，支持 PDF、视频、音频、网页；16+ AI 提供商；可生成多说话人的播客）
- 写作：Scientific Writing、Peer Review
- 文档处理：XLSX、MarkItDown、Document Skills
- 发表：Venue Templates
- 演示：Scientific Slides、LaTeX Posters、PPTX Posters
- 图示：Scientific Schematics、Markdown & Mermaid Writing
- 信息图：Infographics（10 种类型、8 种风格、色盲安全配色）
- 引文：Citation Management
- 插图：Generate Image（使用 FLUX.2 Pro 和 Gemini 3 Pro（Nano Banana Pro）的 AI 图像生成）

#### 🔬 **科学数据库与数据访问**（5 项技能 → 合计 100+ 数据库）
>
> 统一的 Database Lookup 技能可通过 REST API 访问 78 个公共数据库，覆盖所有领域。专用技能则覆盖更专业的数据平台。BioServices（约 40 个生物信息服务）、BioPython（通过 Entrez 访问 38 个 NCBI 子数据库）和 gget（20+ 基因组数据库）等多数据库包进一步拓展了能力边界。

- 统一访问：Database Lookup（78 个数据库，覆盖化学、基因组学、临床、通路、专利、经济等领域，包括 PubChem、ChEMBL、UniProt、PDB、AlphaFold、KEGG、Reactome、STRING、ClinVar、COSMIC、ClinicalTrials.gov、FDA、FRED、USPTO、SEC EDGAR 等数十个来源）
- 癌症基因组学：DepMap（癌症细胞系依赖性、药物敏感性、基因效应谱）
- 癌症影像：Imaging Data Commons（通过 idc-index 访问 NCI 放射和病理数据集）
- 知识图谱：PrimeKG（精准医疗知识图谱，涵盖基因、药物、疾病、表型）
- 财政数据：U.S. Treasury Fiscal Data（国债、财政报表、拍卖、汇率）

#### 🔧 **基础设施与平台**（7+ 项技能）

- 云计算：Modal
- GPU 加速：Optimize for GPU（CuPy、Numba CUDA、Warp、cuDF、cuML、cuGraph、KvikIO、cuCIM、cuxfilter、cuVS、cuSpatial、RAFT）
- 基因组平台：DNAnexus、LatchBio
- 显微镜：OMERO
- 自动化：Opentrons
- 资源探测：Get Available Resources

#### 🎓 **研究方法学与规划**（12+ 项技能）

- 创意生成：Scientific Brainstorming、Hypothesis Generation
- 批判分析：Scientific Critical Thinking、Scholar Evaluation
- 情景分析：What-If Oracle（多分支可能性探索、风险分析、战略选项）
- 多视角讨论：Consciousness Council（多元专家视角、唱反调分析）
- 认知画像：DHDNA Profiler（从任意文本中提取思维模式和认知特征）
- 资金申请：Research Grants
- 研究发现：Research Lookup、Paper Lookup（10 个学术数据库）
- 市场分析：Market Research Reports

#### ⚖️ **法规与标准**（1 项技能）

- 医疗器械标准：ISO 13485 Certification

> 📖 **查看全部技能详情**，请参考 [docs/scientific-skills.md](docs/scientific-skills.md)

> 💡 **想看实际示例？** 请查看 [docs/examples.md](docs/examples.md)，其中包含覆盖各科研领域的完整工作流示例。

---

<a id="contributing"></a>

## 🤝 贡献指南

欢迎贡献内容，帮助我们扩展并改进这个科研技能仓库。

### 贡献方式

✨ **新增技能**

- 为更多科研软件包或数据库创建技能
- 为科研平台和工具新增集成

📚 **改进现有技能**

- 用更多示例和用例增强文档
- 增加新的工作流和参考资料
- 改进代码示例和脚本
- 修复 bug 或更新过时信息

🐛 **报告问题**

- 提交带有详细复现步骤的 bug 报告
- 提出改进建议或新功能请求

### 如何贡献

1. **Fork** 这个仓库
2. **创建** 一个功能分支（`git checkout -b feature/amazing-skill`）
3. **遵循** 现有目录结构和文档模式
4. **确保** 所有新技能都包含完整的 `SKILL.md` 文件
5. **充分测试** 你的示例和工作流
6. **提交** 你的更改（`git commit -m 'Add amazing skill'`）
7. **推送** 到你的分支（`git push origin feature/amazing-skill`）
8. **发起** 一份清晰描述改动内容的 Pull Request

### 贡献要求

✅ **遵循 [Agent Skills Specification](https://agentskills.io/specification)** — 每项技能都必须符合官方规范（有效的 `SKILL.md` frontmatter、命名约定和目录结构）  
✅ 与现有技能文档格式保持一致  
✅ 确保所有代码示例都经过测试且能正常工作  
✅ 在示例和工作流中遵循科研最佳实践  
✅ 新增能力时同步更新相关文档  
✅ 在代码中提供清晰的注释和 docstring  
✅ 附上官方文档引用

### 安全扫描

本仓库中的所有技能都使用 [Cisco AI Defense Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner) 做安全扫描。这是一个开源工具，可检测 Agent Skills 中的提示词注入、数据外泄和恶意代码模式。

如果你正在贡献新技能，我们建议在提交 Pull Request 前先在本地运行扫描器：

```bash
uv pip install cisco-ai-skill-scanner
skill-scanner scan /path/to/your/skill --use-behavioral
```

> **注意：** 扫描结果干净有助于减少评审噪音，但不代表该技能绝对不存在风险。所有贡献的技能在合并前也会经过人工审查。

### 致谢与认可

贡献者会在社区中得到认可，并有机会出现在：

- 仓库贡献者列表
- 发行说明中的特别鸣谢
- K-Dense 社区精选内容

你的贡献将帮助科研计算变得更易获得，也能让研究人员更高效地利用 AI 工具。

### 支持开源

本项目建立在 50+ 个优秀开源项目之上。如果你觉得这些技能有价值，欢迎考虑[支持我们所依赖的项目](docs/open-source-sponsors.md)。

---

<a id="troubleshooting"></a>

## 🔧 故障排查

### 常见问题

**问题：技能没有加载**

- 确认技能文件夹位于正确目录中（见[快速开始](#getting-started)）
- 每个技能文件夹都必须包含 `SKILL.md`
- 复制技能后，重启你的代理或 IDE
- 在 Cursor 中，检查 Settings → Rules，确认技能已被发现

**问题：缺少 Python 依赖**

- 解决方案：查看对应 `SKILL.md` 中列出的所需软件包
- 安装依赖：`uv pip install package-name`

**问题：API 限流**

- 解决方案：许多数据库都有速率限制，请查看对应数据库文档
- 可考虑实现缓存或批量请求

**问题：认证错误**

- 解决方案：某些服务需要 API key，请查看 `SKILL.md` 中的认证设置
- 确认你的凭据和权限配置正确

**问题：示例过时**

- 解决方案：通过 GitHub Issues 报告问题
- 同时查看官方软件包文档，确认最新语法

---

<a id="faq"></a>

## ❓ 常见问题

### 通用问题

**问：这是免费的吗？**  
答：是的。本仓库采用 MIT 许可证。不过，每个单独技能都有自己的许可证，并写在对应 `SKILL.md` 文件中的 `license` 元数据字段里，请务必查看并遵守相关条款。

**问：为什么所有技能都放在一起，而不是拆成独立包？**  
答：我们认为，在 AI 时代，优秀科研天然是跨学科的。把所有技能打包在一起，可以让你和你的代理轻松跨领域协作，例如在同一条工作流里整合基因组学、化学信息学、临床数据和机器学习，而不必操心分别安装或手动串联单项技能。

**问：我可以把它用于商业项目吗？**  
答：仓库本身采用 MIT 许可证，因此允许商业使用。不过，单个技能可能有不同许可证，请检查每个技能 `SKILL.md` 文件里的 `license` 字段，确认符合你的预期用途。

**问：所有技能都使用同一个许可证吗？**  
答：不是。每个技能都有自己的许可证，写在对应 `SKILL.md` 中的 `license` 元数据字段里。这些许可证可能与仓库的 MIT License 不同。用户有责任审查并遵守自己所使用技能的许可证条款。

**问：更新频率如何？**  
答：我们会定期更新技能，以反映最新的软件包和 API 版本。重大更新会在 release notes 中公布。

**问：它能和其他 AI 模型一起使用吗？**  
答：这些技能遵循开放的 [Agent Skills](https://agentskills.io/) 标准，可与任何兼容代理配合使用，包括 Cursor、Claude Code 和 Codex。

### 安装与配置

**问：我需要安装所有 Python 包吗？**  
答：不需要。只安装你需要的即可。每项技能都会在其 `SKILL.md` 文件中说明自己的依赖要求。

**问：如果某个技能不能工作怎么办？**  
答：先查看[故障排查](#troubleshooting)部分。如果问题仍存在，请在 GitHub 上提交 issue，并附上详细复现步骤。

**问：这些技能可以离线工作吗？**  
答：数据库类技能需要联网访问 API。Python 包类技能在安装完依赖后可以离线工作。

### 贡献相关

**问：我可以贡献自己的技能吗？**  
答：当然可以。我们非常欢迎贡献。请查看[贡献指南](#contributing)部分了解要求和最佳实践。

**问：如何报告 bug 或提出功能建议？**  
答：请在 GitHub 上提交 issue，并清晰描述问题。对于 bug，请附上复现步骤以及期望行为和实际行为。

---

<a id="support"></a>

## 💬 支持

如果你需要帮助，可以通过以下方式获取支持：

- 📖 **文档**：查看相关 `SKILL.md` 和 `references/` 文件夹
- 🐛 **Bug 报告**：[提交 issue](https://github.com/K-Dense-AI/scientific-agent-skills/issues)
- 💡 **功能请求**：[提交功能请求](https://github.com/K-Dense-AI/scientific-agent-skills/issues/new)
- 💼 **企业支持**：联系 [K-Dense](https://k-dense.ai/) 获取商业支持
- 🌐 **社区**：[加入我们的 Slack](https://join.slack.com/t/k-densecommunity/shared_invite/zt-3iajtyls1-EwmkwIZk0g_o74311Tkf5g)

---

<a id="join-our-community"></a>

## 🎉 加入我们的社区

**我们很期待你加入！** 🚀

欢迎与其他正在用 AI 代理做科研计算的科学家、研究人员和 AI 爱好者建立联系。你可以分享发现、提出问题、获得项目帮助，并与社区成员一起协作。

🌟 **[加入我们的 Slack 社区](https://join.slack.com/t/k-densecommunity/shared_invite/zt-3iajtyls1-EwmkwIZk0g_o74311Tkf5g)** 🌟

无论你是刚开始使用，还是已经是重度用户，社区都会为你提供支持。我们会分享技巧、一起排查问题、展示有趣项目，并讨论 AI 驱动科研的最新进展。

**社区见！** 💬

---

<a id="citation"></a>

## 📖 引用方式

如果你在研究或项目中使用了 Scientific Agent Skills，请按以下方式引用：

### BibTeX

```bibtex
@software{scientific_agent_skills_2026,
  author = {{K-Dense Inc.}},
  title = {Scientific Agent Skills: A Comprehensive Collection of Scientific Tools for AI Agents},
  year = {2026},
  url = {https://github.com/K-Dense-AI/scientific-agent-skills},
  note = {133 skills covering databases, packages, integrations, and analysis tools}
}
```

### APA

```
K-Dense Inc. (2026). Scientific Agent Skills: A comprehensive collection of scientific tools for AI agents [Computer software]. https://github.com/K-Dense-AI/scientific-agent-skills
```

### MLA

```
K-Dense Inc. Scientific Agent Skills: A Comprehensive Collection of Scientific Tools for AI Agents. 2026, github.com/K-Dense-AI/scientific-agent-skills.
```

### Plain Text

```
Scientific Agent Skills by K-Dense Inc. (2026)
Available at: https://github.com/K-Dense-AI/scientific-agent-skills
```

如果这些技能为你的论文、演示或项目提供了帮助，我们将非常感谢你的引用与致谢。

---

<a id="license"></a>

## 📄 许可证

本项目采用 **MIT License** 许可。

**Copyright © 2026 K-Dense Inc.** ([k-dense.ai](https://k-dense.ai/))

### 关键点

- ✅ **可免费用于任何用途**（商业和非商业）
- ✅ **开源** - 你可以自由修改、分发和使用
- ✅ **宽松许可** - 对复用限制很少
- ⚠️ **不提供担保** - 按“现状”提供，不附带任何形式的保证

完整条款请参见 [LICENSE.md](LICENSE.md)。

### 各技能的许可证

> ⚠️ **重要：** 每项技能都有自己的许可证，并写在对应 `SKILL.md` 文件中的 `license` 元数据字段里。这些许可证可能不同于仓库的 MIT License，也可能附带额外条款或限制。**用户有责任自行审查并遵守自己所使用技能的许可证条款。**

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=K-Dense-AI/scientific-agent-skills&type=date&legend=top-left)](https://www.star-history.com/#K-Dense-AI/scientific-agent-skills&type=date&legend=top-left)
