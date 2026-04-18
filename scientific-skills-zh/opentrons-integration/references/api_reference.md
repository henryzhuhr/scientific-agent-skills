# Opentrons Python 协议 API v2 参考

## 协议上下文方法

### 实验室器具管理

|方法|描述 |返回 |
|--------|-------------|---------|
| `load_labware(name, location, label=None, namespace=None, version=None)` |将实验室器具装载到甲板上 |实验室器具对象|
| `load_adapter(name, location, namespace=None, version=None)` |将适配器装载到甲板上 |实验室器具对象|
| `load_labware_from_definition(definition, location, label=None)` |从 JSON 加载自定义实验室器具 |实验室器具对象|
| `load_labware_on_adapter(name, adapter, label=None)` |将实验室器具装载到适配器上 |实验室器具对象|
| `load_labware_by_name(name, location, label=None, namespace=None, version=None)` |替代加载方法 |实验室器具对象|
| `load_lid_stack(load_name, location, quantity=None)` |装载盖叠层（仅限 Flex）|实验室器具对象 |

### 仪器管理

|方法|描述 |返回 |
|--------|-------------|---------|
| `load_instrument(instrument_name, mount, tip_racks=None, replace=False)` |装载移液器|仪器上下文 |

### 模块管理

|方法|描述 |返回 |
|--------|-------------|---------|
| `load_module(module_name, location=None, configuration=None)` |加载硬件模块| ModuleContext |

### 液体管理

|方法|描述 |返回 |
|--------|-------------|---------|
| `define_liquid(name, description=None, display_color=None)` |定义液体类型 |液体对象 |

### 执行控制

|方法|描述 |返回 |
|--------|-------------|---------|
| `pause(msg=None)` |暂停协议执行 |无 |
| `resume()` |暂停后继续 |无 |
| `delay(seconds=0, minutes=0, msg=None)` |延迟执行 |无 |
| `comment(msg)` |向协议日志添加注释 |无|
| `home()` |首页所有轴|无 |
| `set_rail_lights(on)` |控制轨灯（仅限 Flex）|无 |

### 协议属性

|物业 |描述 |类型|
|----------|----------|------|
| `deck` |甲板布局|甲板对象|
| `fixed_trash` |固定垃圾位置（OT-2）|垃圾箱对象 |
| `loaded_labwares` |装载实验室器具词典|字典 |
| `loaded_instruments` |加载仪器词典|字典 |
| `loaded_modules` |加载模块的字典 |字典 |
| `is_simulating()` |检查协议是否正在模拟 |布尔|
| `bundled_data` |访问捆绑数据文件 |字典 |
| `params` |运行时参数|参数上下文 |

## 仪器上下文（移液器）方法

### 吸头管理

|方法|描述 |返回 |
|--------|-------------|---------|
| `pick_up_tip(location=None, presses=None, increment=None)` |拾取提示|仪器上下文|
| `drop_tip(location=None, home_after=True)` |将小费扔进垃圾桶 |仪器上下文|
| `return_tip(home_after=True)` |将吸头放回到架子上 |仪器上下文|
| `reset_tipracks()` |重置提示跟踪 |无 |

### 液体处理 - 基本

|方法|描述 |返回 |
|--------|-------------|---------|
| `aspirate(volume=None, location=None, rate=1.0)` |吸出液体 |仪器上下文|
| `dispense(volume=None, location=None, rate=1.0, push_out=None)` |分配液体 |仪器上下文|
| `blow_out(location=None)` |排出残留液体 |仪器上下文|
| `touch_tip(location=None, radius=1.0, v_offset=-1.0, speed=60.0)` |去除尖端上的液滴 |仪器上下文|
| `mix(repetitions=1, volume=None, location=None, rate=1.0)` |混合液体|仪器上下文|
| `air_gap(volume=None, height=None)` |创建气隙 | InstrumentContext |

### 液体处理 - Complex

|方法|描述 |返回 |
|--------|-------------|---------|
| `transfer(volume, source, dest, **kwargs)` |转移液体 |仪器上下文|
| `distribute(volume, source, dest, **kwargs)` |从一对多分发 |仪器上下文|
| `consolidate(volume, source, dest, **kwargs)` |从多到一整合 |仪器上下文 |

* *transfer()、distribute()、consolidate() kwargs：**
- `new_tip`：“总是”、“一次”或“从不”
- `trash`：True/False - 使用后垃圾提示
- `touch_tip`：True/False - 使用后触摸提示吸液/分配
- `blow_out`：真/假 - 分配后吹出
- `mix_before`：（重复，体积）元组
- `mix_after`：（重复，体积）元组
- `disposal_volume`：额外体积污染预防
- `carryover`：真/假 - 启用大体积多次传输
- `gradient`：梯度（开始浓度、结束浓度）

### 移动和定位

