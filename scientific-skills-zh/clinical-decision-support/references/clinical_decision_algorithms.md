# 临床决策算法指南

## 概述

临床决策算法为诊断、治疗选择和患者管理提供系统、分步的指导。本指南涵盖使用决策树和流程图的算法开发、验证和可视化演示。

## 算法设计原则

### 关键组件

* *决策节点**
- **问题/标准**：清晰、可测量的临床参数
- **二元与多路**：是/否（简单）与多个选项（复杂）
- **客观**：实验室值、影像学表现与主观：临床判断

* *作用节点**
- **治疗**：具体剂量干预
- **测试**：附加诊断程序
- **转诊**：专家咨询，更高水平的护理
- **观察**：观察等待并定义后续

* *终端节点**
- **结果**：最终决策点
- **后续**：重新评估时间表
- **退出标准**：何时退出算法

### 设计标准

* *清晰度**
- 明确的决策点
- 相互排斥的途径
- 无循环（除非有意的重新评估循环）
- 清晰的进入和退出点

* *临床有效性**
- 基于证据的决策标准
- 经过验证的生物标志物切点
- 与指南一致的建议
- 证据有限的专家共识

* *可用性**
- 每个路径最多7个决策点（认知负荷）
- 视觉层次结构（最常见的路径）突出显示）
- 首选可打印单页格式
- 紧急/安全的颜色编码

* *完整性**
- 涵盖所有可能的场景
- 边缘情况的默认路径
- 针对异常演示的安全网规定
- 明确升级标准所述

## 临床决策树

### 诊断算法

* *胸痛评估算法**

```
Entry: Patient with chest pain

├─ STEMI Criteria? (ST elevation ≥1mm in ≥2 contiguous leads)
│  ├─ YES → Activate cath lab, aspirin 325mg, heparin, clopidogrel 600mg
│  │        Transfer for primary PCI (goal door-to-balloon <90 minutes)
│  └─ NO → Continue evaluation

├─ High-Risk Features? (Hemodynamic instability, arrhythmia, troponin elevation)
│  ├─ YES → Admit CCU, serial troponins, cardiology consultation
│  │        Consider early angiography if NSTEMI
│  └─ NO → Calculate TIMI or HEART score

├─ TIMI Score 0-1 or HEART Score 0-3? (Low risk)
│  ├─ YES → Observe 6-12 hours, serial troponins, stress test if negative
│  │        Discharge if all negative with cardiology follow-up in 72 hours
│  └─ NO → TIMI 2-4 or HEART 4-6 (Intermediate risk)

├─ TIMI Score 2-4 or HEART Score 4-6? (Intermediate risk)
│  ├─ YES → Admit telemetry, serial troponins, stress imaging vs CT angiography
│  │        Medical management: Aspirin, statin, beta-blocker
│  └─ NO → TIMI ≥5 or HEART ≥7 (High risk) → Treat as NSTEMI

Decision Endpoint: Risk-stratified pathway with 30-day event rate documented
```

* *肺栓塞诊断算法（Wells 标准）**

```
Entry: Suspected PE

Step 1: Calculate Wells Score
  Clinical features points:
  - Clinical signs of DVT: 3 points
  - PE more likely than alternative diagnosis: 3 points  
  - Heart rate >100: 1.5 points
  - Immobilization/surgery in past 4 weeks: 1.5 points
  - Previous PE/DVT: 1.5 points
  - Hemoptysis: 1 point
  - Malignancy: 1 point

Step 2: Risk Stratify
  ├─ Wells Score ≤4 (PE unlikely)
  │  └─ D-dimer test
  │     ├─ D-dimer negative (<500 ng/mL) → PE excluded, consider alternative diagnosis
  │     └─ D-dimer positive (≥500 ng/mL) → CTPA
  │
  └─ Wells Score >4 (PE likely)
     └─ CTPA (skip D-dimer)

Step 3: CTPA Results
  ├─ Positive for PE → Risk stratify severity
  │  ├─ Massive PE (hypotension, shock) → Thrombolytics vs embolectomy
  │  ├─ Submassive PE (RV strain, troponin+) → Admit ICU, consider thrombolytics
  │  └─ Low-risk PE → Anticoagulation, consider outpatient management
  │
  └─ Negative for PE → PE excluded, investigate alternative diagnosis

Step 4: Treatment Decision (if PE confirmed)
  ├─ Absolute contraindication to anticoagulation?
  │  ├─ YES → IVC filter placement, treat underlying condition
  │  └─ NO → Anticoagulation therapy
  │
  ├─ Cancer-associated thrombosis?
  │  ├─ YES → LMWH preferred (edoxaban alternative)
  │  └─ NO → DOAC preferred (apixaban, rivaroxaban, edoxaban)
  │
  └─ Duration: Minimum 3 months, extended if unprovoked or recurrent
```

