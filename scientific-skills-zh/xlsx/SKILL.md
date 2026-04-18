---
name: xlsx
description: "当电子表格文件是主要输入或输出时，请使用此技能。这意味着用户想要执行的任何任务：打开、读取、编辑或修复现有的 .xlsx、.xlsm、.csv 或 .tsv 文件（例如，添加列、计算公式、格式化、图表、清理混乱数据）；从头开始或从其他数据源创建新的电子表格；或在表格文件格式之间进行转换。特别是当用户通过名称或路径引用电子表格文件时（甚至是随意引用（例如“我下载的 xlsx”））并希望对其执行某些操作或从中生成某些内容时，尤其会触发。还可以触发清理或重组混乱的表格数据文件（格式错误的行、错误的标题、垃圾数据）到正确的电子表格中。可交付成果必须是电子表格文件。当主要交付成果是 Word 文档、HTML 报告、独立 Python 脚本、数据库管道或 Google Sheets API 集成时，即使涉及表格数据，也不要触发。"
license: Proprietary. LICENSE.txt has complete terms
---

# 输出要求

## 所有 Excel 文件

### 专业字体
- 除非用户另有指示，否则所有可交付成果使用一致的专业字体（例如 Arial、Times New Roman）

### 零公式错误
- 每个 Excel 模型交付时必须具有零公式错误（#REF！、#DIV/0！、#VALUE！、#N/A、#NAME？）

### 保留现有模板（更新模板时）
- 修改文件时研究并完全匹配现有格式、样式和约定
- 切勿对具有已建立模式的文件强加标准化格式
- 现有模板约定始终覆盖这些约定指南

## 金融模型

### 颜色编码标准
除非用户或现有模板另有说明

#### 行业标准颜色约定
- **蓝色文本（RGB：0,0,255）**：硬编码输入，以及用户将根据场景更改的数字
- **黑色文本 (RGB: 0,0,0)**：所有公式和计算
- **绿色文本 (RGB: 0,128,0)**：从同一工作簿内的其他工作表中提取的链接
- **红色文本 (RGB: 255,0,0)**：指向其他文件的外部链接
- **黄色背景 (RGB: 255,255,0)**：需要注意的关键假设或需要更新的单元格

### 数字格式标准

#### 所需格式规则
- **年份**：格式为文本字符串（例如，“2024”而不是“2,024”）
- **货币**：使用$#,##0 格式；始终在标题中指定单位（“收入 ($mm)”）
- **零**：使用数字格式将所有零设为“-”，包括百分比（例如“$#,##0;($#,##0);-”）
- **百分比**：默认为 0.0% 格式（一位小数）
- **倍数**：估值倍数的格式为 0.0x（EV/EBITDA、P/E）
- **负数**：使用括号 (123)不减 -123

### 公式构造规则

#### 假设放置
- 将所有假设（增长率、利润率、倍数等）放在单独的假设单元格中
- 在公式中使用单元格引用而不是硬编码值
- 示例：使用=B5*(1+$B$6)而不是=B5*1.05

#### 公式错误预防
- 验证所有单元格引用是否正确
- 检查范围中的相差一错误
- 确保所有投影周期内的公式一致
- 使用边缘情况进行测试（零值、负数）
- 验证没有意外的循环引用