|方法|描述 |返回 |
|--------|-------------|---------|
| `move_to(location, force_direct=False, minimum_z_height=None, speed=None)` |移至地点 |仪器上下文|
| `home()` |家用移液器轴 |无 |

### 移液器属性

|物业 |描述 |型号|
|----------|----------|------|
| `default_speed` |默认移动速度 |浮球|
| `min_volume` |最小移液量|浮球|
| `max_volume` |最大移液量|浮球|
| `current_volume` |提示中的当前音量 |浮球|
| `has_tip` |检查尖端是否已连接 |布尔|
| `name` |移液器名称 |字符串|
| `model` |移液器模型|字符串|
| `mount` |安装位置 |字符串|
| `channels` |频道数量 |国际|
| `tip_racks` |相关吸头架 |列表|
| `trash_container` |垃圾位置 |垃圾箱对象 |
| `starting_tip` |协议起始提示|井对象|
| `flow_rate` |流量设置| FlowRates 对象 |

### 流量属性

通过 `pipette.flow_rate`:

| 访问物业 |描述 |单位 |
|----------|-------------|--------|
| `aspirate` |吸气流量| µL/s |
| `dispense` |点胶流量| µL/s |
| `blow_out` |吹出流量| µL/s |

## 实验室器具方法

### Well Access

|方法|描述 |返回 |
|--------|-------------|---------|
| `wells()` |获取所有井 |列表[嗯] |
| `wells_by_name()` |获取井词典|字典[str，嗯] |
| `rows()` |按行获取井 |列表[列表[井]] |
| `columns()` |按列获取孔 |列表[列表[井]] |
| `rows_by_name()` |获取行字典 |字典[str，列表[Well]] |
| `columns_by_name()` |获取列字典 | Dict[str, List[Well]] |

### 实验室器具属性

|物业 |描述 |类型|
|----------|-------------|-----|
| `name` |实验室器具名称 |字符串 |
| `parent` |家长位置 |位置对象|
| `quirks` |实验室器具怪癖列表|列表|
| `magdeck_engage_height` |磁性模块高度|浮球|
| `uri` |实验室器具 URI |字符串|
| `calibrated_offset` |校准偏移|点 |

## 井方法和性质

### 液体作业

|方法|描述 |返回 |
|--------|-------------|---------|
| `load_liquid(liquid, volume)` |将液体装入孔中 |无 |
| `load_empty()` |将井标记为空 |无 |
| `from_center_cartesian(x, y, z)` |获取中心位置 |位置 |

### 位置方法

|方法|描述 |返回 |
|--------|-------------|---------|
| `top(z=0)` |获取井顶位置 |位置|
| `bottom(z=0)` |获取井底位置 |位置|
| `center()` |获取井中心位置 |位置 |

### 井属性

|物业 |描述 |类型|
|----------|----------|------|
| `diameter` |井径（圆形）|浮球|
| `length` |井长（矩形）|浮球|
| `width` |孔宽度（矩形）|浮球|
| `depth` |井深|浮球|
| `max_volume` |最大音量|浮球|
| `display_name` |显示名称 |字符串|
| `has_tip` |检查尖端是否存在 | Bool |

## 模块上下文

### 温度模块

|方法|描述 |返回 |
|--------|-------------|---------|
| `set_temperature(celsius)` |设定目标温度|无 |
| `await_temperature(celsius)` |等待温度 |无 |
| `deactivate()` |关闭温度控制|无 |
| `load_labware(name, label=None, namespace=None, version=None)` |在模块上加载实验室器具 |实验室器具 |

* *属性：**
- `temperature`：当前温度 (°C)
- `target`：目标温度 (°C)
- `status`：“空闲”、“保持”、“冷却”或“加热”
- `labware`：已加载实验室器具

### 磁性模块

|方法|描述 |返回 |
|--------|-------------|---------|
| `engage(height_from_base=None, offset=None, height=None)` |接合磁铁 |无 |
| `disengage()` |松开磁铁 |无 |
| `load_labware(name, label=None, namespace=None, version=None)` |在模块上加载实验室器具 |实验室器具 |

* *属性：**
- `status`：“接合”或“​​脱离”
- `labware`：已加载的实验室器具

### 加热摇床模块

|方法|描述 |返回 |
|--------|-------------|---------|
| `set_target_temperature(celsius)` |设定加热器目标 |无 |
| `wait_for_temperature()` |等待温度|无|
| `set_and_wait_for_temperature(celsius)` |设置并等待 |无 |
| `deactivate_heater()` |关闭加热器|无 |
| `set_and_wait_for_shake_speed(rpm)` |设置摇动速度|无 |
| `deactivate_shaker()` |关闭摇床|无|
| `open_labware_latch()` |打开闩锁|无 |
| `close_labware_latch()` |关闭闩锁|无 |
| `load_labware(name, label=None, namespace=None, version=None)` |在模块上加载实验室器具 |实验室器具 |

