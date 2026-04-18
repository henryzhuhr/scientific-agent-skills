# PyLabRobot

## 中的资源管理 ## 概述

PyLabRobot 中的资源代表实验方案中使用的实验室设备、实验室器具或组件。资源系统提供了一个分层结构，用于管理板、吸头架、槽、管、载体和其他实验室器具，具有精确的空间定位和状态跟踪。

## 资源基础

### 什么是资源？

A资源代表：
- 一件实验室器具（板、吸头架、槽、管）
- 设备（液体处理机、读板器）
- 实验室器具的一部分（孔、尖端）
- 实验室器具的容器（甲板、载体）

所有资源继承自基础 `Resource` 类，并形成具有父子关系的树结构（树状）。

### 资源属性

每个资源需要：
- **名称**：资源的唯一标识符
- **size_x，size_y，size_z**：以毫米为单位的尺寸（长方体表示）
- **位置**：相对于父级原点的坐标（可选，分配时设置）

```python
from pylabrobot.resources import Resource

# Create a basic resource
resource = Resource(
    name="my_resource",
    size_x=127.76,  # mm
    size_y=85.48,   # mm
    size_z=14.5     # mm
)
```

## 资源类型

### 板

带用于容纳液体的孔的微孔板：

```python
from pylabrobot.resources import (
    Cos_96_DW_1mL,      # 96-well plate, 1mL deep well
    Cos_96_DW_500ul,    # 96-well plate, 500µL
    Plate_384_Sq,       # 384-well square plate
    Cos_96_PCR          # 96-well PCR plate
)

# Create plate
plate = Cos_96_DW_1mL(name="sample_plate")

# Access wells
well_a1 = plate["A1"]                  # Single well
row_a = plate["A1:H1"]                 # Entire row (A1-H1)
col_1 = plate["A1:A12"]                # Entire column (A1-A12)
range_wells = plate["A1:C3"]           # Range of wells
all_wells = plate.children             # All wells as list
```

### 吸头架

装有移液器吸头的容器：

```python
from pylabrobot.resources import (
    TIP_CAR_480_A00,    # 96 standard tips
    HTF_L,              # Hamilton tips, filtered
    TipRack             # Generic tip rack
)

# Create tip rack
tip_rack = TIP_CAR_480_A00(name="tips")

# Access tips
tip_a1 = tip_rack["A1"]                # Single tip position
tips_row = tip_rack["A1:H1"]           # Row of tips
tips_col = tip_rack["A1:A12"]          # Column of tips

# Check tip presence (requires tip tracking enabled)
from pylabrobot.resources import set_tip_tracking
set_tip_tracking(True)

has_tip = tip_rack["A1"].tracker.has_tip
```

### 槽

试剂储存容器：

```python
from pylabrobot.resources import Trough_100ml

# Create trough
trough = Trough_100ml(name="buffer")

# Access channels
channel_1 = trough["channel_1"]
all_channels = trough.children
```

### 试管

单个试管或试管架：

```python
from pylabrobot.resources import Tube, TubeRack

# Create tube rack
tube_rack = TubeRack(name="samples")

# Access tubes
tube_a1 = tube_rack["A1"]
```

### 载体

平台固定板、吸头或其他实验室器具：

```python
from pylabrobot.resources import (
    PlateCarrier,
    TipCarrier,
    MFXCarrier
)

# Carriers provide positions for labware
carrier = PlateCarrier(name="plate_carrier")

# Assign plate to carrier
plate = Cos_96_DW_1mL(name="plate")
carrier.assign_child_resource(plate, location=(0, 0, 0))
```

## 平台管理

### 使用平台

平台代表机器人的工作表面：

```python
from pylabrobot.resources import STARLetDeck, OTDeck

# Hamilton STARlet deck
deck = STARLetDeck()

# Opentrons OT-2 deck
deck = OTDeck()
```

### 将资源分配给甲板

使用导轨或坐标将资源分配到特定甲板位置：

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.resources import STARLetDeck, TIP_CAR_480_A00, Cos_96_DW_1mL

lh = LiquidHandler(backend=backend, deck=STARLetDeck())