#### 硬编码的文档要求
- 注释或单元格中旁边（如果在表末尾）。格式：“来源：[系统/文档]、[日期]、[具体参考]、[URL（如果适用）”
- 示例：
  - “来源：公司 10-K，2024 财年，第 45 页，收入票据，[SEC EDGAR URL]”
  - “来源：公司 10-Q，2025 年第 2 季度，附录99.1，[SEC EDGAR URL]“
  - “来源：彭博终端，2025 年 8 月 15 日，AAPL 美国股票”
  - “来源：FactSet，2025 年 8 月 20 日，共识估计屏幕”

# XLSX 创建、编辑和Analysis

## 概述

A 用户可能会要求您创建、编辑或分析 .xlsx 文件的内容。您可以使用不同的工具和工作流程来执行不同的任务。

## 重要要求

* *公式重新计算需要 LibreOffice**：您可以假设安装了 LibreOffice，以便使用 `scripts/recalc.py` 脚本重新计算公式值。该脚本会在首次运行时自动配置 LibreOffice，包括在 Unix 套接字受到限制的沙盒环境中（由 `scripts/office/soffice.py` 处理）

## 读取和分析数据

### 使用 pandas 进行数据分析
对于数据分析、可视化和基本操作，请使用提供强大数据操作功能的 **pandas**功能：

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('output.xlsx', index=False)
```

## Excel 文件工作流程

## 关键：使用公式，而不是硬编码值

* *始终使用 Excel 公式，而不是在 Python 中计算值并对它们进行硬编码。** 这可确保电子表格保持动态和可更新。

### ❌错误 - 硬编码计算值
```python
# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# Bad: Computing growth rate in Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcodes 0.15

# Bad: Python calculation for average
avg = sum(values) / len(values)
sheet['D20'] = avg  # Hardcodes 42.5
```

### ✅ 正确 - 使用 Excel 公式
```python
# Good: Let Excel calculate the sum
sheet['B10'] = '=SUM(B2:B9)'

# Good: Growth rate as Excel formula
sheet['C5'] = '=(C4-C2)/C2'

# Good: Average using Excel function
sheet['D20'] = '=AVERAGE(D2:D19)'
```

这适用所有计算 - 总计、百分比、比率、差异等。当源数据发生变化时，电子表格应该能够重新计算。

## 通用工作流程
1. **选择工具**：pandas 用于数据，openpyxl 用于公式/格式
2. **创建/加载**：创建新工作簿或加载现有文件
3. **修改**：添加/编辑数据、公式和格式
4. **保存**：写入文件
5. **重新计算公式（如果使用公式则必须）**：使用scripts/recalc.py script
 ```bash
 python script/recalc.py output.xlsx
 ```
6. **验证并修复任何错误**：
  - 脚本返回带有错误详细信息的 JSON
  - 如果 `status` 是 `errors_found`，请检查 `error_summary` 的特定错误类型和位置
  - 修复已识别的错误并重新重新计算
  - 要修复的常见错误：
  - `#REF!`：无效的单元格引用
  - `#DIV/0!`：除以零
  - `#VALUE!`：公式中的数据类型错误
  - `#NAME?`：无法识别的公式名称

### 创建新的Excel文件

```python
# Using openpyxl for formulas and formatting
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### 编辑现有Excel 文件

```python
# Using openpyxl to preserve formulas and formatting
from openpyxl import load_workbook

# Load existing file
wb = load_workbook('existing.xlsx')
sheet = wb.active  # or wb['SheetName'] for specific sheet

# Working with multiple sheets
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # Insert row at position 2
sheet.delete_cols(3)  # Delete column 3

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## 重新计算公式

由openpyxl 创建或修改的Excel 文件包含字符串形式的公式，但不包含计算值。使用提供的`scripts/recalc.py`脚本重新计算公式：

```bash
python scripts/recalc.py <excel_file> [timeout_seconds]
```

示例：
```bash
python scripts/recalc.py output.xlsx 30
```

脚本：
- 首次运行时自动设置 LibreOffice 宏
- 重新计算所有工作表中的所有公式
- 扫描所有单元格中的 Excel 错误（#REF!、#DIV/0!、等）
- 返回包含详细错误位置和计数的 JSON
- 适用于 Linux 和 macOS

## 公式验证检查表

快速检查以确保公式正确工作：

### 基本验证
- [ ] **测试 2-3 个示例参考**：验证它们在构建完整版本之前提取正确的值model
- [ ] **列映射**：确认 Excel 列匹配（例如，第 64 列 = BL，而不是 BK）
- [ ] **行偏移**：记住 Excel 行是 1 索引的（DataFrame 第 5 行 = Excel 第 6 行）

### 常见陷阱
- [ ] **NaN 处理**：检查是否存在`pd.notna()`
- [ ] **最右列**：FY 数据通常在第 50+ 列中 `pd.notna()`
- [ ] **多个匹配**：搜索所有出现的情况，而不仅仅是第一个 
- [ ] **除以零**：在公式中使用 `/` 之前检查分母(#DIV/0!)
- [ ] **错误引用**：验证所有单元格引用都指向预期单元格 (#REF!)
- [ ] **跨工作表引用**：使用正确的格式 (Sheet1!A1)链接工作表

### 公式测试策略
- [ ] **从小处开始**：在 2-3 个单元格上测试公式在广泛应用之前
- [ ] **验证依赖关系**：检查公式中引用的所有单元格是否存在
- [ ] **测试边缘情况**：包括零、负和非常大的值

### 解释脚本/recalc.py输出
脚本返回JSON，但有错误详细信息：
```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,              // Total error count
  "total_formulas": 42,           // Number of formulas in file
  "error_summary": {              // Only present if errors found
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## 最佳实践

### 库选择
- **pandas**：最适合数据分析、批量操作和简单数据导出
- **openpyxl**：最适合复杂格式、公式和Excel特定功能

### 使用 openpyxl
- 单元格索引从 1 开始（行=1，列=1 指单元格 A1）
- 使用 `data_only=True` 读取计算值：`load_workbook('file.xlsx', data_only=True)`
- **警告**：如果使用 `data_only=True` 打开并保存，公式将被值替换并永久lost
- 对于大文件：使用 `read_only=True` 进行读取或使用 `write_only=True` 进行写入
- 保留公式但不求值 - 使用脚本/recalc.py 更新值

### 使用 pandas
- 指定数据类型以避免推理问题： `pd.read_excel('file.xlsx', dtype={'id': str})`
- 对于大文件，读取特定列：`pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- 正确处理日期：`pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## 代码风格指南
* *重要**：为 Excel 操作生成 Python 代码时：
- 编写最少、简洁的 Python 代码，无需不必要的代码注释
- 避免冗长的变量名和冗余操作
- 避免不必要的打印语句

* *对于Excel 文件本身**：
- 向具有复杂公式或重要假设的单元格添加注释
- 记录硬编码值的数据源
- 包括关键计算和模型部分的注释