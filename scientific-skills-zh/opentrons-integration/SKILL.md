---
name: opentrons-integration
description: 适用于 OT-2 和 Flex 机器人的官方 Opentrons 协议 API。在专门为 Opentrons 硬件编写协议时使用，可以完全访问协议 API v2 功能。最适合生产 Opentrons 协议，官方 API 兼容性。对于多供应商自动化或更广泛的设备控制，请使用 pylabrobot。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Opentrons 集成

## 概述

Opentrons 是一个基于 Python 的实验室自动化平台，适用于 Flex 和 OT-2 机器人。编写用于液体处理的 Protocol API v2 协议、控制硬件模块（加热器摇床、热循环仪）、管理实验室器具、用于自动移液工作流程。

## 何时使用此技能

此技能应在以下情况下使用：
- 在 Python 中编写 Opentrons Protocol API v2 协议
- 在 Flex 或 OT-2 上自动化液体处理工作流程机器人
- 控制硬件模块（温度、磁力、加热摇床、热循环仪）
- 设置实验室器具配置和平台布局
- 实施复杂的移液操作（连续稀释、板复制、PCR 设置）
- 管理吸头使用和优化方案效率
- 使用用于 96 孔板的多通道移液器操作
- 在机器人执行之前模拟和测试协议

## 核心功能

### 1. 协议结构和元数据

每个Opentrons协议都遵循标准结构：

```python
from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@example.com>',
    'description': 'Protocol description',
    'apiLevel': '2.19'  # Use latest available API version
}

# Requirements (optional)
requirements = {
    'robotType': 'Flex',  # or 'OT-2'
    'apiLevel': '2.19'
}

# Run function
def run(protocol: protocol_api.ProtocolContext):
    # Protocol commands go here
    pass
```

* *关键要素：**
- 导入`protocol_api` 来自 `opentrons`
- 使用协议名称、作者、描述、apiLevel 定义 `metadata` 字典
- 用于机器人类型和 API 版本的可选 `requirements` 字典
- 实现 `run()` 函数接收 `ProtocolContext` 作为参数
- 所有协议逻辑均位于`run()`功能内部

### 2.加载硬件

* *加载仪器（移液器）：**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Load pipette on specific mount
    left_pipette = protocol.load_instrument(
        'p1000_single_flex',  # Instrument name
        'left',               # Mount: 'left' or 'right'
        tip_racks=[tip_rack]  # List of tip rack labware objects
    )
```

常用移液器名称：
- Flex： `p50_single_flex`、`p1000_single_flex`、`p50_multi_flex`、`p1000_multi_flex`
- OT-2：`p20_single_gen2`、`p300_single_gen2`、`p1000_single_gen2`、`p20_multi_gen2`、 `p300_multi_gen2`

* *加载实验室器具：**

```python
# Load labware directly on deck
plate = protocol.load_labware(
    'corning_96_wellplate_360ul_flat',  # Labware API name
    'D1',                                # Deck slot (Flex: A1-D3, OT-2: 1-11)
    label='Sample Plate'                 # Optional display label
)

# Load tip rack
tip_rack = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'C1')

# Load labware on adapter
adapter = protocol.load_adapter('opentrons_flex_96_tiprack_adapter', 'B1')
tips = adapter.load_labware('opentrons_flex_96_tiprack_200ul')
```

* *加载模块：**

```python
# Temperature module
temp_module = protocol.load_module('temperature module gen2', 'D3')
temp_plate = temp_module.load_labware('corning_96_wellplate_360ul_flat')

# Magnetic module
mag_module = protocol.load_module('magnetic module gen2', 'C2')
mag_plate = mag_module.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

# Heater-Shaker module
hs_module = protocol.load_module('heaterShakerModuleV1', 'D1')
hs_plate = hs_module.load_labware('corning_96_wellplate_360ul_flat')

# Thermocycler module (takes up specific slots automatically)
tc_module = protocol.load_module('thermocyclerModuleV2')
tc_plate = tc_module.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
```

### 3. 液体处理操作

* *基本运算：**

```python
# Pick up tip
pipette.pick_up_tip()

# Aspirate (draw liquid in)
pipette.aspirate(
    volume=100,           # Volume in µL
    location=source['A1'] # Well or location object
)

# Dispense (expel liquid)
pipette.dispense(
    volume=100,
    location=dest['B1']
)

# Drop tip
pipette.drop_tip()

# Return tip to rack
pipette.return_tip()
```

* *复杂运算：**

```python
# Transfer (combines pick_up, aspirate, dispense, drop_tip)
pipette.transfer(
    volume=100,
    source=source_plate['A1'],
    dest=dest_plate['B1'],
    new_tip='always'  # 'always', 'once', or 'never'
)

# Distribute (one source to multiple destinations)
pipette.distribute(
    volume=50,
    source=reservoir['A1'],
    dest=[plate['A1'], plate['A2'], plate['A3']],
    new_tip='once'
)

