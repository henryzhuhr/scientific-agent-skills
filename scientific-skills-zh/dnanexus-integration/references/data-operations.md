# DNAnexus 数据操作

## 概述

DNAnexus 为文件、记录、数据库和其他数据对象提供全面的数据管理功能。所有数据操作都可以通过Python SDK（dxpy）或命令行界面（dx）执行。

## 数据对象类型

### 文件
平台上存储的二进制或文本数据。

### 记录
具有任意JSON详细信息和元数据的结构化数据对象。

### 数据库
关系数据的结构化数据库对象。

### 小程序和应用程序
可执行程序（在app-development.md中介绍）。

### 工作流程
多步骤分析管道。

## 数据对象生命周期

### 状态

* *打开状态**：可以修改数据
- 文件：可以写入内容
- 记录：可以更新详细信息
- 小程序：默认在关闭状态下创建

* *关闭状态**：数据变得不可变
- 文件内容是固定
- 元数据字段被锁定（类型、详细信息、链接、可见性）
- 对象已准备好共享和分析

### 转换

```
Create (open) → Modify → Close (immutable)
```

大多数对象开始打开并需要显式闭包：
```python
# Close a file
file_obj.close()
```

一些对象可以在一次操作中创建和关闭：
```python
# Create closed record
record = dxpy.new_dxrecord(details={...}, close=True)
```

## 文件操作

### 上传文件

* *来自本地文件**:
```python
import dxpy

# Upload a file
file_obj = dxpy.upload_local_file("data.txt", project="project-xxxx")
print(f"Uploaded: {file_obj.get_id()}")
```

* *带元数据**:
```python
file_obj = dxpy.upload_local_file(
    "data.txt",
    name="my_data",
    project="project-xxxx",
    folder="/results",
    properties={"sample": "sample1", "type": "raw"},
    tags=["experiment1", "batch2"]
)
```

* *流式上传**:
```python
# For large files or generated data
file_obj = dxpy.new_dxfile(project="project-xxxx", name="output.txt")
file_obj.write("Line 1\n")
file_obj.write("Line 2\n")
file_obj.close()
```

### 下载文件

* *到本地文件**:
```python
# Download by ID
dxpy.download_dxfile("file-xxxx", "local_output.txt")

# Download using handler
file_obj = dxpy.DXFile("file-xxxx")
dxpy.download_dxfile(file_obj.get_id(), "local_output.txt")
```

* *读取文件内容**:
```python
file_obj = dxpy.DXFile("file-xxxx")
with file_obj.open_file() as f:
    contents = f.read()
```

* *下载到特定目录**:
```python
dxpy.download_dxfile("file-xxxx", "/path/to/directory/filename.txt")
```

### 文件元数据

* *获取文件信息**：
```python
file_obj = dxpy.DXFile("file-xxxx")
describe = file_obj.describe()

print(f"Name: {describe['name']}")
print(f"Size: {describe['size']} bytes")
print(f"State: {describe['state']}")
print(f"Created: {describe['created']}")
```

* *更新文件元数据**：
```python
file_obj.set_properties({"experiment": "exp1", "version": "v2"})
file_obj.add_tags(["validated", "published"])
file_obj.rename("new_name.txt")
```

## 记录操作

记录使用任意JSON存储结构化元数据。

### 创建记录

```python
# Create a record
record = dxpy.new_dxrecord(
    name="sample_metadata",
    types=["SampleMetadata"],
    details={
        "sample_id": "S001",
        "tissue": "blood",
        "age": 45,
        "conditions": ["diabetes"]
    },
    project="project-xxxx",
    close=True
)
```

### 读取记录

```python
record = dxpy.DXRecord("record-xxxx")
describe = record.describe()

# Access details
details = record.get_details()
sample_id = details["sample_id"]
tissue = details["tissue"]
```

### 更新记录

```python
# Record must be open to update
record = dxpy.DXRecord("record-xxxx")
details = record.get_details()
details["processed"] = True
record.set_details(details)
record.close()
```

## 搜索和发现

### 查找数据对象

* *按名称搜索**:
```python
results = dxpy.find_data_objects(
    name="*.fastq",
    project="project-xxxx",
    folder="/raw_data"
)

for result in results:
    print(f"{result['describe']['name']}: {result['id']}")
```

