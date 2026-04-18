# 信息图表类型参考指南

此参考为每种信息图表类型提供扩展模板、示例和提示模式。

- --

## 1. 统计/数据驱动信息图表

### 目的
以引人入胜的视觉格式呈现定量数据、统计数据、调查结果和数值比较。

### Visual元素
- **条形图**：水平或垂直比较
- **饼图/圆环图**：用于比例和百分比
- **折线图**：用于随时间变化的趋势
- **大数字标注**：突出显示关键统计数据
- **图标**：直观地表示类别
- **进度条形**：显示百分比或完成情况

### 布局模式
- **单统计英雄**：具有支持上下文的一大数字
- **多统计网格**：网格布局中的3-6个统计数据
- **以图表为中心**：带有支持文本的大型可视化
- **比较条形**：并排栏比较

### 提示模板

* *单统计英雄：**
```
Statistical infographic featuring one key statistic about [TOPIC]:
Main stat: [LARGE NUMBER] [UNIT/CONTEXT]
Supporting context: [2-3 sentences explaining the significance]
Large bold number in center, supporting text below,
relevant icon or illustration, [COLOR] accent color,
clean minimal design, white background.
```

* *多统计网格：**
```
Statistical infographic presenting [TOPIC] data:
Stat 1: [NUMBER] [LABEL] (icon: [ICON])
Stat 2: [NUMBER] [LABEL] (icon: [ICON])
Stat 3: [NUMBER] [LABEL] (icon: [ICON])
Stat 4: [NUMBER] [LABEL] (icon: [ICON])
2x2 grid layout, large bold numbers, small icons above each,
[COLOR SCHEME], modern clean typography, white background.
```

* *以图表为中心：**
```
Statistical infographic with [CHART TYPE] showing [TOPIC]:
Data points: [VALUE 1], [VALUE 2], [VALUE 3], [VALUE 4]
Labels: [LABEL 1], [LABEL 2], [LABEL 3], [LABEL 4]
Large [bar/pie/donut] chart as main element,
title at top, legend below chart, [COLOR SCHEME],
data labels on chart, clean professional design.
```

### 示例提示

* *医疗保健统计：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Statistical infographic about heart disease: \
   Main stat: 17.9 million deaths per year globally. \
   Supporting stats in grid: 1 in 4 deaths caused by heart disease, \
   80% of heart disease is preventable, \
   150 minutes of exercise weekly reduces risk by 30%. \
   Heart icon, red and pink color scheme with gray accents, \
   large bold numbers, clean medical professional design, white background" \
  --output figures/heart_disease_stats.png
```

* *业务指标：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Statistical infographic for Q4 business results: \
   Revenue: $2.4M (+15% YoY), Customers: 12,500 (+22%), \
   NPS Score: 78 (+8 points), Retention: 94%. \
   4-stat grid with upward arrow indicators for growth, \
   bar chart showing quarterly trend, \
   navy blue and gold corporate color scheme, \
   professional business design, white background" \
  --output figures/q4_metrics.png
```

- --

## 2. 时间线信息图表

### 目的
按时间顺序显示事件、里程碑或发展。

### 视觉元素
- **时间线轴**：水平或垂直线
- **日期标记**：年、月或特定日期
- **事件节点**：每个点的圆圈、图标或图像
- **描述框**：每个事件的简短文本
- **连接元素**：线条、箭头或路径

### 布局模式
- **水平时间线**：从左到右进展
- **垂直时间线**：从上到下进展
- **缠绕/蛇形时间线**：适用于许多事件的S曲线
- **圆形时间线**：适用于循环或重复事件

### 提示模板

* *水平时间线：**
```
Horizontal timeline infographic showing [TOPIC] from [START YEAR] to [END YEAR]:
[YEAR 1]: [EVENT 1] - [brief description]
[YEAR 2]: [EVENT 2] - [brief description]
[YEAR 3]: [EVENT 3] - [brief description]
[YEAR 4]: [EVENT 4] - [brief description]
Left-to-right timeline with circular nodes for each event,
connecting line between nodes, icons above each node,
[COLOR] gradient from past to present, date labels below,
clean modern design, white background.
```

 * *垂直时间线：**
