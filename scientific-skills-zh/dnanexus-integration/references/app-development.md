# DNAnexus 应用程序开发

## 概述

应用程序和小程序是在DNAnexus 平台上运行的可执行程序。它们可以用 Python 或 Bash 编写，并使用所有必要的依赖项和配置进行部署。

## Applet 与 Apps

- **Applet**：存在于项目内部的数据对象。适合开发和测试。
- **应用程序**：版本控制的、可共享的可执行文件，不存在于项目内部。可以发布供其他人使用。

 两者的创建方式相同，直到最终构建步骤。小程序可以稍后转换为应用程序。

## 创建应用程序/小程序

### 使用dx-app-wizard

生成骨架应用程序目录结构：

```bash
dx-app-wizard
```

这将创建：
- `dxapp.json` - 配置文件
- `src/` - 源代码目录
- `resources/` - 捆绑依赖项
- `test/` - 测试文件

### 构建和部署

构建小程序：
```bash
dx build
```

构建应用程序：
```bash
dx build --app
```

构建过程：
1. 验证 dxapp.json 配置
2. 捆绑源代码和资源
3. 部署到平台
4. 返回小程序/应用程序 ID

## 应用程序目录结构

```
my-app/
├── dxapp.json          # Metadata and configuration
├── src/
│   └── my-app.py       # Main executable (Python)
│   └── my-app.sh       # Or Bash script
├── resources/          # Bundled files and dependencies
│   └── tools/
│   └── data/
└── test/               # Test data and scripts
    └── test.json
```

## Python 应用程序结构

#### 入口点

Python 应用程序使用 `@dxpy.entry_point()` 装饰器来定义功能：

```python
import dxpy

@dxpy.entry_point('main')
def main(input1, input2):
    # Process inputs
    # Return outputs
    return {
        "output1": result1,
        "output2": result2
    }

dxpy.run()
```

### 输入/输出处理

* *输入**：DNAnexus 数据对象表示为包含链接的字典：

```python
@dxpy.entry_point('main')
def main(reads_file):
    # Convert link to handler
    reads_dxfile = dxpy.DXFile(reads_file)

    # Download to local filesystem
    dxpy.download_dxfile(reads_dxfile.get_id(), "reads.fastq")

    # Process file...
```

* *输出**：直接返回原始类型，将文件输出转换为链接：

```python
    # Upload result file
    output_file = dxpy.upload_local_file("output.fastq")

    return {
        "trimmed_reads": dxpy.dxlink(output_file)
    }
```

## Bash应用程序结构

Bash应用程序使用更简单的shell脚本方法：

```bash
#!/bin/bash
set -e -x -o pipefail

main() {
    # Download inputs
    dx download "$reads_file" -o reads.fastq

    # Process
    process_reads reads.fastq > output.fastq

    # Upload outputs
    trimmed_reads=$(dx upload output.fastq --brief)

    # Set job output
    dx-jobutil-add-output trimmed_reads "$trimmed_reads" --class=file
}
```

## 常见开发模式

### 1.生物信息学管道

下载→处理→上传模式：

```python
# Download input
dxpy.download_dxfile(input_file_id, "input.fastq")

# Run analysis
subprocess.check_call(["tool", "input.fastq", "output.bam"])

# Upload result
output = dxpy.upload_local_file("output.bam")
return {"aligned_reads": dxpy.dxlink(output)}
```

### 2. 多文件处理

```python
# Process multiple inputs
for file_link in input_files:
    file_handler = dxpy.DXFile(file_link)
    local_path = f"{file_handler.name}"
    dxpy.download_dxfile(file_handler.get_id(), local_path)
    # Process each file...
```

### 3. 并行处理

应用程序可以生成并行子作业执行：

```python
# Create subjobs
subjobs = []
for item in input_list:
    subjob = dxpy.new_dxjob(
        fn_input={"input": item},
        fn_name="process_item"
    )
    subjobs.append(subjob)

# Collect results
results = [job.get_output_ref("result") for job in subjobs]
```

## 执行环境

应用程序在隔离的 Linux VM (Ubuntu 24.04)中运行，其中：
- Internet 访问
- DNAnexus API 访问
- `/home/dnanexus`
 中的临时暂存空间- 下载到作业工作区的输入文件
- 用于安装依赖项的根访问权限

## 测试Apps

### 本地测试

部署前在本地测试应用程序逻辑：

```bash
cd my-app
python src/my-app.py
```

### 平台测试

在平台上运行小程序：

```bash
dx run applet-xxxx -i input1=file-yyyy
```

监控作业执行：

```bash
dx watch job-zzzz
```

查看作业日志：

```bash
dx watch job-zzzz --get-streams
```

## 最佳实践

1. **错误处理**：使用 try-except 块并提供信息性错误消息
2. **日志记录**：将进度和调试信息打印到 stdout/stderr
3. **验证**：在处理
4之前验证输入。 **清理**：完成后删除临时文件
5. **文档**：在 dxapp.json
6 中包含清晰的描述。 **测试**：使用各种输入类型和边缘情况
7进行测试。 **版本控制**：对应用程序使用语义版本控制

## 常见问题

### 找不到文件
确保在访问之前正确下载文件：
```python
dxpy.download_dxfile(file_id, local_path)
# Now safe to open local_path
```

### 内存不足
在dxapp.json中指定更大的实例类型系统要求

### 超时
增加dxapp.json中的超时或拆分为更小的作业

### 权限错误
确保应用程序在dxapp.json中具有必要的权限
