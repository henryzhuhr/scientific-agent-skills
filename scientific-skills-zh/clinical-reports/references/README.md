# 临床报告技能

## 概述

撰写临床报告的综合技能，包括病例报告、诊断报告、临床试验报告和患者文件。提供模板、法规遵从性和验证工具的全面支持。

## 包含内容

### 📋 四种主要报告类型

1. **临床病例报告** - 医学期刊出版物 
2 的符合 CARE 的病例报告。 **诊断报告** - 放射学 (ACR)、病理学 (CAP)和实验室报告
3. **临床试验报告** - SAE 报告、临床研究报告 (ICH-E3)、DSMB 报告
4. **患者文档** - SOAP 注释、H&P、出院摘要、咨询注释

### 📚 参考文件（8 个综合指南）

- `case_report_guidelines.md` - CARE 指南、去标识化、期刊要求
- `diagnostic_reports_standards.md` - ACR、CAP、CLSI 标准、结构化报告系统
- `clinical_trial_reporting.md` - ICH-E3、CONSORT、SAE 报告、MedDRA 编码
- `patient_documentation.md` - SOAP 注释、H&P、出院摘要标准
- `regulatory_compliance.md` - HIPAA、21 CFR 第 11 部分、ICH-GCP、FDA法规
- `medical_terminology.md` - SNOMED-CT、LOINC、ICD-10、CPT 代码
- `data_presentation.md` - 临床表格、图形、Kaplan-Meier 曲线
- `peer_review_standards.md` - 临床手稿审查标准

### 📄 模板 (12专业模板）

- `case_report_template.md` - 遵循 CARE 指南的结构化病例报告
- `soap_note_template.md` - SOAP 进度说明格式
- `history_physical_template.md` - 完整的 H&P 检查模板
- `discharge_summary_template.md` - 出院文件
- `consult_note_template.md` - 专家咨询格式
- `radiology_report_template.md` - 具有结构化报告的影像报告
- `pathology_report_template.md` - 具有CAP概要要素的外科病理学
- `lab_report_template.md` - 临床实验室测试结果
- `clinical_trial_sae_template.md` - 严重不良事件报告表
- `clinical_trial_csr_template.md` - 临床研究报告大纲 (ICH-E3)
- `quality_checklist.md` - 所有报告类型的质量保证
- `hipaa_compliance_checklist.md` - 隐私和去身份验证

### 🔧 验证脚本（8 个自动化工具）

- `validate_case_report.py` - 检查 CARE 指南合规性和完整性
- `check_deidentification.py` - 扫描报告中的 18 个 HIPAA 标识符
- `validate_trial_report.py` - 验证 ICH-E3 结构和所需元素
- `format_adverse_events.py` - 从 CSV 生成 AE 汇总表数据
- `generate_report_template.py` - 交互式模板选择和生成
- `extract_clinical_data.py` - 解析和提取结构化临床数据
- `compliance_checker.py` - 验证法规遵从性要求
- `terminology_validator.py` - 验证医学术语和禁止缩写

## 快速入门

### 生成模板

```bash
cd .claude/skills/clinical-reports/scripts
python generate_report_template.py

# Or specify type directly
python generate_report_template.py --type case_report --output my_case_report.md
```

### 验证案例报告

```bash
python validate_case_report.py my_case_report.md
```

### 检查去识别化

```bash
python check_deidentification.py my_case_report.md
```

### 验证临床试验报告

```bash
python validate_trial_report.py my_csr.md
```

## 主要功能

### CARE 指南合规性
- 完整的CARE 检查清单覆盖
- 去识别化验证
- 知情同意文件
- 时间线创建协助
- 文献综述集成

### 监管合规性
- **HIPAA** - 隐私保护、18 标识符删除、安全港方法
- **FDA** - 21 CFR 第 11、50、56、312 部分合规性
- **ICH-GCP** - 良好临床实践标准
- **ALCOA-CCEA** - 数据完整性原则

### 专业标准
- **ACR** - 美国放射学会报告标准
- **CAP** - 美国病理学家学会概要报告
- **CLSI** - 临床实验室标准研究所
- **CONSORT** - 临床试验报告
- **ICH-E3** - 临床研究报告结构