### 治疗选择算法

* *NSCLC 一线治疗算法**

```
Entry: Advanced/Metastatic NSCLC, adequate PS (ECOG 0-2)

Step 1: Biomarker Testing Complete?
  ├─ NO → Reflex testing: EGFR, ALK, ROS1, BRAF, PD-L1, consider NGS
  │       Hold systemic therapy pending results (unless rapidly progressive)
  └─ YES → Proceed to Step 2

Step 2: Actionable Genomic Alteration?
  ├─ EGFR exon 19 deletion or L858R → Osimertinib 80mg daily
  │  └─ Alternative: Erlotinib, gefitinib, afatinib (less preferred)
  │
  ├─ ALK rearrangement → Alectinib 600mg BID
  │  └─ Alternatives: Brigatinib, lorlatinib, crizotinib (less preferred)
  │
  ├─ ROS1 rearrangement → Crizotinib 250mg BID or entrectinib
  │
  ├─ BRAF V600E → Dabrafenib + trametinib
  │
  ├─ MET exon 14 skipping → Capmatinib or tepotinib
  │
  ├─ RET rearrangement → Selpercatinib or pralsetinib
  │
  ├─ NTRK fusion → Larotrectinib or entrectinib
  │
  ├─ KRAS G12C → Sotorasib or adagrasib (if no other options)
  │
  └─ NO actionable alteration → Proceed to Step 3

Step 3: PD-L1 Testing Result?
  ├─ PD-L1 ≥50% (TPS)
  │  ├─ Option 1: Pembrolizumab 200mg Q3W (monotherapy, NCCN Category 1)
  │  ├─ Option 2: Pembrolizumab + platinum doublet chemotherapy
  │  └─ Option 3: Atezolizumab + bevacizumab + carboplatin + paclitaxel
  │
  ├─ PD-L1 1-49% (TPS)
  │  ├─ Preferred: Pembrolizumab + platinum doublet chemotherapy
  │  └─ Alternative: Platinum doublet chemotherapy alone
  │
  └─ PD-L1 <1% (TPS)
     ├─ Preferred: Pembrolizumab + platinum doublet chemotherapy
     └─ Alternative: Platinum doublet chemotherapy ± bevacizumab

Step 4: Platinum Doublet Selection (if applicable)
  ├─ Squamous histology
  │  └─ Carboplatin AUC 6 + paclitaxel 200 mg/m² Q3W (4 cycles)
  │      or Carboplatin AUC 5 + nab-paclitaxel 100 mg/m² D1,8,15 Q4W
  │
  └─ Non-squamous histology  
     └─ Carboplatin AUC 6 + pemetrexed 500 mg/m² Q3W (4 cycles)
         Continue pemetrexed maintenance if responding
         Add bevacizumab 15 mg/kg if eligible (no hemoptysis, brain mets)

Step 5: Monitoring and Response Assessment
  - Imaging every 6 weeks for first 12 weeks, then every 9 weeks
  - Continue until progression or unacceptable toxicity
  - At progression, proceed to second-line algorithm
```

* *心力衰竭管理算法（AHA/ACC 指南）**

