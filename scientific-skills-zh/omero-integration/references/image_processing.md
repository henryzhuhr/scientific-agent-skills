# 图像处理和渲染

此参考内容涵盖访问原始像素数据、图像渲染以及在 OMERO 中创建新图像。

## 访问原始像素数据

### 获取单个平面

```python
# Get image
image = conn.getObject("Image", image_id)

# Get dimensions
size_z = image.getSizeZ()
size_c = image.getSizeC()
size_t = image.getSizeT()

# Get pixels object
pixels = image.getPrimaryPixels()

# Get single plane (returns NumPy array)
z, c, t = 0, 0, 0  # First Z-section, channel, and timepoint
plane = pixels.getPlane(z, c, t)

print(f"Shape: {plane.shape}")
print(f"Data type: {plane.dtype.name}")
print(f"Min: {plane.min()}, Max: {plane.max()}")
```

### 获取多个平面平面

```python
import numpy as np

# Get Z-stack for specific channel and timepoint
pixels = image.getPrimaryPixels()
c, t = 0, 0  # First channel and timepoint

# Build list of (z, c, t) coordinates
zct_list = [(z, c, t) for z in range(size_z)]

# Get all planes at once
planes = pixels.getPlanes(zct_list)

# Stack into 3D array
z_stack = np.array([p for p in planes])
print(f"Z-stack shape: {z_stack.shape}")
```

### 获取超立方体（5D 数据的子集）

```python
# Get subset of 5D data (Z, C, T)
zct_list = []
for z in range(size_z // 2, size_z):  # Second half of Z
    for c in range(size_c):           # All channels
        for t in range(size_t):       # All timepoints
            zct_list.append((z, c, t))

# Get planes
planes = pixels.getPlanes(zct_list)

# Process each plane
for i, plane in enumerate(planes):
    z, c, t = zct_list[i]
    print(f"Plane Z={z}, C={c}, T={t}: Min={plane.min()}, Max={plane.max()}")
```

### 获取图块（感兴趣区域）

```python
# Define tile coordinates
x, y = 50, 50          # Top-left corner
width, height = 100, 100  # Tile size
tile = (x, y, width, height)

# Get tile for specific Z, C, T
z, c, t = 0, 0, 0
zct_list = [(z, c, t, tile)]

tiles = pixels.getTiles(zct_list)
tile_data = tiles[0]

print(f"Tile shape: {tile_data.shape}")  # Should be (height, width)
```

### 获取多个瓷砖

```python
# Get tiles from Z-stack
c, t = 0, 0
tile = (50, 50, 100, 100)  # x, y, width, height

# Build list with tiles
zct_list = [(z, c, t, tile) for z in range(size_z)]

tiles = pixels.getTiles(zct_list)

for i, tile_data in enumerate(tiles):
    print(f"Tile Z={i}: {tile_data.shape}, Min={tile_data.min()}")
```

## 图像直方图

### 获取直方图

```python
# Get histogram for first channel
channel_index = 0
num_bins = 256
z, t = 0, 0

histogram = image.getHistogram([channel_index], num_bins, False, z, t)
print(f"Histogram bins: {len(histogram)}")
print(f"First 10 bins: {histogram[:10]}")
```

### 多通道直方图

```python
# Get histograms for all channels
channels = list(range(image.getSizeC()))
histograms = image.getHistogram(channels, 256, False, 0, 0)

for c, hist in enumerate(histograms):
    print(f"Channel {c}: Total pixels = {sum(hist)}")
```

## 图像渲染

### 使用当前设置渲染图像

```python
from PIL import Image
from io import BytesIO

# Get image
image = conn.getObject("Image", image_id)

# Render at specific Z and T
z = image.getSizeZ() // 2  # Middle Z-section
t = 0

rendered_image = image.renderImage(z, t)
# rendered_image is a PIL Image object
rendered_image.save("rendered_image.jpg")
```

### 获取缩略图

```python
from PIL import Image
from io import BytesIO

# Get thumbnail (uses current rendering settings)
thumbnail_data = image.getThumbnail()

# Convert to PIL Image
thumbnail = Image.open(BytesIO(thumbnail_data))
thumbnail.save("thumbnail.jpg")

# Get specific thumbnail size
thumbnail_data = image.getThumbnail(size=(96, 96))
thumbnail = Image.open(BytesIO(thumbnail_data))
```

