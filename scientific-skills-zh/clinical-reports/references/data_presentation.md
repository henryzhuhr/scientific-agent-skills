# 临床报告中的数据呈现

## 临床数据表格

### 表格设计原则

* *一般准则：**
- 描述表格内容的清晰、简洁的标题
- 带单位的列标题
- 行标签左对齐，数据适当对齐（数字右对齐，文本左对齐）
- 脚注缩写、统计符号、特殊情况
- 一致的小数位（百分比通常为 1-2，连续变量为 1-3）
- 整个文档的格式一致

* *标题位置：**
- 上表
- 按顺序编号（表 1、表 2、等）
- 描述性足以独立

* *脚注符号（按顺序）：**
- *, †, ‡, §, ||, ¶, #
- 或使用上标字母 (a, b, c...)
- 或使用上标数字（如果不与混淆）参考文献

### 人口统计和基线特征表

* *目的：**描述基线的研究人群

* *标准格式：**

```
Table 1. Baseline Demographics and Clinical Characteristics

Characteristic                  Treatment Group    Control Group    Total
                               (N=150)            (N=145)          (N=295)
─────────────────────────────────────────────────────────────────────────
Age, years
  Mean (SD)                    64.2 (8.5)         63.8 (9.1)       64.0 (8.8)
  Median (IQR)                 65 (58-71)         64 (57-70)       64 (58-71)
  Range                        45-82              43-85            43-85

Sex, n (%)
  Male                         95 (63.3)          88 (60.7)        183 (62.0)
  Female                       55 (36.7)          57 (39.3)        112 (38.0)

Race, n (%)
  White                        110 (73.3)         105 (72.4)       215 (72.9)
  Black/African American       25 (16.7)          28 (19.3)        53 (18.0)
  Asian                        10 (6.7)           8 (5.5)          18 (6.1)
  Other                        5 (3.3)            4 (2.8)          9 (3.0)

BMI, kg/m²
  Mean (SD)                    28.5 (4.2)         28.1 (4.5)       28.3 (4.4)

Baseline HbA1c, %
  Mean (SD)                    8.9 (1.2)          9.0 (1.3)        9.0 (1.2)

Disease duration, years
  Median (IQR)                 6 (3-10)           5 (3-9)          6 (3-10)

Prior medications, n (%)
  Metformin                    135 (90.0)         130 (89.7)       265 (89.8)
  Sulfonylurea                 45 (30.0)          42 (29.0)        87 (29.5)
  Insulin                      20 (13.3)          18 (12.4)        38 (12.9)
─────────────────────────────────────────────────────────────────────────
SD = standard deviation; IQR = interquartile range; BMI = body mass index;
HbA1c = hemoglobin A1c
```

* *关键要素：**
- 每组的样本量(N=)
- 连续变量：平均值 (SD)、中位数 (IQR)、范围
- 分类变量：n (%)
- 基线比较无 p 值（有争议，但一般不推荐）

### 功效结果表

* *目的：** 目前主要和次要终点结果

* *示例：**

```
Table 2. Primary and Secondary Efficacy Endpoints at Week 24

Endpoint                           Treatment      Control        Difference    P-value
                                   (N=150)        (N=145)        (95% CI)
──────────────────────────────────────────────────────────────────────────────────
Primary Endpoint
Change in HbA1c from baseline, %
  Mean (SE)                        -1.8 (0.1)     -0.6 (0.1)     -1.2          <0.001
  95% CI                           (-2.0, -1.6)   (-0.8, -0.4)   (-1.5, -0.9)

Secondary Endpoints
Change in FPG, mg/dL
  Mean (SE)                        -42.5 (3.2)    -15.2 (3.4)    -27.3         <0.001
  95% CI                           (-48.8, -36.2) (-21.9, -8.5)  (-36.4, -18.2)

% achieving HbA1c <7%
  n (%)                            78 (52.0)      25 (17.2)      -              <0.001
  95% CI                           (43.9, 60.1)   (11.4, 24.5)   

Change in body weight, kg
  Mean (SE)                        -3.2 (0.4)     -0.5 (0.4)     -2.7          <0.001
  95% CI                           (-4.0, -2.4)   (-1.3, 0.3)    (-3.8, -1.6)
──────────────────────────────────────────────────────────────────────────────
SE = standard error; CI = confidence interval; HbA1c = hemoglobin A1c; 
FPG = fasting plasma glucose
```

* *统计表示：**
- 具有精度测量的点估计（SE 或 CI）
- p 值（考虑多重性调整）
- 效应大小（差异或比率）为 95% CI
- 注明显着性水平（例如，p<0.05、p<0.01、p<0.001）

