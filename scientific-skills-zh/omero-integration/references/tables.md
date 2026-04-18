# OMERO Tables

此参考涵盖使用 OMERO.tables 在 OMERO 中创建和管理结构化表格数据。

## OMERO.tables 概述

OMERO.tables 提供了一种存储与 OMERO 对象关联的结构化表格数据的方法。表存储为 HDF5 文件，可以高效查询。常见用例包括：

- 存储图像的定量测量值
- 记录分析结果
- 跟踪实验元数据
- 将测量值链接到特定图像或 ROI

## 列类型

OMERO.tables 支持各种列类型：

- **长列**：整数值（64 位）
- **DoubleColumn**：浮点值
- **StringColumn**：文本数据（固定最大长度）
- **BoolColumn**：布尔值
- **LongArrayColumn**：整数数组
- **DoubleArrayColumn**：数组floats
- **FileColumn**：对 OMERO 文件的引用
- **ImageColumn**：对 OMERO 图像的引用
- **RoiColumn**：对 OMERO ROI 的引用
- **WellColumn**：对 OMERO 井的引用

## 创建表

### 基本建表

```python
from random import random
import omero.grid

# Create unique table name
table_name = f"MyAnalysisTable_{random()}"

# Define columns (empty data for initialization)
col1 = omero.grid.LongColumn('ImageID', 'Image identifier', [])
col2 = omero.grid.DoubleColumn('MeanIntensity', 'Mean pixel intensity', [])
col3 = omero.grid.StringColumn('Category', 'Classification', 64, [])

columns = [col1, col2, col3]

# Get resources and create table
resources = conn.c.sf.sharedResources()
repository_id = resources.repositories().descriptions[0].getId().getValue()
table = resources.newTable(repository_id, table_name)

# Initialize table with column definitions
table.initialize(columns)
```

### 向表中添加数据

```python
# Prepare data
image_ids = [1, 2, 3, 4, 5]
intensities = [123.4, 145.2, 98.7, 156.3, 132.8]
categories = ["Good", "Good", "Poor", "Excellent", "Good"]

# Create data columns
data_col1 = omero.grid.LongColumn('ImageID', 'Image identifier', image_ids)
data_col2 = omero.grid.DoubleColumn('MeanIntensity', 'Mean pixel intensity', intensities)
data_col3 = omero.grid.StringColumn('Category', 'Classification', 64, categories)

data = [data_col1, data_col2, data_col3]

# Add data to table
table.addData(data)

# Get file reference
orig_file = table.getOriginalFile()
table.close()  # Always close table when done
```

### 将表链接到数据集

```python
# Create file annotation from table
orig_file_id = orig_file.id.val
file_ann = omero.model.FileAnnotationI()
file_ann.setFile(omero.model.OriginalFileI(orig_file_id, False))
file_ann = conn.getUpdateService().saveAndReturnObject(file_ann)

# Link to dataset
link = omero.model.DatasetAnnotationLinkI()
link.setParent(omero.model.DatasetI(dataset_id, False))
link.setChild(omero.model.FileAnnotationI(file_ann.getId().getValue(), False))
conn.getUpdateService().saveAndReturnObject(link)

print(f"Linked table to dataset {dataset_id}")
```

## 详细列类型

### Long列（整数）

```python
# Column for integer values
image_ids = [101, 102, 103, 104, 105]
col = omero.grid.LongColumn('ImageID', 'Image identifier', image_ids)
```

### 双列（浮点数）

```python
# Column for floating-point values
measurements = [12.34, 56.78, 90.12, 34.56, 78.90]
col = omero.grid.DoubleColumn('Measurement', 'Value in microns', measurements)
```

### 字符串列（文本）

```python
# Column for text (max length required)
labels = ["Control", "Treatment A", "Treatment B", "Control", "Treatment A"]
col = omero.grid.StringColumn('Condition', 'Experimental condition', 64, labels)
```