```
Vertical timeline infographic showing [TOPIC]:
Top (earliest): [YEAR] - [EVENT]
Middle events: [YEAR] - [EVENT], [YEAR] - [EVENT]
Bottom (latest): [YEAR] - [EVENT]
Top-to-bottom flow, alternating left-right event boxes,
central vertical line connecting all events,
circular nodes with dates, [COLOR SCHEME],
professional clean design, white background.
```

 * *项目里程碑时间线：**
```
Project timeline infographic for [PROJECT NAME]:
Phase 1: [DATES] - [MILESTONE] (status: complete)
Phase 2: [DATES] - [MILESTONE] (status: in progress)
Phase 3: [DATES] - [MILESTONE] (status: upcoming)
Phase 4: [DATES] - [MILESTONE] (status: planned)
Gantt-style horizontal bars, color-coded by status,
green for complete, yellow for in progress, gray for upcoming,
project name header, clean professional design.
```

### 示例提示

* *技术演变：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Horizontal timeline infographic: Evolution of Mobile Phones \
   1983: First mobile phone (Motorola DynaTAC), \
   1992: First smartphone (IBM Simon), \
   2007: iPhone launches touchscreen era, \
   2010: First 4G networks, \
   2019: First 5G phones, \
   2023: Foldable phones mainstream. \
   Phone icons evolving at each node, gradient from gray (old) to blue (new), \
   connecting timeline arrow, year labels, clean tech design" \
  --output figures/mobile_evolution.png
```

* *公司历史：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Vertical timeline infographic: Our Company Journey \
   2010: Founded in garage with 2 employees, \
   2012: First major client signed, \
   2015: Reached 100 employees, \
   2018: IPO on NASDAQ, \
   2022: Expanded to 30 countries, \
   2025: 10,000 employees worldwide. \
   Milestone icons for each event, alternating left-right layout, \
   blue and gold corporate colors, growth trajectory feel, \
   professional business design" \
  --output figures/company_history.png
```

- --

## 3. 流程/操作信息图表

### 目的
解释分步程序、工作流程、说明或方法。

### 视觉元素
- **编号步骤**：清除顺序指示器
- **箭头/连接器**：显示流程和方向
- **操作图标**：说明每个步骤
- **简介描述**：简洁的动作文本
- **开始/结束指示器**：清晰的开始和结束

### 布局模式
- **垂直级联**：步骤从上到下流动
- **水平流动**：从左到右递进
- **循环过程**：步骤形成一个周期
- **分支流程**：具有替代方案的决策点

### 提示模板

* *线性过程：**
```
Process infographic: How to [ACCOMPLISH GOAL]
Step 1: [ACTION] - [brief explanation] (icon: [ICON])
Step 2: [ACTION] - [brief explanation] (icon: [ICON])
Step 3: [ACTION] - [brief explanation] (icon: [ICON])
Step 4: [ACTION] - [brief explanation] (icon: [ICON])
Step 5: [ACTION] - [brief explanation] (icon: [ICON])
Numbered circles connected by arrows, icons for each step,
[VERTICAL/HORIZONTAL] flow, [COLOR SCHEME],
clear step labels, clean instructional design, white background.
```

* *循环流程：**
```
Circular process infographic showing [CYCLE NAME]:
Step 1: [ACTION] leads to
Step 2: [ACTION] leads to
Step 3: [ACTION] leads to
Step 4: [ACTION] returns to Step 1
Circular arrangement with arrows forming a cycle,
icons at each point, step numbers, [COLOR SCHEME],
continuous flow design, white background.
```

* *决策流程图：**
```
Decision flowchart infographic for [SCENARIO]:
Start: [INITIAL QUESTION]
If Yes: [PATH A] → [OUTCOME A]
If No: [PATH B] → [OUTCOME B]
Diamond shapes for decisions, rectangles for actions,
arrows connecting all elements, [COLOR SCHEME],
clear yes/no labels, flowchart style, white background.
```

### 提示示例