```
Entry: Heart Failure Diagnosis Confirmed

Step 1: Determine HF Type
  ├─ HFrEF (EF ≤40%)
  │  └─ Proceed to Guideline-Directed Medical Therapy (GDMT)
  │
  ├─ HFpEF (EF ≥50%)
  │  └─ Treat comorbidities, diuretics for congestion, consider SGLT2i
  │
  └─ HFmrEF (EF 41-49%)
     └─ Consider HFrEF GDMT, evidence less robust

Step 2: GDMT for HFrEF (All patients unless contraindicated)

Quadruple Therapy (Class 1 recommendations):

1. ACE Inhibitor/ARB/ARNI
   ├─ Preferred: Sacubitril-valsartan 49/51mg BID → titrate to 97/103mg BID
   │  └─ If ACE-I naïve or taking <10mg enalapril equivalent
   ├─ Alternative: ACE-I (enalapril, lisinopril, ramipril) to target dose
   └─ Alternative: ARB (losartan, valsartan) if ACE-I intolerant

2. Beta-Blocker (start low, titrate slowly)
   ├─ Bisoprolol 1.25mg daily → 10mg daily target
   ├─ Metoprolol succinate 12.5mg daily → 200mg daily target
   └─ Carvedilol 3.125mg BID → 25mg BID target (50mg BID if >85kg)

3. Mineralocorticoid Receptor Antagonist (MRA)
   ├─ Spironolactone 12.5-25mg daily → 50mg daily target
   └─ Eplerenone 25mg daily → 50mg daily target
   └─ Contraindications: K >5.0, CrCl <30 mL/min

4. SGLT2 Inhibitor (regardless of diabetes status)
   ├─ Dapagliflozin 10mg daily
   └─ Empagliflozin 10mg daily

Step 3: Additional Therapies Based on Phenotype

├─ Sinus rhythm + HR ≥70 despite beta-blocker?
│  └─ YES: Add ivabradine 5mg BID → 7.5mg BID target
│
├─ African American + NYHA III-IV?
│  └─ YES: Add hydralazine 37.5mg TID + isosorbide dinitrate 20mg TID
│           (Target: hydralazine 75mg TID + ISDN 40mg TID)
│
├─ Atrial fibrillation?
│  ├─ Rate control (target <80 bpm at rest, <110 bpm with activity)
│  └─ Anticoagulation (DOAC preferred, warfarin if valvular)
│
└─ Iron deficiency (ferritin <100 or <300 with TSAT <20%)?
   └─ YES: IV iron supplementation (ferric carboxymaltose)

Step 4: Device Therapy Evaluation

├─ EF ≤35%, NYHA II-III, LBBB with QRS ≥150 ms, sinus rhythm?
│  └─ YES: Cardiac resynchronization therapy (CRT-D)
│
├─ EF ≤35%, NYHA II-III, on GDMT ≥3 months?
│  └─ YES: ICD for primary prevention
│           (if life expectancy >1 year with good functional status)
│
└─ EF ≤35%, NYHA IV despite GDMT, or advanced HF?
   └─ Refer to advanced HF specialist
      ├─ LVAD evaluation
      ├─ Heart transplant evaluation
      └─ Palliative care consultation

Step 5: Monitoring and Titration

Weekly to biweekly visits during titration:
- Blood pressure (target SBP ≥90 mmHg)
- Heart rate (target 50-60 bpm)
- Potassium (target 4.0-5.0 mEq/L, hold MRA if >5.5)
- Creatinine (expect 10-20% increase, acceptable if <30% and stable)
- Symptoms and congestion status (daily weights, NYHA class)

Stable on GDMT:
- Visits every 3-6 months
- Echocardiogram at 3-6 months after GDMT optimization, then annually
- NT-proBNP or BNP trending (biomarker-guided therapy investigational)
```

## 风险分层工具

### 心血管风险评分

* *TIMI 风险评分（NSTEMI/不稳定）心绞痛）**