### 布尔值列

```python
# Column for boolean values
flags = [True, False, True, True, False]
col = omero.grid.BoolColumn('QualityPass', 'Passes quality control', flags)
```

### 图像列（对图像的引用）

```python
# Column linking to OMERO images
image_ids = [101, 102, 103, 104, 105]
col = omero.grid.ImageColumn('Image', 'Source image', image_ids)
```

### ROI 列（对ROI 的引用）

```python
# Column linking to OMERO ROIs
roi_ids = [201, 202, 203, 204, 205]
col = omero.grid.RoiColumn('ROI', 'Associated ROI', roi_ids)
```

### 数组列

```python
# Column for arrays of doubles
histogram_data = [
    [10, 20, 30, 40],
    [15, 25, 35, 45],
    [12, 22, 32, 42]
]
col = omero.grid.DoubleArrayColumn('Histogram', 'Intensity histogram', histogram_data)

# Column for arrays of longs
bin_counts = [[5, 10, 15], [8, 12, 16], [6, 11, 14]]
col = omero.grid.LongArrayColumn('Bins', 'Histogram bins', bin_counts)
```

## 读取表数据

### 打开现有表

```python
# Get table file by name
orig_table_file = conn.getObject("OriginalFile",
                                 attributes={'name': table_name})

# Open table
resources = conn.c.sf.sharedResources()
table = resources.openTable(orig_table_file._obj)

print(f"Opened table: {table.getOriginalFile().getName().getValue()}")
print(f"Number of rows: {table.getNumberOfRows()}")
```

### 读取所有数据

```python
# Get column headers
print("Columns:")
for col in table.getHeaders():
    print(f"  {col.name}: {col.description}")

# Read all data
row_count = table.getNumberOfRows()
data = table.readCoordinates(range(row_count))

# Display data
for col in data.columns:
    print(f"\nColumn: {col.name}")
    for value in col.values:
        print(f"  {value}")

table.close()
```

### 读取特定数据行

```python
# Read rows 10-20
start = 10
stop = 20
data = table.read(list(range(table.getHeaders().__len__())), start, stop)

for col in data.columns:
    print(f"Column: {col.name}")
    for value in col.values:
        print(f"  {value}")
```

### 读取特定列

```python
# Read only columns 0 and 2
column_indices = [0, 2]
start = 0
stop = table.getNumberOfRows()

data = table.read(column_indices, start, stop)

for col in data.columns:
    print(f"Column: {col.name}")
    print(f"Values: {col.values}")
```

## 查询表

### 带条件查询

```python
# Query rows where MeanIntensity > 100
row_count = table.getNumberOfRows()

query_rows = table.getWhereList(
    "(MeanIntensity > 100)",
    variables={},
    start=0,
    stop=row_count,
    step=0
)

print(f"Found {len(query_rows)} matching rows")

# Read matching rows
data = table.readCoordinates(query_rows)

for col in data.columns:
    print(f"\n{col.name}:")
    for value in col.values:
        print(f"  {value}")
```

### 复杂查询

```python
# Multiple conditions with AND
query_rows = table.getWhereList(
    "(MeanIntensity > 100) & (MeanIntensity < 150)",
    variables={},
    start=0,
    stop=row_count,
    step=0
)

# Multiple conditions with OR
query_rows = table.getWhereList(
    "(Category == 'Good') | (Category == 'Excellent')",
    variables={},
    start=0,
    stop=row_count,
    step=0
)

# String matching
query_rows = table.getWhereList(
    "(Category == 'Good')",
    variables={},
    start=0,
    stop=row_count,
    step=0
)
```

## 完整示例：图像分析结果

