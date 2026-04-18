# TDC 数据集综合目录

本文档提供了治疗数据共享中所有可用数据集的综合目录，按任务类别组织。

## 单实例预测数据集

### ADME（吸收、分布、代谢、排泄）

* *吸收：**
- `Caco2_Wang` - Caco-2 细胞渗透性（906 种化合物）
- `Caco2_AstraZeneca` - 阿斯利康的 Caco-2 渗透性（700 种化合物）
- `HIA_Hou` - 人体肠道吸收（578 种化合物）
- `Pgp_Broccatelli` - P-糖蛋白抑制（1,212化合物）
- `Bioavailability_Ma` - 口服生物利用度（640 种化合物）
- `F20_edrug3d` - 口服生物利用度 F>=20%（1,017 种化合物）
- `F30_edrug3d` - 口服生物利用度 F>=30%（1,017 种化合物）化合物）

* *分布：**
- `BBB_Martins` - 血脑屏障渗透（1,975 种化合物）
- `PPBR_AZ` - 血浆蛋白结合率（1,797 种化合物）
- `VDss_Lombardo` - 稳态分布体积（1,130）化合物）

* *代谢：**
- `CYP2C19_Veith` - CYP2C19 抑制（12,665 种化合物）
- `CYP2D6_Veith` - CYP2D6 抑制（13,130 种化合物）
- `CYP3A4_Veith` - CYP3A4 抑制（12,328 种化合物）
- `CYP1A2_Veith` - CYP1A2 抑制（12,579 种化合物）
- `CYP2C9_Veith` - CYP2C9 抑制（12,092 种化合物）
- `CYP2C9_Substrate_CarbonMangels` - CYP2C9 底物（666 种化合物）
- `CYP2D6_Substrate_CarbonMangels` - CYP2D6 底物（664 种化合物）
- `CYP3A4_Substrate_CarbonMangels` - CYP3A4 底物（667 种化合物）

* *排泄：**
- `Half_Life_Obach` - 半衰期（667）化合物）
- `Clearance_Hepatocyte_AZ` - 肝细胞清除率（1,020 种化合物）
- `Clearance_Microsome_AZ` - 微粒体清除率（1,102 种化合物）

* *溶解度和亲脂性：**
- `Solubility_AqSolDB` - 水溶性(9,982 种化合物)
- `Lipophilicity_AstraZeneca` - 亲脂性 (logD) (4,200 种化合物)
- `HydrationFreeEnergy_FreeSolv` - 水合自由能 (642 种化合物)

### 毒性

* *器官毒性：**
- `hERG` - hERG 通道抑制/心脏毒性（648 种化合物）
- `hERG_Karim` - hERG 阻滞剂扩展数据集（13,445 种化合物）
- `DILI` - 药物引起的肝损伤（475化合物）
- `Skin_Reaction` - 皮肤反应（404 种化合物）
- `Carcinogens_Lagunin` - 致癌性（278 种化合物）
- `Respiratory_Toxicity` - 呼吸道毒性（278 种化合物）

* *一般毒性：**
- `AMES` - Ames 致突变性（7,255 种化合物）
- `LD50_Zhu` - 急性毒性 LD50（7,385 种化合物）
- `ClinTox` - 临床试验毒性（1,478 种化合物）
- `SkinSensitization` - 皮肤致敏（278 种化合物）
- `EyeCorrosion` - 眼睛腐蚀（278 种化合物）
- `EyeIrritation` - 眼睛刺激（278 种化合物）

* *环境毒性：**
- `Tox21-AhR` - 核受体信号传导（8,169化合物）
- `Tox21-AR` - 雄激素受体（9,362 种化合物）
- `Tox21-AR-LBD` - 雄激素受体配体结合（8,343 种化合物）
- `Tox21-ARE` - 抗氧化反应元件（6,475 种化合物）
- `Tox21-aromatase` - 芳香酶抑制（6,733 种化合物）
- `Tox21-ATAD5` - DNA 损伤（8,163 种化合物）
- `Tox21-ER` - 雌激素受体（7,257 种化合物）
- `Tox21-ER-LBD` - 雌激素受体配体结合（8,163 种化合物）
- `Tox21-HSE` - 热休克反应（8,162 种化合物）
- `Tox21-MMP` - 线粒体膜电位（7,394 种化合物）
- `Tox21-p53` - p53 途径（8,163 种）化合物）
- `Tox21-PPAR-gamma` - PPAR gamma 激活（7,396 种化合物）

### HTS（高通量筛选）

* *SARS-CoV-2:**
- `SARSCoV2_Vitro_Touret` - 体外抗病毒活性（1,484化合物）
- `SARSCoV2_3CLPro_Diamond` - 3CL 蛋白酶抑制（879 种化合物）
- `SARSCoV2_Vitro_AlabdulKareem` - 体外筛选（5,953 种化合物）

* *其他靶标：**
- `Orexin1_Receptor_Butkiewicz` - 食欲素受体筛选（4,675 种化合物）
- `M1_Receptor_Agonist_Butkiewicz` - M1 受体激动剂（1,700 种化合物）
- `M1_Receptor_Antagonist_Butkiewicz` - M1 受体拮抗剂（1,700 种化合物）
- `HIV_Butkiewicz` - HIV 抑制（40,000 多种化合物）
- `ToxCast` - 环境化学筛选（8,597 种化合物）

### QM（量子力学）