* *配方流程：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Process infographic: How to Make Perfect Coffee \
   Step 1: Grind fresh beans (coffee grinder icon), \
   Step 2: Heat water to 200°F (thermometer icon), \
   Step 3: Add 2 tablespoons per 6 oz water (measuring spoon icon), \
   Step 4: Brew for 4 minutes (timer icon), \
   Step 5: Serve and enjoy (coffee cup icon). \
   Vertical flow with large numbered circles, \
   brown and cream coffee color scheme, \
   arrows between steps, cozy design feel" \
  --output figures/coffee_process.png
```

* *入职工作流程：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Process infographic: New Employee Onboarding \
   Day 1: Welcome orientation and paperwork (clipboard icon), \
   Week 1: Meet your team and set up workspace (people icon), \
   Week 2: Training and system access (laptop icon), \
   Week 3: Shadow senior colleagues (handshake icon), \
   Week 4: First independent project (checkmark icon). \
   Horizontal timeline flow with milestones, \
   teal and coral corporate colors, \
   professional HR design style" \
  --output figures/onboarding_process.png
```

- --

## 4.比较信息图

### 目的
比较两个或多个选项、产品、概念或

### 视觉元素
- **分割布局**：选项之间的明确划分
- **匹配行**：相同类别进行公平比较
- **检查/叉号**：快速视觉指示器
- **评级系统**：星星、条形或数字
- **标题**：清晰标识每个选项

### 布局模式
- **两列分割**：左与右
- **表格格式**：行和列
- **维恩图**：重叠比较
- **特征矩阵**：多选项比较grid

### 提示模板

* *两种选项比较：**
```
Comparison infographic: [OPTION A] vs [OPTION B]
Header: [OPTION A] on left | [OPTION B] on right
Row 1 - [CATEGORY 1]: [A VALUE] | [B VALUE]
Row 2 - [CATEGORY 2]: [A VALUE] | [B VALUE]
Row 3 - [CATEGORY 3]: [A VALUE] | [B VALUE]
Row 4 - [CATEGORY 4]: [A VALUE] | [B VALUE]
Row 5 - [CATEGORY 5]: [A VALUE] | [B VALUE]
Split layout with [COLOR A] for left, [COLOR B] for right,
icons for each option header, checkmarks for advantages,
clean symmetrical design, white background.
```

* *多选项矩阵：**
```
Comparison matrix infographic: [TOPIC]
Options: [OPTION 1], [OPTION 2], [OPTION 3]
Feature 1: [✓/✗ for each]
Feature 2: [✓/✗ for each]
Feature 3: [✓/✗ for each]
Feature 4: [✓/✗ for each]
Table layout with colored headers for each option,
checkmarks and X marks in cells, [COLOR SCHEME],
clean grid design, white background.
```

* *优点和缺点：**
```
Pros and Cons infographic for [TOPIC]:
Pros (left side, green):
- [PRO 1]
- [PRO 2]
- [PRO 3]
Cons (right side, red):
- [CON 1]
- [CON 2]
- [CON 3]
Split layout with green left side, red right side,
thumbs up icon for pros, thumbs down for cons,
balanced visual weight, white background.
```

### 示例提示

* *软件比较：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Comparison infographic: Slack vs Microsoft Teams \
   Pricing: Both offer free tiers with paid upgrades, \
   Integration: Slack 2000+ apps, Teams Microsoft ecosystem, \
   Video calls: Teams native, Slack via Huddles, \
   File storage: Teams 1TB, Slack 5GB free, \
   Best for: Slack small teams, Teams enterprise. \
   Purple left side (Slack), blue right side (Teams), \
   logos at top, feature comparison rows, \
   checkmarks for strengths, modern tech design" \
  --output figures/slack_vs_teams.png
```

* *饮食比较：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Comparison infographic: Keto Diet vs Mediterranean Diet \
   Weight loss: Both effective, Keto faster initial, \
   Heart health: Mediterranean better long-term, \
   Sustainability: Mediterranean easier to maintain, \
   Foods allowed: Keto high fat low carb, Med balanced, \
   Research support: Mediterranean more studied. \
   Green left (Keto), blue right (Mediterranean), \
   food icons for each, health/heart icons, \
   clean wellness design style" \
  --output figures/diet_comparison.png
```

- --

## 5. 列表/信息信息图表

### 目的
呈现提示、事实、要点或信息

