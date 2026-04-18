# 患者文档标准

## SOAP Notes

SOAP（主观、客观、评估、计划）是临床实践中进度记录的标准格式。

### 目的和使用

* *何时使用 SOAP 记录：**
- 医院每日进度记录
- 门诊就诊记录
- 专科咨询
- 随访
- 记录治疗反应

* *好处：**
- 标准化结构
- 有组织的临床推理
- 促进沟通
- 支持计费和编码
- 法律文档

### SOAP 组件

#### S - 主观

* *定义：** 患者报告的信息（症状、疑虑、病史）

* *要包括的元素：**
- 主诉或就诊原因
- 现病史 (HPI)
- 与访问相关的系统 (ROS)审查
- 患者对症状的描述
- 对先前治疗的反应
- 功能影响
- 患者担忧或问题

* *HPI 元素（使用 OPQRST 治疗疼痛/症状）：**
- **开始：何时开始？突然的还是渐进的？
- **P**rocation/Palliation：什么使它变得更好或更糟？
- **Q**质量：感觉如何？ （尖锐、钝、灼烧等）
- **R**区域/辐射：在哪里？它会传播吗？
- **S**everity：有多严重？ （0-10 刻度）
- **T**计时：恒定还是间歇？期间？频率？

* *相关症状：**
- 与主诉一起出现的其他症状
- 相关阴性（缺乏预期症状）

* * 对治疗的反应：**
- 服用的药物和效果
- 先前的干预措施和结果
- 治疗依从性计划

* *示例主观部分：**
```
S: Patient reports persistent cough for 5 days, productive of yellow sputum. Associated
with fever to 101.5°F, measured at home yesterday. Denies shortness of breath, chest
pain, or hemoptysis. Started on azithromycin 2 days ago by urgent care, with minimal
improvement. Reports decreased appetite but able to maintain hydration. Denies recent
travel or sick contacts.
```

#### O - 目标

* *定义：**可测量、可观察的临床数据

* *要包括的元素：**

* *生命体征：**
- 温度（°F 或°C）
- 血压（mmHg）
- 心率（bpm）
- 呼吸频率（呼吸/分钟）
- 氧饱和度（%）
- 身高和体重（计算） BMI)
- 疼痛评分（如果适用）

* *一般外观：**
- 整体外观（健康、生病、痛苦）
- 年龄适宜性
- 营养状况
- 卫生状况
- 情感和行为

* * 身体按系统检查：**
- 从头到脚或按系统组织
- 提出投诉的相关调查结果
- 包括相关的阳性和阴性

* * 标准检查系统：**
1. **HEENT**（头、眼睛、耳朵、鼻子、喉咙）
2. **颈部**（甲状腺、淋巴结、JVD、颈动脉）
3. **心血管**（心音、杂音、末梢脉搏、水肿）
4. **肺/呼吸**（呼吸音、呼吸功）
5. **腹部**（肠鸣音、压痛、器官肿大、肿块）
6. **四肢**（水肿、脉搏、ROM、畸形）
7. **神经系统**（精神状态、脑神经、运动、感觉、反射、步态）
8. **皮肤**（皮疹、病变、伤口）
9. **精神**（情绪、情感、思维过程/内容）

* *实验室和影像结果：**
- 相关测试结果
- 包括异常值的参考范围
- 注意相对于访问的测试时间

* *示例目标部分：**
```
O: Vitals: T 100.8°F, BP 128/82, HR 92, RR 18, SpO2 96% on room air
General: Alert, mild respiratory distress, appears mildly ill
HEENT: Oropharynx without erythema or exudates, TMs clear bilaterally
Neck: No lymphadenopathy, no JVD
Cardiovascular: Regular rate and rhythm, no murmurs
Pulmonary: Decreased breath sounds right lower lobe, dullness to percussion, egophony
present. No wheezes.
Abdomen: Soft, non-tender, no organomegaly
Extremities: No edema, pulses 2+ bilaterally
Neurological: Alert and oriented x3, no focal deficits

Labs (drawn today):
WBC 14.2 x10³/μL (H) [ref 4.5-11.0]
Hemoglobin 13.5 g/dL
Platelets 245 x10³/μL
CRP 8.5 mg/dL (H) [ref <0.5]

Chest X-ray: Right lower lobe consolidation consistent with pneumonia
```

#### A - 评估

* *定义：**临床印象、诊断和患者状态评估

* *要包括的要素：**
- 主要诊断或问题
- 次要诊断或问题
- 鉴别诊断，如果不确定
- 严重程度评估
- 实现治疗目标的进展
- 并发症或新问题

