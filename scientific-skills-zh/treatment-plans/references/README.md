# 治疗计划技能

## 概述

跨所有临床专业制定**简洁、以临床医生为中心**医疗计划的技能。提供包含 SMART 目标框架、基于证据的干预措施、法规遵从性和验证工具的 LaTeX/PDF 模板，用于以患者为中心的护理计划。

* *默认为 1 页格式**，大多数情况下 - 认为“快速参考卡”而不是“综合教科书”。

## 包含内容

### 📋 七种治疗计划类型

1. **一页治疗计划**（首选）- 适用于大多数临床情况的简洁、快速参考格式
2. **一般医疗计划** - 初级保健、慢性病（糖尿病、高血压、心力衰竭）
3. **康复治疗计划** - 物理治疗、职业治疗、心脏/肺康复
4. **心理健康治疗计划** - 精神科护理、抑郁、焦虑、创伤后应激障碍、物质使用
5. **慢性病管理计划** - 复杂的多发病、长期护理协调
6. **围手术期护理计划** - 术前优化、ERAS 方案、术后恢复
7. **疼痛管理计划** - 急性和慢性疼痛、多模式镇痛、阿片类药物节约策略

### 📚 参考文件（5 个综合指南）

- `treatment_plan_standards.md` - 专业标准、文件要求、法律考虑
- `goal_setting_frameworks.md` - 智能目标、以患者为中心的结果、共享决策
- `intervention_guidelines.md` - 循证治疗、药物和非药物
- `regulatory_compliance.md` - HIPAA 合规性、计费文档、质量措施
- `specialty_specific_guidelines.md` - 每种治疗计划类型的详细指南

### 📄 LaTeX 模板（7个专业模板）

- `one_page_treatment_plan.tex` - **第一选择** - 密集、可扫描的单页格式（如精准肿瘤学报告）
- `general_medical_treatment_plan.tex` - 综合医疗护理规划
- `rehabilitation_treatment_plan.tex` - 功能恢复和治疗
- `mental_health_treatment_plan.tex` - 精神科和行为科health
- `chronic_disease_management_plan.tex` - 长期疾病管理
- `perioperative_care_plan.tex` - 手术和程序护理
- `pain_management_plan.tex` - 多模式疼痛治疗

### 🔧 验证脚本（4 个自动化工具）

- `generate_template.py` - 交互式模板选择和生成
- `validate_treatment_plan.py` - 全面的质量和合规性检查
- `check_completeness.py` - 验证所有必需的部分
- `timeline_generator.py` - 创建视觉治疗时间表和时间表

## 快速入门

### 生成治疗计划模板

```bash
cd .claude/skills/treatment-plans/scripts
python generate_template.py

# Or specify type directly
python generate_template.py --type general_medical --output diabetes_plan.tex
```

可用模板类型：
- `one_page`（首选 - 用于大多数情况）
- `general_medical`
- `rehabilitation`
- `mental_health`
- `chronic_disease`
- `perioperative`
- `pain_management`

### 编译为PDF

```bash
cd /path/to/your/treatment/plan
pdflatex my_treatment_plan.tex
```

### 验证您的治疗计划

```bash
# Check for completeness
python check_completeness.py my_treatment_plan.tex

# Comprehensive validation
python validate_treatment_plan.py my_treatment_plan.tex
```

### 生成治疗时间表

```bash
python timeline_generator.py --plan my_treatment_plan.tex --output timeline.pdf
```

## 标准治疗计划组件

所有模板都包含这些基本内容部分：

### 1. 患者信息（去识别化）
- 人口统计和相关医疗背景
- 活动状况和合并症
- 当前药物和过敏情况
- 功能状态基线
- 符合HIPAA 标准去识别化

### 2.诊断与评估总结
- 初次诊断（ICD-10编码）
- 二次诊断
- 严重程度分类
- 功能限制
- 风险分层

### 3.治疗目标（SMART格式）

