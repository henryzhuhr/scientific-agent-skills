# IDC 索引表指南

* *测试使用：** idc-index 0.11.14（IDC 数据版本 v23）

本指南涵盖 IDC 索引表的结构和访问模式：编程模式发现、DataFrame 访问和连接列引用。有关可用表及其用途的概述，请参阅主 SKILL.md.

* * 完整索引表文档中的“索引表”部分：** https://idc-index.readthedocs.io/en/latest/indices_reference.html

## 何时使用本指南

当您需要时加载本指南：
 - 发现表模式和列类型以编程方式
- 作为 pandas DataFrame 访问索引表（不通过 SQL）
- 了解关键列和表之间的联接关系

有关 SQL 查询示例（过滤器发现、查找注释、大小估计），请参阅 `references/sql_patterns.md`.

## 先决条件

```bash
pip install --upgrade idc-index
```

## 访问索引表

### 通过SQL（推荐用于过滤/聚合）

```python
from idc_index import IDCClient
client = IDCClient()

# Query the primary index (always available)
results = client.sql_query("SELECT * FROM index WHERE Modality = 'CT' LIMIT 10")

# Fetch and query additional indices
client.fetch_index("collections_index")
collections = client.sql_query("SELECT collection_id, CancerTypes, TumorLocations FROM collections_index")

client.fetch_index("analysis_results_index")
analysis = client.sql_query("SELECT * FROM analysis_results_index LIMIT 5")
```

### 作为pandas DataFrames（直接访问）

```python
# Primary index (always available after client initialization)
df = client.index

# Fetch and access on-demand indices
client.fetch_index("sm_index")
sm_df = client.sm_index
```

## 发现表模式

The `indices_overview` 字典包含所有表的完整架构信息。 **在编写查询或探索数据结构时，请务必参考此内容。**

* *DICOM 属性映射：** 许多列直接从源文件中的 DICOM 属性填充。架构中的列描述指示列何时对应于 DICOM 属性（例如，“DICOM 模态属性”或引用 DICOM 标签）。这允许在查询时利用 DICOM 知识 - 标准 DICOM 属性名称（如 `PatientID`、`StudyInstanceUID`、`Modality`、`BodyPartExamined`）按预期工作。

```python
from idc_index import IDCClient
client = IDCClient()

# List all available indices with descriptions
for name, info in client.indices_overview.items():
    print(f"\n{name}:")
    print(f"  Installed: {info['installed']}")
    print(f"  Description: {info['description']}")

# Get complete schema for a specific index (columns, types, descriptions)
schema = client.indices_overview["index"]["schema"]
print(f"\nTable: {schema['table_description']}")
print("\nColumns:")
for col in schema['columns']:
    desc = col.get('description', 'No description')
    # Description indicates if column is from DICOM attribute
    print(f"  {col['name']} ({col['type']}): {desc}")

# Find columns that are DICOM attributes (check description for "DICOM" reference)
dicom_cols = [c['name'] for c in schema['columns'] if 'DICOM' in c.get('description', '').upper()]
print(f"\nDICOM-sourced columns: {dicom_cols}")
```

 * *替代方案：使用 `get_index_schema()`方法：**
```python
schema = client.get_index_schema("index")
# Returns same schema dict: {'table_description': ..., 'columns': [...]}
```

## 关键列参考

主 `index` 表中最常见的列（使用 `indices_overview` 获取完整列表和说明）：

|专栏 |类型 | DICOM |描述 |
|--------|------|--------|-------------|
| `collection_id` |字符串 |没有 | IDC集合标识符|
| `analysis_result_id` |字符串 |没有 |如果适用，指示给定系列的分析结果集合是 |
| 的一部分`source_DOI` |字符串 |没有 | DOI 链接到数据集详细信息；用于了解有关内容的更多信息和归属（参见下面的引用）|
| `PatientID` |字符串 |是的 |患者标识符|
| `StudyInstanceUID` |字符串 |是的 | DICOM 研究 UID |
| `SeriesInstanceUID` |字符串 |是的 | DICOM 系列 UID — 用于下载/查看 |
| `Modality` |字符串 |是的 |成像模式（CT、MR、PT、SM、SEG、ANN、RTSTRUCT 等）|
| `BodyPartExamined` |字符串 |是的 |解剖区域|
| `SeriesDescription` |字符串 |是的 |系列说明|
| `Manufacturer` |字符串 |是的 |设备制造商|
| `StudyDate` |字符串 |是的 |研究进行日期 |
| `PatientSex` |字符串 |是的 |患者性别|
| `PatientAge` |字符串 |是的 |研究时患者年龄|
| `license_short_name` |字符串 |没有 |许可证类型（CC BY 4.0、CC BY-NC 4.0 等）|
| `series_size_MB` |浮动|没有 |系列大小（兆字节）|
| `instanceCount` |整数|没有 |系列中 DICOM 实例的数量 |
| `SOPClassUID` |字符串 |是的 | DICOM SOP 类 UID（标识对象/服务类，例如 CT 图像存储）|
| `TransferSyntaxUID` |字符串 |是的 | DICOM 传输语法 UID（编码/压缩方法）|

* *DICOM = 是**：从具有相同名称的 DICOM 属性中提取的列值。有关数字标签映射，请参阅 [DICOM 标准](https://dicom.nema.org/medical/dicom/current/output/chtml/part06/chapter_6.html)。使用标准 DICOM 知识来获取预期值和格式。

## 连接列参考

使用此表来标识索引表之间的连接列。在 SQL 中使用表之前始终调用 `client.fetch_index("table_name")`。

|表A |表 B |加入条件 |
|---------|---------|----------------|
| `index` | `collections_index` | `index.collection_id = collections_index.collection_id` |
| `index` | `sm_index` | `index.SeriesInstanceUID = sm_index.SeriesInstanceUID` |
| `index` | `seg_index` | `index.SeriesInstanceUID = seg_index.segmented_SeriesInstanceUID` |
| `index` | `ann_index` | `index.SeriesInstanceUID = ann_index.SeriesInstanceUID` |
| `ann_index` | `ann_group_index` | `ann_index.SeriesInstanceUID = ann_group_index.SeriesInstanceUID` |
| `index` | `clinical_index` | `index.collection_id = clinical_index.collection_id`（然后按患者过滤）|
| `index` | `contrast_index` | `index.SeriesInstanceUID = contrast_index.SeriesInstanceUID` |
| `index` | `volume_geometry_index` | `index.SeriesInstanceUID = volume_geometry_index.SeriesInstanceUID` |
| `index` | `rtstruct_index` | `index.SeriesInstanceUID = rtstruct_index.SeriesInstanceUID` |
| `rtstruct_index` | `index`（源图像）| `rtstruct_index.referenced_SeriesInstanceUID = index.SeriesInstanceUID` |

有关使用这些联接的完整查询示例，请参阅 `references/sql_patterns.md`.

## 故障排除

* *问题：** 在表中找不到列
- **原因：** 列名称拼写错误或该表中不存在
- **解决方案：**使用`client.indices_overview["table_name"]["schema"]["columns"]`列出可用列

  * *问题：** DataFrame访问返回None
- **原因：**索引未获取或属性名称不正确
- **解决方案：**先使用`client.fetch_index()`获取，然后通过与索引名称匹配的属性访问

## 资源

- 完整索引表文档：https://idc-index.readthedocs.io/en/latest/indices_reference.html
- `references/sql_patterns.md` 用于使用这些表的查询示例
- `references/clinical_data_guide.md` 用于临床数据工作流程
- `references/digital_pathology_guide.md` 用于病理特定指数
