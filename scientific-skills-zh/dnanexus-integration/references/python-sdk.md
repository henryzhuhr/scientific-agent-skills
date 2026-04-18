# DNAnexus Python SDK (dxpy)

## 概述

dxpy 库提供 Python 绑定以与 DNAnexus 平台交互。它可在 DNAnexus 执行环境（适用于在平台上运行的应用程序）和访问 API 的外部脚本中使用。

## 安装

```bash
# Install dxpy
pip install dxpy

# Or using conda
conda install -c bioconda dxpy
```

* *要求**：Python 3.8 或更高版本

## 身份验证

### 登录

```bash
# Login via command line
dx login
```

### API令牌

```python
import dxpy

# Set authentication token
dxpy.set_security_context({
    "auth_token_type": "Bearer",
    "auth_token": "YOUR_API_TOKEN"
})
```

### 环境变量

```bash
# Set token via environment
export DX_SECURITY_CONTEXT='{"auth_token": "YOUR_TOKEN", "auth_token_type": "Bearer"}'
```

## 核心类

### DXFile

Handler文件对象。

```python
import dxpy

# Get file handler
file_obj = dxpy.DXFile("file-xxxx")

# Get file info
desc = file_obj.describe()
print(f"Name: {desc['name']}")
print(f"Size: {desc['size']} bytes")

# Download file
dxpy.download_dxfile(file_obj.get_id(), "local_file.txt")

# Read file contents
with file_obj.open_file() as f:
    contents = f.read()

# Update metadata
file_obj.set_properties({"key": "value"})
file_obj.add_tags(["tag1", "tag2"])
file_obj.rename("new_name.txt")

# Close file
file_obj.close()
```

### 记录对象的 DXRecord

Handler。

```python
# Create record
record = dxpy.new_dxrecord(
    name="metadata",
    types=["Metadata"],
    details={"key": "value"},
    project="project-xxxx",
    close=True
)

# Get record handler
record = dxpy.DXRecord("record-xxxx")

# Get details
details = record.get_details()

# Update details (must be open)
record.set_details({"updated": True})
record.close()
```

### 小程序的 DXApplet

Handler对象.

```python
# Get applet
applet = dxpy.DXApplet("applet-xxxx")

# Get applet info
desc = applet.describe()
print(f"Name: {desc['name']}")
print(f"Version: {desc.get('version', 'N/A')}")

# Run applet
job = applet.run({
    "input1": {"$dnanexus_link": "file-yyyy"},
    "param1": "value"
})
```

### 应用程序对象的 DXApp

Handler。

```python
# Get app by name
app = dxpy.DXApp(name="my-app")

# Or by ID
app = dxpy.DXApp("app-xxxx")

# Run app
job = app.run({
    "input": {"$dnanexus_link": "file-yyyy"}
})
```

### 工作流的 DXWorkflow

Handler对象.

```python
# Create workflow
workflow = dxpy.new_dxworkflow(
    name="My Pipeline",
    project="project-xxxx"
)

# Add stage
stage = workflow.add_stage(
    dxpy.DXApplet("applet-xxxx"),
    name="Step 1"
)

# Set stage input
stage.set_input("input1", {"$dnanexus_link": "file-yyyy"})

# Close workflow
workflow.close()

# Run workflow
analysis = workflow.run({})
```

### 作业对象的 DXJob

Handler。

```python
# Get job
job = dxpy.DXJob("job-xxxx")

# Get job info
desc = job.describe()
print(f"State: {desc['state']}")
print(f"Name: {desc['name']}")

# Wait for completion
job.wait_on_done()

# Get output
output = desc.get("output", {})

# Terminate job
job.terminate()
```

### 项目的 DXProject

Handler objects.

```python
# Get project
project = dxpy.DXProject("project-xxxx")

# Get project info
desc = project.describe()
print(f"Name: {desc['name']}")
print(f"Region: {desc.get('region', 'N/A')}")

# List folder contents
contents = project.list_folder("/data")
print(f"Objects: {contents['objects']}")
print(f"Folders: {contents['folders']}")
```

## 高级函数

### 文件操作

```python
# Upload file
file_obj = dxpy.upload_local_file(
    "local_file.txt",
    project="project-xxxx",
    folder="/data",
    name="uploaded_file.txt"
)

# Download file
dxpy.download_dxfile("file-xxxx", "downloaded.txt")

# Upload string as file
file_obj = dxpy.upload_string("Hello World", project="project-xxxx")
```

### 创建数据对象

```python
# New file
file_obj = dxpy.new_dxfile(
    project="project-xxxx",
    name="output.txt"
)
file_obj.write("content")
file_obj.close()

# New record
record = dxpy.new_dxrecord(
    name="metadata",
    details={"key": "value"},
    project="project-xxxx"
)
```

### 搜索函数

```python
# Find data objects
results = dxpy.find_data_objects(
    classname="file",
    name="*.fastq",
    project="project-xxxx",
    folder="/raw_data",
    describe=True
)

for result in results:
    print(f"{result['describe']['name']}: {result['id']}")

# Find projects
projects = dxpy.find_projects(
    name="*analysis*",
    describe=True
)

# Find jobs
jobs = dxpy.find_jobs(
    project="project-xxxx",
    created_after="2025-01-01",
    state="failed"
)

# Find apps
apps = dxpy.find_apps(
    category="Read Mapping"
)
```

### 链接和参考