* *短期目标**（1-3个月）：
- 具体的、可衡量的结果
- 具有明确时间范围的现实目标
- 以患者为中心的优先事项

* *长期目标**（6-12 个月）：
- 疾病控制目标
- 功能改善目标
- 生活质量提高
- 并发症预防

### 4. 干预措施

- **药理学**：药物剂量、频率、监测
- **非药物**：生活方式改变、行为干预、教育
- **程序**：计划程序、专家转诊、诊断测试

### 5. 时间表和时间表
- 治疗阶段和时间范围
- 预约频率
- 里程碑评估
- 预期治疗持续时间

### 6. 监测参数
- 跟踪的临床结果
- 评估工具和量表
- 监测频率
- 干预阈值

### 7. 预期结果
- 主要结果测量
- 成功标准
- 改善时间表
- 长期预后

### 8. 随访计划
- 预定预约
- 沟通协议
- 紧急程序
- 过渡计划

### 9. 患者教育
- 病情了解
- 自我管理技能
- 警告标志
- 资源和支持

### 10. 风险缓解
- 不良反应管理
- 安全监测
- 紧急行动计划
- 跌倒/感染预防

## 常见用例

### 1. 2 型糖尿病管理

```
Goal: Create comprehensive treatment plan for newly diagnosed diabetes

Template: general_medical_treatment_plan.tex

Key Components:
- SMART goals: HbA1c <7% in 3 months, weight loss 10 lbs in 6 months
- Medications: Metformin titration schedule
- Lifestyle: Diet, exercise, glucose monitoring
- Monitoring: HbA1c every 3 months, quarterly visits
- Education: Diabetes self-management education
```

### 2. 中风后康复

```
Goal: Develop rehab plan for stroke patient with hemiparesis

Template: rehabilitation_treatment_plan.tex

Key Components:
- Functional assessment: FIM scores, ROM, strength testing
- PT goals: Ambulation 150 feet with cane in 12 weeks
- OT goals: Independent ADLs, upper extremity function
- Treatment schedule: PT/OT/SLP 3x week each
- Home exercise program
```

### 3. 重度抑郁症

```
Goal: Create integrated treatment plan for depression

Template: mental_health_treatment_plan.tex

Key Components:
- Assessment: PHQ-9 score 16 (moderate depression)
- Goals: Reduce PHQ-9 to <5, return to work in 12 weeks
- Psychotherapy: CBT weekly sessions
- Medication: SSRI with titration schedule
- Safety planning: Crisis contacts, warning signs
```

### 4. 全膝关节置换

```
Goal: Perioperative care plan for elective TKA

Template: perioperative_care_plan.tex

Key Components:
- Preop optimization: Medical clearance, medication management
- ERAS protocol implementation
- Postop milestones: Ambulation POD 1, discharge POD 2-3
- Pain management: Multimodal analgesia
- Rehab plan: PT starting POD 0
```

### 5. 慢性腰背疼痛

```
Goal: Multimodal pain management plan

Template: pain_management_plan.tex

Key Components:
- Pain assessment: Location, intensity, functional impact
- Goals: Reduce pain 7/10 to 3/10, return to work
- Medications: Non-opioid analgesics, adjuvants
- PT: Core strengthening, McKenzie exercises
- Behavioral: CBT for pain, mindfulness
- Interventional: Consider ESI if inadequate response
```

## SMART目标框架

所有治疗计划均使用SMART标准进行目标设定：

- **具体**：明确、明确的结果（不含糊）
- **可衡量**：可量化的指标或可观察的行为
- **可实现**：现实的给定患者能力和资源
- **相关**：与患者优先事项和价值观保持一致
- **有时限**：特定的时间范围成就

### 示例

* *良好的 SMART 目标**：
- 在 3 个月内将 HbA1c 从 8.5% 降低至 <7%
- 在 8 周内使用辅助装置独立行走 150 英尺
- 在 8 天内将 PHQ-9 抑郁评分从 18 降低至 <10周
- 术后第14天实现膝关节屈曲>90度
- 在6周内将疼痛从7/10减少到≤4/10

