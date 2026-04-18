# Matchms 过滤函数参考

本文档提供了 matchms 中用于处理质谱数据的所有过滤函数的综合参考。

## 元数据处理过滤器

### 化合物和化学信息

* *add_compound_name(spectrum)**
- 将化合物名称添加到正确的元数据中字段
- 标准化化合物名称存储位置

* *clean_compound_name(spectrum)**
- 从化合物名称中删除常见的不需要的添加物
- 清除格式不一致

* *derive_adduct_from_name(spectrum)**
- 从化合物中提取加合物信息名称
- 将加合物符号移动到正确的元数据字段

* *derive_formula_from_name(spectrum)**
- 检测化合物名称中的化学式
- 将公式重新定位到适当的元数据字段

* *derive_annotation_from_compound_name(spectrum)**
- 使用化合物名称从PubChem检索SMILES/InChI
- 自动注释化学结构

### 化学结构转换

* *derive_inchi_from_smiles(spectrum)**
- 从SMILES字符串生成InChI
- 需要rdkit库

* *derive_inchikey_from_inchi(spectrum)**
- 从SMILES计算InChIKey InChI
- 27 字符散列标识符

* *derive_smiles_from_inchi(spectrum)**
- 从 InChI 表示创建 SMILES
- 需要 rdkit库

* *repair_inchi_inchikey_smiles(spectrum)**
- 更正放错位置的化学标识符
- 修复元数据字段混淆

* *repair_not_matching_annotation(spectrum)**
- 确保SMILES、InChI和InChIKey
- 验证化学结构注释匹配

* *add_fingerprint(spectrum, Fingerprint_type="daylight", nbits=2048, radius=2)**
- 生成用于相似性计算的分子指纹
- 指纹类型：“daylight”、“morgan1”、“morgan2”、“morgan3”
- 与指纹相似性评分一起使用

### 质量和电荷信息

* *add_precursor_mz(spectrum)**
- 标准化前体m/z值
- 标准化前体质量元数据

* *add_parent_mass(spectrum,estimate_from_adduct=True)**
- 根据前体m/z和加合物计算中性母体质量
- 可以估计加合物（如果不直接可用）

* * Correct_charge(spectrum)**
- 将电荷值与离子模式对齐
- 确保电荷符号与电离模式匹配

* *make_charge_int(spectrum)**
- 将电荷转换为整数格式
- 标准化电荷表示

* *clean_adduct(spectrum)**
- 标准化加合物符号
- 纠正常见的加合物格式问题

* *interpret_pepmass(spectrum)**
- 将pepmass字段解析为分量值
- 从组合中提取母体m/z和强度字段

### 离子模式和验证

* *derive_ionmode(spectrum)**
- 根据加合物信息确定离子模式
- 根据加合物类型推断正/负模式

* *require_ Correct_ionmode(spectrum, ion_mode)**
- 按指定过滤光谱ionmode
- 如果 ionmode 不匹配则返回 None
- 使用：`spectrum = require_correct_ionmode(spectrum, "positive")`

* *require_precursor_mz(spectrum,minimum_accepted_mz=0.0)**
- 验证前体 m/z 存在和值
- 如果缺失或低于则返回 None Threshold

* *require_precursor_below_mz(spectrum, Maximum_accepted_mz=1000.0)**
- 强制执行最大前体 m/z 限制
- 如果前体超过阈值，则返回 None

### 保留信息

* *add_retention_time(spectrum)**
- 将保留时间协调为浮点值
- 标准化 RT 元数据字段

* *add_retention_index(spectrum)**
- 在标准化字段中存储保留索引
- 标准化 RI 元数据

### 数据协调

* *harmonize_undefined_inchi(spectrum, undefined="", aliases=None)**
- 标准化未定义/空 InChI条目
- 用一致的值替换各种“未知”表示

* *harmonize_undefined_inchikey(spectrum, undefined="", aliases=None)**
- 标准化未定义/空的InChIKey条目
- 统一缺失数据表示

* *harmonize_undefined_smiles(spectrum, undefined="", aliases=None)**
- 标准化未定义/空的 SMILES 条目
- 缺失结构数据的一致处理

### 修复和质量功能

* *repair_adduct_based_on_smiles(spectrum, Mass_tolerance=0.1)**
- 纠正加合物使用 SMILES 和质量匹配
- 验证加合物与计算质量的匹配

* *repair_parent_mass_is_mol_wt(spectrum,mass_tolerance=0.1)**
- 将分子量转换为单同位素质量
- 修复通用元数据混淆

* *repair_precursor_is_parent_mass(spectrum)**
- 修复交换的前体/母体质量值
- 更正字段错误分配

* *repair_smiles_of_salts(spectrum,mass_tolerance=0.1)**
- 删除盐成分匹配母体质量
- 提取相关分子片段

* *require_parent_mass_match_smiles(spectrum,mass_tolerance=0.1)**
- 根据SMILES计算的质量验证母体质量
- 如果质量在范围内不匹配则返回None公差

* *require_valid_annotation(spectrum)**
- 确保完整、一致的化学注释
- 验证SMILES、InChI和InChIKey的存在和一致性

## 峰处理过滤器