### 视觉元素
- **数字或项目符号**：清晰的列表指示符
- **图标**：每个点的视觉表示
- **简短文本**：简洁描述
- **标题**：主题介绍
- **一致的样式**：统一处理所有项目

### 布局模式
- **垂直列表**：标准从上到下
- **两列列表**：用于较长的列表
- **图标网格**：下面带有标签的图标
- **卡片**：卡片/框中的每个点

### 提示模板

* *编号列表：**
```
List infographic: [NUMBER] [TOPIC]
1. [POINT 1] - [brief explanation] (icon: [ICON])
2. [POINT 2] - [brief explanation] (icon: [ICON])
3. [POINT 3] - [brief explanation] (icon: [ICON])
4. [POINT 4] - [brief explanation] (icon: [ICON])
5. [POINT 5] - [brief explanation] (icon: [ICON])
Large numbers in circles, icons next to each point,
brief text descriptions, [COLOR SCHEME],
vertical layout with spacing, white background.
```

* *提示格式：**
```
Tips infographic: [NUMBER] Tips for [TOPIC]
Tip 1: [TIP] (lightbulb icon)
Tip 2: [TIP] (star icon)
Tip 3: [TIP] (checkmark icon)
Tip 4: [TIP] (target icon)
Tip 5: [TIP] (rocket icon)
Colorful tip boxes or cards, icons for each tip,
[COLOR SCHEME], engaging friendly design,
header at top, white background.
```

* *事实格式：**
```
Facts infographic: [NUMBER] Facts About [TOPIC]
Fact 1: [INTERESTING FACT]
Fact 2: [INTERESTING FACT]
Fact 3: [INTERESTING FACT]
Fact 4: [INTERESTING FACT]
Fact 5: [INTERESTING FACT]
Speech bubble or card style for each fact,
relevant icons, [COLOR SCHEME],
educational engaging design, white background.
```

### 示例提示

* *生产力提示：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "List infographic: 7 Productivity Tips for Remote Workers \
   1. Create a dedicated workspace (desk icon), \
   2. Set regular working hours (clock icon), \
   3. Take scheduled breaks (coffee icon), \
   4. Use noise-canceling headphones (headphones icon), \
   5. Batch similar tasks together (stack icon), \
   6. Limit social media during work (phone icon), \
   7. End each day with tomorrow's plan (checklist icon). \
   Large colorful numbers, icons beside each tip, \
   teal and orange color scheme, friendly modern design" \
  --output figures/remote_work_tips.png
```

* *有趣事实：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Facts infographic: 5 Amazing Facts About Honey \
   Fact 1: Honey never spoils - 3000 year old honey is still edible, \
   Fact 2: Bees visit 2 million flowers to make 1 lb of honey, \
   Fact 3: Honey can be used to treat wounds and burns, \
   Fact 4: A bee produces only 1/12 teaspoon in its lifetime, \
   Fact 5: Honey contains natural antibiotics. \
   Hexagon honeycomb shapes for each fact, \
   golden yellow and black color scheme, bee illustrations, \
   fun educational design" \
  --output figures/honey_facts.png
```

- --

## 6. 基于地理/地图的信息图表

### 目的
显示基于位置的数据、区域统计数据或地理趋势。

### 视觉元素
- **地图可视化**：世界、国家或地区
- **颜色编码**：按地区划分的数据强度
- **数据标注**：地区的关键统计数据
- **图例**：色阶说明
- **标签**：地区或国家名称

### 布局模式
- **完整地图**：映射为主要元素
- **带侧边栏的地图**：旁边的数据摘要
- **区域焦点**：缩放地图部分
- **多地图**：显示不同数据的多张地图

### 提示模板

* *世界地图数据：**
```
Geographic infographic showing [TOPIC] globally:
Highest: [REGION/COUNTRY] - [VALUE]
Medium: [REGIONS] - [VALUE RANGE]
Lowest: [REGION/COUNTRY] - [VALUE]
World map with color-coded countries,
[DARK COLOR] for highest values, [LIGHT COLOR] for lowest,
legend showing color scale, key statistics callout,
clean cartographic design, light gray background.
```

