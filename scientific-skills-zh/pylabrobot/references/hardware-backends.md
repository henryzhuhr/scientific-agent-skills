# PyLabRobot

中的硬件后端## 概述

PyLabRobot 使用后端抽象系统，允许相同的协议代码在不同的液体处理机器人和平台上运行。后端处理特定于设备的通信，而 `LiquidHandler` 前端提供统一的接口。

## 后端架构

### 后端如何工作

1. **前端**：`LiquidHandler` 类提供高级 API
2. **后端**：设备特定类处理硬件通信
3. **协议**：相同的代码可以在不同的后端工作

```python
# Same protocol code
await lh.pick_up_tips(tip_rack["A1"])
await lh.aspirate(plate["A1"], vols=100)
await lh.dispense(plate["A2"], vols=100)
await lh.drop_tips()

# Works with any backend (STAR, Opentrons, simulation, etc.)
```

### 后端接口

所有后端继承自`LiquidHandlerBackend`并实现：
- `setup()`：初始化与硬件的连接
- `stop()`：关闭连接和清理
- 设备特定的命令方法（吸液、分配等）

## 支持的后端

### Hamilton STAR（完全支持）

Hamilton STAR 和 STARlet 液体处理机器人具有完整的 PyLabRobot支持.

* *设置：**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck

# Create STAR backend
backend = STAR()

# Initialize liquid handler
lh = LiquidHandler(backend=backend, deck=STARLetDeck())
await lh.setup()
```

* *平台支持：**
- Windows ✅
- macOS ✅
- Linux ✅
- Raspberry Pi ✅

* *通讯：**
- USB 连接到机器人
- 直接固件命令
- 无需 Hamilton 软件

* * 功能：**
- 完整的液体处理操作
- CO-RE 尖端支持
- 96 通道头支持（如果配备）
- 温度控制
- 基于载体和轨道的定位

* *甲板类型：**
```python
from pylabrobot.resources import STARLetDeck, STARDeck

# For STARlet (smaller deck)
deck = STARLetDeck()

# For STAR (full deck)
deck = STARDeck()
```

* *示例：**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck, TIP_CAR_480_A00, Cos_96_DW_1mL

# Initialize
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# Define resources
tip_rack = TIP_CAR_480_A00(name="tips")
plate = Cos_96_DW_1mL(name="plate")

# Assign to rails
lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(plate, rails=10)

# Execute protocol
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(plate["A1"], plate["A2"], vols=100)
await lh.drop_tips()

await lh.stop()
```

### Opentrons OT-2（支持）

Opentrons OT-2 通过 Opentrons HTTP API 支持。

* *设置：**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import OpentronsBackend
from pylabrobot.resources import OTDeck

# Create Opentrons backend (requires robot IP address)
backend = OpentronsBackend(host="192.168.1.100")  # Replace with your robot's IP

# Initialize liquid handler
lh = LiquidHandler(backend=backend, deck=OTDeck())
await lh.setup()
```

* *平台支持：**
- 任何可通过网络访问的平台OT-2

* *通信：**
- 通过网络的 HTTP API
- 需要机器人 IP 地址
- 无需 Opentrons 应用程序

* * 功能：**
- 8 通道移液器支持
- 单通道移液器支持
- 标准OT-2甲板布局
- 基于坐标的定位

* *限制：**
- 使用较旧的 Opentrons HTTP API
- 与 STAR

 相比，某些功能可能受到限制**示例：**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import OpentronsBackend
from pylabrobot.resources import OTDeck

# Initialize with robot IP
lh = LiquidHandler(
    backend=OpentronsBackend(host="192.168.1.100"),
    deck=OTDeck()
)
await lh.setup()

# Load deck layout
lh.deck = Deck.load_from_json_file("opentrons_layout.json")

# Execute protocol
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(plate["A1"], plate["A2"], vols=100)
await lh.drop_tips()

await lh.stop()
```

### Tecan EVO（正在进行中）

对 Tecan EVO 液体处理机器人的支持正在进行中development.