### 医疗编码系统
- **ICD-10-CM** - 诊断编码
- **CPT** - 程序编码
- **SNOMED-CT** - 临床术语
- **LOINC** - 实验室观察代码
- **MedDRA** - 监管医学词典活动

## 常见用例

### 1. 发布临床病例报告

```
> Create a clinical case report for a 65-year-old patient with atypical 
  presentation of acute appendicitis

> Check this case report for HIPAA compliance
> Validate against CARE guidelines
```

### 2. 撰写诊断报告

```
> Generate a radiology report template for chest CT
> Create a pathology report for colon resection specimen with adenocarcinoma
> Write a laboratory report for complete blood count
```

### 3. 临床试验文档

```
> Write a serious adverse event report for hospitalization due to pneumonia
> Create a clinical study report outline for phase 3 diabetes trial
> Generate adverse events summary table from trial data
```

### 4. 患者临床记录

```
> Create a SOAP note for follow-up visit
> Generate an H&P for patient admitted with chest pain
> Write a discharge summary for heart failure hospitalization
> Create a cardiology consultation note
```

## 工作流程示例

### 病例报告工作流程

1. **获得患者
2的知情同意**。 **生成模板**：`python generate_report_template.py --type case_report`
3. **按照 CARE 结构 
4 撰写病例报告**。 **验证合规性**：`python validate_case_report.py case_report.md`
5. **检查去识别化**：`python check_deidentification.py case_report.md`
6. **提交至期刊**，附上 CARE 检查表 

### 临床试验 SAE 工作流程 

1. **生成SAE模板**：`python generate_report_template.py --type sae`
2. **在事件发生后 24 小时内填写 SAE 表格**
3. **使用 WHO-UMC 或 Naranjo 标准 
4 评估因果关系**。 **验证完整性**：`python validate_trial_report.py sae_report.md`
5. **在监管期限内（7 或 15 天）
6 提交给申办者**。 **根据机构政策通知 IRB**

## 最佳实践

### 隐私和道德
✓ 始终获得病例报告的知情同意书 
✓ 在发布前删除所有 18 个 HIPAA 标识符 
✓ 使用去识别验证脚本 
✓ 在手稿中记录同意书 
✓ 考虑罕见情况的重新识别风险 

### 临床质量
✓ 使用专业医学术语
✓ 遵循结构化报告模板 
✓ 包括所有必需元素 
✓ 清晰记录时间顺序 
✓ 用证据支持诊断 

### 法规遵从性
✓ 满足 SAE 报告时间表（7 天、15 天） 
✓ 遵循 CSR 的 ICH-E3 结构
✓ 保持 ALCOA-CCEA 数据完整性 
✓ 记录方案遵守情况 
✓ 对不良事件使用 MedDRA 编码 

### 文档标准
✓ 在所有临床记录上签名并注明日期 
✓ 记录医疗必要性 
✓ 仅使用标准缩写
✓ 避免禁用缩写（JCAHO“请勿使用”列表） 
✓ 保持易读性和完整性 

## 集成 

clinical-reports 技能与以下内容无缝集成：

- **scientific-writing** - 清晰、专业的医学写作
- **peer-review** - 用于病例报告的质量评估
- **citation-management** - 用于病例报告中的文献参考
- **research-grants** - 用于临床试验方案制定

## 资源

### 外部标准
- CARE 指南： https://www.care-statement.org/
- ICH-E3 指南：https://database.ich.org/sites/default/files/E3_Guideline.pdf
- CONSORT 声明：http://www.consort-statement.org/
- HIPAA：https://www.hhs.gov/hipaa/
- ACR 实践参数：https://www.acr.org/Clinical-Resources/Practice-Parameters-and-Technical-Standards
- CAP 癌症方案：https://www.cap.org/protocols-and-guidelines

### 专业组织
- 美国医学会 (AMA) 
- 美国放射学会 (ACR) 
- 美国病理学家学会 (CAP) 
- 临床实验室标准协会 (CLSI) 
- 国际协调委员会 (ICH) 

## 支持 

有关clinical-reports技能：
1. 查看综合参考文件
2. 查看示例 
3 的模板。运行验证脚本来识别问题
4. 请参阅 SKILL.md 了解详细指导

## 许可证

Claude Scientific Writer 项目的一部分。请参阅主许可证文件.