* *差目标**（非SMART）：
- “感觉更好”（不具体或可测量）
- “改善糖尿病”（不具体或有时间限制）
- “变得更强”（不可测量）
- “恢复正常”（模糊，不具体）

## 工作流程示例

### 标准治疗计划工作流程

1. **评估患者** - 完整的病史、体格、诊断测试
2. **选择模板** - 选择适合临床背景的模板
3. **生成模板** - `python generate_template.py --type [type]`
4. **定制计划** - 填写患者特定信息（去识别化）
5. **设定 SMART 目标** - 定义可衡量的短期和长期目标
6. **指定干预措施** - 基于证据的药理学和非药理学
7. **创建时间表** - 安排约会、里程碑、重新评估
8. **定义监控** - 结果测量、评估频率
9. **验证完整性** - `python check_completeness.py plan.tex`
10. **质量检查** - `python validate_treatment_plan.py plan.tex`
11. **审查质量检查表** - 与 `quality_checklist.md`
12 进行比较。 **生成 PDF** - `pdflatex plan.tex`
13. **与患者一起审查** - 共同决策，确认理解
14. **实施和记录** - 执行计划，跟踪临床记录中的进展
15. **重新评估和修改** - 根据结果调整计划

### 多学科护理计划工作流程

1. **确定团队成员** - PCP、专家、治疗师、病例经理
2. **创建基本计划** - 生成主要条件
3 的模板。 **添加专业部分** - 整合顾问建议
4. **协调目标** - 确保跨学科的一致性
5. **定义沟通** - 团队会议日程、文档共享
6. **分配职责** - 明确由谁管理每项干预
7. **创建护理时间表** - 协调跨提供商的预约
8. **分享计划** - 分发给所有团队成员和患者
9. **集体跟踪** - 共享监控和结果跟踪
10. **定期团队审查** - 协同调整计划

## 最佳实践

### 以患者为中心的护理
✓ 让患者参与目标设定和决策 
✓ 尊重文化信仰和语言偏好 
✓ 用适当的语言提高健康素养 
✓ 使计划与患者价值观和生活环境相一致 
✓ 支持患者激活和自我管理 

### 循证实践
✓遵循当前的临床实践指南
✓使用已证明有效的干预措施
✓纳入质量措施（HEDIS、CMS）
✓避免低价值或无效的干预措施
✓根据新出现的证据更新计划

### 监管合规
✓根据HIPAA 安全港方法（18 个标识符） 
✓ 记录计费支持的医疗必要性 
✓ 包括知情同意文件 
✓ 在所有治疗计划上签名并注明日期 
✓ 维护专业文档标准 

### 质量文档
✓ 完成所有必需部分 
✓ 使用清晰、专业的医学语言
✓ 包括具体的、可衡量的目标 
✓ 指定确切的药物（剂量、途径、频率） 
✓ 定义监测参数和频率 
✓ 解决安全和风险缓解问题 

### 护理协调
✓ 向整个护理团队传达计划 
✓ 定义角色和职责
✓ 跨护理环境协调 
✓ 整合专家建议 
✓ 护理过渡计划 

## 与其他技能集成

### 临床报告
- **SOAP 注释**：记录治疗计划的实施和进展
- **H&P 文件**：初步评估为治疗提供信息规划
- **出院总结**：总结治疗计划执行情况
- **进度注释**：跟踪目标实现情况和计划修改

### 科学写作
- **引文管理**：参考临床实践指南
- **文献综述**：了解干预措施的证据基础
- **研究查找**：查找当前的治疗建议

### 研究
- **研究资助**：临床试验的治疗方案
- **临床试验报告**：文档试验干预

## 临床实践指南

治疗计划应符合循证指南：

### 普通医学
- 美国糖尿病协会(ADA)护理标准
- ACC/AHA心血管指南
- 黄金慢性阻塞性肺病指南
- JNC-8高血压指南
- KDIGO 慢性肾病指南