```
Score Calculation (0-7 points):
☐ Age ≥65 years (1 point)
☐ ≥3 cardiac risk factors (HTN, hyperlipidemia, diabetes, smoking, family history) (1)
☐ Known CAD (stenosis ≥50%) (1)
☐ ASA use in past 7 days (1)
☐ Severe angina (≥2 episodes in 24 hours) (1)
☐ ST deviation ≥0.5 mm (1)
☐ Elevated cardiac biomarkers (1)

Risk Stratification:
├─ Score 0-1: 5% risk of death/MI/urgent revasc at 14 days (Low)
│  └─ Management: Observation, stress test, outpatient follow-up
│
├─ Score 2: 8% risk (Low-intermediate)
│  └─ Management: Admission, medical therapy, stress imaging
│
├─ Score 3-4: 13-20% risk (Intermediate-high)
│  └─ Management: Admission, aggressive medical therapy, early invasive strategy
│
└─ Score 5-7: 26-41% risk (High)
   └─ Management: Aggressive treatment, urgent angiography (<24 hours)
```

* *CHA2DS2-VASc 评分（房颤中的中风风险）**

```
Score Calculation:
☐ Congestive heart failure (1 point)
☐ Hypertension (1)
☐ Age ≥75 years (2)
☐ Diabetes mellitus (1)
☐ Prior stroke/TIA/thromboembolism (2)
☐ Vascular disease (MI, PAD, aortic plaque) (1)
☐ Age 65-74 years (1)
☐ Sex category (female) (1)

Maximum score: 9 points

Treatment Algorithm:
├─ Score 0 (male) or 1 (female): 0-1.3% annual stroke risk
│  └─ No anticoagulation or aspirin (Class IIb)
│
├─ Score 1 (male): 1.3% annual stroke risk
│  └─ Consider anticoagulation (Class IIa)
│      Factors: Patient preference, bleeding risk, comorbidities
│
└─ Score ≥2 (male) or ≥3 (female): ≥2.2% annual stroke risk
   └─ Anticoagulation recommended (Class I)
      ├─ Preferred: DOAC (apixaban, rivaroxaban, edoxaban, dabigatran)
      └─ Alternative: Warfarin (INR 2-3) if DOAC contraindicated

Bleeding Risk Assessment (HAS-BLED):
H - Hypertension (SBP >160)
A - Abnormal renal/liver function (1 point each)
S - Stroke history
B - Bleeding history or predisposition
L - Labile INR (if on warfarin)
E - Elderly (age >65)
D - Drugs (antiplatelet, NSAIDs) or alcohol (1 point each)

HAS-BLED ≥3: High bleeding risk → Modifiable factors, consider DOAC over warfarin
```

### 肿瘤学风险计算器

* *MELD 评分（肝细胞癌）资格）**

```
MELD = 3.78×ln(bilirubin mg/dL) + 11.2×ln(INR) + 9.57×ln(creatinine mg/dL) + 6.43

Interpretation:
├─ MELD <10: 1.9% 3-month mortality (Low)
│  └─ Consider resection or ablation for HCC
│
├─ MELD 10-19: 6-20% 3-month mortality (Moderate)
│  └─ Transplant evaluation if within Milan criteria
│      Milan: Single ≤5cm or ≤3 lesions each ≤3cm, no vascular invasion
│
├─ MELD 20-29: 20-45% 3-month mortality (High)
│  └─ Urgent transplant evaluation, bridge therapy (TACE, ablation)
│
└─ MELD ≥30: 50-70% 3-month mortality (Very high)
   └─ Transplant vs palliative care discussion
      Too ill for transplant if MELD >35-40 typically
```

* *辅助！在线（乳腺癌复发风险）**