### 不良事件表

* *目的：** 总结安全性数据

* *示例：**

```
Table 3. Summary of Adverse Events

Event Category                        Treatment     Control       P-value
                                      (N=150)       (N=145)
                                      n (%)         n (%)
──────────────────────────────────────────────────────────────────────────
Any adverse event                     120 (80.0)    95 (65.5)     0.004

Treatment-related adverse events       85 (56.7)    42 (29.0)     <0.001

Serious adverse events                 12 (8.0)     8 (5.5)       0.412

Adverse events leading to              8 (5.3)      4 (2.8)       0.257
discontinuation

Deaths                                 0 (0.0)      1 (0.7)       0.492

Common adverse events (≥5% in any group)
  Nausea                              45 (30.0)     12 (8.3)      <0.001
  Diarrhea                            38 (25.3)     10 (6.9)      <0.001
  Headache                            22 (14.7)     18 (12.4)     0.568
  Hypoglycemia                        18 (12.0)     5 (3.4)       0.007
  Dizziness                           12 (8.0)      8 (5.5)       0.412
──────────────────────────────────────────────────────────────────────────
Adverse events coded using MedDRA version 24.0
```

* *关键要素：**
- 总体不良事件摘要
- 突出显示严重不良事件
- 报告的死亡情况
- 常见不良事件（通常≥5% 或≥10%）阈值）
- MedDRA 编码表示

### 实验室异常表

* *显示相对于基线的变化的移位表：**

```
Table 4. Laboratory Values Meeting Predefined Criteria for Abnormality

Laboratory Parameter                 Treatment      Control
                                     (N=150)        (N=145)
                                     n (%)          n (%)
──────────────────────────────────────────────────────────────────────────
ALT >3× ULN                          8 (5.3)        3 (2.1)
AST >3× ULN                          5 (3.3)        2 (1.4)
Total bilirubin >2× ULN              2 (1.3)        1 (0.7)
Creatinine >1.5× baseline            12 (8.0)       5 (3.4)
Hemoglobin <10 g/dL                  3 (2.0)        2 (1.4)
Platelets <100 × 10³/μL              1 (0.7)        0 (0.0)
──────────────────────────────────────────────────────────────────────────
ULN = upper limit of normal; ALT = alanine aminotransferase; 
AST = aspartate aminotransferase
```

### 患者处置表（CONSORT 格式）

```
Table 5. Patient Disposition

Disposition                              Treatment     Control       Total
                                         (N=150)       (N=145)       (N=295)
────────────────────────────────────────────────────────────────────────────
Screened                                 -             -             425

Randomized                               150           145           295

Completed study                          135 (90.0)    130 (89.7)    265 (89.8)

Discontinued, n (%)                      15 (10.0)     15 (10.3)     30 (10.2)
  Adverse event                          8 (5.3)       4 (2.8)       12 (4.1)
  Lack of efficacy                       2 (1.3)       5 (3.4)       7 (2.4)
  Lost to follow-up                      3 (2.0)       4 (2.8)       7 (2.4)
  Withdrawal of consent                  2 (1.3)       2 (1.4)       4 (1.4)

Included in efficacy analysis
  ITT population                         150 (100)     145 (100)     295 (100)
  Per-protocol population                142 (94.7)    138 (95.2)    280 (94.9)

Included in safety analysis              150 (100)     145 (100)     295 (100)
────────────────────────────────────────────────────────────────────────────
ITT = intent-to-treat
```

## 临床数据图

### 图形设计原则

* *一般准则：**
- 清晰、简洁图下的标题/图例
- 按顺序编号（图 1、图 2 等）
- 带单位的轴标签
- 清晰的字体大小（最小 8-10 点）
- 高分辨率（打印 300 dpi，网页 150 dpi）
- 色盲友好调色板
- 黑白兼容（使用不同的符号/图案）

* *图标题：**
- 描述所显示的内容
- 解释符号、误差线、统计注释
- 定义缩写
- 提供解释上下文

### CONSORT流程图

* *目的：**显示随机试验的患者流程