* *国家/地区重点：**
```
Geographic infographic showing [TOPIC] in [COUNTRY/REGION]:
Region 1: [VALUE]
Region 2: [VALUE]
Region 3: [VALUE]
Map of [COUNTRY/REGION] with color-coded areas,
data labels for key regions, [COLOR] gradient,
legend with value scale, clean map design.
```

### 提示示例

* *全球数据：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Geographic infographic: Global Renewable Energy Adoption 2025 \
   Leaders: Iceland 100%, Norway 98%, Costa Rica 95%, \
   Growing: Germany 50%, UK 45%, China 30%, \
   Emerging: USA 22%, India 20%, Brazil 18%. \
   World map with green gradient coloring, \
   darker green for higher adoption, \
   legend showing percentage scale, \
   key country callouts with percentages, \
   clean modern cartographic style" \
  --output figures/renewable_map.png
```

* *美国区域：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Geographic infographic: Tech Jobs by US Region 2025 \
   West Coast: 35% of tech jobs (California, Washington), \
   Northeast: 25% (New York, Massachusetts), \
   South: 22% (Texas, Florida, Georgia), \
   Midwest: 18% (Illinois, Colorado, Michigan). \
   US map with color-coded regions, \
   percentage labels on each region, \
   blue and purple tech color scheme, \
   legend showing job concentration, \
   professional business design" \
  --output figures/tech_jobs_map.png
```

- --

## 7. 分层/金字塔信息图表

### 目的
显示重要性、组织级别结构，或排名信息。

### 视觉元素
- **金字塔形状**：带有级别的三角形
- **级别标签**：清晰的层级标识
- **尺寸级数**：底部较大，顶部较小
- **颜色级数**：每个级别的渐变或不同颜色
- **图标**：每个级别可选

### 布局模式
- **传统金字塔**：宽底、窄顶
- **倒金字塔**：窄底、宽顶
- **组织结构图**：树形结构
- **堆叠块**：方形层级

### 提示模板

* *经典金字塔：**
```
Hierarchical pyramid infographic: [TOPIC]
Top (Level 1 - most important/rare): [ITEM]
Level 2: [ITEM]
Level 3: [ITEM]
Level 4: [ITEM]
Base (Level 5 - foundation/most common): [ITEM]
Triangle pyramid with 5 horizontal sections,
[COLOR] gradient from [TOP COLOR] to [BASE COLOR],
labels on each tier, icons optional,
clean geometric design, white background.
```

* *组织层次结构：**
```
Organizational chart infographic for [ORGANIZATION]:
Top: [CEO/LEADER]
Level 2: [VPs/DIRECTORS] (3-4 boxes)
Level 3: [MANAGERS] (6-8 boxes)
Level 4: [TEAM LEADS] (multiple boxes)
Tree structure flowing down, connecting lines between levels,
[COLOR SCHEME], professional corporate design,
role titles in boxes, white background.
```

### 示例提示

* *学习金字塔：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Hierarchical pyramid infographic: Learning Retention Rates \
   Top: Teaching others - 90% retention, \
   Level 2: Practice by doing - 75% retention, \
   Level 3: Discussion groups - 50% retention, \
   Level 4: Demonstration - 30% retention, \
   Level 5: Audio/Visual - 20% retention, \
   Base: Lecture/Reading - 5-10% retention. \
   Colorful pyramid with 6 levels, \
   gradient from green (top) to red (base), \
   percentage labels, educational design" \
  --output figures/learning_pyramid.png
```

* *能量金字塔：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Hierarchical pyramid infographic: Ecological Energy Pyramid \
   Top: Apex predators (eagles, wolves) - smallest, \
   Level 2: Secondary consumers (snakes, foxes), \
   Level 3: Primary consumers (rabbits, deer), \
   Base: Producers (plants, algae) - largest. \
   Triangle pyramid with animal silhouettes, \
   green gradient from base to top, \
   energy flow arrows on side, \
   scientific educational design" \
  --output figures/energy_pyramid.png
```

- --

## 8. 解剖/视觉隐喻信息图

### 目的
解释复杂系统使用熟悉的视觉隐喻（身体、机器、树木等）。

### 视觉元素
- **中心隐喻图像**：主视觉（身体、树、机器）
- **标记零件**：识别的组件
- **标注线**：将标签连接到零件
- **描述**：解释对于每个部件
- **颜色编码**：不同颜色的不同部件