* *格式：**
- 问题列表（编号）
- 每个问题及简要评估
- 在适合的情况下包括ICD-10 代码计费

* *示例评估部分：**
```
A: 
1. Community-acquired pneumonia (CAP), right lower lobe (J18.1)
   - Moderate severity (CURB-65 score 1)
   - Appropriate for outpatient management
   - Minimal improvement on azithromycin, likely bacterial etiology
   
2. Dehydration, mild (E86.0)
   - Secondary to decreased PO intake
   
3. Type 2 diabetes mellitus (E11.9)
   - Well-controlled, continue home medications
```

#### P - Plan

* *定义：**诊断和治疗干预

* *要素包括：**
- 诊断计划（进一步检测、影像学、转诊）
- 治疗计划（药物、手术、疗法）
- 患者教育和咨询
- 随访安排
- 患者具体说明
- 返回预防措施（何时寻求紧急护理）

* *药物文件：**
- 药物名称（通用首选）
- 剂量和途径
- 频率
- 持续时间
- 适应症

* *计划组织：**
- 按问题（匹配）评估）
- 按干预类型（诊断、治疗、教育）

* *示例计划部分：**
```
P:
1. Community-acquired pneumonia:
   Diagnostics: None additional at this time
   Therapeutics:
   - Discontinue azithromycin
   - Start amoxicillin-clavulanate 875/125 mg PO BID x 7 days
   - Supportive care: adequate hydration, rest, acetaminophen for fever
   Education: 
   - Explained bacterial pneumonia diagnosis and antibiotic change
   - Discussed expected improvement within 48-72 hours
   - Return precautions: worsening dyspnea, high fever >103°F, confusion
   Follow-up: Phone call in 48 hours to assess response, clinic visit in 1 week
   
2. Dehydration:
   - Encourage PO fluids, goal 2 liters/day
   - Sports drinks or electrolyte solutions acceptable
   
3. Type 2 diabetes:
   - Continue metformin 1000 mg PO BID
   - Home glucose monitoring
   - Follow-up with endocrinology as scheduled

Patient verbalized understanding and agreement with plan.
```

### SOAP 注释最佳实践

* *文档标准：**
- 清晰地书写，如果手写
- 仅使用标准缩写
- 每个条目的日期和时间
- 对所有条目进行签名和凭证
- 实时或尽快记录
- 避免复制转发错误
- 审查和更新问题列表

* *计费注意事项：**
- 记录医疗必要性
- 将文档与计费级别相匹配
- 包括E/M 编码所需的元素
- 记录基于时间的计费的时间

* *法律注意事项：**
- 记录事实，而不是意见或判断
- 在何时向患者报价相关
- 客观记录不合规情况
- 切勿更改记录
- 使用附录进行更正

## 病史和体检(H&P)

### 目的

- 综合基线评估
- 记录入院或初始时的患者状态遭遇
- 指导诊断和治疗计划
- 入院24小时内需要（TJC要求）

### H&P组件

#### 标题信息

- 患者姓名、出生日期、MRN
- 检查日期和时间
- 入院诊断
- 主治医生
- 服务
- 地点（急诊室、楼层、ICU）

#### 主诉（CC）

* *定义：** 简要说明患者寻求护理的原因

* *格式：**
- 一句话
- 使用患者自己的话（在引号中）
- 示例：CC：“我无法呼吸”

#### 现病史（HPI）

* *目的：**当前问题的详细时间顺序叙述

* *必填元素（用于计费）：**
- 位置
- 质量
- 严重性
- 持续时间
- 计时
- 上下文
- 修改因素
- 关联体征/症状

* *结构：**
- 开场陈述（人口统计、提出问题）
- 时间顺序描述
- 症状特征
- 之前的检查或治疗
- 提示的呈现内容现在

* *示例：**
```
HPI: Mr. Smith is a 65-year-old man with history of CHF (EF 35%) who presents with
3 days of progressive dyspnea on exertion. Patient reports dyspnea now occurs with
walking 10 feet (baseline 1-2 blocks). Associated with orthopnea (now requiring
3 pillows, baseline 1) and lower extremity swelling. Denies chest pain, palpitations,
or syncope. Reports medication compliance but notes running out of furosemide 2 days
ago. Weight increased 8 lbs over past week. Has not been monitoring daily weights
at home. Presented to ED today when dyspnea worsened and developed while at rest.
```

#### 既往病史 (PMH)

* *包括：**
- 慢性疾病
- 以前住院治疗
- 主要疾病
- 受伤
- 童年疾病（如果相关）