```
Input Variables:
- Age at diagnosis
- Tumor size
- Tumor grade (1-3)
- ER status
- Node status (0, 1-3, 4-9, ≥10)
- HER2 status
- Comorbidity index

Output: 10-year risk of:
- Recurrence
- Breast cancer mortality
- Overall mortality

Treatment Benefit Estimates:
- Chemotherapy: Absolute reduction in recurrence
- Endocrine therapy: Absolute reduction in recurrence
- Trastuzumab: Absolute reduction (if HER2+)

Clinical Application:
├─ Low risk (<10% recurrence): Consider endocrine therapy alone if ER+
├─ Intermediate risk (10-20%): Chemotherapy discussion, genomic assay
│  └─ Oncotype DX score <26: Endocrine therapy alone
│  └─ Oncotype DX score ≥26: Chemotherapy + endocrine therapy
└─ High risk (>20%): Chemotherapy + endocrine therapy if ER+
```

## TikZ 流程图最佳实践

### 视觉设计原则

* *节点样式**
```latex
% Decision nodes (diamond)
\tikzstyle{decision} = [diamond, draw, fill=yellow!20, text width=4.5em, text centered, inner sep=0pt]

% Process nodes (rectangle)
\tikzstyle{process} = [rectangle, draw, fill=blue!20, text width=5em, text centered, rounded corners, minimum height=3em]

% Terminal nodes (rounded rectangle)
\tikzstyle{terminal} = [rectangle, draw, fill=green!20, text width=5em, text centered, rounded corners=1em, minimum height=3em]

% Input/Output (parallelogram)
\tikzstyle{io} = [trapezium, draw, fill=purple!20, text width=5em, text centered, minimum height=3em]
```

* *颜色编码紧急**
- **红色**：危及生命，需要立即采取行动
- **橙色**：紧急，在数小时内采取行动
- **黄色**：半紧急，在24-48小时内采取行动
- **绿色**：常规，稳定的临床情况
- **蓝色**：信息性，监测仅

* *路径强调**
- 最常见路径的粗体箭头
- 罕见场景的虚线箭头
- 箭头厚度与路径频率成正比
- 突出显示关键决策点周围的框

### LaTeX TikZ模板

```latex
\documentclass{article}
\usepackage{tikz}
\usetikzlibrary{shapes, arrows, positioning}

\begin{document}

\tikzstyle{decision} = [diamond, draw, fill=yellow!20, text width=4em, text centered, inner sep=2pt, font=\small]
\tikzstyle{process} = [rectangle, draw, fill=blue!20, text width=6em, text centered, rounded corners, minimum height=2.5em, font=\small]
\tikzstyle{terminal} = [rectangle, draw, fill=green!20, text width=6em, text centered, rounded corners=8pt, minimum height=2.5em, font=\small]
\tikzstyle{alert} = [rectangle, draw=red, line width=1.5pt, fill=red!10, text width=6em, text centered, rounded corners, minimum height=2.5em, font=\small\bfseries]
\tikzstyle{arrow} = [thick,->,>=stealth]

\begin{tikzpicture}[node distance=2cm, auto]
    % Nodes
    \node [terminal] (start) {Patient presents with symptom X};
    \node [decision, below of=start] (decision1) {Criterion A met?};
    \node [alert, below of=decision1, node distance=2.5cm] (alert1) {Immediate action};
    \node [process, right of=decision1, node distance=4cm] (process1) {Standard evaluation};
    \node [terminal, below of=process1, node distance=2.5cm] (end) {Outcome};
    
    % Arrows
    \draw [arrow] (start) -- (decision1);
    \draw [arrow] (decision1) -- node {Yes} (alert1);
    \draw [arrow] (decision1) -- node {No} (process1);
    \draw [arrow] (process1) -- (end);
    \draw [arrow] (alert1) -| (end);
\end{tikzpicture}

\end{document}
```

## 算法验证

### 开发流程

* *步骤1：文献综述和证据合成**
- 指南的系统回顾（NCCN、ASCO、ESMO、AHA/ACC）
- 临床的荟萃分析试验
- 专家共识声明
- 本地实践模式和资源可用性

* *步骤2：算法草案开发**
- 多学科团队输入（医生、护士、药剂师）
- 定义决策节点和标准
- 指定行动和结果
- 识别不确定性区域