* *当前状态：**
- 正在进行中
- 基本命令可能可用
- 检查当前功能支持的文档

* *设置（如果可用）：**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import TecanBackend
from pylabrobot.resources import TecanDeck

backend = TecanBackend()
lh = LiquidHandler(backend=backend, deck=TecanDeck())
```

### Hamilton Vantage（主要是支持）

Hamilton Vantage“大部分”完全支持。

* *设置：**

```python
from pylabrobot.liquid_handling.backends import Vantage
from pylabrobot.resources import VantageDeck

lh = LiquidHandler(backend=Vantage(), deck=VantageDeck())
```

* *功能：**
- 类似于STAR支持
- 一些高级功能可能受到限制

## 模拟后端

### Chatterbox后端（模拟）

使用模拟后端无需物理硬件即可测试协议。

* *设置：**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
from pylabrobot.resources import STARLetDeck

# Create simulation backend
backend = ChatterboxBackend(num_channels=8)

# Initialize liquid handler
lh = LiquidHandler(backend=backend, deck=STARLetDeck())
await lh.setup()
```

* *功能：**
- 无需硬件
- 模拟所有液体处理操作
- 与可视化工具配合使用以实现实时反馈
- 验证协议逻辑
- 跟踪提示和量

* *用例：**
- 协议开发和测试
- 培训和教育
- CI/CD 管道测试
- 无需硬件访问即可进行调试

* *示例：**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
from pylabrobot.resources import STARLetDeck, TIP_CAR_480_A00, Cos_96_DW_1mL
from pylabrobot.resources import set_tip_tracking, set_volume_tracking

# Enable tracking for simulation
set_tip_tracking(True)
set_volume_tracking(True)

# Initialize with simulation backend
lh = LiquidHandler(
    backend=ChatterboxBackend(num_channels=8),
    deck=STARLetDeck()
)
await lh.setup()

# Define resources
tip_rack = TIP_CAR_480_A00(name="tips")
plate = Cos_96_DW_1mL(name="plate")

lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(plate, rails=10)

# Set initial volumes
for well in plate.children:
    well.tracker.set_liquids([(None, 200)])

# Run simulated protocol
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(plate["A1:H1"], plate["A2:H2"], vols=100)
await lh.drop_tips()

# Check results
print(f"A1 volume: {plate['A1'].tracker.get_volume()} µL")  # 100 µL
print(f"A2 volume: {plate['A2'].tracker.get_volume()} µL")  # 100 µL

await lh.stop()
```

## 切换后端

### 后端无关协议

编写可与任何协议一起使用的协议后端：

```python
def get_backend(robot_type: str):
    """Factory function to create appropriate backend"""
    if robot_type == "star":
        from pylabrobot.liquid_handling.backends import STAR
        return STAR()
    elif robot_type == "opentrons":
        from pylabrobot.liquid_handling.backends import OpentronsBackend
        return OpentronsBackend(host="192.168.1.100")
    elif robot_type == "simulation":
        from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
        return ChatterboxBackend()
    else:
        raise ValueError(f"Unknown robot type: {robot_type}")

def get_deck(robot_type: str):
    """Factory function to create appropriate deck"""
    if robot_type == "star":
        from pylabrobot.resources import STARLetDeck
        return STARLetDeck()
    elif robot_type == "opentrons":
        from pylabrobot.resources import OTDeck
        return OTDeck()
    elif robot_type == "simulation":
        from pylabrobot.resources import STARLetDeck
        return STARLetDeck()
    else:
        raise ValueError(f"Unknown robot type: {robot_type}")

# Use in protocol
robot_type = "simulation"  # Change to "star" or "opentrons" as needed
backend = get_backend(robot_type)
deck = get_deck(robot_type)

lh = LiquidHandler(backend=backend, deck=deck)
await lh.setup()

# Protocol code works with any backend
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(plate["A1"], plate["A2"], vols=100)
await lh.drop_tips()
```

### 开发工作流程

1. **开发**：使用 ChatterboxBackend
2 编写协议。 **测试**：使用可视化工具运行以验证逻辑
3. **验证**：使用真实甲板布局
4进行模拟测试。 **部署**：切换到硬件后端（STAR、Opentrons）

```python
# Development
lh = LiquidHandler(backend=ChatterboxBackend(), deck=STARLetDeck())

