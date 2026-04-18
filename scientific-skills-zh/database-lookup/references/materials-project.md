# 材料项目 API

## 基本 URL

```
https://api.materialsproject.org
```

## 身份验证

需要免费的 API 密钥。在 https://materialsproject.org 注册（免费帐户）。

|环境变量 |标题 |
|---|---|
| `MP_API_KEY` | `X-API-KEY: your_key_here` |

所有请求都必须包含 API 密钥标头。

## API 版本

当前 API 是 **v2**（基于 `mp-api` Python 客户端和新的 MAPI 端点）。 `https://www.materialsproject.org/rest/v2/` 的旧版 v1 REST API 已弃用。

## 关键端点

### 按公式或元素搜索材料

```
GET /materials/summary/?formula=Fe2O3&_fields=material_id,formula_pretty,band_gap,formation_energy_per_atom
```

```
GET /materials/summary/?elements=Si,O&_fields=material_id,formula_pretty,band_gap
```

查询参数：
- `formula` — 准确的化学式（例如，`Fe2O3`、`SiO2`）
- `chemsys` — 化学体系，以破折号分隔（例如，`Fe-O`、`Li-Fe-P-O`）
- `elements` —必须存在的逗号分隔元素
- `band_gap_min` / `band_gap_max` — 按带隙 (eV)过滤
- `is_stable` — `true` 仅返回热力学稳定相
- `_fields` — 逗号分隔列表要返回的字段数
- `_limit` — 最大结果（默认 10，最大 1000）
- `_skip` — 分页偏移量

### 通过 ID 获取材料

```
GET /materials/summary/mp-149?_fields=material_id,formula_pretty,band_gap,formation_energy_per_atom,symmetry
```

 材料 ID 的格式如下`mp-NNNNN`（例如，`mp-149` 用于硅）。

### 可用字段（摘要）

`material_id`、`formula_pretty`、`formula_anonymous`、`chemsys`、`volume`、 `density`、`density_atomic`、`symmetry`、`band_gap`、`cbm`、`vbm`、`is_gap_direct`、`is_metal`、`is_magnetic`、`ordering`、 `total_magnetization`、`formation_energy_per_atom`、`energy_above_hull`、`is_stable`、`equilibrium_reaction_energy_per_atom`、`nsites`、`elements`、`nelements`、`composition`、 `structure`

### 晶体结构

```
GET /materials/summary/mp-149?_fields=structure
```

将结构作为具有晶格参数和原子位点的pymatgen兼容的JSON字典返回。

### 弹性属性

```
GET /materials/elasticity/?material_id=mp-149&_fields=material_id,bulk_modulus,shear_modulus,elastic_tensor
```

### 电子结构（能带结构/DOS）

```
GET /materials/electronic_structure/bandstructure/mp-149
GET /materials/electronic_structure/dos/mp-149
```

### 热力学性质

```
GET /materials/thermo/?formula=Fe2O3&_fields=material_id,formation_energy_per_atom,energy_above_hull
```

### 示例：查找带隙 > 2 的稳定氧化物eV

```
GET /materials/summary/?elements=O&band_gap_min=2&is_stable=true&_fields=material_id,formula_pretty,band_gap,formation_energy_per_atom&_limit=10
```

## 响应格式

```json
{
  "data": [
    {
      "material_id": "mp-149",
      "formula_pretty": "Si",
      "band_gap": 0.6105,
      "formation_energy_per_atom": 0.0
    }
  ],
  "meta": {
    "total_doc": 1
  }
}
```

## 速率限制

- 已验证：约 50 个请求/分钟（因服务器负载而异）
- 优先于许多单独调用的批量请求
- 使用`_fields` 可减少负载大小并提高性能
  - Python 客户端 `mp-api` 自动处理分页和重试

## 错误格式

```json
{
  "detail": "Not authenticated"
}
```

HTTP 401 = 丢失或无效 API 密钥。 HTTP 404 = 未找到材料。 HTTP 429 = 速率受限。