# Consolidate (multiple sources to one destination)
pipette.consolidate(
    volume=50,
    source=[plate['A1'], plate['A2'], plate['A3']],
    dest=reservoir['A1'],
    new_tip='once'
)
```

* *高级技术：**

```python
# Mix (aspirate and dispense in same location)
pipette.mix(
    repetitions=3,
    volume=50,
    location=plate['A1']
)

# Air gap (prevent dripping)
pipette.aspirate(100, source['A1'])
pipette.air_gap(20)  # 20µL air gap
pipette.dispense(120, dest['A1'])

# Blow out (expel remaining liquid)
pipette.blow_out(location=dest['A1'].top())

# Touch tip (remove droplets on tip exterior)
pipette.touch_tip(location=plate['A1'])
```

* *流量控制：**

```python
# Set flow rates (µL/s)
pipette.flow_rate.aspirate = 150
pipette.flow_rate.dispense = 300
pipette.flow_rate.blow_out = 400
```

### 4. 进入井和位置

* *井进入方法：**

```python
# By name
well_a1 = plate['A1']

# By index
first_well = plate.wells()[0]

# All wells
all_wells = plate.wells()  # Returns list

# By rows
rows = plate.rows()  # Returns list of lists
row_a = plate.rows()[0]  # All wells in row A

# By columns
columns = plate.columns()  # Returns list of lists
column_1 = plate.columns()[0]  # All wells in column 1

# Wells by name (dictionary)
wells_dict = plate.wells_by_name()  # {'A1': Well, 'A2': Well, ...}
```

* *位置方法：**

```python
# Top of well (default: 1mm below top)
pipette.aspirate(100, well.top())
pipette.aspirate(100, well.top(z=5))  # 5mm above top

# Bottom of well (default: 1mm above bottom)
pipette.aspirate(100, well.bottom())
pipette.aspirate(100, well.bottom(z=2))  # 2mm above bottom

# Center of well
pipette.aspirate(100, well.center())
```

### 5. 硬件模块控制

* *温度模块：**

```python
# Set temperature
temp_module.set_temperature(celsius=4)

# Wait for temperature
temp_module.await_temperature(celsius=4)

# Deactivate
temp_module.deactivate()

# Check status
current_temp = temp_module.temperature  # Current temperature
target_temp = temp_module.target  # Target temperature
```

* *磁性模块：**

```python
# Engage (raise magnets)
mag_module.engage(height_from_base=10)  # mm from labware base

# Disengage (lower magnets)
mag_module.disengage()

# Check status
is_engaged = mag_module.status  # 'engaged' or 'disengaged'
```

* *加热摇床模块：**

```python
# Set temperature
hs_module.set_target_temperature(celsius=37)

# Wait for temperature
hs_module.wait_for_temperature()

# Set shake speed
hs_module.set_and_wait_for_shake_speed(rpm=500)

# Close labware latch
hs_module.close_labware_latch()

# Open labware latch
hs_module.open_labware_latch()

# Deactivate heater
hs_module.deactivate_heater()

# Deactivate shaker
hs_module.deactivate_shaker()
```

* *热循环仪模块：**

```python
# Open lid
tc_module.open_lid()

# Close lid
tc_module.close_lid()

# Set lid temperature
tc_module.set_lid_temperature(celsius=105)

# Set block temperature
tc_module.set_block_temperature(
    temperature=95,
    hold_time_seconds=30,
    hold_time_minutes=0.5,
    block_max_volume=50  # µL per well
)

# Execute profile (PCR cycling)
profile = [
    {'temperature': 95, 'hold_time_seconds': 30},
    {'temperature': 57, 'hold_time_seconds': 30},
    {'temperature': 72, 'hold_time_seconds': 60}
]
tc_module.execute_profile(
    steps=profile,
    repetitions=30,
    block_max_volume=50
)

# Deactivate
tc_module.deactivate_lid()
tc_module.deactivate_block()
```

* *吸光度板读数器：**

```python
# Initialize and read
result = plate_reader.read(wavelengths=[450, 650])

# Access readings
absorbance_data = result  # Dict with wavelength keys
```

### 6. 液体跟踪和标记

* *定义液体：**

```python
# Define liquid types
water = protocol.define_liquid(
    name='Water',
    description='Ultrapure water',
    display_color='#0000FF'  # Hex color code
)

sample = protocol.define_liquid(
    name='Sample',
    description='Cell lysate sample',
    display_color='#FF0000'
)
```

* *将液体加载到孔中：**

```python
# Load liquid into specific wells
reservoir['A1'].load_liquid(liquid=water, volume=50000)  # µL
plate['A1'].load_liquid(liquid=sample, volume=100)

# Mark wells as empty
plate['B1'].load_empty()
```

### 7. 协议控制和实用程序

* *执行控制：**

```python
# Pause protocol
protocol.pause(msg='Replace tip box and resume')