# Assign using rail positions (Hamilton STAR)
tip_rack = TIP_CAR_480_A00(name="tips")
source_plate = Cos_96_DW_1mL(name="source")
dest_plate = Cos_96_DW_1mL(name="dest")

lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(source_plate, rails=10)
lh.deck.assign_child_resource(dest_plate, rails=15)

# Assign using coordinates (x, y, z in mm)
lh.deck.assign_child_resource(
    resource=tip_rack,
    location=(100, 200, 0)
)
```

### 取消分配资源

从甲板上删除资源：

```python
# Unassign specific resource
lh.deck.unassign_child_resource(tip_rack)

# Access assigned resources
all_resources = lh.deck.children
resource_names = [r.name for r in lh.deck.children]
```

## 坐标系统

PyLabRobot使用右手笛卡尔坐标系：

- **X 轴**：从左到右（向右增加）
- **Y 轴**：从前到后（向后增加）
- **Z 轴**：从下到上（向上增加）
- **原点**：父级的左下前角

### 位置计算

```python
# Get absolute location (relative to deck/root)
absolute_loc = plate.get_absolute_location()

# Get location relative to another resource
relative_loc = well.get_location_wrt(deck)

# Get location relative to parent
parent_relative = plate.location
```

## 状态管理

### 跟踪液体体积

跟踪孔和容器中的液体体积：

```python
from pylabrobot.resources import set_volume_tracking

# Enable volume tracking globally
set_volume_tracking(True)

# Set liquid in well
plate["A1"].tracker.set_liquids([
    (None, 200)  # (liquid_type, volume_in_uL)
])

# Multiple liquids
plate["A2"].tracker.set_liquids([
    ("water", 100),
    ("ethanol", 50)
])

# Get current volume
volume = plate["A1"].tracker.get_volume()  # Returns total volume

# Get liquids
liquids = plate["A1"].tracker.get_liquids()  # Returns list of (type, vol) tuples
```

### 跟踪吸头存在情况

跟踪吸头中存在哪些吸头机架：

```python
from pylabrobot.resources import set_tip_tracking

# Enable tip tracking globally
set_tip_tracking(True)

# Check if tip is present
has_tip = tip_rack["A1"].tracker.has_tip

# Tips are automatically tracked when using pick_up_tips/drop_tips
await lh.pick_up_tips(tip_rack["A1"])  # Marks tip as absent
await lh.return_tips()                  # Marks tip as present
```

## 序列化

### 保存和加载资源

将资源定义和状态保存到JSON：

```python
# Save resource definition
plate.save("plate_definition.json")

# Load resource from JSON
from pylabrobot.resources import Plate
plate = Plate.load_from_json_file("plate_definition.json")

# Save deck layout
lh.deck.save("deck_layout.json")

# Load deck layout
from pylabrobot.resources import Deck
deck = Deck.load_from_json_file("deck_layout.json")
```

### 状态序列化

分别保存和恢复资源状态定义：

```python
# Save state (tip presence, liquid volumes)
state = plate.serialize_state()
with open("plate_state.json", "w") as f:
    json.dump(state, f)

# Load state
with open("plate_state.json", "r") as f:
    state = json.load(f)
plate.load_state(state)

# Save all states in hierarchy
all_states = lh.deck.serialize_all_state()

# Load all states
lh.deck.load_all_state(all_states)
```

## 自定义资源

### 定义自定义实验室器具

当内置资源与您的设备不匹配时创建自定义实验室器具：

```python
from pylabrobot.resources import Plate, Well

# Define custom plate
class CustomPlate(Plate):
    def __init__(self, name: str):
        super().__init__(
            name=name,
            size_x=127.76,
            size_y=85.48,
            size_z=14.5,
            num_items_x=12,  # 12 columns
            num_items_y=8,   # 8 rows
            dx=9.0,          # Well spacing X
            dy=9.0,          # Well spacing Y
            dz=0.0,          # Well spacing Z (usually 0)
            item_dx=9.0,     # Distance between well centers X
            item_dy=9.0      # Distance between well centers Y
        )

# Use custom plate
custom_plate = CustomPlate(name="my_custom_plate")
```

### 自定义井

定义自定义井几何形状：

```python
from pylabrobot.resources import Well