# ... develop protocol ...

# Production (just change backend)
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
```

## 后端配置

### 自定义后端参数

一些后端接受配置参数：

```python
# Opentrons with custom parameters
backend = OpentronsBackend(
    host="192.168.1.100",
    port=31950  # Default Opentrons API port
)

# ChatterboxBackend with custom channels
backend = ChatterboxBackend(
    num_channels=8  # 8-channel simulation
)
```

### 连接故障排除

* *Hamilton STAR：**
- 确保 USB 电缆已连接
- 检查是否有其他软件正在使用机器人
- 验证固件是否为最新
- 在 macOS/Linux 上，可能需要 USB 权限

* *Opentrons OT-2：**
- 验证机器人 IP 地址是否正确
- 检查网络连接（ping 机器人）
- 确保机器人已开机
- 确认 Opentrons 应用程序未阻止 API 访问

* *常规：**
- 使用 `await lh.setup()` 测试连接
- 检查特定问题的错误消息
- 确保设备访问的适当权限

## 后端特定功能

### Hamilton STAR Specific

```python
# Access backend directly for hardware-specific features
star_backend = lh.backend

# Hamilton-specific commands (if needed)
# Most operations should go through LiquidHandler interface
```

### Opentrons Specific

```python
# Opentrons-specific configuration
ot_backend = lh.backend

# Access OT-2 API directly if needed (advanced)
# Most operations should go through LiquidHandler interface
```

## 最佳做法

1. **抽象硬件**：尽可能编写与后端无关的协议
2. **模拟测试**：始终首先使用 ChatterboxBackend
3 进行测试。 **工厂模式**：使用工厂函数创建后端
4. **错误处理**：优雅地处理连接错误
5. **文档**：您的协议后端支持
6的文档。 **配置**：使用后端参数
7的配置文件。 **版本控制**：跟踪后端版本和兼容性
8. **清理**：始终调用`await lh.stop()`来释放硬件
9. **单一连接**：一次只能有一个程序连接到硬件
10. **平台测试**：部署前在目标平台上进行测试

## 常见模式

### 多后端支持

```python
import asyncio
from typing import Literal

async def run_protocol(
    robot_type: Literal["star", "opentrons", "simulation"],
    visualize: bool = False
):
    """Run protocol on specified backend"""

    # Create backend
    if robot_type == "star":
        from pylabrobot.liquid_handling.backends import STAR
        backend = STAR()
        deck = STARLetDeck()
    elif robot_type == "opentrons":
        from pylabrobot.liquid_handling.backends import OpentronsBackend
        backend = OpentronsBackend(host="192.168.1.100")
        deck = OTDeck()
    elif robot_type == "simulation":
        from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
        backend = ChatterboxBackend()
        deck = STARLetDeck()

    # Initialize
    lh = LiquidHandler(backend=backend, deck=deck)
    await lh.setup()

    try:
        # Load deck layout (backend-agnostic)
        # lh.deck = Deck.load_from_json_file(f"{robot_type}_layout.json")

        # Execute protocol (backend-agnostic)
        await lh.pick_up_tips(tip_rack["A1"])
        await lh.transfer(plate["A1"], plate["A2"], vols=100)
        await lh.drop_tips()

        print("Protocol completed successfully!")

    finally:
        await lh.stop()

# Run on different backends
await run_protocol("simulation")      # Test in simulation
await run_protocol("star")            # Run on Hamilton STAR
await run_protocol("opentrons")       # Run on Opentrons OT-2
```

## 其他资源

- 后端文档： https://docs.pylabrobot.org/user_guide/backends.html
- 支持的机器： https://docs.pylabrobot.org/user_guide/machines.html
- API 参考： https://docs.pylabrobot.org/api/pylabrobot.liquid_handling.backends.html
- GitHub 示例：https://github.com/PyLabRobot/pylabrobot/tree/main/examples
