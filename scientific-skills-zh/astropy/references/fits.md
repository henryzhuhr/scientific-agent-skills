# FITS 文件处理 (astropy.io.fits)

`astropy.io.fits` 模块提供了用于读取、写入和操作 FITS（灵活图像传输系统）文件的综合工具。

## 打开 FITS 文件

### 基本文件打开

```python
from astropy.io import fits

# Open file (returns HDUList - list of HDUs)
hdul = fits.open('filename.fits')

# Always close when done
hdul.close()

# Better: use context manager (automatically closes)
with fits.open('filename.fits') as hdul:
    hdul.info()  # Display file structure
    data = hdul[0].data
```

### 文件打开模式

```python
fits.open('file.fits', mode='readonly')   # Read-only (default)
fits.open('file.fits', mode='update')     # Read and write
fits.open('file.fits', mode='append')     # Add HDUs to file
```

### 内存映射

对于大文件，使用内存映射（默认行为）：

```python
hdul = fits.open('large_file.fits', memmap=True)
# Only loads data chunks as needed
```

### 远程文件

访问云托管的FITS文件：

```python
uri = "s3://bucket-name/image.fits"
with fits.open(uri, use_fsspec=True, fsspec_kwargs={"anon": True}) as hdul:
    # Use .section to get cutouts without downloading entire file
    cutout = hdul[1].section[100:200, 100:200]
```

## HDU结构

FITS文件包含标头数据单元(HDU)：
- **主HDU** (`hdul[0]`)：始终是第一个HDU present
- **扩展 HDU** (`hdul[1:]`)：图像或表扩展

```python
hdul.info()  # Display all HDUs
# Output:
# No.    Name      Ver    Type      Cards   Dimensions   Format
#  0  PRIMARY       1 PrimaryHDU     220   ()
#  1  SCI           1 ImageHDU       140   (1014, 1014)   float32
#  2  ERR           1 ImageHDU        51   (1014, 1014)   float32
```

## 访问 HDU

```python
# By index
primary = hdul[0]
extension1 = hdul[1]

# By name
sci = hdul['SCI']

# By name and version number
sci2 = hdul['SCI', 2]  # Second SCI extension
```

## 使用标头

### 读取标头值

```python
hdu = hdul[0]
header = hdu.header

# Get keyword value (case-insensitive)
observer = header['OBSERVER']
exptime = header['EXPTIME']

# Get with default if missing
filter_name = header.get('FILTER', 'Unknown')

# Access by index
value = header[7]  # 8th card's value
```

### 修改标头

```python
# Update existing keyword
header['OBSERVER'] = 'Edwin Hubble'

# Add/update with comment
header['OBSERVER'] = ('Edwin Hubble', 'Name of observer')

# Add keyword at specific position
header.insert(5, ('NEWKEY', 'value', 'comment'))

# Add HISTORY and COMMENT
header['HISTORY'] = 'File processed on 2025-01-15'
header['COMMENT'] = 'Note about the data'

# Delete keyword
del header['OLDKEY']
```

### 标头卡

每个关键字存储为“卡”（80 个字符） record):

```python
# Access full card
card = header.cards[0]
print(f"{card.keyword} = {card.value} / {card.comment}")

# Iterate over all cards
for card in header.cards:
    print(f"{card.keyword}: {card.value}")
```

## 使用图像数据

### 读取图像数据

```python
# Get data from HDU
data = hdul[1].data  # Returns NumPy array

# Data properties
print(data.shape)      # e.g., (1024, 1024)
print(data.dtype)      # e.g., float32
print(data.min(), data.max())

# Access specific pixels
pixel_value = data[100, 200]
region = data[100:200, 300:400]
```

### 数据操作

Data 是一个 NumPy 数组，因此使用标准 NumPy 操作：

```python
import numpy as np

# Statistics
mean = np.mean(data)
median = np.median(data)
std = np.std(data)

# Modify data
data[data < 0] = 0  # Clip negative values
data = data * gain + bias  # Calibration

# Mathematical operations
log_data = np.log10(data)
smoothed = scipy.ndimage.gaussian_filter(data, sigma=2)
```

### 剪切和部分

提取区域而不加载整个array:

```python
# Section notation [y_start:y_end, x_start:x_end]
cutout = hdul[1].section[500:600, 700:800]
```

## 创建新的 FITS 文件

### 简单图像文件

```python
# Create data
data = np.random.random((100, 100))

# Create HDU
hdu = fits.PrimaryHDU(data=data)

# Add header keywords
hdu.header['OBJECT'] = 'Test Image'
hdu.header['EXPTIME'] = 300.0

# Write to file
hdu.writeto('new_image.fits')

# Overwrite if exists
hdu.writeto('new_image.fits', overwrite=True)
```

### 多扩展文件

