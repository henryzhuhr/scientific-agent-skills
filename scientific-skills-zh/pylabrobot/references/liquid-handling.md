# 使用 PyLabRobot

## 概述

液体处理模块（`pylabrobot.liquid_handling`）为控制液体处理机器人提供统一的接口。 `LiquidHandler` 类作为所有移液操作的主接口，通过后端抽象跨不同的硬件平台工作。

## 基本设置

### 初始化液体处理器

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck

# Create liquid handler with STAR backend
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# When done
await lh.stop()
```

### 在后端之间切换

通过交换后端来更改机器人，无需重写协议：

```python
# Hamilton STAR
from pylabrobot.liquid_handling.backends import STAR
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())

# Opentrons OT-2
from pylabrobot.liquid_handling.backends import OpentronsBackend
lh = LiquidHandler(backend=OpentronsBackend(host="192.168.1.100"), deck=OTDeck())

# Simulation (no hardware required)
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
lh = LiquidHandler(backend=ChatterboxBackend(), deck=STARLetDeck())
```

## 核心操作

### 吸头管理

拾取和放下吸头对于液体处理操作至关重要：

```python
# Pick up tips from specific positions
await lh.pick_up_tips(tip_rack["A1"])           # Single tip
await lh.pick_up_tips(tip_rack["A1:H1"])        # Row of 8 tips
await lh.pick_up_tips(tip_rack["A1:A12"])       # Column of 12 tips

# Drop tips
await lh.drop_tips()                             # Drop at current location
await lh.drop_tips(waste)                        # Drop at specific location

# Return tips to original rack
await lh.return_tips()
```

* *吸头跟踪**：启用自动吸头跟踪以监控吸头用法：

```python
from pylabrobot.resources import set_tip_tracking
set_tip_tracking(True)  # Enable globally
```

### 吸取液体

从孔或容器中吸取液体：

```python
# Basic aspiration
await lh.aspirate(plate["A1"], vols=100)         # 100 µL from A1

# Multiple wells with same volume
await lh.aspirate(plate["A1:H1"], vols=100)      # 100 µL from each well

# Multiple wells with different volumes
await lh.aspirate(
    plate["A1:A3"],
    vols=[100, 150, 200]                          # Different volumes
)

# Advanced parameters
await lh.aspirate(
    plate["A1"],
    vols=100,
    flow_rate=50,                                 # µL/s
    liquid_height=5,                              # mm from bottom
    blow_out_air_volume=10                        # µL air
)
```

### 分配液体

将液体分配到孔或容器中容器：

```python
# Basic dispensing
await lh.dispense(plate["A2"], vols=100)         # 100 µL to A2

# Multiple wells
await lh.dispense(plate["A1:H1"], vols=100)      # 100 µL to each

# Different volumes
await lh.dispense(
    plate["A1:A3"],
    vols=[100, 150, 200]
)

# Advanced parameters
await lh.dispense(
    plate["A2"],
    vols=100,
    flow_rate=50,                                 # µL/s
    liquid_height=2,                              # mm from bottom
    blow_out_air_volume=10                        # µL air
)
```

### 转移液体

转移在一次操作中结合了吸液和分配：

```python
# Basic transfer
await lh.transfer(
    source=source_plate["A1"],
    dest=dest_plate["A1"],
    vols=100
)

# Multiple transfers (same tips)
await lh.transfer(
    source=source_plate["A1:H1"],
    dest=dest_plate["A1:H1"],
    vols=100
)

# Different volumes per well
await lh.transfer(
    source=source_plate["A1:A3"],
    dest=dest_plate["B1:B3"],
    vols=[50, 100, 150]
)

# With tip handling
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(
    source=source_plate["A1:H12"],
    dest=dest_plate["A1:H12"],
    vols=100
)
await lh.drop_tips()
```

## 高级技术

### 系列稀释

创建系列跨板行或列的稀释：

```python
# 2-fold serial dilution
source_vols = [100, 50, 50, 50, 50, 50, 50, 50]
dest_vols = [0, 50, 50, 50, 50, 50, 50, 50]

# Add diluent first
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(
    source=buffer["A1"],
    dest=plate["A2:A8"],
    vols=50
)
await lh.drop_tips()

# Perform serial dilution
await lh.pick_up_tips(tip_rack["A2"])
for i in range(7):
    await lh.aspirate(plate[f"A{i+1}"], vols=50)
    await lh.dispense(plate[f"A{i+2}"], vols=50)
    # Mix
    await lh.aspirate(plate[f"A{i+2}"], vols=50)
    await lh.dispense(plate[f"A{i+2}"], vols=50)
await lh.drop_tips()
```

### 板复制

将整个板布局复制到另一个板：

```python
# Setup tips
await lh.pick_up_tips(tip_rack["A1:H1"])

# Replicate 96-well plate (12 columns)
for col in range(1, 13):
    await lh.transfer(
        source=source_plate[f"A{col}:H{col}"],
        dest=dest_plate[f"A{col}:H{col}"],
        vols=100
    )

