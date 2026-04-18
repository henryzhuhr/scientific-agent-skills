# PyHealth 临床预测任务

## 概述

PyHealth 为常见医疗保健 AI 应用提供 20 多个预定义的临床预测任务。每个任务函数将原始患者数据转换为结构化输入输出对以进行模型训练。

## 任务函数结构

所有任务函数继承自`BaseTask`并提供：

- **input_schema**：定义输入特征（诊断、药物、实验室等）
- **output_schema**：定义预测目标（标签、值）
- **pre_filter()**：可选患者/就诊过滤逻辑

* *使用模式：**
```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn

dataset = MIMIC4Dataset(root="/path/to/data")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)
```

## 电子健康记录 (EHR)任务

### 死亡率预测

* *目的：** 预测下次就诊时或指定范围内的患者死亡风险时间范围

* *MIMIC-III 死亡率** (`mortality_prediction_mimic3_fn`)
- 预测下次医院就诊时的死亡
- 二元分类任务
- 输入：历史诊断、手术、药物
- 输出：二元标签（已故/活着）

* *MIMIC-IV 死亡率** (`mortality_prediction_mimic4_fn`)
- MIMIC-IV 数据集的更新版本
- 增强的功能集
- 改进的标签质量

* *eICU 死亡率** (`mortality_prediction_eicu_fn`)
- 多中心 ICU 死亡率预测
- 考虑医院级别变异

* *OMOP 死亡率** (`mortality_prediction_omop_fn`)
- 标准化死亡率预测
- 使用 OMOP 通用数据模型

* *院内死亡率** (`inhospital_mortality_prediction_mimic4_fn`)
- 预测当前住院期间的死亡
- 实时风险评估
- 比下次就诊死亡率更早的预测窗口

* *StageNet Mortality** (`mortality_prediction_mimic4_fn_stagenet`)
- 专门用于 StageNet 模型架构
- 时间阶段感知预测

### 医院再入院预测

* *目的：** 识别在指定时间范围内（通常为 30 天）有再入院风险的患者

* *MIMIC-III 再入院** (`readmission_prediction_mimic3_fn`)
- 30 天再入院预测
- 二元分类
- 输入：诊断史、药物、人口统计数据
- 输出：二元标签（再入院/未再入院）

* *MIMIC-IV 再入院** (`readmission_prediction_mimic4_fn`)
- 增强的再入院功能
- 改进的时间建模

* *eICU 再入院** (`readmission_prediction_eicu_fn`)
- ICU 特定的再入院风险
- 多站点数据

* *OMOP 再入院** (`readmission_prediction_omop_fn`)
- 标准化再入院预测

### 住院时间预测

* *目的：** 估计住院时间以进行资源规划和患者管理

* *MIMIC-III 住院时间** (`length_of_stay_prediction_mimic3_fn`)
- 回归任务
- 输入：入院诊断、生命体征、人口统计数据
- 输出：连续值（天）

* *MIMIC-IV 住院时间** (`length_of_stay_prediction_mimic4_fn`)
- LOS 预测的增强功能
- 更好的时间粒度

* *eICU 住院时间住院** (`length_of_stay_prediction_eicu_fn`)
- ICU住院时间预测
- 多医院数据

* *OMOP住院时间** (`length_of_stay_prediction_omop_fn`)
- 标准化LOS预测

### 药物推荐

* *用途：**根据患者病史和当前病情建议适当的药物

* *MIMIC-III药物推荐** (`drug_recommendation_mimic3_fn`)
- 多标签分类
- 输入：诊断、既往用药、人口统计
- 输出：推荐药物代码集
- 考虑药物-药物交互作用

* *MIMIC-IV 药物推荐** (`drug_recommendation_mimic4_fn`)
- 更新用药数据
- 增强交互建模

* *eICU 药物推荐** (`drug_recommendation_eicu_fn`)
- 重症监护用药建议

* *OMOP 药物推荐** (`drug_recommendation_omop_fn`)
- 标准化药品推荐

* *关键考虑因素：**
- 处理多药场景
- 多标签预测（每位患者使用多种药物）
- 可以与 SafeDrug/GAMENet 模型集成以提供安全意识建议

## 专业临床任务

### 医疗编码

* *MIMIC-III ICD-9 编码** (`icd9_coding_mimic3_fn`)
- 将 ICD-9 诊断/程序代码分配给临床记录
- 多标签文本分类
- 输入：临床文本/文档
- 输出：ICD-9 代码集
- 支持诊断和程序编码

### 患者链接

* *MIMIC-III 患者链接** (`patient_linkage_mimic3_fn`)
- 记录匹配和重复数据删除
- 二元分类（是否同一患者）
- 输入：来自两个记录的人口统计和临床特征
- 输出：匹配概率

## 生理学信号任务

### 睡眠分期

* *目的：** 根据脑电图/生理信号对睡眠阶段进行分类，用于睡眠障碍诊断

* *ISRUC 睡眠分期** (`sleep_staging_isruc_fn`)
- 多类分类（唤醒、N1、N2、N3、REM）
- 输入：多通道脑电图信号
- 输出：每个时期的睡眠阶段（通常为30秒）

* *SleepEDF睡眠分期**（`sleep_staging_sleepedf_fn`）
- 标准睡眠分期任务
- PSG信号处理

* *SHHS睡眠分期** (`sleep_staging_shhs_fn`)
- 大规模睡眠研究数据
- 人群水平睡眠分析