```
                    Assessed for eligibility (n=425)
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
    Excluded (n=130)                                │
    • Not meeting inclusion criteria (n=85)         │
    • Declined to participate (n=32)                │
    • Other reasons (n=13)                          │
                                                    │
                                           Randomized (n=295)
                                                    │
                    ┌───────────────────────────────┴───────────────────────────────┐
                    │                                                               │
        Allocated to Treatment (n=150)                             Allocated to Control (n=145)
        • Received allocated intervention (n=148)                  • Received allocated intervention (n=143)
        • Did not receive allocated intervention (n=2)             • Did not receive allocated intervention (n=2)
          Reasons: withdrew consent before treatment                Reasons: withdrew consent before treatment
                    │                                                               │
        ┌───────────┴────────────┐                                  ┌──────────────┴─────────────┐
        │                        │                                  │                            │
    Lost to follow-up (n=3)  Discontinued (n=12)              Lost to follow-up (n=4)     Discontinued (n=11)
                             • Adverse events (n=8)                                       • Adverse events (n=4)
                             • Lack of efficacy (n=2)                                     • Lack of efficacy (n=5)
                             • Withdrew consent (n=2)                                     • Withdrew consent (n=2)
                    │                                                               │
            Analyzed (n=150)                                               Analyzed (n=145)
            • ITT analysis (n=150)                                         • ITT analysis (n=145)
            • Per-protocol analysis (n=142)                                • Per-protocol analysis (n=138)
            • Excluded from analysis (n=0)                                 • Excluded from analysis (n=0)
```

### Kaplan-Meier生存曲线

* *目的：**显示事件发生时间数据

* *元素：**
- X轴：时间（周、月、年）
- Y 轴：无事件生存概率（0 至 1 或 0% 至 100%）
- 每个治疗组的单独曲线
- 标记的截尾观察结果（通常带有垂直刻度线）
- 下表中的危险人数
- 中位生存时间指示
- 对数秩p值
- 95％CI

的危险比**标题示例：**
```
Figure 1. Kaplan-Meier Curves for Overall Survival

Kaplan-Meier estimates of overall survival in the treatment and control groups.
Tick marks indicate censored observations. Number at risk shown below graph.
Log-rank p<0.001. Median survival: Treatment 24.5 months (95% CI: 22.1-26.8),
Control 18.2 months (95% CI: 16.5-20.1). Hazard ratio 0.68 (95% CI: 0.55-0.84).
```

### 森林图

* *用途：**显示子组分析或荟萃分析结果

* *元素：**
- 点估计（正方形或菱形）
- 与精度（逆方差）或样本大小成正比的符号大小
- 显示95％的水平线CI
- 零效应时的垂直线（HR = 1.0，OR = 1.0，或差异 = 0)
- 左侧的子组标签
- 右侧的效应大小值
- 总体估计（如果荟萃分析）
- 异质性统计（I²，p 值）

* *标题示例：**
```
Figure 2. Forest Plot of Treatment Effect by Subgroup

Effect of treatment vs. control on primary endpoint across pre-specified subgroups.
Squares represent point estimates; horizontal lines represent 95% confidence intervals.
Square size is proportional to subgroup sample size. Overall effect shown as diamond.
p-value for interaction testing heterogeneity of treatment effect across subgroups.
```

### 箱线图

* *用途：**显示连续变量

的分布**元素：**
- 方框：IQR（第 25 到第 75 个百分位）
- 方框中的行：中值
- 晶须：扩展到 1.5 × IQR
 内的最极端数据点 - 离群值：超出晶须的点（通常显示为圆圈）
- X 轴：组或时间点
- Y轴：带单位的连续变量

### 带回归的散点图

* *用途：**显示两个连续变量之间的关系

* *元素：**
- X轴：自变量
- Y轴：因变量
- 个体数据点
- 回归线（如果适用）
- 回归方程
- R² 值
- 斜率的P 值
- 回归线的95% 置信区间（可选，显示为阴影区域）

### Spaghetti图

* *目的：**显示随时间变化的个体轨迹

* *元素：**
- X轴：时间
- Y轴：结果变量
- 个体患者线（通常是半透明的）
- 平均轨迹（粗体）线）
- 治疗组的单独颜色

### 条形图

* *目的：**比较各组之间的比例或平均值

* *元素：**
- 条形之间的清晰分隔
- 误差条（SEM或95％CI）
- Y轴从0开始（条形图不要截断）
- X 轴上的组标签
- Y 轴上带有单位的值标签
- 指示统计显着性（p 值或星号）

* *避免：**
- 3D 条形图（扭曲感知）
- 过多装饰
- 条形截断的Y 轴

### 折线图

* *用途：** 显示随时间的变化

* *元素：**
- X 轴：时间（间隔一致）
- Y 轴：结果变量
- 每个单独的线组（不同颜色/图案）
- 标记的数据点（圆形、正方形、三角形）
- 每个时间点的误差线（SE 或 95% CI）
- 识别组的图例
- 网格线（可选，浅灰色）

### 直方图

* *用途：**显示连续变量的分布