```python
from omero.gateway import BlitzGateway
import omero.grid
import omero.model
import numpy as np

HOST = 'omero.example.com'
PORT = 4064
USERNAME = 'user'
PASSWORD = 'pass'

with BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT) as conn:
    # Get dataset
    dataset = conn.getObject("Dataset", dataset_id)
    print(f"Analyzing dataset: {dataset.getName()}")

    # Collect measurements from images
    image_ids = []
    mean_intensities = []
    max_intensities = []
    cell_counts = []

    for image in dataset.listChildren():
        image_ids.append(image.getId())

        # Get pixel data
        pixels = image.getPrimaryPixels()
        plane = pixels.getPlane(0, 0, 0)  # Z=0, C=0, T=0

        # Calculate statistics
        mean_intensities.append(float(np.mean(plane)))
        max_intensities.append(float(np.max(plane)))

        # Simulate cell count (would be from actual analysis)
        cell_counts.append(np.random.randint(50, 200))

    # Create table
    table_name = f"Analysis_Results_{dataset.getId()}"

    # Define columns
    col1 = omero.grid.ImageColumn('Image', 'Source image', [])
    col2 = omero.grid.DoubleColumn('MeanIntensity', 'Mean pixel value', [])
    col3 = omero.grid.DoubleColumn('MaxIntensity', 'Maximum pixel value', [])
    col4 = omero.grid.LongColumn('CellCount', 'Number of cells detected', [])

    # Initialize table
    resources = conn.c.sf.sharedResources()
    repository_id = resources.repositories().descriptions[0].getId().getValue()
    table = resources.newTable(repository_id, table_name)
    table.initialize([col1, col2, col3, col4])

    # Add data
    data_col1 = omero.grid.ImageColumn('Image', 'Source image', image_ids)
    data_col2 = omero.grid.DoubleColumn('MeanIntensity', 'Mean pixel value',
                                        mean_intensities)
    data_col3 = omero.grid.DoubleColumn('MaxIntensity', 'Maximum pixel value',
                                        max_intensities)
    data_col4 = omero.grid.LongColumn('CellCount', 'Number of cells detected',
                                      cell_counts)

    table.addData([data_col1, data_col2, data_col3, data_col4])

    # Get file and close table
    orig_file = table.getOriginalFile()
    table.close()

    # Link to dataset
    orig_file_id = orig_file.id.val
    file_ann = omero.model.FileAnnotationI()
    file_ann.setFile(omero.model.OriginalFileI(orig_file_id, False))
    file_ann = conn.getUpdateService().saveAndReturnObject(file_ann)

    link = omero.model.DatasetAnnotationLinkI()
    link.setParent(omero.model.DatasetI(dataset_id, False))
    link.setChild(omero.model.FileAnnotationI(file_ann.getId().getValue(), False))
    conn.getUpdateService().saveAndReturnObject(link)

    print(f"Created and linked table with {len(image_ids)} rows")

    # Query results
    table = resources.openTable(orig_file)

    high_cell_count_rows = table.getWhereList(
        "(CellCount > 100)",
        variables={},
        start=0,
        stop=table.getNumberOfRows(),
        step=0
    )

    print(f"Images with >100 cells: {len(high_cell_count_rows)}")

    # Read those rows
    data = table.readCoordinates(high_cell_count_rows)
    for i in range(len(high_cell_count_rows)):
        img_id = data.columns[0].values[i]
        count = data.columns[3].values[i]
        print(f"  Image {img_id}: {count} cells")

    table.close()
```

## 从对象中检索表

### 查找附加到数据集的表

```python
# Get dataset
dataset = conn.getObject("Dataset", dataset_id)

# List file annotations
for ann in dataset.listAnnotations():
    if isinstance(ann, omero.gateway.FileAnnotationWrapper):
        file_obj = ann.getFile()
        file_name = file_obj.getName()

        # Check if it's a table (might have specific naming pattern)
        if "Table" in file_name or file_name.endswith(".h5"):
            print(f"Found table: {file_name} (ID: {file_obj.getId()})")

            # Open and inspect
            resources = conn.c.sf.sharedResources()
            table = resources.openTable(file_obj._obj)

            print(f"  Rows: {table.getNumberOfRows()}")
            print(f"  Columns:")
            for col in table.getHeaders():
                print(f"    {col.name}")

            table.close()
```