## 渲染设置

### 查看当前设置

```python
# Display rendering settings
print("Current Rendering Settings:")
print(f"Grayscale mode: {image.isGreyscaleRenderingModel()}")
print(f"Default Z: {image.getDefaultZ()}")
print(f"Default T: {image.getDefaultT()}")
print()

# Channel settings
print("Channel Settings:")
for idx, channel in enumerate(image.getChannels()):
    print(f"Channel {idx + 1}:")
    print(f"  Label: {channel.getLabel()}")
    print(f"  Color: {channel.getColor().getHtml()}")
    print(f"  Active: {channel.isActive()}")
    print(f"  Window: {channel.getWindowStart()} - {channel.getWindowEnd()}")
    print(f"  Min/Max: {channel.getWindowMin()} - {channel.getWindowMax()}")
```

### 设置渲染模型

```python
# Switch to grayscale rendering
image.setGreyscaleRenderingModel()

# Switch to color rendering
image.setColorRenderingModel()
```

### 设置活动通道

```python
# Activate specific channels (1-indexed)
image.setActiveChannels([1, 3])  # Channels 1 and 3 only

# Activate all channels
all_channels = list(range(1, image.getSizeC() + 1))
image.setActiveChannels(all_channels)

# Activate single channel
image.setActiveChannels([2])
```

### 设置通道颜色

```python
# Set channel colors (hex format)
channels = [1, 2, 3]
colors = ['FF0000', '00FF00', '0000FF']  # Red, Green, Blue

image.setActiveChannels(channels, colors=colors)

# Use None to keep existing color
colors = ['FF0000', None, '0000FF']  # Keep channel 2's color
image.setActiveChannels(channels, colors=colors)
```

### 设置通道窗口（强度范围）

```python
# Set intensity windows for channels
channels = [1, 2]
windows = [
    [100.0, 500.0],  # Channel 1: 100-500
    [50.0, 300.0]    # Channel 2: 50-300
]

image.setActiveChannels(channels, windows=windows)

# Use None to keep existing window
windows = [[100.0, 500.0], [None, None]]
image.setActiveChannels(channels, windows=windows)
```

### 设置默认 Z 和 T

```python
# Set default Z-section and timepoint
image.setDefaultZ(5)
image.setDefaultT(0)

# Render using defaults
rendered_image = image.renderImage(z=None, t=None)
rendered_image.save("default_rendering.jpg")
```

## 单独渲染通道

### 单独渲染每个通道

```python
# Set grayscale mode
image.setGreyscaleRenderingModel()

z = image.getSizeZ() // 2
t = 0

# Render each channel
for c in range(1, image.getSizeC() + 1):
    image.setActiveChannels([c])
    rendered = image.renderImage(z, t)
    rendered.save(f"channel_{c}.jpg")
```

### 渲染多通道合成

```python
# Color composite of first 3 channels
image.setColorRenderingModel()
channels = [1, 2, 3]
colors = ['FF0000', '00FF00', '0000FF']  # RGB

image.setActiveChannels(channels, colors=colors)
rendered = image.renderImage(z, t)
rendered.save("rgb_composite.jpg")
```

## 图像投影

### 最大强度投影

```python
# Set projection type
image.setProjection('intmax')

# Render (projects across all Z)
z, t = 0, 0  # Z is ignored for projections
rendered = image.renderImage(z, t)
rendered.save("max_projection.jpg")

# Reset to normal rendering
image.setProjection('normal')
```

### 平均强度投影

```python
image.setProjection('intmean')
rendered = image.renderImage(z, t)
rendered.save("mean_projection.jpg")
image.setProjection('normal')
```

### 可用投影类型

- `'normal'`：无投影（默认）
- `'intmax'`：最大强度投影
- `'intmean'`：平均强度投影
- `'intmin'`：最小强度投影（如果支持）

## 保存并重置渲染设置

#### 将当前设置保存为默认值

```python
# Modify rendering settings
image.setActiveChannels([1, 2])
image.setDefaultZ(5)

# Save as new default
image.saveDefaults()
```

### 重置为导入设置

```python
# Reset to original import settings
image.resetDefaults(save=True)
```

## 从NumPy数组创建图像

### 创建简单图像