```python
# Create link to data object
link = dxpy.dxlink("file-xxxx")
# Returns: {"$dnanexus_link": "file-xxxx"}

# Create link with project
link = dxpy.dxlink("file-xxxx", "project-yyyy")

# Get job output reference (for chaining jobs)
output_ref = job.get_output_ref("output_name")
```

## API 方法

### 直接API 调用

对于高级未涵盖的操作函数：

```python
# Call API method directly
result = dxpy.api.project_new({
    "name": "New Project",
    "description": "Created via API"
})

project_id = result["id"]

# File describe
file_desc = dxpy.api.file_describe("file-xxxx")

# System find data objects
results = dxpy.api.system_find_data_objects({
    "class": "file",
    "project": "project-xxxx",
    "name": {"regexp": ".*\\.bam$"}
})
```

### 常用API方法

```python
# Project operations
dxpy.api.project_invite("project-xxxx", {"invitee": "user-yyyy", "level": "VIEW"})
dxpy.api.project_new_folder("project-xxxx", {"folder": "/new_folder"})

# File operations
dxpy.api.file_close("file-xxxx")
dxpy.api.file_remove("file-xxxx")

# Job operations
dxpy.api.job_terminate("job-xxxx")
dxpy.api.job_get_log("job-xxxx")
```

## 应用开发函数

### 入口点

```python
import dxpy

@dxpy.entry_point('main')
def main(input1, input2):
    """Main entry point for app"""
    # Process inputs
    result = process(input1, input2)

    # Return outputs
    return {
        "output1": result
    }

# Required at end of app code
dxpy.run()
```

### 创建子作业

```python
# Spawn subjob within app
subjob = dxpy.new_dxjob(
    fn_input={"input": value},
    fn_name="helper_function"
)

# Get output reference
output_ref = subjob.get_output_ref("result")

@dxpy.entry_point('helper_function')
def helper_function(input):
    # Process
    return {"result": output}
```

## 错误处理

### 异常类型

```python
import dxpy
from dxpy.exceptions import DXError, DXAPIError

try:
    file_obj = dxpy.DXFile("file-xxxx")
    desc = file_obj.describe()
except DXAPIError as e:
    print(f"API Error: {e}")
    print(f"Status Code: {e.code}")
except DXError as e:
    print(f"General Error: {e}")
```

### 常见异常

- `DXAPIError`：API 请求失败
- `DXError`：常规 DNAnexus 错误
- `ResourceNotFound`：对象不存在
- `PermissionDenied`：权限不足
- `InvalidInput`：输入参数无效

## 实用功能

### 获取处理程序

```python
# Get handler from ID/link
handler = dxpy.get_handler("file-xxxx")
# Returns DXFile, DXRecord, etc. based on object class

# Bind handler to project
handler = dxpy.DXFile("file-xxxx", project="project-yyyy")
```

### 描述方法

```python
# Describe any object
desc = dxpy.describe("file-xxxx")
print(desc)

# Describe with fields
desc = dxpy.describe("file-xxxx", fields={"name": True, "size": True})
```

## 配置

### 设置项目上下文

```python
# Set default project
dxpy.set_workspace_id("project-xxxx")

# Get current project
project_id = dxpy.WORKSPACE_ID
```

### 设置区域

```python
# Set API server
dxpy.set_api_server_info(host="api.dnanexus.com", port=443)
```

## 最佳实践

1. **使用高级函数**：优先使用 `upload_local_file()` 而不是手动创建文件 
2. **处理程序重用**：创建处理程序一次并重用它们
3. **批量操作**：使用find函数处理多个对象
4. **错误处理**：始终将 API 调用包装在 try- except 块中 
5. **关闭对象**：修改后记得关闭文件和记录
6. **项目上下文**：设置 apps
7 的工作区上下文。 **API 令牌安全**：切勿在源代码中硬编码令牌
8. **描述字段**：仅请求所需的字段以减少延迟
9. **搜索过滤器**：使用特定过滤器来缩小搜索结果
10. **链接格式**：使用 `dxpy.dxlink()` 进行一致的链接创建

## 常见模式

### 上传和处理模式

```python
# Upload input
input_file = dxpy.upload_local_file("data.txt", project="project-xxxx")

# Run analysis
job = dxpy.DXApplet("applet-xxxx").run({
    "input": dxpy.dxlink(input_file.get_id())
})

# Wait and download result
job.wait_on_done()
output_id = job.describe()["output"]["result"]["$dnanexus_link"]
dxpy.download_dxfile(output_id, "result.txt")
```

### 批量文件处理

```python
# Find all FASTQ files
files = dxpy.find_data_objects(
    classname="file",
    name="*.fastq",
    project="project-xxxx"
)

# Process each file
jobs = []
for file_result in files:
    job = dxpy.DXApplet("applet-xxxx").run({
        "input": dxpy.dxlink(file_result["id"])
    })
    jobs.append(job)

# Wait for all jobs
for job in jobs:
    job.wait_on_done()
    print(f"Job {job.get_id()} completed")
```

### 工作流程依赖项

```python
# Job 1
job1 = applet1.run({"input": data})

# Job 2 depends on job1 output
job2 = applet2.run({
    "input": job1.get_output_ref("result")
})

# Job 3 depends on job2
job3 = applet3.run({
    "input": job2.get_output_ref("processed")
})

# Wait for final result
job3.wait_on_done()
```