await lh.drop_tips()
```

### 多通道移液

同时使用多个通道进行平行操作：

```python
# 8-channel transfer (entire row)
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(
    source=source_plate["A1:H1"],
    dest=dest_plate["A1:H1"],
    vols=100
)
await lh.drop_tips()

# Process entire plate with 8-channel
for col in range(1, 13):
    await lh.pick_up_tips(tip_rack[f"A{col}:H{col}"])
    await lh.transfer(
        source=source_plate[f"A{col}:H{col}"],
        dest=dest_plate[f"A{col}:H{col}"],
        vols=100
    )
    await lh.drop_tips()
```

### 混合液体

通过反复吸液和分配来混合液体：

```python
# Mix by aspiration/dispensing
await lh.pick_up_tips(tip_rack["A1"])

# Mix 5 times
for _ in range(5):
    await lh.aspirate(plate["A1"], vols=80)
    await lh.dispense(plate["A1"], vols=80)

await lh.drop_tips()
```

## 体积跟踪

跟踪孔中的液体体积自动：

```python
from pylabrobot.resources import set_volume_tracking

# Enable volume tracking globally
set_volume_tracking(True)

# Set initial volumes
plate["A1"].tracker.set_liquids([(None, 200)])  # 200 µL

# After aspirating 100 µL
await lh.aspirate(plate["A1"], vols=100)
print(plate["A1"].tracker.get_volume())  # 100 µL

# Check remaining volume
remaining = plate["A1"].tracker.get_volume()
```

## 液体类别

定义液体属性以实现最佳移液：

```python
# Liquid classes control aspiration/dispense parameters
from pylabrobot.liquid_handling import LiquidClass

# Create custom liquid class
water = LiquidClass(
    name="Water",
    aspiration_flow_rate=100,
    dispense_flow_rate=150,
    aspiration_mix_flow_rate=100,
    dispense_mix_flow_rate=100,
    air_transport_retract_dist=10
)

# Use with operations
await lh.aspirate(
    plate["A1"],
    vols=100,
    liquid_class=water
)
```

## 错误处理

处理液体处理中的错误操作：

```python
try:
    await lh.setup()
    await lh.pick_up_tips(tip_rack["A1"])
    await lh.transfer(source["A1"], dest["A1"], vols=100)
    await lh.drop_tips()
except Exception as e:
    print(f"Error during liquid handling: {e}")
    # Attempt to drop tips if holding them
    try:
        await lh.drop_tips()
    except:
        pass
finally:
    await lh.stop()
```

## 最佳实践

1. **始终设置和停止**：操作前调用`await lh.setup()`，完成后调用`await lh.stop()`
2. **启用跟踪**：使用尖端跟踪和音量跟踪进行准确的状态管理
3. **吸头管理**：在吸液前始终拿起吸头并在完成后将其放下
4. **流量**：根据液体粘度和容器类型
5调整流量。 **液体高度**：设置适当的吸取/分配高度以避免飞溅
6. **错误处理**：使用 try/finally 块来确保正确清理
7. **模拟测试**：在硬件
8 上运行之前，使用 ChatterboxBackend 测试协议。 **体积限制**：遵守吸头体积限制和孔容量
9. **混合**：分配粘性液体后或当精度至关重要时进行混合
10. **文档**：记录液体类别和自定义参数以实现可重复性

## 常见模式

### 完整液体处理协议

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck, TIP_CAR_480_A00, Cos_96_DW_1mL
from pylabrobot.resources import set_tip_tracking, set_volume_tracking

# Enable tracking
set_tip_tracking(True)
set_volume_tracking(True)

# Initialize
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

try:
    # Define resources
    tip_rack = TIP_CAR_480_A00(name="tips")
    source = Cos_96_DW_1mL(name="source")
    dest = Cos_96_DW_1mL(name="dest")

    # Assign to deck
    lh.deck.assign_child_resource(tip_rack, rails=1)
    lh.deck.assign_child_resource(source, rails=10)
    lh.deck.assign_child_resource(dest, rails=15)

    # Set initial volumes
    for well in source.children:
        well.tracker.set_liquids([(None, 200)])

    # Execute protocol
    await lh.pick_up_tips(tip_rack["A1:H1"])
    await lh.transfer(
        source=source["A1:H12"],
        dest=dest["A1:H12"],
        vols=100
    )
    await lh.drop_tips()

finally:
    await lh.stop()
```

## 硬件特定说明

### Hamilton STAR

- 支持完整液体处理功能
- 使用 USB 连接进行通信
- 直接执行固件命令
- 支持 CO-RE（压缩 O 形圈扩展）提示

### Opentrons OT-2

- 需要 IP 地址进行网络连接
- 使用 HTTP API通信
- 仅限于 8 通道和单通道移液器
- 与 STAR

 相比，平台布局更简单### Tecan EVO

- 正在进行的工作支持
- 与 Hamilton STAR
 类似的功能

## 其他资源

- 官方液体处理指南：https://docs.pylabrobot.org/user_guide/basic.html
- API 参考：https://docs.pylabrobot.org/api/pylabrobot.liquid_handling.html
- 示例协议： https://github.com/PyLabRobot/pylabrobot/tree/main/examples