# Create custom well
well = Well(
    name="custom_well",
    size_x=8.0,
    size_y=8.0,
    size_z=10.5,
    max_volume=200,      # µL
    bottom_shape="flat"  # or "v", "u"
)
```

## 资源发现

### 查找资源

导航资源层次结构：

```python
# Get all wells in a plate
wells = plate.children

# Find resource by name
resource = lh.deck.get_resource("plate_name")

# Iterate through resources
for resource in lh.deck.children:
    print(f"{resource.name}: {resource.get_absolute_location()}")

# Get wells by pattern
wells_a = [w for w in plate.children if w.name.startswith("A")]
```

### 资源元数据

访问资源信息：

```python
# Resource properties
print(f"Name: {plate.name}")
print(f"Size: {plate.size_x} x {plate.size_y} x {plate.size_z} mm")
print(f"Location: {plate.get_absolute_location()}")
print(f"Parent: {plate.parent.name if plate.parent else None}")
print(f"Children: {len(plate.children)}")

# Type checking
from pylabrobot.resources import Plate, TipRack
if isinstance(resource, Plate):
    print("This is a plate")
elif isinstance(resource, TipRack):
    print("This is a tip rack")
```

## 最佳实践

1. **唯一名称**：对所有资源使用描述性的唯一名称
2. **启用跟踪**：打开尖端和体积跟踪以进行准确的状态管理
3. **坐标验证**：验证资源位置在甲板
4上不重叠。 **状态序列化**：保存可重现协议
5的甲板布局和状态。 **资源清理**：不再需要时取消分配资源
6. **自定义资源**：当内置选项与
7 不匹配时，定义自定义实验室器具。 **文档**：记录自定义资源维度和属性
8. **类型检查**：在操作之前使用 isinstance()验证资源类型
9. **层次结构导航**：使用父/子关系来导航资源树
10. **JSON 存储**：以 JSON 格式存储牌组布局以进行版本控制和共享

## 常见模式

### 完整牌组设置

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import (
    STARLetDeck,
    TIP_CAR_480_A00,
    Cos_96_DW_1mL,
    Trough_100ml,
    set_tip_tracking,
    set_volume_tracking
)

# Enable tracking
set_tip_tracking(True)
set_volume_tracking(True)

# Initialize liquid handler
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# Define resources
tip_rack_1 = TIP_CAR_480_A00(name="tips_1")
tip_rack_2 = TIP_CAR_480_A00(name="tips_2")
source_plate = Cos_96_DW_1mL(name="source")
dest_plate = Cos_96_DW_1mL(name="dest")
buffer = Trough_100ml(name="buffer")

# Assign to deck
lh.deck.assign_child_resource(tip_rack_1, rails=1)
lh.deck.assign_child_resource(tip_rack_2, rails=2)
lh.deck.assign_child_resource(buffer, rails=5)
lh.deck.assign_child_resource(source_plate, rails=10)
lh.deck.assign_child_resource(dest_plate, rails=15)

# Set initial volumes
for well in source_plate.children:
    well.tracker.set_liquids([(None, 200)])

buffer["channel_1"].tracker.set_liquids([(None, 50000)])  # 50 mL

# Save deck layout
lh.deck.save("my_protocol_deck.json")

# Save initial state
import json
with open("initial_state.json", "w") as f:
    json.dump(lh.deck.serialize_all_state(), f)
```

### 加载保存的牌组

```python
from pylabrobot.resources import Deck

# Load deck from file
deck = Deck.load_from_json_file("my_protocol_deck.json")

# Load state
import json
with open("initial_state.json", "r") as f:
    state = json.load(f)
deck.load_all_state(state)

# Use with liquid handler
lh = LiquidHandler(backend=STAR(), deck=deck)
await lh.setup()

# Access resources by name
source_plate = deck.get_resource("source")
dest_plate = deck.get_resource("dest")
```

## 其他资源

- 资源文档：https://docs.pylabrobot.org/resources/introduction.html
- 自定义资源指南：https://docs.pylabrobot.org/resources/custom-resources.html
- API 参考： https://docs.pylabrobot.org/api/pylabrobot.resources.html
- 甲板布局：https://github.com/PyLabRobot/pylabrobot/tree/main/pylabrobot/resources/deck