* * 格式：**
```
PMH:
1. Heart failure with reduced ejection fraction (2018), EF 35% on echo 6 months ago
2. Coronary artery disease, s/p CABG (2019)
3. Type 2 diabetes mellitus (2010)
4. Hypertension (2005)
5. Chronic kidney disease stage 3 (baseline Cr 1.8 mg/dL)
6. Hyperlipidemia
```

#### 既往手术史 (PSH)

* * 包括：**
- 所有手术和程序
- 日期（如果准确，年份可接受）日期未知）
- 并发症（如果有）

* *格式：**
```
PSH:
1. CABG x4 (2019), complicated by post-op atrial fibrillation
2. Cholecystectomy (2015)
3. Appendectomy (childhood)
```

#### 药物

* *文档：**
- 通用名称首选
- 剂量、路线、频率
- 指示如果不明显
- 包括非处方药
- 草药补充剂
- 如果患者无法提供列表请注意

* *格式：**
```
Medications:
1. Furosemide 40 mg PO daily (ran out 2 days ago)
2. Carvedilol 12.5 mg PO BID
3. Lisinopril 20 mg PO daily
4. Spironolactone 25 mg PO daily
5. Metformin 1000 mg PO BID
6. Atorvastatin 40 mg PO daily
7. Aspirin 81 mg PO daily
8. Multivitamin daily
```

#### 过敏

* *文件：**
- 药物过敏反应
- 食物过敏
- 环境过敏
- NKDA（如果未知）过敏症

* *格式：**
```
Allergies:
1. Penicillin → anaphylaxis (childhood)
2. Shellfish → hives
3. ACE inhibitors → angioedema
```

#### 家族史（FH）

* *包括：**
- 一级亲属（父母、兄弟姐妹、子女）
- 年龄和健康状况或死亡年龄和原因
- 相关遗传性疾病
- 出现相关疾病的家族史

* *格式：**
```
Family History:
Father: CAD, MI age 58, alive age 85
Mother: Breast cancer, deceased age 72
Brother: Type 2 diabetes
Sister: Healthy
Children: 2 sons, both healthy
```

#### 社会史（SH）

* *包括：**
- 烟草使用（当前、以前、从未；包年，如果适用）
- 饮酒（每周饮酒，CAGE 问题，如果有指示）
- 非法药物使用（当前、以前、从未；类型和途径）
- 职业 
- 生活状况（独自、与家人在一起、辅助生活、等）
- 婚姻状况
- 性史（如果相关）
- 运动习惯
- 饮食
- 功能状态

* *格式：**
```
Social History:
Tobacco: Former smoker, quit 10 years ago (30 pack-year history)
Alcohol: 2-3 beers per week, denies binge drinking
Illicit drugs: Denies
Occupation: Retired electrician
Living situation: Lives at home with wife, 2-story house, bedroom upstairs
Marital status: Married
Exercise: Unable to exercise due to dyspnea
Diet: Low sodium diet (usually adherent)
Functional status: Independent in ADLs at baseline
```

#### 系统回顾(ROS)

* *目的：**按身体系统对症状进行系统筛查

* *要求：**
- 至少 10 个系统进行综合检查
- 相关阳性和阴性 
- 如果满足以下条件，“所有其他系统均经过审查且呈阴性”则可以接受记录了

* *系统：**
1. **体质**：发烧、发冷、盗汗、体重变化、疲劳
2. **眼睛**：视力变化、疼痛、放电
3. **耳鼻喉科**：听力损失、耳鸣、鼻窦问题、喉咙痛
4. **心血管**：胸痛、心悸、水肿、跛行
5. **呼吸系统**：咳嗽、呼吸困难、喘息、咯血
6. **胃肠道**：恶心、呕吐、腹泻、便秘、腹痛
7. **泌尿生殖系统**：排尿困难、尿频、血尿、失禁
8. **肌肉骨骼**：关节疼痛、肿胀、僵硬、无力
9. **皮肤**：皮疹、病变、瘙痒、痣变化
10. **神经系统**：头痛、头晕、晕厥、癫痫发作、虚弱、麻木
11. **精神科**：情绪变化、抑郁、焦虑、睡眠障碍
12. **内分泌**：热/冷不耐受、多尿、烦渴
13. **血液/淋巴**：容易瘀伤、出血、淋巴结肿胀
14. **过敏性/免疫性**：季节性过敏、频繁感染