* *元素：**
- X轴：变量（分为箱）
- Y轴：频率或密度
- 适当的箱宽度（不要太少，不要太多）
- 叠加正态分布曲线（如果测试正态性）

## 临床数据的特殊注意事项

### 呈现比例

* *分子和分母：**
- 始终提供两者：25/100 (25%)
- 不仅仅是百分比 (25%)

* *百分比：**
- 如果 n<100
，则没有小数位- 如果 n<100
，则为 1 位小数n≥100
- 永远不要报告 > 1 位小数的百分比

* *比例的置信区间：**
- Wilson 得分区间或精确二项式（对于小样本优于 Wald）
- 始终以百分比报告

### 呈现连续数据

* *中心的测量趋势：**
- 正态分布数据的均值
- 偏斜数据或序数数据的中位数
- 如果分布不清楚，则报告两者

* * 离散度测量：**
- **标准偏差 (SD)**：描述数据中的变异性
- **标准误差 (SE)**：描述平均值估计的精度
- **95% 置信区间**：推论统计的首选
- **四分位数间距 (IQR)**：使用偏斜数据的中位数
- **范围**：最小值到最大值

* *何时使用每个：**
- 描述性统计 → 平均值 (SD)或中位数 (IQR)
- 推论统计 → 平均值 (95% CI)或平均值 (SE)
- 切勿在未指定 SD、SE 或 CI 的情况下使用 ± 

### 呈现 P 值

* *报告指南：**
- 报告精确的 p 值，精确到小数点后 2-3 位(p=0.042)
- 对于非常小的 p 值，使用 p<0.001（而不是 p=0.000）
- 请勿报告为“NS”或“p=NS”
- 对于不显着的结果，报告精确的 p 值（p=0.18，而不是 p>0.05）
- 指定双尾，除非预先指定单尾
- 在适当时正确进行多重比较
- 报告使用的显着性阈值（α=0.05 是标准）

* *避免：**
- p<0.05（报告精确值）
- p=0.00（不可能）
- 多个小数位（p=0.04235891）

### 统计显着性指标

* *选项：**
1. 在表
2 中报告p 值。使用带有图例的星号：
 - *p<0.05
  - **p<0.01
  - ***p<0.001
3. 使用置信区间（首选）

### 置信区间

* *报告：**
- 95% CI 为标准
- 格式：（下限、上限）
- 或：下限到上限
- 或：下限-上限limit

* *解释：**
- 如果差异的 CI 排除 0 → 显着性 
- 如果比率的 CI 排除 1 → 显着性 
- CI 的宽度表示精度

### 缺失数据

* * 明确指出：**
- 解释缺失的脚注数据
- 清楚地说明分析是否完成情况
- 如果使用则描述插补方法
- 报告每个变量的缺失数据量

### 小数位和舍入

* *一般规则：**
- 报告测量精度水平
- 内部一致的小数位表
- 将p值四舍五入到2-3位小数
- 将百分比四舍五入到0-1位小数
- 将平均值/中位数四舍五入到1-2位小数
- 包括适当的有效数字

## 用于创建数字的软件

* *统计软件：**
- R (ggplot2) - 高度可定制
- GraphPad Prism - 用户友好的生物医学
- SAS、Stata、SPSS - 全面的统计软件包
- Python (matplotlib、seaborn) - 灵活且功能强大

* *通用图形软件：**
- Adobe Illustrator - 专业出版质量
- Inkscape - 免费矢量图形编辑器
- PowerPoint - 基本图形，易于使用
- BioRender - 生物原理图和图形

## 配色方案

* *色盲友好调色板：**
- 避免红绿组合
- 使用蓝橙色、蓝黄色
- 包括形状/图案差异
- 以灰度测试图形

* *推荐调色板：**
- ColorBrewer（专为数据可视化而设计）
- Viridis（感知均匀）
- IBM 色盲安全调色板

## 图像质量标准

* *分辨率：**
- 300 dpi 用于印刷出版物
- 网页/屏幕为 150 dpi
- 图形首选矢量图形（PDF、SVG）

* *文件格式：**
- 用于打印的 TIFF 或 EPS
- 用于网页的 PNG
- 用于矢量图形的 PDF
- 可接受 JPEG照片（高质量）

* *图像编辑：**
- 禁止更改数据的操作
- 仅可接受的调整：应用于整个图像的亮度、对比度、色彩平衡
- 记录所有调整
- 如果需要，请提供原始图像

- --

此参考为在表格中呈现临床数据提供全面指导以及遵循最佳实践和出版标准的数据。使用这些指南来创建清晰、准确和专业的数据演示。