### 康复
- APTA 物理治疗临床实践指南
- AOTA 职业治疗实践指南
- AHA/AACVPR 心脏康复指南
- 中风康复最佳实践

### 心理健康
- APA（美国精神病学协会）实践指南
- VA/DoD 心理健康临床实践指南
- NICE 指南（英国）
- 循证心理治疗方案（CBT、DBT、ACT）

### 疼痛管理
- CDC阿片类药物处方指南
- AAPM（美国疼痛医学会）指南
- WHO镇痛阶梯
- 多模式镇痛最佳实践

### 围手术期护理
- ERAS（术后加速康复）协会指南
- ASA围手术期指南
- SCIP（手术护理改善项目）措施

## 专业标准

### 文件要求
- 完整准确的患者信息
- 使用适当的ICD-10编码明确诊断
- 循证干预措施
- 可衡量的目标和结果
- 定义的监控和跟进
- 提供者签名、凭证和日期

### 医疗必要性
治疗计划必须证明：
- 干预措施的医疗适当性
- 与诊断和严重程度相符
- 支持治疗选择的证据
- 预期结果和获益
- 频率和持续时间合理性

### 法律注意事项
- 知情同意文件
- 患者理解和协议
- 风险披露和缓解
- 专业责任保护
- 遵守州/联邦法规

## 支持和资源

### 获取帮助

1. **检查参考文件** - `references/` 目录
2 中的综合指南。 **查看模板** - 请参阅 `assets/` 目录 
3 中的示例结构。 **运行验证脚本** - 使用自动化工具
4 识别问题。 **查阅 SKILL.md** - 详细文档和最佳实践
5. **审查质量检查表** - 确保满足所有质量标准

### 外部资源

- 来自专业协会的临床实践指南
- UpToDate 和 DynaMed 的治疗建议
- AHRQ 有效的医疗保健计划
- 用于干预证据的 Cochrane 图书馆
- CMS 质量测量和HEDIS 规范
- HEDIS（医疗保健有效性数据和信息集）

### 专业组织

- 美国医学会（AMA）
- 美国家庭医师学会（AAFP）
- 专业协会指南（ADA、ACC、AHA、APA 等）
- 联合委员会标准
- 医疗保险和医疗补助服务中心 (CMS)

## 常见问题

### 我如何选择正确的模板？

将模板与您的主要临床重点相匹配：
- **慢性医疗状况** → 一般_医疗或慢性_疾病
- **手术后或受伤** → 康复或围手术期
- **精神疾病** → 心理健康
- **疼痛为主要问题** → 疼痛管理

### 如果我的患者有多种病症怎么办？

使用 `chronic_disease_management_plan.tex` 模板处理复杂的多发病，或选择主要病症的模板并添加合并症部分。

### 治疗计划应多久更新一次？

- **初始创建**：在诊断或治疗开始时
- **定期更新**：每 3-6 个月更新一次慢性病
- **重大变化**：当达到目标或修改治疗时
- **年度审查**：所有慢性病计划的最低限度

### 我可以修改LaTeX模板吗？

是的！模板旨在定制。修改部分、添加特定于专业的内容或调整格式以满足您的需求。

### 如何确保 HIPAA 合规性？

- 删除所有 18 个 HIPAA 标识符（请参阅安全港方法）
- 使用年龄范围而不是确切年龄（例如，“60-65”而不是“63”）
- 删除特定日期，使用相对日期时间线
- 省略小于州的地理标识符
- 使用clinical-reports技能中的`check_deidentification.py`脚本

### 如果验证脚本发现问题怎么办？

查看已识别的具体问题，查阅参考文件以获取指导，并相应地修改计划。常见问题包括：
- 缺少必需的部分
- 目标不符合SMART标准
- 监测参数不足
- 药物信息不完整

## 许可证

Claude Scientific Writer项目的一部分。参见主LICENSE文件。

- --

详细文档参见`SKILL.md`。如有问题或疑问，请查阅 `references/` 目录中的综合参考文件。