* *标准化标签：**
- 唤醒(W)
- 非快速眼动阶段1(N1)
- 非快速眼动阶段2 (N2)
- 非 REM 第 3 阶段（N3/深度睡眠）
- REM（快速眼动）

### 脑电图分析

* *异常检测** (`abnormality_detection_tuab_fn`)
- 二元分类（正常/异常） EEG)
- 临床筛查应用
- 输入：多通道脑电图记录
- 输出：二进制标签

* *事件检测** (`event_detection_tuev_fn`)
- 识别特定脑电图事件（尖峰、癫痫发作）
- 多类别分类
- 输入：EEG 时间序列
- 输出：事件类型和计时

* *癫痫发作检测** (`seizure_detection_tusz_fn`)
- 专门癫痫发作检测
- 对于癫痫监测至关重要
- 输入：连续 EEGZXXQNL3QXZ- 输出：癫痫发作/非癫痫发作分类

## 医学成像任务

### COVID-19 胸部X 射线分类

* *COVID-19 CXR** (`covid_classification_cxr_fn`)
- 多类图像分类
- 类别：COVID-19、细菌性肺炎、病毒性肺炎、正常
- 输入：胸部 X 射线图像
- 输出：疾病分类

## 基于文本任务

### 医学转录分类

* *医学专业分类** (`medical_transcription_classification_fn`)
- 按医学专业对临床笔记进行分类
- 多类文本分类
- 输入：临床转录文本
- 输出：医学专业（心脏病学、神经病学、等）

## 自定义任务创建

### 创建自定义任务

通过指定输入/输出模式定义自定义预测任务：

```python
from pyhealth.tasks import BaseTask

def custom_task_fn(patient):
    """Custom prediction task"""

    # Define input features
    samples = []

    for i, visit in enumerate(patient.visits):
        # Skip if not enough history
        if i < 2:
            continue

        # Create input from historical visits
        input_info = {
            "diagnoses": [],
            "medications": [],
            "procedures": []
        }

        # Collect features from previous visits
        for past_visit in patient.visits[:i]:
            for event in past_visit.events:
                if event.vocabulary == "ICD10CM":
                    input_info["diagnoses"].append(event.code)
                elif event.vocabulary == "NDC":
                    input_info["medications"].append(event.code)

        # Define prediction target
        # Example: predict specific outcome at current visit
        output_info = {
            "label": 1 if some_condition else 0
        }

        samples.append({
            "patient_id": patient.patient_id,
            "visit_id": visit.visit_id,
            "input_info": input_info,
            "output_info": output_info
        })

    return samples

# Apply custom task
sample_dataset = dataset.set_task(custom_task_fn)
```

### 任务功能组件

1. **输入模式定义**
  - 指定要提取的特征
  - 定义特征类型（代码、序列、值）
  - 设置时间窗口

2. **输出模式定义**
  - 定义预测目标
  - 设置标签类型（二元、多类、多标签、回归）
  - 指定评估指标

3. **过滤逻辑**
  - 排除数据不足的患者/就诊
  - 应用纳入/排除标准
  - 处理缺失数据

4. **样本生成**
  - 创建输入-输出对
  - 维护患者/就诊标识符
  - 保留时间顺序

## 任务选择指南

### 临床预测任务
 * *使用场合：** 处理结构化 EHR 数据（诊断、药物、程序）

* *数据集：** MIMIC-III、MIMIC-IV、eICU、OMOP

* *常见任务：**
- 风险分层的死亡率预测
- 护理过渡计划的再入院预测
- 资源分配的住院时间
- 临床决策支持的药物推荐

### 信号处理任务
* * 何时使用：** 处理生理时间序列数据

* *数据集：** SleepEDF、SHHS、ISRUC、TUEV、TUAB、TUSZ

* *常见任务：**
- 用于睡眠障碍诊断的睡眠分期
- 用于筛查的脑电图异常检测
- 用于癫痫监测的癫痫发作检测

### 成像任务
* *适用于：** 处理医学图像

* *数据集：** COVID-19 CXR

* *常见任务：**
- 根据放射线照片进行疾病分类
- 异常检测

### 文本任务
* * 适用于：** 与临床工作注释和文档

* *数据集：**医学转录，MIMIC-III（带注释）

* *常见任务：**
- 来自临床文本的医学编码
- 专业分类
- 临床信息提取

## 任务输出结构

所有任务函数返回`SampleDataset` 与：

```python
sample = {
    "patient_id": "unique_patient_id",
    "visit_id": "unique_visit_id",  # if applicable
    "input_info": {
        # Input features (diagnoses, medications, etc.)
    },
    "output_info": {
        # Prediction targets (labels, values)
    }
}
```

## 与模型集成

任务定义模型的输入/输出协定：

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.models import Transformer

# 1. Create task-specific dataset
dataset = MIMIC4Dataset(root="/path/to/data")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)

# 2. Model automatically adapts to task schema
model = Transformer(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",  # matches task output
)
```

## 最佳实践

1. **将任务与临床问题相匹配**：选择可用于标准化基准测试的预定义任务

2. **考虑时间窗口**：确保有足够的历史记录来进行有意义的预测

3. **处理类别不平衡**：许多临床结果都很罕见（死亡率、再入院）

4. **验证临床相关性**：确保预测窗口与临床决策时间表

5保持一致。 **使用适当的指标**：不同的任务需要不同的评估指标（二进制为AUROC，多类为宏F1）

6. **文档排除标准**：跟踪哪些患者/就诊被过滤以及原因

7. **保护患者隐私**：始终使用去识别化数据并遵循 HIPAA/GDPR 指南