- `QM7` - 量子力学性质（7,160 个分子）
- `QM8` - 电子光谱和激发态（21,786 个分子）
- `QM9` - 几何、能量、电子、热力学性质（133,885 个分子）

### 产量

- `Buchwald-Hartwig` - 反应产量预测（3,955）反应）
- `USPTO_Yields` - USPTO 的产量预测（853,879 次反应）

### 表位

- `IEDBpep-DiseaseBinder` - 疾病相关表位结合（6,080 个肽）
- `IEDBpep-NonBinder` - 非结合肽（24,320 个肽）

### Develop（开发）

- `Manufacturing` - 制造成功预测
- `Formulation` - 制剂稳定性

### CRISPROutcome

- `CRISPROutcome_Doench` - 基因编辑效率预测（5,310 个指导 RNA）

## 多实例预测数据集

### DTI（药物-靶点相互作用）

* *结合亲和力：**
- `BindingDB_Kd` - 解离常数（52,284 对，10,665 种药物， 1,413 个蛋白质）
- `BindingDB_IC50` - 半最大抑制浓度（991,486 对、549,205 种药物、5,078 个蛋白质）
- `BindingDB_Ki` - 抑制常数（375,032 对、174,662 种药物、3,070 个）蛋白）

* *激酶结合：**
- `DAVIS` - Davis 激酶结合数据集（30,056 对，68 种药物，442 个蛋白）
- `KIBA` - KIBA 激酶结合数据集（118,254 对，2,111 种药物，229蛋白）

* *二元相互作用：**
- `BindingDB_Patent` - 专利衍生的 DTI（8,503 对）
- `BindingDB_Approval` - FDA 批准的药物 DTI（1,649 对）

### DDI（药物-药物相互作用）

- `DrugBank` - 药物-药物相互作用（191,808 对，1,706 种药物）
- `TWOSIDES` - 基于副作用的 DDI（4,649,441 对，645 种药物）

### PPI （蛋白质-蛋白质相互作用）

- `HuRI` - 人类参考蛋白质相互作用组（52,569 个相互作用）
- `STRING` - 蛋白质功能关联（19,247 个相互作用）

### GDA（基因疾病协会）

- `DisGeNET` -基因-疾病关联（81,746对）
- `PrimeKG_GDA` - PrimeKG知识图谱中的基因疾病

### DrugRes（药物反应/耐药）

- `GDSC1` - 癌症药物敏感性基因组学 v1（178,000）对）
- `GDSC2` - 癌症药物敏感性基因组学 v2（125,000 对）

### DrugSyn（药物协同）

- `DrugComb` - 药物组合协同（345,502 种组合）
- `DrugCombDB` - 药物组合数据库（448,555 个组合）
- `OncoPolyPharmacology` - 肿瘤药物组合（22,737 个组合）

### 肽MHC

- `MHC1_NetMHCpan` - MHC I 类结合（184,983 个）对）
- `MHC2_NetMHCIIpan` - MHC II 类结合（134,281 对）

### AntibodyAff（抗体亲和力）

- `Protein_SAbDab` - 抗体-抗原亲和力（1,500+ 对）

### MTI（miRNA 目标）相互作用）

- `miRTarBase` - 经过实验验证的 miRNA-靶标相互作用（380,639 对）

### Catalyst

- `USPTO_Catalyst` - 反应的催化剂预测（11,000+ 反应）

### TrialOutcome

- `TrialOutcome_WuXi` - 临床试验结果预测（3,769 项试验）

## 生成数据集

### MolGen（分子生成）

- `ChEMBL_V29` - 来自 ChEMBL 的药物样分子（1,941,410）分子）
- `ZINC` - ZINC 数据库子集（100,000+ 分子）
- `GuacaMol` - 目标导向基准分子
- `Moses` - 分子集基准（1,936,962 个分子）

### RetroSyn（逆合成）

- `USPTO` - USPTO 专利逆合成（1,939,253 个反应）
- `USPTO-50K` - 策划的 USPTO 子集（50,000 个反应）

### PairMolGen（配对分子）生成）

- `Prodrug` - 前药到药物的转化（1,000+对）
- `Metabolite` - 药物到代谢物的转化

## 使用retrieve_dataset_names

以编程方式访问特定的所有可用数据集任务：

```python
from tdc.utils import retrieve_dataset_names

# Get all datasets for a specific task
adme_datasets = retrieve_dataset_names('ADME')
tox_datasets = retrieve_dataset_names('Tox')
dti_datasets = retrieve_dataset_names('DTI')
hts_datasets = retrieve_dataset_names('HTS')
```

## 数据集统计

直接访问数据集统计：

```python
from tdc.single_pred import ADME
data = ADME(name='Caco2_Wang')

# Print basic statistics
data.print_stats()

# Get label distribution
data.label_distribution()
```

## 加载数据集

所有数据集遵循相同的加载模式：

```python
from tdc.<problem_type> import <TaskType>
data = <TaskType>(name='<DatasetName>')

# Get full dataset
df = data.get_data(format='df')  # or 'dict', 'DeepPurpose', etc.

# Get train/valid/test split
split = data.get_split(method='scaffold', seed=1, frac=[0.7, 0.1, 0.2])
```

## 注释

- 数据集大小和统计数据是近似值，可能会更新
- 新数据集定期添加到TDC
- 某些数据集可能需要额外的依赖项
- 检查官方TDC网站以获取最新的数据集列表： https://tdcommons.ai/overview/