* *步骤 3：试点测试**
- 回顾性应用历史案例 (n=20-50)
- 识别算法未涵盖的场景
- 细化决策标准
- 与最终用户进行可用性测试

* *步骤 4：前瞻性验证**
- 用数据在临床实践中实施集合
- 跟踪遵守率（目标> 80％）
- 监控结果与历史控制
- 用户满意度调查

* *步骤5：持续质量改进**
- 算法性能的季度审查
- 根据新证据进行更新
- 解决偏差和原因不遵守
- 版本控制和变更文档

### 性能指标

* *流程指标**
- 算法遵守率（遵循算法的病例百分比）
- 决策时间（从呈现到治疗开始的中位时间）
- 完成率（达到终点的病例百分比）节点）

* *结果指标**
- 护理的适当性（与指南一致）
- 临床结果（死亡率、发病率、再入院）
- 资源利用率（住院时间、不必要的测试）
- 安全性（不良事件、错误）

* *用户体验指标**
- 易用性（李克特量表调查）
- 使用时间（导航算法的中位时间）
- 感知效用（报告算法有用的用户百分比）
- 使用障碍（定性反馈）

## 实施策略

### 集成临床工作流程

* *电子健康记录集成**
- 关键决策点的临床决策支持 (CDS)警报
- 链接到算法路径的订单集
- 根据 EHR 数据自动填充风险评分
- 遵循算法结构的文档模板

* *护理点工具**
- 用于快速参考的袖珍卡
- 具有交互式算法的移动应用程序
- 临床区域的墙海报
- 链接到完整算法的二维码

* *教育和培训**
- 算法原理的教学演示
- 基于案例的练习
- 模拟场景
- 遵守情况的审核和反馈

### 克服障碍

* *常见障碍**
- 算法复杂性（太多决策）点）
- 缺乏认识（未有效传播）
- 不同意建议（被视为菜谱医学）
- 竞争优先事项（时间压力、多名患者）
- 资源限制（推荐的测试/治疗不可用）

* * 缓解策略**
- 简化算法（每个路径≤7 个决策点首选）
- 冠军网络（当地意见领袖推广算法）
- 根据当地情况进行定制（允许临床判断的灵活性）
- 测量和报告结果（展示价值）
- 提供资源（确保算法推荐选项）可用）

## 算法维护和更新

### 版本控制

* *更改日志文档**
```
Algorithm: NSCLC First-Line Treatment
Version: 3.2
Effective Date: January 1, 2024
Previous Version: 3.1 (effective July 1, 2023)

Changes in Version 3.2:
1. Added KRAS G12C-mutated pathway (sotorasib, adagrasib)
   - Evidence: FDA approval May 2021/2022
   - Guideline: NCCN v4.2023

2. Updated PD-L1 ≥50% recommendation to include pembrolizumab monotherapy as Option 1
   - Evidence: KEYNOTE-024 5-year follow-up
   - Guideline: NCCN Category 1 preferred

3. Removed crizotinib as preferred ALK inhibitor, moved to alternative
   - Evidence: ALEX, CROWN trials showing superiority of alectinib, lorlatinib
   - Guideline: NCCN/ESMO Category 1 for alectinib as first-line

Reviewed by: Thoracic Oncology Committee
Approved by: Dr. [Name], Medical Director
Next Review Date: July 1, 2024
```

### 更新触发

* *强制更新（3个月内）**
- FDA批准算法适应症的新药
- 指南变更（NCCN、ASCO、ESMO 1 类推荐）
- 推荐药物中添加安全警报或黑框警告
- 主要临床试验结果改变护理标准

* *常规更新（每年）**
- 次要证据更新
- 基于优化本地性能数据
- 格式或可用性改进
- 添加遇到的新临床场景

* *紧急更新（1周内）**
- 药物短缺需要替代途径
- 药物召回或安全撤回
- 需要修改协议的疫情或大流行
