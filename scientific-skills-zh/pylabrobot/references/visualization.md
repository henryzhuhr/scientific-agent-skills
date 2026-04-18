# PyLabRobot

## 中的可视化和模拟概述

PyLabRobot 提供可视化和模拟工具，用于在没有物理硬件的情况下开发、测试和验证实验室协议。可视化工具提供甲板状态的实时 3D 可视化，而模拟后端支持协议测试和验证。

## 可视化工具

### 什么是可视化工具？

PyLabRobot 可视化工具是一个基于浏览器的工具，它：
- 显示甲板布局的 3D 可视化
- 显示实时尖端存在和液体体积
- 适用于模拟和物理机器人
- 提供交互式甲板状态检查
- 启用视觉协议验证

### 启动可视化工具

可视化工具作为Web服务器运行并显示在浏览器中：

```python
from pylabrobot.visualizer import Visualizer

# Create visualizer
vis = Visualizer()

# Start web server (opens browser automatically)
await vis.start()

# Stop visualizer
await vis.stop()
```

* *默认设置：**
- 端口：1234 (http://localhost:1234)
- 启动时自动打开浏览器

### 将液体处理器连接到可视化工具

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
from pylabrobot.resources import STARLetDeck
from pylabrobot.visualizer import Visualizer

# Create visualizer
vis = Visualizer()
await vis.start()

# Create liquid handler with simulation backend
lh = LiquidHandler(
    backend=ChatterboxBackend(num_channels=8),
    deck=STARLetDeck()
)

# Connect liquid handler to visualizer
lh.visualizer = vis

await lh.setup()

# Now all operations are visualized in real-time
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.aspirate(plate["A1:H1"], vols=100)
await lh.dispense(plate["A2:H2"], vols=100)
await lh.drop_tips()
```

### 跟踪功能

#### 启用跟踪

对于显示提示和液体的可视化工具，启用跟踪：

```python
from pylabrobot.resources import set_tip_tracking, set_volume_tracking

# Enable globally (before creating resources)
set_tip_tracking(True)
set_volume_tracking(True)
```

#### 设置初始液体

定义可视化的初始液体内容：

```python
# Set liquid in a single well
plate["A1"].tracker.set_liquids([
    (None, 200)  # (liquid_type, volume_in_µL)
])

# Set multiple liquids in one well
plate["A2"].tracker.set_liquids([
    ("water", 100),
    ("ethanol", 50)
])

# Set liquids in multiple wells
for well in plate["A1:H1"]:
    well.tracker.set_liquids([(None, 200)])

# Set liquids in entire plate
for well in plate.children:
    well.tracker.set_liquids([("sample", 150)])
```

#### 可视化提示Presence

```python
# Tips are automatically tracked when using pick_up/drop operations
await lh.pick_up_tips(tip_rack["A1:H1"])  # Tips shown as absent in visualizer
await lh.return_tips()                     # Tips shown as present in visualizer
```

### 完整的可视化器示例

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
from pylabrobot.resources import (
    STARLetDeck,
    TIP_CAR_480_A00,
    Cos_96_DW_1mL,
    set_tip_tracking,
    set_volume_tracking
)
from pylabrobot.visualizer import Visualizer

# Enable tracking
set_tip_tracking(True)
set_volume_tracking(True)

# Create visualizer
vis = Visualizer()
await vis.start()

# Create liquid handler
lh = LiquidHandler(
    backend=ChatterboxBackend(num_channels=8),
    deck=STARLetDeck()
)
lh.visualizer = vis
await lh.setup()

# Define resources
tip_rack = TIP_CAR_480_A00(name="tips")
source_plate = Cos_96_DW_1mL(name="source")
dest_plate = Cos_96_DW_1mL(name="dest")

# Assign to deck
lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(source_plate, rails=10)
lh.deck.assign_child_resource(dest_plate, rails=15)

# Set initial volumes
for well in source_plate.children:
    well.tracker.set_liquids([("sample", 200)])

# Execute protocol with visualization
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(
    source_plate["A1:H12"],
    dest_plate["A1:H12"],
    vols=100
)
await lh.drop_tips()

# Keep visualizer open to inspect final state
input("Press Enter to close visualizer...")

# Cleanup
await lh.stop()
await vis.stop()
```

## 甲板布局编辑器

### 使用甲板编辑器

PyLabRobot 包括图形甲板布局编辑器：

* *功能：**
- 可视化平台设计界面
- 拖放资源放置
- 编辑初始液体状态
- 设置提示存在
- 将布局保存/加载为JSON

* *用法：**
- 通过可视化界面访问
- 以图形方式创建布局而不是代码
- 导出到 JSON 以在协议中使用

### 加载 Deck 布局

```python
from pylabrobot.resources import Deck

# Load deck from JSON file
deck = Deck.load_from_json_file("my_deck_layout.json")

# Use with liquid handler
lh = LiquidHandler(backend=backend, deck=deck)
await lh.setup()

# Resources are already assigned
source = deck.get_resource("source")
dest = deck.get_resource("dest")
tip_rack = deck.get_resource("tips")
```

## 模拟

### ChatterboxBackend

The ChatterboxBackend 模拟液体处理操作：

* *功能：**
- 无需硬件
- 验证协议逻辑
- 跟踪吸头和体积
- 支持所有液体处理操作
- 与可视化工具配合使用

* * 设置：**

```python
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend

# Create simulation backend
backend = ChatterboxBackend(
    num_channels=8  # Simulate 8-channel pipette
)

# Use with liquid handler
lh = LiquidHandler(backend=backend, deck=STARLetDeck())
```

### 模拟使用案例

#### 协议开发

```python
async def develop_protocol():
    """Develop protocol using simulation"""

    # Use simulation for development
    lh = LiquidHandler(
        backend=ChatterboxBackend(),
        deck=STARLetDeck()
    )

    # Connect visualizer
    vis = Visualizer()
    await vis.start()
    lh.visualizer = vis

    await lh.setup()

    try:
        # Develop and test protocol
        await lh.pick_up_tips(tip_rack["A1"])
        await lh.transfer(plate["A1"], plate["A2"], vols=100)
        await lh.drop_tips()

        print("Protocol development complete!")

    finally:
        await lh.stop()
        await vis.stop()
```

#### 协议验证

```python
async def validate_protocol():
    """Validate protocol logic without hardware"""

    set_tip_tracking(True)
    set_volume_tracking(True)

    lh = LiquidHandler(
        backend=ChatterboxBackend(),
        deck=STARLetDeck()
    )
    await lh.setup()

    try:
        # Setup resources
        tip_rack = TIP_CAR_480_A00(name="tips")
        plate = Cos_96_DW_1mL(name="plate")

        lh.deck.assign_child_resource(tip_rack, rails=1)
        lh.deck.assign_child_resource(plate, rails=10)

        # Set initial state
        for well in plate.children:
            well.tracker.set_liquids([(None, 200)])

        # Execute protocol
        await lh.pick_up_tips(tip_rack["A1:H1"])

        # Test different volumes
        test_volumes = [50, 100, 150]
        for i, vol in enumerate(test_volumes):
            await lh.transfer(
                plate[f"A{i+1}:H{i+1}"],
                plate[f"A{i+4}:H{i+4}"],
                vols=vol
            )

        await lh.drop_tips()

        # Validate volumes
        for i, vol in enumerate(test_volumes):
            for row in "ABCDEFGH":
                well = plate[f"{row}{i+4}"]
                actual_vol = well.tracker.get_volume()
                assert actual_vol == vol, f"Volume mismatch in {well.name}"

        print("✓ Protocol validation passed!")

    finally:
        await lh.stop()
```

#### 测试边缘案例

```python
async def test_edge_cases():
    """Test protocol edge cases in simulation"""

    lh = LiquidHandler(
        backend=ChatterboxBackend(),
        deck=STARLetDeck()
    )
    await lh.setup()

    try:
        # Test 1: Empty well aspiration
        try:
            await lh.aspirate(empty_plate["A1"], vols=100)
            print("✗ Should have raised error for empty well")
        except Exception as e:
            print(f"✓ Correctly raised error: {e}")

        # Test 2: Overfilling well
        try:
            await lh.dispense(small_well, vols=1000)  # Too much
            print("✗ Should have raised error for overfilling")
        except Exception as e:
            print(f"✓ Correctly raised error: {e}")

        # Test 3: Tip capacity
        try:
            await lh.aspirate(large_volume_well, vols=2000)  # Exceeds tip capacity
            print("✗ Should have raised error for tip capacity")
        except Exception as e:
            print(f"✓ Correctly raised error: {e}")

    finally:
        await lh.stop()
```

### CI/CD集成

使用模拟进行自动化测试：

```python
# test_protocols.py
import pytest
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend

@pytest.mark.asyncio
async def test_transfer_protocol():
    """Test liquid transfer protocol"""

    lh = LiquidHandler(
        backend=ChatterboxBackend(),
        deck=STARLetDeck()
    )
    await lh.setup()

    try:
        # Setup
        tip_rack = TIP_CAR_480_A00(name="tips")
        plate = Cos_96_DW_1mL(name="plate")

        lh.deck.assign_child_resource(tip_rack, rails=1)
        lh.deck.assign_child_resource(plate, rails=10)

        # Set initial volumes
        plate["A1"].tracker.set_liquids([(None, 200)])

        # Execute
        await lh.pick_up_tips(tip_rack["A1"])
        await lh.transfer(plate["A1"], plate["A2"], vols=100)
        await lh.drop_tips()

        # Assert
        assert plate["A1"].tracker.get_volume() == 100
        assert plate["A2"].tracker.get_volume() == 100

    finally:
        await lh.stop()
```

## 最佳实践

1. **始终首先使用仿真**：在硬件
2 上运行之前，在仿真中开发和测试协议。 **启用跟踪**：打开尖端和体积跟踪以实现准确的可视化
3. **设置初始状态**：定义实际模拟的初始液体体积
4. **目视检查**：使用可视化工具验证甲板布局和协议执行
5. **验证逻辑**：在模拟
6中测试边缘情况和错误条件。 **自动化测试**：将模拟集成到 CI/CD 管道
7 中。 **保存布局**：使用 JSON 保存和共享牌组布局
8. **文档状态**：记录再现性的初始状态
9. **交互式开发**：在开发过程中保持可视化工具打开
10. **协议细化**：在硬件运行之前进行仿真迭代

## 常见模式

### 开发到生产工作流程

```python
import os

# Configuration
USE_HARDWARE = os.getenv("USE_HARDWARE", "false").lower() == "true"

# Create appropriate backend
if USE_HARDWARE:
    from pylabrobot.liquid_handling.backends import STAR
    backend = STAR()
    print("Running on Hamilton STAR hardware")
else:
    from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
    backend = ChatterboxBackend()
    print("Running in simulation mode")

# Rest of protocol is identical
lh = LiquidHandler(backend=backend, deck=STARLetDeck())

if not USE_HARDWARE:
    # Enable visualizer for simulation
    vis = Visualizer()
    await vis.start()
    lh.visualizer = vis

await lh.setup()

# Protocol execution
# ... (same code for hardware and simulation)

# Run with: USE_HARDWARE=false python protocol.py  # Simulation
# Run with: USE_HARDWARE=true python protocol.py   # Hardware
```

### 可视化协议验证

```python
async def visual_verification():
    """Run protocol with visual verification pauses"""

    vis = Visualizer()
    await vis.start()

    lh = LiquidHandler(
        backend=ChatterboxBackend(),
        deck=STARLetDeck()
    )
    lh.visualizer = vis
    await lh.setup()

    try:
        # Step 1
        await lh.pick_up_tips(tip_rack["A1:H1"])
        input("Press Enter to continue...")

        # Step 2
        await lh.aspirate(source["A1:H1"], vols=100)
        input("Press Enter to continue...")

        # Step 3
        await lh.dispense(dest["A1:H1"], vols=100)
        input("Press Enter to continue...")

        # Step 4
        await lh.drop_tips()
        input("Press Enter to finish...")

    finally:
        await lh.stop()
        await vis.stop()
```

## 故障排除

### 可视化工具未更新

- 确保在操作之前设置 `lh.visualizer = vis`
- 检查是否已全局启用跟踪
- 验证可视化工具是否正在运行 (`vis.start()`)
- 如果连接丢失，请刷新浏览器

### 跟踪不工作

```python
# Must enable tracking BEFORE creating resources
set_tip_tracking(True)
set_volume_tracking(True)

# Then create resources
tip_rack = TIP_CAR_480_A00(name="tips")
plate = Cos_96_DW_1mL(name="plate")
```

### 模拟错误

- 模拟验证操作（例如，不能从空孔中吸液）
- 使用 try/ except 处理验证错误
- 检查初始状态是否设置正确
- 验证体积不超过容量

## 其他资源

- 可视化工具文档： https://docs.pylabrobot.org/user_guide/using-the-visualizer.html（如果有）
- 模拟指南：https://docs.pylabrobot.org/user_guide/simulation.html（如果有）
- API 参考： https://docs.pylabrobot.org/api/pylabrobot.visualizer.html
- GitHub 示例：https://github.com/PyLabRobot/pylabrobot/tree/main/examples