### 布局模式
- **带有标注的中心图像**：指向部件的标签
- **分解视图**：部件分离但排列
- **横截面**：隐喻的内部视图
- **之前/之后**：不同状态下的隐喻

### 提示模板

* *身体隐喻：**
```
Anatomical infographic using human body to explain [TOPIC]:
Brain represents [CONCEPT] - [explanation]
Heart represents [CONCEPT] - [explanation]
Hands represent [CONCEPT] - [explanation]
Feet represent [CONCEPT] - [explanation]
Human body silhouette with labeled callouts,
[COLOR SCHEME], clean medical illustration style,
connecting lines to descriptions, white background.
```

* *机器隐喻：**
```
Anatomical infographic using machine/engine to explain [TOPIC]:
Fuel tank represents [CONCEPT]
Engine represents [CONCEPT]
Wheels represent [CONCEPT]
Steering represents [CONCEPT]
Machine illustration with labeled components,
callout lines and descriptions, [COLOR SCHEME],
technical illustration style, white background.
```

### 示例提示

* *企业作为主体：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Anatomical infographic: A Business is Like a Human Body \
   Brain = Leadership and strategy (makes decisions), \
   Heart = Company culture (pumps energy), \
   Arms = Sales and marketing (reaches out), \
   Legs = Operations (keeps moving forward), \
   Skeleton = Systems and processes (provides structure). \
   Human body silhouette in blue, \
   labeled callout boxes for each part, \
   professional corporate design, white background" \
  --output figures/business_body.png
```

* *计算机作为房屋：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Anatomical infographic: Computer as a House \
   CPU = The brain/office (processes information), \
   RAM = The desk (temporary workspace), \
   Hard Drive = The filing cabinet (long-term storage), \
   GPU = The entertainment room (handles visuals), \
   Motherboard = The foundation (connects everything). \
   House illustration with cutaway view, \
   labeled rooms matching computer parts, \
   blue and gray tech colors, educational style" \
  --output figures/computer_house.png
```

- --

## 9. 简历/专业信息图表

### 目的
直观地呈现专业信息、技能、经验和成就。

### 视觉元素
- **照片/头像部分**：个人品牌
- **技能可视化**：条形图、图表、评级
- **时间线**：职业发展
- **联系图标**：电子邮件、电话、社交
- **成就徽章**：认证、奖项

### 布局模式
- **单栏**：垂直流动
- **两栏**：左信息，右技能
- **标题焦点**：带照片的大标题
- **模块化**：不同的部分/卡片

### 提示模板

* *专业简历：**
```
Resume infographic for [NAME], [PROFESSION]:
Photo area: Circular avatar placeholder
Skills: [SKILL 1] 90%, [SKILL 2] 85%, [SKILL 3] 75%
Experience: [YEAR-YEAR] [ROLE] at [COMPANY], [YEAR-YEAR] [ROLE] at [COMPANY]
Education: [DEGREE] from [INSTITUTION]
Contact: Email, LinkedIn, Portfolio icons
Professional photo area at top, horizontal skill bars,
timeline for experience, [COLOR SCHEME],
modern professional design, white background.
```

### 提示示例

* *设计师简历：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Resume infographic for a Graphic Designer: \
   Circular avatar placeholder at top, \
   Skills with colored bars: Adobe Suite 95%, UI/UX 90%, Branding 85%, Motion 75%. \
   Experience timeline: 2018-2020 Junior Designer at Agency X, \
   2020-2023 Senior Designer at Studio Y, 2023-Present Creative Director at Company Z. \
   Education: BFA Graphic Design. \
   Contact icons row at bottom. \
   Coral and teal color scheme, creative modern design" \
  --output figures/designer_resume.png
