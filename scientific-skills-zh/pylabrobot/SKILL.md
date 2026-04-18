---
name: pylabrobot
description: 与供应商无关的实验室自动化框架。当控制多种设备类型（Hamilton、Tecan、Opentron、读板机、泵）或需要跨不同供应商进行统一编程时使用。最适合复杂的工作流程、多供应商设置、模拟。对于具有官方 API 的仅限 Opentrons 的协议，opentrons-integration 可能更简单。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PyLabRobot

## 概述

PyLabRobot 是一款与硬件无关的纯 Python 软件开发套件，适用于自动化和自主实验室。使用此技能通过跨平台（Windows、macOS、Linux）工作的统一 Python 界面来控制液体处理机器人、读板器、泵、加热器摇床、培养箱、离心机和其他实验室自动化设备。

## 何时使用此技能

在以下情况下使用此技能：
- 编程液体处理机器人（Hamilton STAR/STARlet、Opentrons OT-2、Tecan） EVO)
- 自动化涉及移液、样品制备或分析测量的实验室工作流程
- 管理平台布局和实验室资源（板、吸头、容器、槽）
- 集成多个实验室设备（液体处理器、读板器、加热摇床、泵）
- 通过状态管理创建可重复的实验室方案
- 在物理硬件上运行之前模拟协议
- 使用 BMG CLARIOstar 或其他支持的读板器读板
- 控制温度、摇动、离心或其他材料处理操作
- 在 Python 中使用实验室自动化

## 核心功能

PyLabRobot 通过六个主要功能领域提供全面的实验室自动化，每个功能领域均在参考文献/中详细介绍目录：

### 1.液体处理(`references/liquid-handling.md`)

控制液体处理机器人来吸取、分配和转移液体。主要操作包括：
- **基本操作**：在孔之间吸液、分配、转移液体
- **吸头管理**：自动拾取、落下和跟踪移液器吸头
- **高级技术**：多通道移液、连续稀释、板复制
- **体积跟踪**：自动跟踪液体体积孔
- **硬件支持**：Hamilton STAR/STARlet、Opentrons OT-2、Tecan EVO 等

### 2. 资源管理 (`references/resources.md`)

在分层系统中管理实验室资源：
- **资源类型**：板、吸头架、槽、管、载体和定制labware
- **甲板布局**：使用坐标系将资源分配到甲板位置
- **状态管理**：跟踪吸头存在、液体体积和资源状态
- **序列化**：从JSON文件保存和加载甲板布局和状态
- **资源发现**：通过直观的API访问孔、吸头和容器

### 3. 硬件后端 (`references/hardware-backends.md`)

通过后端抽象连接到各种实验室设备：
- **液体处理器**：Hamilton STAR（完全支持）、Opentrons OT-2、Tecan EVO
- **模拟**：无需硬件即可进行协议测试的 Chatterbox 后端
- **平台支持**：适用于 Windows、macOS、Linux 和 Raspberry Pi
- **后端切换**：通过交换后端来更改机器人，无需重写协议

### 4. 分析设备 (`references/analytical-equipment.md`)

集成读板器和分析仪器：
- **读板器**：用于吸光度、发光、荧光的 BMG CLARIOstar
- **秤**：用于质量测量的梅特勒-托利多集成
- **集成模式**：将液体处理器与分析设备相结合
- **自动化工作流程**：在设备之间移动板自动

### 5. 物料处理 (`references/material-handling.md`)

控制环境和物料处理设备：
- **加热器摇床**：Hamilton HeaterShaker、Inheco ThermoShake
- **培养箱**：带温度控制功能的 Inheco 和 Thermo Fisher 培养箱
- **离心机**：安捷伦带有铲斗定位和旋转控制的 VSpin
- **泵**：用于流体泵送操作的 Cole Parmer Masterflex
- **温度控制**：在协议期间设置和监控温度

### 6. 可视化和模拟 (`references/visualization.md`)

可视化和模拟实验室协议：
- **浏览器可视化器**：平台状态的实时 3D 可视化
- **模拟模式**：无需物理硬件即可测试协议
- **状态跟踪**：直观地监控尖端存在和液体体积
- **平台编辑器**：用于设计平台布局的图形工具
- **协议验证**：在硬件上运行之前验证协议

## 快速入门

要开始使用 PyLabRobot，请安装软件包并初始化液体处理程序：

```python
# Install PyLabRobot
# uv pip install pylabrobot

# Basic liquid handling setup
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck

# Initialize liquid handler
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# Basic operations
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.aspirate(plate["A1"], vols=100)
await lh.dispense(plate["A2"], vols=100)
await lh.drop_tips()
```

## 使用引用

此技能可以组织多个参考文件中的详细信息。在以下情况下加载相关参考：
- **液体处理**：编写移液方案、吸头管理、转移
- **资源**：定义平台布局、管理板/吸头、定制实验室器具
- **硬件后端**：连接到特定机器人、切换平台
- **分析设备**：集成读板器、天平或分析设备设备
- **材料处理**：使用加热器摇床、培养箱、离心机、泵
- **可视化**：模拟协议、可视化平台状态

所有参考文件都可以在`references/`目录中找到，并包含全面的示例、API使用模式和最佳实践。

## 最佳实践

创建实验室自动化协议时PyLabRobot：

1. **从模拟开始**：在硬件 
2 上运行之前，使用 ChatterboxBackend 和可视化工具测试协议。 **启用跟踪**：打开尖端跟踪和音量跟踪以进行准确的状态管理
3. **资源命名**：为所有资源（板、吸头架、容器）使用清晰的描述性名称
4. **状态序列化**：将牌组布局和状态保存为 JSON 以实现可重复性
5. **错误处理**：为硬件操作实现正确的异步错误处理
6. **温度控制**：尽早设定温度，因为加热/冷却需要时间
7. **模块化协议**：将复杂的工作流程分解为可重用的功能
8. **文档**：参考官方文档 https://docs.pylabrobot.org 了解最新功能

## 常用工作流程

### 液体传输协议

```python
# Setup
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# Define resources
tip_rack = TIP_CAR_480_A00(name="tip_rack")
source_plate = Cos_96_DW_1mL(name="source")
dest_plate = Cos_96_DW_1mL(name="dest")

lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(source_plate, rails=10)
lh.deck.assign_child_resource(dest_plate, rails=15)

# Transfer protocol
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(source_plate["A1:H12"], dest_plate["A1:H12"], vols=100)
await lh.drop_tips()
```

### 板读取工作流程

```python
# Setup plate reader
from pylabrobot.plate_reading import PlateReader
from pylabrobot.plate_reading.clario_star_backend import CLARIOstarBackend

pr = PlateReader(name="CLARIOstar", backend=CLARIOstarBackend())
await pr.setup()

# Set temperature and read
await pr.set_temperature(37)
await pr.open()
# (manually or robotically load plate)
await pr.close()
data = await pr.read_absorbance(wavelength=450)
```

## 其他资源

- **官方文档**：https://docs.pylabrobot.org
- **GitHub 存储库**：https://github.com/PyLabRobot/pylabrobot
- **社区论坛**：https://discuss.pylabrobot.org
- **PyPI 包**： https://pypi.org/project/PyLabRobot/

具体能力的详细使用，请参考`references/`目录下对应的参考文件