### 归一化和选择

* *normalize_intensities(spectrum)**
- 将峰值强度缩放到单位高度（最大值= 1.0）
- 相似性计算的基本预处理步骤

* *select_by_intensity（spectrum，intensity_from=0.0，intensity_to=1.0）**
- 保留指定绝对强度范围内的峰
- 按原始强度值过滤

* *select_by_relative_intensity（spectrum，intensity_from=0.0，intensity_to=1.0）**
- 将峰保持在指定的绝对强度范围内相对强度范围
- 作为最大强度的分数进行过滤

* *select_by_mz(spectrum, mz_from=0.0, mz_to=1000.0)**
- 按 m/z 值范围过滤峰值
- 删除指定 m/z 窗口之外的峰值

### 峰值减少 &过滤

* *reduce_to_number_of_peaks(spectrum, n_max=None,ratio_desired=None)**
- 超过最大值时删除最低强度峰值
- 可以指定绝对数量或比率
- 使用： `spectrum = reduce_to_number_of_peaks(spectrum, n_max=100)`

* *remove_peaks_around_precursor_mz(spectrum, mz_tolerance=17)**
- 消除前体容差内的峰
- 删除前体和同位素峰
- 基于片段的通用预处理相似性

* *remove_peaks_outside_top_k(spectrum, k=10,ratio_desired=None)**
- 仅保留k个最高强度峰附近的峰
- 专注于最具信息性的信号

* *require_minimum_number_of_peaks(spectrum, n_required=10)**
- 丢弃峰值不足的光谱
- 质量控制过滤器
- 如果峰值计数低于阈值则返回 None

* *require_minimum_number_of_high_peaks(spectrum, n_required=5, Intensity_threshold=0.05)**
- 删除光谱缺少高强度峰值
- 确保数据质量
- 如果高于阈值的峰值不足，则返回“无”

### 损失计算

* *add_losses(spectrum, loss_mz_from=5.0, loss_mz_to=200.0)**
- 从中得出中性损失前体质量
- 计算损失 = 前体_mz - 片段_mz
- 将损失添加到谱图以进行中性损失余弦评分

## 管道函数

* *default_filters(spectrum)**
- 按顺序应用九个基本元数据过滤器：
  1. make_charge_int
  2. add_precursor_mz
  3. add_retention_time
  4. add_retention_index
  5. derive_adduct_from_name
  6. derive_formula_from_name
  7. clean_compound_name
  8. harmonize_undefined_smiles
  9. harmonize_undefined_inchi
  - 建议的元数据起点协调

* *SpectrumProcessor（滤波器）**
- 协调多滤波器管道
- 接受滤波器函数列表
- 示例：
```python
from matchms import SpectrumProcessor
processor = SpectrumProcessor([
    default_filters,
    normalize_intensities,
    lambda s: select_by_relative_intensity(s, intensity_from=0.01)
])
processed = processor(spectrum)
```

## 常见滤波器组合

### 标准预处理流程
```python
from matchms.filtering import (default_filters, normalize_intensities,
                               select_by_relative_intensity,
                               require_minimum_number_of_peaks)

spectrum = default_filters(spectrum)
spectrum = normalize_intensities(spectrum)
spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01)
spectrum = require_minimum_number_of_peaks(spectrum, n_required=5)
```

### 质量控制流程
```python
from matchms.filtering import (require_precursor_mz, require_minimum_number_of_peaks,
                               require_minimum_number_of_high_peaks)

spectrum = require_precursor_mz(spectrum, minimum_accepted_mz=50.0)
if spectrum is None:
    # Spectrum failed quality control
    pass
spectrum = require_minimum_number_of_peaks(spectrum, n_required=10)
spectrum = require_minimum_number_of_high_peaks(spectrum, n_required=5)
```

### 化学注释流程
```python
from matchms.filtering import (derive_inchi_from_smiles, derive_inchikey_from_inchi,
                               add_fingerprint, require_valid_annotation)

spectrum = derive_inchi_from_smiles(spectrum)
spectrum = derive_inchikey_from_inchi(spectrum)
spectrum = add_fingerprint(spectrum, fingerprint_type="morgan2", nbits=2048)
spectrum = require_valid_annotation(spectrum)
```

### 峰清洗Pipeline
```python
from matchms.filtering import (normalize_intensities, remove_peaks_around_precursor_mz,
                               select_by_relative_intensity, reduce_to_number_of_peaks)

spectrum = normalize_intensities(spectrum)
spectrum = remove_peaks_around_precursor_mz(spectrum, mz_tolerance=17)
spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01)
spectrum = reduce_to_number_of_peaks(spectrum, n_max=200)
```

## 过滤器使用注意事项

1. **顺序很重要**：按逻辑顺序应用过滤器（例如，在相对强度选择之前进行归一化）
2. **过滤器返回 None**：许多过滤器对于无效光谱返回 None；在继续之前检查 None 
3. **不变性**：过滤器通常返回修改后的副本；将结果重新分配给变量
4. **管道效率**：使用 SpectrumProcessor 进行一致的多光谱处理
5. **文档**：详细参数请参见matchms.readthedocs.io/en/latest/api/matchms.filtering.html