* *按属性搜索**:
```python
results = dxpy.find_data_objects(
    classname="file",
    properties={"sample": "sample1", "type": "processed"},
    project="project-xxxx"
)
```

* *按类型搜索**:
```python
# Find all records of specific type
results = dxpy.find_data_objects(
    classname="record",
    typename="SampleMetadata",
    project="project-xxxx"
)
```

* *按状态搜索过滤**：
```python
# Find only closed files
results = dxpy.find_data_objects(
    classname="file",
    state="closed",
    project="project-xxxx"
)
```

### 系统范围搜索

```python
# Search across all accessible projects
results = dxpy.find_data_objects(
    name="important_data.txt",
    describe=True  # Include full descriptions
)
```

## 克隆和复制

### 在项目之间克隆数据

```python
# Clone file to another project
new_file = dxpy.DXFile("file-xxxx").clone(
    project="project-yyyy",
    folder="/imported_data"
)
```

### 克隆多个对象

```python
# Clone folder contents
files = dxpy.find_data_objects(
    classname="file",
    project="project-xxxx",
    folder="/results"
)

for file in files:
    file_obj = dxpy.DXFile(file['id'])
    file_obj.clone(project="project-yyyy", folder="/backup")
```

## 项目管理

### 创建项目

```python
# Create a new project
project = dxpy.api.project_new({
    "name": "My Analysis Project",
    "description": "RNA-seq analysis for experiment X"
})

project_id = project['id']
```

### 项目权限

```python
# Invite user to project
dxpy.api.project_invite(
    project_id,
    {
        "invitee": "user-xxxx",
        "level": "CONTRIBUTE"  # VIEW, UPLOAD, CONTRIBUTE, ADMINISTER
    }
)
```

### 列表项目

```python
# List accessible projects
projects = dxpy.find_projects(describe=True)

for proj in projects:
    desc = proj['describe']
    print(f"{desc['name']}: {proj['id']}")
```

## 文件夹操作

### 创建文件夹

```python
# Create nested folders
dxpy.api.project_new_folder(
    "project-xxxx",
    {"folder": "/analysis/batch1/results", "parents": True}
)
```

### 移动对象

```python
# Move file to different folder
file_obj = dxpy.DXFile("file-xxxx", project="project-xxxx")
file_obj.move("/new_location")
```

### 删除对象

```python
# Remove file from project (not permanent deletion)
dxpy.api.project_remove_objects(
    "project-xxxx",
    {"objects": ["file-xxxx"]}
)

# Permanent deletion
file_obj = dxpy.DXFile("file-xxxx")
file_obj.remove()
```

## 存档

### 存档数据

存档数据移至更便宜的长期存储：

```python
# Archive a file
dxpy.api.project_archive(
    "project-xxxx",
    {"files": ["file-xxxx"]}
)
```

### 取消存档数据

```python
# Unarchive when needed
dxpy.api.project_unarchive(
    "project-xxxx",
    {"files": ["file-xxxx"]}
)
```

## 批量操作

### 上传多个文件

```python
import os

# Upload all files in directory
for filename in os.listdir("./data"):
    filepath = os.path.join("./data", filename)
    if os.path.isfile(filepath):
        dxpy.upload_local_file(
            filepath,
            project="project-xxxx",
            folder="/batch_upload"
        )
```

### 下载多个文件

```python
# Download all files from folder
files = dxpy.find_data_objects(
    classname="file",
    project="project-xxxx",
    folder="/results"
)

for file in files:
    file_obj = dxpy.DXFile(file['id'])
    filename = file_obj.describe()['name']
    dxpy.download_dxfile(file['id'], f"./downloads/{filename}")
```

## 最佳做法

1. **关闭文件**：写入后始终关闭文件以使其可访问
2. **使用属性**：使用有意义的属性标记数据，以便于发现
3. **组织文件夹**：使用逻辑文件夹结构
4. **清理**：删除临时或过时的数据
5. **批量操作**：处理多个对象时的分组操作
6. **错误处理**：操作前检查对象状态
7. **权限**：数据操作前验证项目权限
8. **归档旧数据**：使用归档来节省长期存储成本