```python
import numpy as np

# Create sample data
size_x, size_y = 512, 512
size_z, size_c, size_t = 10, 2, 1

# Generate planes
def plane_generator():
    """Generator that yields planes"""
    for z in range(size_z):
        for c in range(size_c):
            for t in range(size_t):
                # Create synthetic data
                plane = np.random.randint(0, 255, (size_y, size_x), dtype=np.uint8)
                yield plane

# Create image
image = conn.createImageFromNumpySeq(
    plane_generator(),
    "Test Image",
    size_z, size_c, size_t,
    description="Image created from NumPy arrays",
    dataset=None
)

print(f"Created image ID: {image.getId()}")
```

### 从硬编码创建图像数组

```python
from numpy import array, int8

# Define dimensions
size_x, size_y = 5, 4
size_z, size_c, size_t = 1, 2, 1

# Create planes
plane1 = array(
    [[0, 1, 2, 3, 4],
     [5, 6, 7, 8, 9],
     [0, 1, 2, 3, 4],
     [5, 6, 7, 8, 9]],
    dtype=int8
)

plane2 = array(
    [[5, 6, 7, 8, 9],
     [0, 1, 2, 3, 4],
     [5, 6, 7, 8, 9],
     [0, 1, 2, 3, 4]],
    dtype=int8
)

planes = [plane1, plane2]

def plane_gen():
    for p in planes:
        yield p

# Create image
desc = "Image created from hard-coded arrays"
image = conn.createImageFromNumpySeq(
    plane_gen(),
    "numpy_image",
    size_z, size_c, size_t,
    description=desc,
    dataset=None
)

print(f"Created image: {image.getName()} (ID: {image.getId()})")
```

### 在数据集中创建图像

```python
# Get target dataset
dataset = conn.getObject("Dataset", dataset_id)

# Create image
image = conn.createImageFromNumpySeq(
    plane_generator(),
    "New Analysis Result",
    size_z, size_c, size_t,
    description="Result from analysis pipeline",
    dataset=dataset  # Add to dataset
)
```

### 创建派生图像

```python
# Get source image
source = conn.getObject("Image", source_image_id)
size_z = source.getSizeZ()
size_c = source.getSizeC()
size_t = source.getSizeT()
dataset = source.getParent()

pixels = source.getPrimaryPixels()
new_size_c = 1  # Average channels

def plane_gen():
    """Average channels together"""
    for z in range(size_z):
        for c in range(new_size_c):
            for t in range(size_t):
                # Get multiple channels
                channel0 = pixels.getPlane(z, 0, t)
                channel1 = pixels.getPlane(z, 1, t)

                # Combine
                new_plane = (channel0.astype(float) + channel1.astype(float)) / 2
                new_plane = new_plane.astype(channel0.dtype)

                yield new_plane

# Create new image
desc = "Averaged channels from source image"
derived = conn.createImageFromNumpySeq(
    plane_gen(),
    f"{source.getName()}_averaged",
    size_z, new_size_c, size_t,
    description=desc,
    dataset=dataset
)

print(f"Created derived image: {derived.getId()}")
```

## 设置物理尺寸

### 使用单位设置像素大小

```python
from omero.model.enums import UnitsLength
import omero.model

# Get image
image = conn.getObject("Image", image_id)

# Create unit objects
pixel_size_x = omero.model.LengthI(0.325, UnitsLength.MICROMETER)
pixel_size_y = omero.model.LengthI(0.325, UnitsLength.MICROMETER)
pixel_size_z = omero.model.LengthI(1.0, UnitsLength.MICROMETER)

# Get pixels object
pixels = image.getPrimaryPixels()._obj

# Set physical sizes
pixels.setPhysicalSizeX(pixel_size_x)
pixels.setPhysicalSizeY(pixel_size_y)
pixels.setPhysicalSizeZ(pixel_size_z)

# Save changes
conn.getUpdateService().saveObject(pixels)

print("Updated pixel dimensions")
```

### 可用长度单位

来自`omero.model.enums.UnitsLength`：
- `ANGSTROM`
- `NANOMETER`
- `MICROMETER`
- `MILLIMETER`
- `CENTIMETER`
- `METER`
- `PIXEL`

### 设置新图像的像素大小