# Delay
protocol.delay(seconds=60)
protocol.delay(minutes=5)

# Comment (appears in logs)
protocol.comment('Starting serial dilution')

# Home robot
protocol.home()
```

* *条件逻辑：**

```python
# Check if simulating
if protocol.is_simulating():
    protocol.comment('Running in simulation mode')
else:
    protocol.comment('Running on actual robot')
```

* *导轨灯（仅限 Flex）：**

```python
# Turn lights on
protocol.set_rail_lights(on=True)

# Turn lights off
protocol.set_rail_lights(on=False)
```

### 8. 多通道和8 通道移液

使用多通道移液器时：

```python
# Load 8-channel pipette
multi_pipette = protocol.load_instrument(
    'p300_multi_gen2',
    'left',
    tip_racks=[tips]
)

# Access entire column with single well reference
multi_pipette.transfer(
    volume=100,
    source=source_plate['A1'],  # Accesses entire column 1
    dest=dest_plate['A1']       # Dispenses to entire column 1
)

# Use rows() for row-wise operations
for row in plate.rows():
    multi_pipette.transfer(100, reservoir['A1'], row[0])
```

### 9. 常用协议模式

* *连续稀释：**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'D1')
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'D2')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D3')

    # Load pipette
    p300 = protocol.load_instrument('p300_single_flex', 'left', tip_racks=[tips])

    # Add diluent to all wells except first
    p300.transfer(100, reservoir['A1'], plate.rows()[0][1:])

    # Serial dilution across row
    p300.transfer(
        100,
        plate.rows()[0][:11],  # Source: wells 0-10
        plate.rows()[0][1:],   # Dest: wells 1-11
        mix_after=(3, 50),     # Mix 3x with 50µL after dispense
        new_tip='always'
    )
```

* *板复制：**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'C1')
    source = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D1')
    dest = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D2')

    # Load pipette
    p1000 = protocol.load_instrument('p1000_single_flex', 'left', tip_racks=[tips])

    # Transfer from all wells in source to dest
    p1000.transfer(
        100,
        source.wells(),
        dest.wells(),
        new_tip='always'
    )
```

* *PCR 设置：**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Load thermocycler
    tc_mod = protocol.load_module('thermocyclerModuleV2')
    tc_plate = tc_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

    # Load tips and reagents
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'C1')
    reagents = protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', 'D1')

    # Load pipette
    p300 = protocol.load_instrument('p300_single_flex', 'left', tip_racks=[tips])

    # Open thermocycler lid
    tc_mod.open_lid()

    # Distribute master mix
    p300.distribute(
        20,
        reagents['A1'],
        tc_plate.wells(),
        new_tip='once'
    )

    # Add samples (example for first 8 wells)
    for i, well in enumerate(tc_plate.wells()[:8]):
        p300.transfer(5, reagents.wells()[i+1], well, new_tip='always')

    # Run PCR
    tc_mod.close_lid()
    tc_mod.set_lid_temperature(105)

    # PCR profile
    tc_mod.set_block_temperature(95, hold_time_seconds=180)

    profile = [
        {'temperature': 95, 'hold_time_seconds': 15},
        {'temperature': 60, 'hold_time_seconds': 30},
        {'temperature': 72, 'hold_time_seconds': 30}
    ]
    tc_mod.execute_profile(steps=profile, repetitions=35, block_max_volume=25)

    tc_mod.set_block_temperature(72, hold_time_minutes=5)
    tc_mod.set_block_temperature(4)

    tc_mod.deactivate_lid()
    tc_mod.open_lid()
```

## 最佳实践

1. **始终指定 API 级别**：使用元数据中最新的稳定 API 版本
2. **使用有意义的标签**：为实验室器具贴上标签，以便在日志中更容易识别
3. **检查吸头可用性**：确保有足够的吸头用于协议完成
4. **添加注释**：使用`protocol.comment()`进行调试和记录
5. **首先模拟**：在 robots
6 上运行之前，始终在模拟中测试协议。 **优雅地处理错误**：在需要时添加暂停以进行手动干预
7. **考虑时间**：当方案需要潜伏期时使用延迟
8. **跟踪液体**：使用液体跟踪可以更好地验证设置
9. **优化小费使用**：在适当的情况下使用`new_tip='once'`来保存小费
10. **控制流量**：调节粘性或挥发性液体的流量

## 故障排除

* *常见问题：**

- **吸头耗尽**：验证吸头架容量是否符合实验方案要求
- **实验室器具碰撞**：检查平台布局是否存在空间冲突
- **体积错误**：确保体积不超过孔或移液器容量
- **模块不响应**：验证模块是否正确连接且固件已更新
- **体积不准确**：校准移液器并检查空气bubbles
- **协议模拟失败**：检查API版本兼容性和实验室器具定义

## 资源

详细API文档，请参阅本技能目录中的`references/api_reference.md`。

，示例协议模板，请参阅`scripts/`目录。
