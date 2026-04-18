# 晶体学开放数据库 (COD) API

## 基本 URL

```
https://www.crystallography.net/cod
```

## 身份验证

* *不需要。** COD 完全开放访问，无需 API 密钥。

## 关键端点

### 搜索公式

```
GET /result?formula=Fe2%20O3&format=json
```

公式格式在元素之间使用空格：`Fe2 O3`、`Si O2`、`C6 H12 O6`。 URL 将空格编码为 `%20`.

### 按元素搜索

```
GET /result?el1=Fe&el2=O&format=json
```

 使用 `el1`、`el2`、`el3` 等进行元素过滤器。使用 `nel=2` 限制为恰好 2 个元素。

### 按单元参数搜索

```
GET /result?a_min=5.0&a_max=6.0&b_min=5.0&b_max=6.0&c_min=5.0&c_max=6.0&format=json
```

 单元参数过滤器：
- `a_min`、`a_max` — a 轴长度（埃）
- `b_min`、`b_max` — b 轴长度
- `c_min`、`c_max` — c 轴长度
- `alpha_min`、`alpha_max` — α 角（度）
- `beta_min`、`beta_max` — β 角
- `gamma_min`、`gamma_max` — 伽玛角
- `vol_min`、`vol_max` — 晶胞体积 (A^3)

### 按空格搜索group

```
GET /result?sg=F%20m%20-3%20m&format=json
```

### 按文本搜索（作者、期刊、标题）

```
GET /result?text=perovskite&format=json
```

### 组合搜索示例

```
GET /result?el1=Ti&el2=O&nel=2&sg=P%2042/m%20n%20m&format=json
```

### 检索特定 CIF file

```
GET /1000000.cif
```

COD ID 是 7 位整数。为晶体信息文件附加 `.cif`，为网页附加 `.html`。

### 以 JSON

```
GET /result?id=1000000&format=json
```

### 输出格式

- `format=json` — JSON 匹配数组检索条目元数据条目
- `format=csv` — CSV 输出
- `format=lst` — 仅 COD ID 列表
- 默认（无格式） — HTML 页面

## 响应格式

```json
[
  {
    "file": "1526463",
    "a": "4.759",
    "b": "4.759",
    "c": "12.992",
    "alpha": "90",
    "beta": "90",
    "gamma": "120",
    "vol": "254.94",
    "sg": "R -3 c",
    "formula": "Fe2 O3",
    "title": "Refinement of the crystal structure of ...",
    "journal": "Zeitschrift fuer Kristallographie",
    "year": "1966",
    "authors": "Blake, R.L.; et al."
  }
]
```

The `file` 字段是 COD ID。用它来获取 CIF：`https://www.crystallography.net/cod/{file}.cif`

## Rate Limits

- 没有记录正式的速率限制
- 要有礼貌：避免快速批量下载数千个条目
- 对于批量访问，COD 在 https://www.crystallography.net/cod/archives/

## 处提供可下载的数据库转储

- COD 包含来自已发表文献的约 500,000 多个晶体结构
- 所有数据均为公共领域/开放许可证下的开放获取
- 搜索API返回元数据；使用 CIF 端点获取完整的结构数据
- 替代访问：MySQL 数据库转储和 SVN 访问可供批量使用
