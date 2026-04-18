# CZ CELLxGENE 人口普查数据架构参考

## 概述

CZ CELLxGENE 人口普查是构建在 TileDB-SOMA 框架上的单细胞数据的版本集合。本参考记录了数据结构、可用元数据字段和查询语法。

## 高级结构

人口普查组织为 `SOMACollection`，具有两个主要组件：

### 1. census_info
摘要信息包括：
- **摘要**：构建日期、单元格计数、数据集stats
- **数据集**：来自 CELLxGENE Discover 的所有数据集和元数据
- **summary_cell_counts**：按元数据类别分层的细胞计数

### 2. census_data
生物体特定的 `SOMAExperiment` 对象：
- **“homo_sapiens”**：人类单细胞数据
- **“mus_musculus”**：小鼠单细胞数据

## 每个生物体的数据结构

每个生物体实验包含：

### obs（细胞元数据）
细胞级注释存储为 `SOMADataFrame`。通过以下方式访问：
```python
census["census_data"]["homo_sapiens"].obs
```

### ms["RNA"]（测量）
RNA 测量数据包括：
- **X**：带层的数据矩阵：
  - `raw`：原始计数数据
  - `normalized`：（如果可用）标准化计数
- **var**：基因元数据
- **feature_dataset_presence_matrix**：稀疏布尔数组显示每个数据集中测量了哪些基因

## 细胞元数据字段（obs）

### 必填/核心字段

* *身份和数据集：**
- `soma_joinid`：连接的唯一整数标识符
- `dataset_id`：源数据集标识符
- `is_primary_data`：布尔标志（True = 唯一单元格，False = 跨数据集重复）

* *单元格类型：**
- `cell_type`：人类可读的细胞类型名称
- `cell_type_ontology_term_id`：标准化本体术语（例如“CL：0000236”）

* *组织：**
- `tissue`：特定组织名称
- `tissue_general`：更广泛的组织类别（用于分组）
- `tissue_ontology_term_id`：标准化本体术语

* *检测：**
- `assay`：使用的测序技术
- `assay_ontology_term_id`：标准化本体术语

* *疾病：**
- `disease`：疾病状态或状况
- `disease_ontology_term_id`：标准化本体术语

* *供体：**
- `donor_id`：唯一的捐赠者标识符
- `sex`：生物性别（男、女、未知） 
- `self_reported_ethnicity`：种族信息
- `development_stage`：生命阶段（成人、儿童、胚胎等）
- `development_stage_ontology_term_id`：标准化本体术语

* *生物：**
- `organism`：学名（智人、小家鼠）
- `organism_ontology_term_id`：标准化本体术语

* *技术：**
- `suspension_type`：样品制备类型（细胞、细胞核、na）

## 基因元数据字段（var）

通过以下方式访问：
```python
census["census_data"]["homo_sapiens"].ms["RNA"].var
```

* *可用字段：**
- `soma_joinid`：连接的唯一整数标识符
- `feature_id`：Ensembl 基因 ID（例如， "ENSG00000161798")
- `feature_name`：基因符号（例如，"FOXP2"）
- `feature_length`：碱基对中的基因长度

## 值过滤语法

查询使用类似Python的表达式进行过滤。语法由TileDB-SOMA处理。

### 比较运算符
- `==`：等于
- `!=`：不等于
- `<`、`>`、`<=`、 `>=`：数字比较
- `in`：成员资格测试（例如，`feature_id in ['ENSG00000161798', 'ENSG00000188229']`）

### 逻辑运算符
- `and`、`&`：逻辑AND
- `or`、`|`：逻辑 OR

### 示例

* *单个条件：**
```python
value_filter="cell_type == 'B cell'"
```

* *使用 AND 的多个条件：**
```python
value_filter="cell_type == 'B cell' and tissue_general == 'lung' and is_primary_data == True"
```

* *使用 IN 表示多个值：**
```python
value_filter="tissue in ['lung', 'liver', 'kidney']"
```

* *复杂条件：**
```python
value_filter="(cell_type == 'neuron' or cell_type == 'astrocyte') and disease != 'normal'"
```

* *过滤基因：**
```python
var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19']"
```

## 数据包含标准

人口普查包括来自CZ CELLxGENE Discover会议的所有数据：

1. **物种**：人类 (*Homo sapiens*)或小鼠 (*Mus musculus*)
2. **技术**：已批准的 RNA
3 测序技术。 **计数类型**：仅原始计数（无处理/仅标准化数据）
4. **元数据**：按照 CELLxGENE 模式 
5 进行标准化。 **空间和非空间数据**：包括传统和空间转录组学

## 重要数据特征

### 重复细胞
细胞可能出现在多个数据集中。在大多数分析中使用 `is_primary_data == True` 过滤独特的细胞。

### 计数类型
人口普查包括：
- **分子计数**：来自基于 UMI 的方法
- **全基因测序读取计数**：来自非 UMI 方法
这些可能需要不同的标准化方法。

### 版本控制
Census 版本已版本化（例如，“2023-07-25”、“稳定”）。始终指定可重复分析的版本：
```python
census = cellxgene_census.open_soma(census_version="2023-07-25")
```

## 数据集存在矩阵

访问每个数据集中测量的基因：
```python
presence_matrix = census["census_data"]["homo_sapiens"].ms["RNA"]["feature_dataset_presence_matrix"]
```

此稀疏布尔矩阵有助于理解：
- 基因覆盖率数据集
- 包含哪些数据集用于特定基因分析
- 与基因覆盖率相关的技术批次效应

## SOMA 对象类型

使用的核心 TileDB-SOMA 对象：
- **DataFrame**：表格数据（obs、var）
- **SparseNDArray**：稀疏矩阵（X 层、存在矩阵）
- **DenseNDArray**：密集数组（不太常见）
- **集合**：相关对象的容器
- **实验**：用于测量的顶级容器
- **SOMAScene**：空间转录组场景
- **obs_spatial_presence**：空间数据可用性