## 更新表

### 追加行

```python
# Open existing table
resources = conn.c.sf.sharedResources()
table = resources.openTable(orig_file._obj)

# Prepare new data
new_image_ids = [106, 107]
new_intensities = [88.9, 92.3]
new_categories = ["Good", "Excellent"]

# Create data columns
data_col1 = omero.grid.LongColumn('ImageID', '', new_image_ids)
data_col2 = omero.grid.DoubleColumn('MeanIntensity', '', new_intensities)
data_col3 = omero.grid.StringColumn('Category', '', 64, new_categories)

# Append data
table.addData([data_col1, data_col2, data_col3])

print(f"New row count: {table.getNumberOfRows()}")
table.close()
```

## 删除表

### 删除表文件

```python
# Get file object
orig_file = conn.getObject("OriginalFile", file_id)

# Delete file (also deletes table)
conn.deleteObjects("OriginalFile", [file_id], wait=True)
print(f"Deleted table file {file_id}")
```

### 从对象中取消链接表

```python
# Find annotation links
dataset = conn.getObject("Dataset", dataset_id)

for ann in dataset.listAnnotations():
    if isinstance(ann, omero.gateway.FileAnnotationWrapper):
        if "Table" in ann.getFile().getName():
            # Delete link (keeps table, removes association)
            conn.deleteObjects("DatasetAnnotationLink",
                             [ann.link.getId()],
                             wait=True)
            print(f"Unlinked table from dataset")
```

## 最佳实践

1. **描述性名称**：使用有意义的表和列名称
2. **关闭表**：使用
3后始终关闭表。 **字符串长度**：为字符串列
4 设置适当的最大长度。 **链接到对象**：将表附加到相关数据集或项目
5. **使用引用**：使用 ImageColumn、RoiColumn 进行对象引用
6. **高效查询**：使用 getWhereList()而不是读取所有数据
7. **文档**：向列
8 添加描述。 **版本控制**：在表名称或元数据中包含版本信息
9. **批量操作**：批量添加数据以获得更好的性能
10. **错误处理**：检查无返回并处理异常

## 常见模式

### ROI测量表

```python
# Table structure for ROI measurements
columns = [
    omero.grid.ImageColumn('Image', 'Source image', []),
    omero.grid.RoiColumn('ROI', 'Measured ROI', []),
    omero.grid.LongColumn('ChannelIndex', 'Channel number', []),
    omero.grid.DoubleColumn('Area', 'ROI area in pixels', []),
    omero.grid.DoubleColumn('MeanIntensity', 'Mean intensity', []),
    omero.grid.DoubleColumn('IntegratedDensity', 'Sum of intensities', []),
    omero.grid.StringColumn('CellType', 'Cell classification', 32, [])
]
```

### 时间序列数据表

```python
# Table structure for time series measurements
columns = [
    omero.grid.ImageColumn('Image', 'Time series image', []),
    omero.grid.LongColumn('Timepoint', 'Time index', []),
    omero.grid.DoubleColumn('Timestamp', 'Time in seconds', []),
    omero.grid.DoubleColumn('Value', 'Measured value', []),
    omero.grid.StringColumn('Measurement', 'Type of measurement', 64, [])
]
```

### 筛选结果表

```python
# Table structure for screening plate analysis
columns = [
    omero.grid.WellColumn('Well', 'Plate well', []),
    omero.grid.LongColumn('FieldIndex', 'Field number', []),
    omero.grid.DoubleColumn('CellCount', 'Number of cells', []),
    omero.grid.DoubleColumn('Viability', 'Percent viable', []),
    omero.grid.StringColumn('Phenotype', 'Observed phenotype', 128, []),
    omero.grid.BoolColumn('Hit', 'Hit in screen', [])
]
```