```python
# Create primary HDU (can have no data)
primary = fits.PrimaryHDU()
primary.header['TELESCOP'] = 'HST'

# Create image extensions
sci_data = np.ones((100, 100))
sci = fits.ImageHDU(data=sci_data, name='SCI')

err_data = np.ones((100, 100)) * 0.1
err = fits.ImageHDU(data=err_data, name='ERR')

# Combine into HDUList
hdul = fits.HDUList([primary, sci, err])

# Write to file
hdul.writeto('multi_extension.fits')
```

## 使用表数据

### 读表

```python
# Open table
with fits.open('table.fits') as hdul:
    table = hdul[1].data  # BinTableHDU or TableHDU

    # Access columns
    ra = table['RA']
    dec = table['DEC']
    mag = table['MAG']

    # Access rows
    first_row = table[0]
    subset = table[10:20]

    # Column info
    cols = hdul[1].columns
    print(cols.names)
    cols.info()
```

### 创建表

```python
# Define columns
col1 = fits.Column(name='ID', format='K', array=[1, 2, 3, 4])
col2 = fits.Column(name='RA', format='D', array=[10.5, 11.2, 12.3, 13.1])
col3 = fits.Column(name='DEC', format='D', array=[41.2, 42.1, 43.5, 44.2])
col4 = fits.Column(name='Name', format='20A',
                   array=['Star1', 'Star2', 'Star3', 'Star4'])

# Create table HDU
table_hdu = fits.BinTableHDU.from_columns([col1, col2, col3, col4])
table_hdu.name = 'CATALOG'

# Write to file
table_hdu.writeto('catalog.fits', overwrite=True)
```

### 列格式

常见FITS表列格式：
- `'A'`：字符串（例如 '20A' 表示 20 个字符）
- `'L'`：逻辑（布尔）
- `'B'`：无符号字节
- `'I'`：16 位整数
- `'J'`：32位整数
- `'K'`：64位整数
- `'E'`：32位浮点
- `'D'`：64位浮点

## 修改现有文件

### 更新模式

```python
with fits.open('file.fits', mode='update') as hdul:
    # Modify header
    hdul[0].header['NEWKEY'] = 'value'

    # Modify data
    hdul[1].data[100, 100] = 999

    # Changes automatically saved when context exits
```

### 追加模式

```python
# Add new extension to existing file
new_data = np.random.random((50, 50))
new_hdu = fits.ImageHDU(data=new_data, name='NEW_EXT')

with fits.open('file.fits', mode='append') as hdul:
    hdul.append(new_hdu)
```

## 便利功能

对于无需管理 HDU 列表的快速操作：

```python
# Get data only
data = fits.getdata('file.fits', ext=1)

# Get header only
header = fits.getheader('file.fits', ext=0)

# Get both
data, header = fits.getdata('file.fits', ext=1, header=True)

# Get single keyword value
exptime = fits.getval('file.fits', 'EXPTIME', ext=0)

# Set keyword value
fits.setval('file.fits', 'NEWKEY', value='newvalue', ext=0)

# Write simple file
fits.writeto('output.fits', data, header, overwrite=True)

# Append to file
fits.append('file.fits', data, header)

# Display file info
fits.info('file.fits')
```

## 比较 FITS 文件

```python
# Print differences between two files
fits.printdiff('file1.fits', 'file2.fits')

# Compare programmatically
diff = fits.FITSDiff('file1.fits', 'file2.fits')
print(diff.report())
```

## 在格式之间转换

### FITS 与 Astropy 之间的转换表

```python
from astropy.table import Table

# FITS to Table
table = Table.read('catalog.fits')

# Table to FITS
table.write('output.fits', format='fits', overwrite=True)
```

## 最佳实践

1. **始终使用上下文管理器**（`with` 语句）进行安全文件处理
2. **避免修改结构关键字**（SIMPLE、BITPIX、NAXIS 等）
3. **对大文件使用内存映射**以节省 RAM
4. **对远程文件使用 .section** 以避免完全下载
5. **在访问数据
6之前使用`.info()`检查HDU结构**。 **操作前验证数据类型**以避免意外行为
7. **使用便利函数**进行简单的一次性操作

## 常见问题

### 处理非标准FITS

某些文件违反FITS标准：

```python
# Ignore verification warnings
hdul = fits.open('bad_file.fits', ignore_missing_end=True)

# Fix non-standard files
hdul = fits.open('bad_file.fits')
hdul.verify('fix')  # Try to fix issues
hdul.writeto('fixed_file.fits')
```

### 大文件性能

```python
# Use memory mapping (default)
hdul = fits.open('huge_file.fits', memmap=True)

# For write operations with large arrays, use Dask
import dask.array as da
large_array = da.random.random((10000, 10000))
fits.writeto('output.fits', large_array)
```