```python
from omero.model.enums import UnitsLength
import omero.model

# Create image
image = conn.createImageFromNumpySeq(
    plane_generator(),
    "New Image with Dimensions",
    size_z, size_c, size_t
)

# Set pixel sizes
pixel_size = omero.model.LengthI(0.5, UnitsLength.MICROMETER)
pixels = image.getPrimaryPixels()._obj
pixels.setPhysicalSizeX(pixel_size)
pixels.setPhysicalSizeY(pixel_size)

z_size = omero.model.LengthI(2.0, UnitsLength.MICROMETER)
pixels.setPhysicalSizeZ(z_size)

conn.getUpdateService().saveObject(pixels)
```

## 完整示例：图像处理管道

```python
from omero.gateway import BlitzGateway
import numpy as np

HOST = 'omero.example.com'
PORT = 4064
USERNAME = 'user'
PASSWORD = 'pass'

with BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT) as conn:
    # Get source image
    source = conn.getObject("Image", source_image_id)
    print(f"Processing: {source.getName()}")

    # Get dimensions
    size_x = source.getSizeX()
    size_y = source.getSizeY()
    size_z = source.getSizeZ()
    size_c = source.getSizeC()
    size_t = source.getSizeT()

    pixels = source.getPrimaryPixels()

    # Process: Maximum intensity projection over Z
    def plane_gen():
        for c in range(size_c):
            for t in range(size_t):
                # Get all Z planes for this C, T
                z_stack = []
                for z in range(size_z):
                    plane = pixels.getPlane(z, c, t)
                    z_stack.append(plane)

                # Maximum projection
                max_proj = np.max(z_stack, axis=0)
                yield max_proj

    # Create result image (single Z-section)
    result = conn.createImageFromNumpySeq(
        plane_gen(),
        f"{source.getName()}_MIP",
        1, size_c, size_t,  # Z=1 for projection
        description="Maximum intensity projection",
        dataset=source.getParent()
    )

    print(f"Created MIP image: {result.getId()}")

    # Copy pixel sizes (X and Y only, no Z for projection)
    from omero.model.enums import UnitsLength
    import omero.model

    source_pixels = source.getPrimaryPixels()._obj
    result_pixels = result.getPrimaryPixels()._obj

    result_pixels.setPhysicalSizeX(source_pixels.getPhysicalSizeX())
    result_pixels.setPhysicalSizeY(source_pixels.getPhysicalSizeY())

    conn.getUpdateService().saveObject(result_pixels)

    print("Processing complete")
```

## 使用不同数据类型

### 处理各种像素类型

```python
# Get pixel type
pixel_type = image.getPixelsType()
print(f"Pixel type: {pixel_type}")

# Common types: uint8, uint16, uint32, int8, int16, int32, float, double

# Get plane with correct dtype
plane = pixels.getPlane(z, c, t)
print(f"NumPy dtype: {plane.dtype}")

# Convert if needed for processing
if plane.dtype == np.uint16:
    # Convert to float for processing
    plane_float = plane.astype(np.float32)
    # Process...
    # Convert back
    result = plane_float.astype(np.uint16)
```

### 处理大图像

```python
# Process large images in tiles to save memory
tile_size = 512
size_x = image.getSizeX()
size_y = image.getSizeY()

for y in range(0, size_y, tile_size):
    for x in range(0, size_x, tile_size):
        # Get tile dimensions
        w = min(tile_size, size_x - x)
        h = min(tile_size, size_y - y)
        tile = (x, y, w, h)

        # Get tile data
        zct_list = [(z, c, t, tile)]
        tile_data = pixels.getTiles(zct_list)[0]

        # Process tile
        # ...
```

## 最佳实践

1. **使用生成器**：创建图像时，使用生成器可以避免加载内存中的所有数据
2. **指定数据类型**：将 NumPy dtypes 与 OMERO 像素类型
3 相匹配。 **设置物理尺寸**：始终为新图像设置像素大小
4. **平铺大图像**：以平铺方式处理大图像以管理内存
5. **关闭连接**：完成后始终关闭连接
6. **渲染效率**：渲染多个图像时缓存渲染设置
7. **通道索引**：请记住，通道的索引为 1 用于渲染，0 索引用于像素访问
8. **保存设置**：保存渲染设置（如果它们应该是永久的）
9. **压缩**：在 renderImage()中使用压缩参数以加快传输速度
10. **错误处理**：检查 None 返回并处理异常
