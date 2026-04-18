# cuCIM Reference

cuCIM (CUDA Clara IMage)是 RAPIDS 生态系统中 NVIDIA GPU 加速的计算机视觉和图像处理库。其 `cucim.skimage` 模块几乎是 scikit-image 的 GPU 替代品，具有 200 多个 GPU 加速功能。它还通过 `cucim.clara.CuImage` 提供高性能全幻灯片图像 (WSI)读取器，比 OpenSlide 快 5-6 倍。

> **完整文档：** https://docs.rapids.ai/api/cucim/stable/
> **GitHub：** https://github.com/rapidsai/cucim

## 内容

1. [安装和设置](#installation-and-setup)
2. [核心概念：CuPy 数组](#core-concept-cupy-arrays)
3. [cucim.skimage — GPU scikit-image](#cucimskimage)
4. [颜色操作](#color-operations)
5. [曝光和直方图](#exposure-and-histogram)
6. [特征检测](#feature-detection)
7. [过滤器](#filters)
8. [测量和区域属性](#measure-and-region-properties)
9. [形态](#形态)
10. [分段](#segmentation)
11. [注册](#注册)
12. [恢复](#restoration)
13. [变换](#transform)
14. [指标](#metrics)
15. [实用函数](#utility-functions)
16. [cucim.core.operations — NVIDIA 特定](#cucimcoreoperations)
17. [整张幻灯片图像读取 (cucim.clara)](#whole-slide-image-reading)
18. [性能特点](#performance-characteristics)
19. [互操作性](#互操作性)
20. [与 scikit-image 的已知限制](#known-limitations-vs-scikit-image)
21. [常见迁移模式](#common-migration-patterns)

- --

## 安装和设置

在所有安装说明、文档字符串、注释和错误消息中始终使用 `uv add`（切勿使用 `pip install` 或 `conda install`）。

```bash
uv add --extra-index-url=https://pypi.nvidia.com cucim-cu12    # For CUDA 12.x
```

* *平台：**仅限 Linux（x86-64 和 aarch64）— 不支持 Windows 或 macOS GPU。
* *需要：** 具有 CUDA 12.x、Python 3.9+、CuPy、NumPy、SciPy、 scikit-image.

Verify:
```python
import cucim
print(cucim.__version__)

import cupy as cp
from cucim.skimage.filters import gaussian
img = cp.random.rand(512, 512).astype(cp.float32)
result = gaussian(img, sigma=3)
print(f"Filtered image shape: {result.shape}")  # Should work on GPU
```

- --

## 核心概念：CuPy 数组

cuCIM 在 **CuPy 数组**上本机运行。所有 `cucim.skimage` 函数都接受 CuPy 数组作为输入，并返回 CuPy 数组作为输出 — 零复制，全部在 GPU 上。

```python
import cupy as cp
import numpy as np
from cucim.skimage.filters import gaussian

# Transfer image to GPU once
image_gpu = cp.asarray(numpy_image)

# All processing stays on GPU — zero-copy between cuCIM calls
blurred = gaussian(image_gpu, sigma=3)
# ... more processing on GPU ...

# Transfer back to CPU only when needed (for display, save, etc.)
result_cpu = cp.asnumpy(blurred)
```

* *最佳实践：** 在开始时将数据移动到 GPU 一次，在 GPU 上链接所有 cuCIM 操作，然后仅在最后传输回 CPU。

- --

## cucim.skimage

`cucim.skimage` 模块镜像 scikit-image 的模块结构。大多数情况下，将 `from skimage` 替换为 `from cucim.skimage` 并传递 CuPy 数组而不是 NumPy 数组。

```python
# Before (CPU — scikit-image)
from skimage.filters import gaussian
import numpy as np
result = gaussian(numpy_image, sigma=3)

# After (GPU — cuCIM)
from cucim.skimage.filters import gaussian
import cupy as cp
result = gaussian(cp.asarray(numpy_image), sigma=3)
```

- --

## 颜色操作

`cucim.skimage.color` — 42 GPU 加速的颜色空间转换函数.

```python
from cucim.skimage.color import rgb2gray, rgb2hsv, rgb2lab, label2rgb
from cucim.skimage.color import separate_stains, combine_stains

# Color space conversions
gray = rgb2gray(rgb_image_gpu)
hsv = rgb2hsv(rgb_image_gpu)
lab = rgb2lab(rgb_image_gpu)

# Stain separation (for H&E histology)
stains = separate_stains(rgb_image_gpu, stain_matrix)
```

* *可用转换：** `rgb2gray`、`rgb2hsv`、`hsv2rgb`、`rgb2lab`、`lab2rgb`、`rgb2xyz`、`xyz2rgb`、 `rgb2luv`、`luv2rgb`、`rgb2ycbcr`、`ycbcr2rgb`、`rgb2yuv`、`yuv2rgb`、`rgb2yiq`、`yiq2rgb`、`rgb2hed`、`hed2rgb`、 `rgb2rgbcie`、`rgbcie2rgb`、`gray2rgb`、`gray2rgba`、`rgba2rgb`、`convert_colorspace`、`label2rgb`

* *色差：** `deltaE_cie76`、`deltaE_ciede94`、 `deltaE_ciede2000`、`deltaE_cmc`

- --

## 曝光和直方图

`cucim.skimage.exposure`—直方图均衡、对比度调整。

```python
from cucim.skimage.exposure import (
    equalize_hist, equalize_adapthist,
    rescale_intensity, adjust_gamma, adjust_log, adjust_sigmoid,
    histogram, match_histograms, is_low_contrast
)

# CLAHE (Contrast Limited Adaptive Histogram Equalization)
enhanced = equalize_adapthist(image_gpu, clip_limit=0.03)

# Gamma correction
brightened = adjust_gamma(image_gpu, gamma=0.5)

# Rescale intensity to [0, 1]
normalized = rescale_intensity(image_gpu)

# Histogram matching between two images
matched = match_histograms(source_gpu, reference_gpu)
```

- --

## 功能检测

`cucim.skimage.feature` — 边缘、角点和斑点检测。

```python
from cucim.skimage.feature import (
    canny, corner_harris, corner_peaks,
    blob_dog, blob_doh, blob_log,
    structure_tensor, hessian_matrix, hessian_matrix_det,
    match_template, peak_local_max, daisy, multiscale_basic_features
)

# Canny edge detection
edges = canny(gray_image_gpu, sigma=2.0)

# Harris corner detection
corners = corner_harris(gray_image_gpu)
corner_coords = corner_peaks(corners, min_distance=5)

# Blob detection (Difference of Gaussian)
blobs = blob_dog(gray_image_gpu, max_sigma=30, threshold=0.1)

# Template matching
result = match_template(image_gpu, template_gpu)
```

- --

## 过滤器

`cucim.skimage.filters` — 47 个 GPU 加速过滤函数。这是最常用的模块之一。

```python
from cucim.skimage.filters import (
    gaussian, median, sobel, laplace, unsharp_mask,
    frangi, hessian, meijering, sato,
    threshold_otsu, threshold_multiotsu, threshold_sauvola,
    gabor, difference_of_gaussians, butterworth
)

# Gaussian blur
blurred = gaussian(image_gpu, sigma=3)

# Sobel edge detection
edges = sobel(gray_image_gpu)

# Unsharp mask (sharpening)
sharpened = unsharp_mask(image_gpu, radius=5, amount=2.0)

# Vessel/ridge detection (for medical imaging)
vessels = frangi(gray_image_gpu, sigmas=range(1, 10))

# Otsu thresholding
threshold = threshold_otsu(gray_image_gpu)
binary = gray_image_gpu > threshold

# Multi-level Otsu
thresholds = threshold_multiotsu(gray_image_gpu, classes=3)
```

* *边缘检测：** `sobel`、`scharr`、`prewitt`、`roberts`、`farid`、`laplace`（加上 `_h`/`_v`变体）

* *平滑：** `gaussian`、`median`、`unsharp_mask`

* *脊/血管检测：** `frangi`、`hessian`、`meijering`、 `sato`

* *阈值（10种方法）：** `threshold_otsu`、`threshold_isodata`、`threshold_li`、`threshold_mean`、`threshold_minimum`、`threshold_multiotsu`、`threshold_niblack`、`threshold_sauvola`、 `threshold_triangle`、`threshold_yen`

* *频域：** `butterworth`、`wiener`

- --

## 测量和区域属性

`cucim.skimage.measure` — 标签、区域属性和形状指标.

```python
from cucim.skimage.measure import label, regionprops, regionprops_table
from cucim.skimage.measure import moments, moments_central, moments_hu
from cucim.skimage.measure import block_reduce, shannon_entropy

# Connected component labeling
labels = label(binary_image_gpu)

# Region properties (area, centroid, bounding box, etc.)
props = regionprops(labels)
table = regionprops_table(labels, intensity_image=gray_gpu,
                          properties=['area', 'centroid', 'mean_intensity'])

# Block reduce (downsampling)
downsampled = block_reduce(image_gpu, block_size=(2, 2), func=cp.mean)
```

* *共定位指标**（用于显微镜）：`manders_coloc_coeff`、`manders_overlap_coeff`、`pearson_corr_coeff`、`intersection_coeff`

- --

## Morphology

`cucim.skimage.morphology` — 30 个 GPU 加速的形态操作。

```python
from cucim.skimage.morphology import (
    binary_erosion, binary_dilation, binary_opening, binary_closing,
    erosion, dilation, opening, closing,
    white_tophat, black_tophat,
    disk, diamond, ball, star,
    remove_small_objects, remove_small_holes,
    reconstruction, medial_axis, thin
)

# Create structuring element
selem = disk(5)

# Binary morphological operations
cleaned = binary_opening(binary_image_gpu, footprint=selem)
cleaned = binary_closing(cleaned, footprint=selem)

# Remove small objects/holes
cleaned = remove_small_objects(labels_gpu, min_size=100)
filled = remove_small_holes(binary_gpu, area_threshold=50)

# Grayscale morphology
tophat = white_tophat(gray_image_gpu, footprint=disk(10))
```

* *结构元素：** `disk`、`diamond`、`ball`、`octagon`、 `octahedron`、`star`、`ellipse`、`footprint_rectangle`

* *各向同性操作：** `isotropic_erosion`、`isotropic_dilation`、`isotropic_opening`、 `isotropic_closing`

- --

## 分段

`cucim.skimage.segmentation` — 水平集方法、边界检测、标签操作。

```python
from cucim.skimage.segmentation import (
    chan_vese, morphological_chan_vese, morphological_geodesic_active_contour,
    find_boundaries, mark_boundaries, clear_border,
    expand_labels, relabel_sequential, random_walker
)

# Chan-Vese segmentation
segmented = chan_vese(gray_image_gpu, mu=0.25, max_num_iter=200)

# Active contours (geodesic)
gimage = inverse_gaussian_gradient(gray_image_gpu)
init_ls = checkerboard_level_set(gray_image_gpu.shape)
seg = morphological_geodesic_active_contour(gimage, num_iter=200, init_level_set=init_ls)

# Find and mark boundaries
boundaries = find_boundaries(labels_gpu, mode='thick')
```

- --

## 配准

`cucim.skimage.registration` — 图像对齐。

```python
from cucim.skimage.registration import (
    phase_cross_correlation,
    optical_flow_tvl1,
    optical_flow_ilk
)

# Subpixel image registration
shift, error, diffphase = phase_cross_correlation(reference_gpu, moving_gpu)

# Optical flow
flow = optical_flow_tvl1(frame1_gpu, frame2_gpu)
```

- --

## 恢复

`cucim.skimage.restoration` — 去噪和de卷积.

```python
from cucim.skimage.restoration import (
    denoise_tv_chambolle,
    richardson_lucy,
    wiener, unsupervised_wiener
)

# Total variation denoising
denoised = denoise_tv_chambolle(noisy_image_gpu, weight=0.1)

# Richardson-Lucy deconvolution
restored = richardson_lucy(blurred_image_gpu, psf_gpu, num_iter=30)
```

- --

## Transform

`cucim.skimage.transform` — 几何变换、调整大小、金字塔。

```python
from cucim.skimage.transform import (
    resize, rescale, rotate, warp, swirl, warp_polar,
    pyramid_gaussian, pyramid_laplacian,
    downscale_local_mean, integral_image,
    AffineTransform, EuclideanTransform, SimilarityTransform
)

# Resize
resized = resize(image_gpu, (256, 256))

# Rescale
half = rescale(image_gpu, 0.5)

# Rotate
rotated = rotate(image_gpu, angle=45, resize=True)

# Gaussian pyramid
pyramid = list(pyramid_gaussian(image_gpu, max_layer=4, downscale=2))

# Affine transform
tform = AffineTransform(rotation=0.3, translation=(50, 50))
warped = warp(image_gpu, tform.inverse)
```

- --

## 指标

`cucim.skimage.metrics` — 图像质量评估。

```python
from cucim.skimage.metrics import (
    mean_squared_error,
    peak_signal_noise_ratio,
    structural_similarity,
    normalized_root_mse
)

mse = mean_squared_error(original_gpu, processed_gpu)
psnr = peak_signal_noise_ratio(original_gpu, processed_gpu)
ssim = structural_similarity(original_gpu, processed_gpu)
```

- --

## 实用函数

`cucim.skimage.util` — 类型转换、数组操作。

```python
from cucim.skimage.util import (
    img_as_float, img_as_float32, img_as_ubyte,
    invert, crop, random_noise, montage
)

# Convert to float32 [0, 1]
float_img = img_as_float32(uint8_image_gpu)

# Add noise for testing
noisy = random_noise(image_gpu, mode='gaussian', var=0.01)
```

- --

## cucim.core.operations

在 scikit-image 中找不到特定于 NVIDIA 的操作。对于数字病理学特别有用。

### 病理特定

```python
from cucim.core.operations.color import (
    color_jitter,
    image_to_absorbance,
    stain_extraction_pca,
    normalize_colors_pca
)

# H&E stain normalization (digital pathology)
normalized = normalize_colors_pca(he_image_gpu)

# Color augmentation
augmented = color_jitter(image_gpu, brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1)
```

### 强度操作

```python
from cucim.core.operations.intensity import normalize_data, scale_intensity_range, zoom

normalized = normalize_data(image_gpu)
scaled = scale_intensity_range(image_gpu, a_min=0, a_max=255, b_min=0.0, b_max=1.0)
```

### 空间增强

```python
from cucim.core.operations.spatial import image_flip, image_rotate_90, rand_image_flip

flipped = image_flip(image_gpu, spatial_axis=1)
rotated = image_rotate_90(image_gpu, k=1)  # 90 degrees
randomly_flipped = rand_image_flip(image_gpu, prob=0.5)
```

### 距离Transform

```python
from cucim.core.operations.morphology import distance_transform_edt

# Exact Euclidean distance transform (faster than scipy.ndimage on GPU)
distances = distance_transform_edt(binary_image_gpu)
```

- --

## 全幻灯片图像读取

`cucim.clara.CuImage` - 高性能WSI阅读器，兼容OpenSlide API，速度提高5-6倍。

```python
from cucim import CuImage

# Open a whole-slide image
img = CuImage("slide.svs")

# Inspect metadata
print(f"Dimensions: {img.shape}")
print(f"Resolution levels: {img.resolutions}")
print(f"Spacing: {img.spacing}")

# Read a region (returns a CuImage object)
region = img.read_region(location=(1000, 2000), size=(256, 256), level=0)

# Convert to CuPy array for processing
import cupy as cp
tile_gpu = cp.asarray(region)

# Process with cucim.skimage
from cucim.skimage.color import rgb2gray
gray_tile = rgb2gray(tile_gpu)
```

* *支持格式：** Aperio SVS、Philips TIFF、通用平铺多分辨率 RGB TIFF（JPEG、JPEG2000、LZW、Deflate 压缩）。

### 平铺缓存

```python
from cucim.clara.cache import ImageCache

# Configure tile cache for repeated access patterns
cache = ImageCache(memory_capacity=2 * 1024**3)  # 2 GB cache
```

### GPUDirect Storage

对于大文件 (2GB+)，GPUDirect Storage 绕过 CPU 内存额外加速 25% 以上：

```python
from cucim.clara.filesystem import CuFileDriver

# Read directly into GPU memory, bypassing CPU
driver = CuFileDriver(path, flags)
driver.pread(gpu_buffer, size, offset)
```

- --

## 性能特征

* *标题数字：**
- 对于大图像上的某些操作，比 scikit-image 快 **1245 倍**
- **5-6x比用于 WSI 多线程补丁读取的 OpenSlide 更快
- **25%+ 额外加速**，在 2GB+ 文件上使用 GPUDirect 存储

* *缩放行为：**
- **4K 分辨率及以上：** GPU 并行性充分利用，最大加速
- **~1000x1000：** 中等但可衡量大多数操作的加速
- **低于〜512x512：**收益递减； GPU 开销开始变得重要
- **低于 ~64x64：** 由于 CUDA 内核启动开销，CPU 可能会更快

  * *首次调用开销：** 第一次内核执行时的 JIT 编译（之后缓存）。后续调用的基准。

* *最佳策略：**将图像传输到 GPU 一次，链接所有处理操作，最后传输回一次。

- --

## 互操作性

- **CuPy：** 本机数组格式。所有 cucim.skimage 函数接受并返回 CuPy 数组。
- **NumPy:** 使用 `cp.asarray()` / `cp.asnumpy()`.
- **PyTorch/TensorFlow:** 通过 DLPack 协议进行零复制：`torch.as_tensor(cupy_array)` 或 `torch.from_dlpack(cupy_array)`.
- **MONAI：** 直接与 cuCIM 集成进行病理转换的医学成像框架。
- **配置：** 可以使用 cuCIM 作为 GPU 后端进行增强。
- **NVIDIA DALI：** 数据加载管道集成。
- **Numba CUDA：** CuPy 阵列可与 Numba GPU 内核互操作。
- **cuDF：** 用于 `regionprops_table` 输出上的表格操作。

### CPU/GPU 无关代码

```python
# Switch between CPU and GPU by changing the array module
import cupy as cp  # or: import numpy as cp
from cucim.skimage.filters import gaussian  # or: from skimage.filters import gaussian

result = gaussian(cp.asarray(image), sigma=5)
```

- --

## 与 scikit-image

1 相比的已知限制。 ** API 覆盖不完整：** 实现了约 50-66% 的 scikit-image 函数。值得注意的差距包括一些基于图的分割（分水岭、SLIC 超像素）、一些特征描述符（ORB、BRIEF、HOG）和一些恢复方法。

2. **仅限 Linux。** 不支持 Windows 或 macOS GPU。

3. **需要 NVIDIA GPU。** 不支持 AMD/Intel GPU。

4. **数据必须显式移动到 GPU。** cuCIM 不会自动传输；您必须致电`cp.asarray()`.

5. **图像损失较小。**低于 ~512x512 的图像可能不会受益。低于 ~64x64，CPU 可能更快。

6. **GPU 内存限制。** 必须平铺非常大的图像。 GPU 内存通常小于系统 RAM.

7. **WSI 格式支持有限。** 仅支持 TIFF/SVS/Philips TIFF。 DICOM、NIFTI、Zarr 尚未稳定发布。

8. **每个会话第一次调用时的 JIT 编译开销**（此后缓存）。

- --

## 常见迁移模式

### 模式 1：直接 scikit-image 替换

```python
# Before (CPU)
from skimage.filters import gaussian, sobel, threshold_otsu
from skimage.morphology import binary_opening, disk
from skimage.measure import label, regionprops_table
import numpy as np

image = np.array(...)  # Load image
blurred = gaussian(image, sigma=3)
edges = sobel(blurred)
binary = blurred > threshold_otsu(blurred)
cleaned = binary_opening(binary, footprint=disk(3))
labels = label(cleaned)
props = regionprops_table(labels, image, properties=['area', 'centroid'])

# After (GPU) — change imports, wrap input with cp.asarray
from cucim.skimage.filters import gaussian, sobel, threshold_otsu
from cucim.skimage.morphology import binary_opening, disk
from cucim.skimage.measure import label, regionprops_table
import cupy as cp

image_gpu = cp.asarray(image)  # Transfer once
blurred = gaussian(image_gpu, sigma=3)
edges = sobel(blurred)
binary = blurred > threshold_otsu(blurred)
cleaned = binary_opening(binary, footprint=disk(3))
labels = label(cleaned)
props = regionprops_table(labels, image_gpu, properties=['area', 'centroid'])
```

### 模式 2：数字病理学Pipeline

```python
from cucim import CuImage
from cucim.skimage.color import rgb2gray, separate_stains
from cucim.skimage.filters import threshold_otsu
from cucim.skimage.morphology import binary_opening, remove_small_objects, disk
from cucim.skimage.measure import label, regionprops_table
from cucim.core.operations.color import normalize_colors_pca
import cupy as cp

# Read whole-slide image tile
slide = CuImage("tissue.svs")
tile = cp.asarray(slide.read_region(location=(1000, 2000), size=(512, 512), level=0))

# Normalize staining
normalized = normalize_colors_pca(tile)

# Segment nuclei
gray = rgb2gray(normalized)
binary = gray < threshold_otsu(gray)
cleaned = binary_opening(binary, footprint=disk(2))
cleaned = remove_small_objects(label(cleaned), min_size=50)
labels = label(cleaned)

# Extract properties
props = regionprops_table(labels, gray, properties=['area', 'centroid', 'mean_intensity'])
```

### 模式 3：深度学习预处理 Pipeline

```python
import cupy as cp
from cucim.skimage.transform import resize
from cucim.skimage.exposure import equalize_adapthist
from cucim.skimage.util import img_as_float32
from cucim.core.operations.spatial import rand_image_flip
from cucim.core.operations.color import color_jitter
import torch

# Load batch of images to GPU
images_gpu = cp.asarray(numpy_batch)  # (N, H, W, C)

# Process each image on GPU
processed = []
for img in images_gpu:
    img = img_as_float32(img)
    img = resize(img, (224, 224))
    img = equalize_adapthist(img)
    img = rand_image_flip(img, prob=0.5)
    img = color_jitter(img, brightness=0.2, contrast=0.2)
    processed.append(img)

batch_gpu = cp.stack(processed)

# Zero-copy to PyTorch for model inference
batch_torch = torch.as_tensor(batch_gpu).permute(0, 3, 1, 2)  # NHWC → NCHW
```