```

- --

## 10. 社交媒体/互动信息图表

### 目的
创建针对社交媒体平台优化的可共享、引人入胜的内容。

### 视觉元素
- **粗体标题**：吸引注意力的文本
- **最小文本**：快速阅读
- **鲜艳的色彩**：在feeds
- **中央视觉**：引人注目的图像或图标
- **号召性用语**：参与提示

### 布局模式
- **方形格式**：Instagram、Facebook
- **垂直格式**：Pinterest、Stories
- **轮播**：多幻灯片系列
- **报价卡**：有影响力的声明焦点

### 平台尺寸
- **Instagram Square**：1080x1080px
- **Instagram Portrait**：1080x1350px
- **Twitter/X**： 1200x675px
- **LinkedIn**：1200x627px
- **Pinterest**：1000x1500px

### 提示模板

* *社交报价卡片：**
```
Social media infographic: Inspirational quote
Quote: "[QUOTE TEXT]"
Attribution: - [AUTHOR]
Large quotation marks, centered quote text,
author name below, [COLOR SCHEME],
Instagram square format, bold typography,
solid gradient background.
```

* *快速统计社交：**
```
Social media infographic: [TOPIC] in Numbers
Headline: [ATTENTION-GRABBING HEADLINE]
Stat 1: [BIG NUMBER] [CONTEXT]
Stat 2: [BIG NUMBER] [CONTEXT]
Call to action: [CTA]
Bold numbers, minimal text, [COLOR SCHEME],
vibrant engaging design, social media optimized,
Instagram square format.
```

### 示例提示

* *励志报价：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Social media infographic quote card: \
   Quote: 'The best time to plant a tree was 20 years ago. \
   The second best time is now.' \
   Attribution: Chinese Proverb. \
   Large decorative quotation marks, centered text, \
   gradient background from deep green to teal, \
   tree silhouette illustration, Instagram square format, \
   modern inspirational design" \
  --output figures/tree_quote.png
```

* *参与统计：**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Social media infographic: Email Marketing Stats \
   Headline: Is Your Email Strategy Working? \
   Stat 1: 4400% ROI on email marketing, \
   Stat 2: 59% of consumers say email influences purchases, \
   Call to action: Double tap if you're an email marketer! \
   Bold colorful numbers, envelope icons, \
   purple and yellow vibrant colors, \
   Instagram square format, engaging design" \
  --output figures/email_stats_social.png
```

- --

## 行业风格变化

### 企业/商务风格
- 颜色：海军蓝、灰色、金色装饰
- 版式：干净的无衬线字体（Arial、Helvetica）
- 设计：简约、专业、结构化
- 元素：图表、图标、简洁线条

### 医疗保健/医疗风格
- 颜色：蓝色、青色、绿色、白色
- 版式：清晰、可读
- 设计：诱导信任、干净、临床
- 元素：医学图标、解剖学、研究图像

### 技术/数据风格
- 颜色：深色背景、霓虹灯口音，蓝色/紫色
- 排版：现代无衬线，数据等宽
- 设计：未来派，干净，黑暗模式友好
- 元素：电路图案，数据可视化，发光

### 教育/学术风格
- 颜色：中性色调，柔和的蓝色，温暖口音
- 版式：可读，略显传统
- 设计：有组织、层次清晰、易于使用
- 元素：书籍、灯泡、毕业图标

### 营销/创意风格
- 颜色：大胆、充满活力、时尚的组合
- 版式：显示和正文字体
- 设计：引人注目、动感、俏皮
- 元素：抽象形状、渐变、插图

- --

## 提示修饰符参考

将这些修饰符添加到任何提示中以调整样式：

### 设计风格
- “干净简约”设计风格"
- "现代专业设计"
- "平面设计大胆用色"
- "手绘插画风格"
- "3D等距风格"
- "复古复古风格"
- "企业商务风格"
- "俏皮友好设计"

### 颜色说明
- "[颜色]和[颜色]配色方案"
- "单色[颜色]调色板"
- "色盲安全调色板"
- "暖/冷色调"
- "高对比度设计"
- "柔和柔和的色彩"
- "大胆鲜艳的色彩"

### 布局说明
- "垂直布局"
- "水平布局"
- "居中构图"
- "不对称平衡"
- "基于网格的布局"
- "流动的有机布局"

### 背景选项
- "白色背景"
- "浅灰色背景"
- "深色背景"
- "从[颜色]到的渐变背景【颜色】》
- 《微妙图案背景》
- 《纯色[颜色]背景》

- --

使用这些模板和示例作为起点，然后根据您的特定需求进行定制。
