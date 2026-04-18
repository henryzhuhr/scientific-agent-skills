# 临床决策支持技能

为制药和临床研究环境中的医疗专业人员提供专业临床决策支持文档。

## 快速入门

此技能可以生成三种类型的临床文档：

1. **个体患者治疗计划** - 针对特定患者的个性化方案
2. **患者队列分析** - 生物标志物分层组分析，结果为 
3. **治疗建议报告** - 基于证据的临床指南

所有文档均生成为紧凑、专业的 LaTeX/PDF 文件。

## 目录结构

```
clinical-decision-support/
├── SKILL.md                     # Main skill definition
├── README.md                    # This file
│
├── references/                  # Clinical guidance documents
│   ├── patient_cohort_analysis.md
│   ├── treatment_recommendations.md
│   ├── clinical_decision_algorithms.md
│   ├── biomarker_classification.md
│   ├── outcome_analysis.md
│   └── evidence_synthesis.md
│
├── assets/                      # Templates and examples
│   ├── cohort_analysis_template.tex
│   ├── treatment_recommendation_template.tex
│   ├── clinical_pathway_template.tex
│   ├── biomarker_report_template.tex
│   ├── example_gbm_cohort.md
│   ├── recommendation_strength_guide.md
│   └── color_schemes.tex
│
└── scripts/                     # Analysis and generation tools
    ├── generate_survival_analysis.py
    ├── create_cohort_tables.py
    ├── build_decision_tree.py
    ├── biomarker_classifier.py
    └── validate_cds_document.py
```

## 示例用例

### 创建患者队列分析
```
> Analyze a cohort of 45 NSCLC patients stratified by PD-L1 expression 
  (<1%, 1-49%, ≥50%) including ORR, PFS, and OS outcomes
```

### 生成治疗建议
```
> Create evidence-based treatment recommendations for HER2-positive 
  metastatic breast cancer with GRADE methodology
```

### 构建临床路径
```
> Generate a clinical decision algorithm for acute chest pain 
  management with TIMI risk score
```

## 主要特点

- **GRADE 方法**：证据质量分级（高/中/低/极低）
- **推荐强度**：强（1 级）与条件（2 级）
- **生物标志物整合**：基因组、表达和分子亚型分类
- **统计分析**：Kaplan-Meier、Cox 回归、对数秩检验
- **指南索引**：NCCN、ASCO、ESMO、AHA/ACC 集成
- **专业输出**：0.5 英寸页边距、颜色编码框、可发布

## 依赖项

Python 脚本需要：
- `pandas`、`numpy`、 `scipy`：数据分析和统计
- `lifelines`：生存分析（Kaplan-Meier、Cox回归）
- `matplotlib`：可视化
- `pyyaml`（可选）：决策树的YAML输入

安装其中：
```bash
pip install pandas numpy scipy lifelines matplotlib pyyaml
```

## 包含参考文献

1. **患者队列分析**：分层方法、生物标志物相关性、统计比较
2. **治疗建议**：证据分级、治疗顺序、特殊人群
3. **临床决策算法**：风险评分、决策树、TikZ 流程图
4. **生物标志物分类**：基因组改变、分子亚型、伴随诊断
5. **结果分析**：生存方法、反应标准 (RECIST)、效应大小
6. **证据综合**：指南整合、系统评价、荟萃分析

## 提供的模板

1. **群组分析**：人口统计表、生物标志物概况、结果、统计数据、建议
2. **治疗建议**：证据审查、GRADE分级选项、监测、决策算法
3. **临床路径**：带有风险分层和紧急编码行动的 TikZ 流程图
4. **生物标志物报告**：具有基于层级的可操作性和治疗匹配的基因组分析

## 包含脚本

1. **`generate_survival_analysis.py`**：创建风险比为 
2 的 Kaplan-Meier 曲线。 **`create_cohort_tables.py`**：生成基线、功效和安全表
3. **`build_decision_tree.py`**：将文本/JSON转换为TikZ流程图
4. **`biomarker_classifier.py`**：按 PD-L1、HER2、分子亚型 
5 对患者进行分层。 **`validate_cds_document.py`**：完整性和合规性质量检查

## 集成

与现有技能集成：
- **scientific-writing**：引文管理、统计报告
- **clinical-reports**：医学术语、HIPAA 合规性
- **scientific-schematics**：TikZ 流程图

## 版本

版本 1.0 - 初始版本
创建时间：2024 年 11 月
最后更新时间：2024 年 11 月 5 日

## 问题或反馈

该技能专为创建临床决策支持文档的制药和临床研究专业人员而设计。有关使用问题或改进建议，请联系 Scientific Writer 开发团队。
