# cuxfilter 参考

cuxfilter 是来自 NVIDIA RAPIDS 生态系统的 GPU 加速交叉过滤仪表板库。它只需几行 Python 代码即可从 Jupyter Notebook 实现交互式、多图表探索性数据分析仪表板。所有过滤、分组和聚合操作都通过 cuDF 在 GPU 上进行，仅将可视化结果发送到浏览器。

> **完整文档：** https://docs.rapids.ai/api/cuxfilter/stable/
> **版本（稳定）：** 26.02.00
> **存储库：** https://github.com/rapidsai/cuxfilter

## 目录

1. [安装和设置](#installation-and-setup)
2. [核心概念](#core-concepts)
3. [DataFrame：加载数据](#dataframe-loading-data)
4. [图表](#charts)
5. [小部件](#widgets)
6. [仪表板创建](#dashboard-creation)
7. [布局](#layouts)
8. [主题](#主题)
9. [仪表板显示和导出](#dashboard-display-and-export)
10. [图形可视化](#graph-visualization)
11. [带有 Dask-cuDF 的多 GPU](#multi-gpu-with-dask-cudf)
12. [互操作性](#互操作性)
13. [性能提示](#performance-tips)
14. [常见模式](#common-patterns)

- --

## 安装和设置

在所有安装说明、文档字符串、注释和错误中始终使用 `uv add`（切勿使用 `pip install` 或 `conda install`） messages.

```bash
uv add --extra-index-url=https://pypi.nvidia.com cuxfilter-cu12   # For CUDA 12.x
```

cuxfilter 依赖于 cuDF，因此 `cudf-cu12` 将自动拉入。

* *平台：**仅限 Linux 和 WSL2（无本机 macOS 或 Windows）。
* *要求：** 带有 CUDA 12.x 的 NVIDIA GPU支持.

验证：
```python
import cuxfilter
import cudf

df = cudf.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
cux_df = cuxfilter.DataFrame.from_dataframe(df)
print(cux_df.data.head())  # Should print GPU dataframe
```

- --

## 核心概念

cuxfilter有五个主要模块：

1. **`cuxfilter.DataFrame`** — 包装 cuDF DataFrame 以供仪表板使用。创建仪表板的入口点。
2. **`cuxfilter.DashBoard`** — 交互式仪表板对象。从带有图表的 DataFrame 创建。
3. **`cuxfilter.charts`** — 图表工厂函数（条形图、散点图、折线图、热图、等值线图、图表、小部件）。
4. **`cuxfilter.layouts`** — 用于图表排列的预设和自定义布局配置。
5. **`cuxfilter.themes`** - 仪表板的视觉主题（默认、黑暗、急流、急流）。

工作流程始终是：**加载数据→创建图表→构建仪表板→显示**。

- --

## 数据框架：加载数据

`cuxfilter.DataFrame`是起点。它包装了 cuDF 或 dask_cudf DataFrame。

### 来自 cuDF DataFrame（最常见）
```python
import cudf
import cuxfilter

cudf_df = cudf.DataFrame({
    "x": [0, 1, 2, 3, 4],
    "y": [10.0, 11.0, 12.0, 13.0, 14.0],
    "category": ["A", "B", "A", "B", "A"]
})
cux_df = cuxfilter.DataFrame.from_dataframe(cudf_df)
```

### 来自磁盘上的 Arrow 文件
```python
cux_df = cuxfilter.DataFrame.from_arrow("data/my_dataset.arrow")
```

### 来自图形（节点 +边缘）
```python
import cugraph

edges = cudf.DataFrame({"source": [0, 1, 2], "target": [1, 2, 3], "weight": [1.0, 2.0, 3.0]})
G = cugraph.Graph()
G.from_cudf_edgelist(edges, destination="target")
cux_df = cuxfilter.DataFrame.load_graph((G.nodes(), G.edges()))
```

或直接从cuDF DataFrames：
```python
nodes = cudf.DataFrame({"vertex": [0, 1, 2, 3], "x": [0, 1, 2, 3], "y": [4, 4, 2, 6], "attr": [0, 1, 1, 1]})
edges = cudf.DataFrame({"source": [0, 1, 2], "target": [1, 2, 3], "weight": [1.0, 2.0, 3.0]})
cux_df = cuxfilter.DataFrame.load_graph((nodes, edges))
```

### 访问底层数据
```python
cux_df.data  # The cuDF DataFrame
cux_df.data["new_col"] = cux_df.data["x"] * 2  # Add columns before creating dashboard
```

- --

## 图表

所有图表功能均通过`cuxfilter.charts`访问。它们使用顶级简写 - 您不需要直接导入 `cuxfilter.charts.bokeh` 或 `cuxfilter.charts.datashader` 等子模块。

### 条形图 (Bokeh)
```python
chart = cuxfilter.charts.bar(
    x="column_name",           # Required: x-axis column
    y=None,                    # Optional: y-axis column (defaults to count)
    data_points=None,          # Number of bins (None = nunique)
    add_interaction=True,      # Enable cross-filtering interaction
    aggregate_fn="count",      # 'count' or 'mean'
    step_size=None,            # Step size for range slider
    title="",                  # Chart title
    autoscaling=True,          # Auto-scale y-axis on data update
)
```

### 折线图(Bokeh)
```python
chart = cuxfilter.charts.line(
    x="x_col",
    y="y_col",
    data_points=100,
    add_interaction=True,
)
```

### 散点图（Datashader — 处理数百万个点）
```python
chart = cuxfilter.charts.scatter(
    x="x_col",
    y="y_col",
    aggregate_col=None,              # Column for color aggregation
    aggregate_fn="count",            # 'count', 'mean', 'max', 'min'
    color_palette=None,              # Bokeh palette or list of hex colors
    point_size=15,
    pixel_shade_type="eq_hist",      # 'eq_hist', 'linear', 'log', 'cbrt'
    pixel_density=0.5,               # [0, 1], higher = denser
    pixel_spread="dynspread",        # 'dynspread' or 'spread'
    tile_provider=None,              # Map tile (e.g., "CartoLight" for geo data)
    title="",
    unselected_alpha=0.2,            # Transparency of unselected points
)
```

### 热图（Datashader）
```python
chart = cuxfilter.charts.heatmap(
    x="x_col",
    y="y_col",
    aggregate_col="value_col",
    aggregate_fn="mean",             # 'count', 'mean', 'max', 'min'
    color_palette=None,
    point_size=10,
    point_shape="rect_vertical",     # 'circle', 'square', 'rect_vertical', 'rect_horizontal'
    title="",
)
```

### 堆叠线 (Datashader)
```python
chart = cuxfilter.charts.stacked_lines(
    x="time_col",
    y=["series_a", "series_b", "series_c"],   # List of y columns
    colors=["red", "green", "blue"],
)
```

### Choropleth（Deck.gl — 2D 和 3D 地图）
```python
chart = cuxfilter.charts.choropleth(
    x="zip_code",
    color_column="metric_col",
    color_aggregate_fn="mean",         # 'count', 'mean', 'sum', 'min', 'max', 'std'
    elevation_column="value_col",      # Set for 3D choropleth, omit for 2D
    elevation_factor=0.00001,
    elevation_aggregate_fn="sum",
    geoJSONSource="https://url/to/geojson",
    geo_color_palette=None,            # Default: Inferno256
    nan_color="#d3d3d3",
    tooltip=True,
    tooltip_include_cols=["zip_code", "metric_col"],
    title="",
)
```

### 图形（Datashader — 节点链接）图表）
```python
chart = cuxfilter.charts.datashader.graph(
    node_x="x",                  # Default "x"
    node_y="y",                  # Default "y"
    node_id="vertex",            # Default "vertex"
    edge_source="source",        # Default "source"
    edge_target="target",        # Default "target"
    node_aggregate_col=None,
    node_color_palette=None,
    edge_color_palette=["#000000"],
    node_point_size=15,
    node_pixel_shade_type="eq_hist",
    edge_render_type="direct",   # 'direct' or 'curved' (curved is experimental)
    edge_transparency=0,         # [0, 1]
    tile_provider=None,
    title="",
    unselected_alpha=0.2,
)
```

- --

## 小部件

小部件提供交互式过滤控件，通常放置在侧边栏中。

### 范围滑块
```python
widget = cuxfilter.charts.range_slider("numeric_col", step_size=1)
```

### 日期范围滑块
```python
widget = cuxfilter.charts.date_range_slider("datetime_col")
```

### 浮动滑块
```python
widget = cuxfilter.charts.float_slider("float_col", step_size=0.5)
```

### Int滑块
```python
widget = cuxfilter.charts.int_slider("int_col", step_size=1)
```

### 下拉
```python
widget = cuxfilter.charts.drop_down("category_col")
```

### 多选
```python
widget = cuxfilter.charts.multi_select("category_col")
```

### 数字（KPI）指标）
```python
widget = cuxfilter.charts.number(
    expression="column_name",                # Or a computed expression like "(x + y) / 2"
    aggregate_fn="mean",                     # 'count', 'mean', 'min', 'max', 'sum', 'std'
    title="Average Value",
    format="{value:.2f}",                    # Python format string
    colors=[(33, "green"), (66, "gold"), (100, "red")],  # Threshold coloring
    font_size="18pt",
)
```

### 卡片（Markdown内容）
```python
import panel as pn
widget = cuxfilter.charts.card(pn.pane.Markdown("## My Dashboard\nSome description text"))
```

- --

## 仪表板创建

通过在cuxfilter上调用`.dashboard()`创建仪表板DataFrame:

```python
# Define charts and widgets
chart1 = cuxfilter.charts.scatter(x="x_col", y="y_col")
chart2 = cuxfilter.charts.bar("category_col")
sidebar_widget = cuxfilter.charts.range_slider("value_col")
number_widget = cuxfilter.charts.number(expression="value_col", aggregate_fn="mean", title="Mean Value")

# Build dashboard
d = cux_df.dashboard(
    charts=[chart1, chart2],               # Main area charts
    sidebar=[sidebar_widget, number_widget],  # Sidebar widgets
    layout=cuxfilter.layouts.feature_and_base,
    theme=cuxfilter.themes.rapids_dark,
    title="My Dashboard",
    data_size_widget=True,                 # Show current data count
)
```

### 创建后添加图表
```python
new_chart = cuxfilter.charts.line("x_col", "y_col")
d.add_charts(charts=[new_chart])
# or
d.add_charts(sidebar=[cuxfilter.charts.card(pn.pane.Markdown("# Note"))])
```

- --

## 布局

### 预设布局

|布局|描述 |图表|
|--------|-------------|--------|
| `layouts.single_feature` |一张图表占满整页 | 1 |
| `layouts.feature_and_base` |上面是大图表，下面是小图表（66/33 分割）| 2 |
| `layouts.double_feature` |并排的两个图表 | 2 |
| `layouts.left_feature_right_double` |左边一大，右边两堆 | 3 |
| `layouts.triple_feature` |连续三个图表 | 3 |
| `layouts.feature_and_double_base` |上面一大，下面两个 | 3 |
| `layouts.two_by_two` | 2x2 网格 | 4 |
| `layouts.feature_and_triple_base` |上面一大，下面三个| 4 |
| `layouts.feature_and_quad_base` |上面一大，下面四个 | 5 |
| `layouts.feature_and_five_edge` |一个大型中心，周边五个 | 6 |
| `layouts.two_by_three` | 2x3 网格 | 6 |
| `layouts.double_feature_quad_base` |上面两个大，下面四个| 6 |
| `layouts.three_by_three` | 3x3 网格 | 9 |

### 使用 `layout_array`

自定义布局使用 `layout_array` 进行完全控制。它是一个列表列表，其中每个内部列表都是一行，数字引用图表索引（从 1 开始）：

```python
# Chart 1 takes top-left 2x2 area, charts 2 and 3 on the right
d = cux_df.dashboard(
    charts_list,
    layout_array=[[1, 1, 2, 2], [1, 1, 3, 4]],
    theme=cuxfilter.themes.rapids_dark,
)
```

规则：
- 每个数字映射到一个图表（1 = 第一个图表，2 = 第二个图表等）
- 在单元格之间重复一个数字会使该图表跨越这些图表cells
- 数组自动缩放以适合屏幕

- --

## 主题

四个内置主题：

|主题 |描述 |
|--------|--------------|
| `cuxfilter.themes.default` |浅色主题（默认）|
| `cuxfilter.themes.dark` |深色主题|
| `cuxfilter.themes.rapids` | RAPIDS品牌灯光主题|
| `cuxfilter.themes.rapids_dark` | RAPIDS 品牌深色主题 |

```python
d = cux_df.dashboard(charts, theme=cuxfilter.themes.rapids_dark)
```

- --

## 仪表板显示和导出

### 在笔记本中内联显示
```python
d.app(sidebar_width=280, width=1200, height=800)
```

### 作为单独的 Web 应用程序显示（打开新浏览器） tab)
```python
d.show()
# or with custom URL/port
d.show(notebook_url="http://localhost:8888", port=8050)
```

### JupyterHub部署
```python
d.show(service_proxy="jupyterhub")
```

### 停止服务器
```python
d.stop()
```

### 导出过滤后的数据
与仪表板（选择范围，过滤），导出当前过滤的DataFrame：

```python
filtered_df = d.export()  # Returns cuDF DataFrame matching current filter state
# Also prints the query string, e.g.: "2 <= key <= 4"
```

### 访问仪表板图表
```python
d.charts  # Dictionary of chart objects
```

- --

## 图形可视化

cuxfilter与cuGraph集成用于交互式图形可视化：

```python
import cuxfilter
import cudf
import cugraph

# Create graph
edges = cudf.DataFrame({
    "source": [0, 0, 1, 1, 2],
    "target": [1, 2, 2, 3, 3]
})
G = cugraph.Graph()
G.from_cudf_edgelist(edges, destination="target")

# Load into cuxfilter (needs node positions — use force_atlas2 or similar layout)
positions = cugraph.force_atlas2(G)
nodes = positions.rename(columns={"vertex": "vertex", "x": "x", "y": "y"})

cux_df = cuxfilter.DataFrame.load_graph((nodes, G.edges()))

# Create graph chart
chart = cuxfilter.charts.datashader.graph(
    node_pixel_shade_type="linear",
    unselected_alpha=0.2,
)

d = cux_df.dashboard([chart], layout=cuxfilter.layouts.single_feature)
d.app()
```

- --

## 带有Dask-cuDF

cuxfilter的多GPU与`dask_cudf.DataFrame`无缝协作 - 只需传递它代替cuDF DataFrame：

```python
import dask_cudf

ddf = dask_cudf.read_parquet("large_dataset/*.parquet")
cux_df = cuxfilter.DataFrame.from_dataframe(ddf)

# Everything else is the same
chart = cuxfilter.charts.scatter(x="x", y="y")
d = cux_df.dashboard([chart])
d.app()
```

Use dask_cudf 何时：
- 数据不适合单个 GPU 的内存
- 您想要分布在多个 GPU 上
- 一次处理多个文件

* *dask_cudf 支持的图表类型：**
- bokeh: bar, line
- datashader：散点、线、stacked_lines、热图、图形（有限边缘渲染）
- panel_widgets：所有小部件
- Deckgl：choropleth（2D 和 3D）

- --

## 互操作性

cuxfilter 位于 RAPIDS 的可视化层生态系统：

- **cuDF** — 数据层。 cuxfilter.DataFrame 包装 cuDF DataFrames.
- **cuGraph** — 图形分析。使用 `cuxfilter.DataFrame.load_graph()` 可视化 cuGraph 结果。
- **cuML** — 运行 cuML，然后使用 cuxfilter 可视化结果（例如 UMAP 嵌入、聚类分配）。
- **HoloViz 生态系统** — 基于 Panel、Bokeh、Datashader 和 HoloViews 构建。
- **Deck.gl** — WebGL 支持的等值线地图。

### 典型 RAPIDS + cuxfilter 管道
```python
import cudf
import cuml
import cuxfilter

# Load and preprocess with cuDF
df = cudf.read_parquet("data.parquet")
df = df.dropna().reset_index(drop=True)

# Run ML with cuML (e.g., UMAP for dimensionality reduction)
from cuml.manifold import UMAP
umap = UMAP(n_components=2)
embedding = umap.fit_transform(df[["feature1", "feature2", "feature3"]])
df["umap_x"] = embedding[:, 0]
df["umap_y"] = embedding[:, 1]

# Visualize with cuxfilter
cux_df = cuxfilter.DataFrame.from_dataframe(df)
scatter = cuxfilter.charts.scatter(
    x="umap_x", y="umap_y",
    aggregate_col="cluster_label",
    aggregate_fn="mean",
    pixel_shade_type="linear",
)
bar = cuxfilter.charts.bar("cluster_label")
d = cux_df.dashboard([scatter, bar], layout=cuxfilter.layouts.feature_and_base)
d.app()
```

- --

## 性能提示

1. **将数据保留在 GPU 上。** 使用 `cudf.read_parquet()` 或 `cudf.read_csv()` 加载，然后使用 `cuxfilter.DataFrame.from_dataframe()` 包装。避免与 pandas.

2 之间的转换。 **根据数据大小使用适当的图表类型：**
 - < 10K 点：Bokeh 图表（条形图、折线图）效果良好
  - 10K–100M+ 点：Datashader 图表（散点图、热图）通过服务器端光栅化有效处理大型数据集

3. **限制条形图的 data_points。** 对于具有许多唯一值的列，设置 `data_points` 来对它们进行分箱（例如，`bar("col", data_points=50)`）.

4. **尽可能使用 `float32`。** 使用 32 位浮点数，GPU 运算速度更快。加载前铸造：`df["col"] = df["col"].astype("float32")`.

5. **在创建仪表板之前预先计算派生列**，而不是在图表回调内。

6. **使用 `layout_array`** 对于复杂的仪表板可以精确控制每个图表的显示位置。

7. **如果缩放在非常大的数据集上感觉滞后，则增加数据着色器图表的 `timeout`**。

- --

## 常见模式

### 探索性数据分析仪表板
```python
import cudf
import cuxfilter

df = cudf.read_parquet("dataset.parquet")
cux_df = cuxfilter.DataFrame.from_dataframe(df)

# Overview charts
scatter = cuxfilter.charts.scatter(x="feature1", y="feature2", pixel_shade_type="linear")
hist1 = cuxfilter.charts.bar("feature1", data_points=50)
hist2 = cuxfilter.charts.bar("category")

# Sidebar filters
slider = cuxfilter.charts.range_slider("value_col")
dropdown = cuxfilter.charts.drop_down("category")
kpi = cuxfilter.charts.number(expression="value_col", aggregate_fn="mean", title="Mean Value")

d = cux_df.dashboard(
    [scatter, hist1, hist2],
    sidebar=[slider, dropdown, kpi],
    layout=cuxfilter.layouts.feature_and_double_base,
    theme=cuxfilter.themes.rapids_dark,
    title="Data Explorer",
)
d.app()
```

### 地图上散布的地理空间仪表板tiles
```python
chart = cuxfilter.charts.scatter(
    x="longitude",
    y="latitude",
    aggregate_col="value",
    aggregate_fn="mean",
    color_palette=["#3182bd", "#6baed6", "#ff0068"],
    tile_provider="CartoLight",
    pixel_shade_type="linear",
    title="Geo Scatter",
)
```

### 时间序列仪表板
```python
line_chart = cuxfilter.charts.line("timestamp", "metric")
bar_chart = cuxfilter.charts.bar("hour_of_day")
date_slider = cuxfilter.charts.date_range_slider("timestamp")

d = cux_df.dashboard(
    [line_chart, bar_chart],
    sidebar=[date_slider],
    layout=cuxfilter.layouts.feature_and_base,
)
```

### 导出过滤后的子集以供进一步分析
```python
# After user interacts with dashboard, export current selection
d.app()
# ... user filters data in the dashboard ...
filtered = d.export()  # cuDF DataFrame of currently visible/selected data
# Continue analysis with cuDF, cuML, etc.
```