* *属性：**
- `temperature`：当前温度（°C）
- `target_temperature`：目标温度（°C）
- `current_speed`：当前摇动速度（rpm）
- `target_speed`：目标摇动速度(rpm)
- `labware_latch_status`：'idle_open'、'idle_close'、'opening'、'close'
- `status`：模块状态
- `labware`：已加载的实验室器具

### 热循环仪模块

|方法|描述 |返回 |
|--------|-------------|---------|
| `open_lid()` |打开盖子|无 |
| `close_lid()` |合上盖子|无 |
| `set_lid_temperature(celsius)` |设置盖子温度 |无 |
| `deactivate_lid()` |关闭盖子加热器 |无 |
| `set_block_temperature(temperature, hold_time_seconds=0, hold_time_minutes=0, ramp_rate=None, block_max_volume=None)` |设置块温度 |无 |
| `deactivate_block()` |关闭块|无 |
| `execute_profile(steps, repetitions, block_max_volume=None)` |运行温度曲线|无 |
| `load_labware(name, label=None, namespace=None, version=None)` |在模块上加载实验室器具 |实验室软件 |

* *配置文件步骤格式：**
```python
{'temperature': 95, 'hold_time_seconds': 30, 'hold_time_minutes': 0}
```

* *属性：**
- `block_temperature`：当前模块温度 (°C)
- `block_target_temperature`：目标模块温度(°C)
- `lid_temperature`：当前盖子温度 (°C)
- `lid_target_temperature`：目标盖子温度 (°C)
- `lid_position`：“打开”、“关闭”、“in_ Between”
- `ramp_rate`：模块升温速率 (°C/s)
- `status`：模块状态
- `labware`：已加载的实验室器具

### 吸光度板读数器模块

|方法|描述 |返回 |
|--------|-------------|---------|
| `initialize(mode, wavelengths)` |初始化阅读器 |无 |
| `read(export_filename=None)` |读盘|字典 |
| `close_lid()` |合上盖子|无|
| `open_lid()` |打开盖子|无 |
| `load_labware(name, label=None, namespace=None, version=None)` |在模块上加载实验室器具 |实验室器具 |

* *读取模式：**
- `'single'`：单波长
- `'multi'`：多波长

* *属性：**
- `is_lid_on`：盖子状态
- `labware`：已加载的实验室器具

## 常见实验室器具 API 名称

### 板

- `corning_96_wellplate_360ul_flat`
- `nest_96_wellplate_100ul_pcr_full_skirt`
- `nest_96_wellplate_200ul_flat`
- `biorad_96_wellplate_200ul_pcr`
- `appliedbiosystems_384_wellplate_40ul`

### 储液罐

- `nest_12_reservoir_15ml`
- `nest_1_reservoir_195ml`
- `usascientific_12_reservoir_22ml`

### 尖端架

* *Flex：**
- `opentrons_flex_96_tiprack_50ul`
- `opentrons_flex_96_tiprack_200ul`
- `opentrons_flex_96_tiprack_1000ul`

* *OT-2:**
- `opentrons_96_tiprack_20ul`
- `opentrons_96_tiprack_300ul`
- `opentrons_96_tiprack_1000ul`

### 管架

- `opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical`
- `opentrons_24_tuberack_nest_1.5ml_snapcap`
- `opentrons_24_tuberack_nest_1.5ml_screwcap`
- `opentrons_15_tuberack_falcon_15ml_conical`

### 适配器

- `opentrons_flex_96_tiprack_adapter`
- `opentrons_96_deep_well_adapter`
- `opentrons_aluminum_flat_bottom_plate`

## 错误处理

常用例外：

- `OutOfTipsError`：没有可用吸头
- `LabwareNotLoadedError`：实验室器具未装载在平台上
- `InvalidContainerError`：实验室器具规格无效
- `InstrumentNotLoadedError`：移液器未装载已加载
- `InvalidVolumeError`：音量超出范围

## 模拟和调试

检查模拟状态：
```python
if protocol.is_simulating():
    protocol.comment('Running in simulation')
```

访问捆绑数据文件：
```python
data_file = protocol.bundled_data['data.csv']
with open(data_file) as f:
    data = f.read()
```

## 版本兼容性

API级别兼容性：

| API 级别 |特点|
|---------|----------|
| 2.19 | 2.19最新功能，Flex支持|
| 2.18 | 2.18吸光度酶标仪|
| 2.17 | 2.17液体跟踪改进|
| 2.16 | 2.16 Flex 8 通道部分尖端拾音器 |
| 2.15 | 2.15加热摇床 Gen1 |
| 2.13 | 2.13温度模块 Gen2 |
| 2.0-2.12 |核心 OT-2 功能 |

 对于新协议始终使用最新的稳定 API 版本。