* *格式：**
```
ROS:
Constitutional: Denies fever, chills. Reports fatigue and weight gain (8 lbs).
Cardiovascular: Reports dyspnea, orthopnea, lower extremity edema. Denies chest pain,
palpitations, syncope.
Respiratory: Denies cough, wheezing, hemoptysis.
Gastrointestinal: Denies nausea, vomiting, diarrhea, constipation, abdominal pain.
All other systems reviewed and negative.
```

#### 体检

* *一般组织：**
- 生命体征优先
- 一般外观
- 从头到脚的系统检查

* *生命体征：**
```
Vitals: T 98.2°F, BP 142/88, HR 105, RR 24, SpO2 88% on room air → 95% on 2L NC
Height: 5'10", Weight: 195 lbs (baseline 187 lbs), BMI 28
```

* *系统检查：**

* *一般：**发育良好，肥胖男性，中度呼吸窘迫，直立在床上

* *HEENT：**
- 头部：正常头颅，无创伤
- 眼睛：PERRLA， EOMI，无巩膜黄疸
- 耳朵：双侧 TM 清晰 
- 鼻子：鼻孔开放，无分泌物 
- 喉咙：口咽部无红斑或渗出物 

* *颈部：** 柔软，无淋巴结肿大，JVP 升高至 12 厘米，无甲状腺肿大

* *心血管：**
- 检查：无可见 PMI
- 触诊：PMI 横向移位
- 听诊：心动过速规则节律，存在 S3 奔马律，心尖处 2/6 全收缩期杂音辐射至腋窝 
- 周围脉搏：双侧 2+ 桡动脉、1+ 足背脉搏 

* * 肺：**
- 检查：呼吸功增加，使用辅助肌肉 
- 触诊：对称性触觉颤动 
- 叩诊：双侧基底叩诊浊音 
- 听诊：双侧肺野中部有爆裂音，无哮鸣音

* *腹部：**
- 检查：肥胖，无胀气
- 听诊：肠鸣音正常
- 叩诊：鼓室
- 触诊：柔软，无压痛，无肿块，无肝脾肿大

* *四肢：**双侧小腿中部凹陷性水肿3+，无发绀或杵状指

* *皮肤：**温暖干燥，无皮疹

* *神经系统：**
- 精神状态：警觉并能适应人、地点、时间
- 脑神经：II-XII 完整 
- 运动：四肢 5/5 力量 
- 感觉：轻触完整 
- 反射：2+ 对称 
- 步态：因呼吸困难而延迟 
- 小脑：手指到鼻子完整

* *精神科：**与疾病相关的焦虑影响，正常思维过程

#### 实验室和影像学

* *包括：**
- 所有相关实验室及参考范围
- 具有主要发现的影像学研究
- 心电图结果
- 其他诊断测试

* *示例：**
```
Laboratory Data:
CBC: WBC 8.5, Hgb 11.2 (L), Hct 34%, Plt 245
BMP: Na 132 (L), K 3.2 (L), Cl 98, CO2 30, BUN 45 (H), Cr 2.1 (H, baseline 1.8), glucose 145
Troponin: <0.04 (normal)
BNP: 1250 pg/mL (H, elevated)

Imaging:
Chest X-ray: Cardiomegaly, bilateral pleural effusions, pulmonary vascular congestion
consistent with volume overload

ECG: Sinus tachycardia at 105 bpm, left ventricular hypertrophy, no acute ST-T changes
```

#### 评估和计划

* *格式：** 基于问题并编号问题列表

* *示例：**
```
Assessment and Plan:

65-year-old man with history of CHF (EF 35%) presenting with acute decompensated
heart failure.

1. Acute decompensated heart failure (I50.23)
   - NYHA Class IV symptoms
   - Volume overload on exam and imaging
   - Precipitated by medication non-adherence (ran out of furosemide)
   - BNP elevated at 1250
   Diagnostics:
   - Echocardiogram to assess current EF and valvular function
   - Daily weights and strict I/O
   Therapeutics:
   - Furosemide 40 mg IV BID, goal negative 1-2L daily
   - Continue carvedilol, lisinopril, spironolactone
   - Oxygen 2L NC, goal SpO2 >92%
   - Low sodium diet (<2g/day), fluid restriction 1.5L/day
   - Telemetry monitoring
   Follow-up: Will reassess after diuresis, goal discharge in 3-5 days

2. Acute kidney injury on CKD stage 3 (N17.9, N18.3)
   - Cr 2.1 from baseline 1.8, likely prerenal from poor forward flow
   - Monitor daily, expect improvement with diuresis
   - Hold nephrotoxic agents

3. Hypokalemia (E87.6)
   - K 3.2, likely from prior diuretic use
   - Replete K 40 mEq PO x1, then reassess
   - Continue spironolactone for K-sparing effect

4. Hyponatremia (E87.1)
   - Na 132, likely dilutional from volume overload
   - Expect improvement with diuresis
   - Fluid restriction as above

5. Type 2 diabetes mellitus (E11.9)
   - Well-controlled
   - Continue home metformin
   - Monitor glucose while hospitalized

6. Coronary artery disease (I25.10)
   - Stable, no acute coronary syndrome
   - Continue aspirin, statin, beta-blocker

Code status: Full code
Disposition: Admit to telemetry floor
```

## 出院总结

### 目的

- 向门诊提供者传达医院护理
- 记录医院病程和结果
- 确保护理的连续性
- 满足监管要求（TJC、CMS）

### 时间

* * 要求：**
- 在出院后30 天内完成(CMS)
- 许多医院要求在 24-48 小时内
- 在后续预约时可用

### 组件

#### 标题

- 患者人口统计数据
- 入院日期和出院日期
- 持续时间在
- 主治医师
- 咨询服务
- 初级保健医师

#### 入院诊断

住院主要原因

#### 出院诊断

* *格式：**编号列表，优先

* *示例：**
```
Discharge Diagnoses:
1. Acute decompensated heart failure
2. Acute kidney injury on chronic kidney disease stage 3
3. Hypokalemia
4. Hyponatremia
5. Coronary artery disease
6. Type 2 diabetes mellitus
```

#### 医院课程

* *内容：**
- 按时间顺序叙述或基于问题
- 关键事件和干预
- 响应治疗
- 执行的程序
- 咨询
- 并发症
- 显着的测试结果

* *示例（简要）：**
```
Hospital Course:
Mr. Smith was admitted with acute decompensated heart failure in the setting of
medication non-adherence. He was diuresed with IV furosemide with net negative
5 liters over 3 days, with significant improvement in dyspnea and resolution of
lower extremity edema. Echocardiogram showed persistent reduced EF of 30%, similar
to prior. Kidney function improved to baseline with diuresis. Electrolytes were
repleted and normalized. Patient was transitioned to oral furosemide on hospital
day 3 and remained stable. He was ambulating without dyspnea on room air by
discharge. Comprehensive heart failure education was provided.
```

#### 程序

```
Procedures:
1. Echocardiogram transthoracic (hospital day 1)
```

#### 出院药物

* *格式：**
- 包含说明的完整列表
- **突出显示新**药物
- **更改**注明的药物
- **停产**药物列出

* *示例：**
```
Discharge Medications:
1. Furosemide 60 mg PO daily [INCREASED from 40 mg]
2. Carvedilol 12.5 mg PO BID [UNCHANGED]
3. Lisinopril 20 mg PO daily [UNCHANGED]
4. Spironolactone 25 mg PO daily [UNCHANGED]
5. Metformin 1000 mg PO BID [UNCHANGED]
6. Atorvastatin 40 mg PO daily [UNCHANGED]
7. Aspirin 81 mg PO daily [UNCHANGED]
```

#### 放电条件

```
Discharge Condition:
Hemodynamically stable, ambulatory, no supplemental oxygen requirement, euvolemic
on exam, baseline functional status restored.
```

#### 放电处置

```
Discharge Disposition:
Home with self-care
```

#### 后续计划

* *包括：**
- 已安排的预约
- 建议的后续时间
- 出院时等待测试或研究
- 转诊制作

* *示例：**
```
Follow-up:
1. Cardiology appointment with Dr. Jones on [date] at [time]
2. Primary care with Dr. Smith in 1 week
3. Home health for vital sign monitoring and medication reconciliation
4. Repeat BMP in 1 week (arranged, lab slip provided)
```

#### 患者说明

* *包括：**
- 活动限制
- 饮食限制
- 伤口护理（如果适用）
- 设备或家居服务
- 监测说明（每日体重、血糖、血压）
- 退货注意事项

* *示例：**
```
Patient Instructions:
1. Weigh yourself daily every morning, call doctor if gain >2 lbs in 1 day or >5 lbs
   in 1 week
2. Low sodium diet (<2 grams per day)
3. Fluid restriction 2 liters per day
4. Take all medications as prescribed, do not run out of medications
5. Activity: Resume normal activities as tolerated
6. Return to ER or call 911 if: severe shortness of breath, chest pain, severe swelling,
   or other concerning symptoms
```

- --

此参考提供了患者临床文档的综合标准，包括 SOAP 注释、H&P 和出院摘要。使用这些指南可确保完整、准确且合规的临床文件。
