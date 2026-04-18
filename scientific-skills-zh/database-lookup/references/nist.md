# NIST Data APIs

## 概述

NIST 提供多种科学数据库。 REST API 可用性因数据集而异。

## 1. NIST CODATA 基本物理常量

### 基本 URL
```
https://physics.nist.gov/cgi-bin/cuu
```

* *没有正式的 REST API。** 数据通过返回 HTML 的 CGI 脚本提供。可以通过结构化 URL 以编程方式访问常量，但响应是 HTML，而不是 JSON/XML。

* *解决方法 - 机器可读的 ASCII：**
```
https://physics.nist.gov/cuu/Constants/Table/allascii.txt
```
 返回所有基本常量的制表符分隔文本文件，其中包含值、不确定性和单位。

* *单个常量查找：**
```
https://physics.nist.gov/cgi-bin/cuu/Value?{constant_key}
```
示例键：`bohrrada0`（玻尔半径）、`c`（光速）、`h`（普朗克常数）、`e`（电子电荷）、`me`（电子质量）、`na`（阿伏加德罗）数），`k`（玻尔兹曼常数）。

示例：
```
https://physics.nist.gov/cgi-bin/cuu/Value?h
```
返回 HTML 页面。从页面内容中解析值。

* *不需要 API 密钥。没有记录速率限制。**

## 2. NIST 原子光谱数据库 (ASD)

### 基本 URL
```
https://physics.nist.gov/cgi-bin/ASD
```

* *没有正式的 REST API。** 查询基于 CGI，返回 HTML。但是，可以通过特定参数获得机器可读的输出。

* *谱线查询：**
```
https://physics.nist.gov/cgi-bin/ASD/lines1.pl?spectra={element}&low_w={min_wavelength}&upp_w={max_wavelength}&unit={unit}&format={format}
```

|参数|类型 |描述|
|------------|--------|-------------|
| `spectra` |字符串|元素符号或离子（例如，`H`、`Fe`、`He+I`、`O+II`）。 |
| `low_w` |浮动|较低的波长范围。 |
| `upp_w` |浮动|波长上限。 |
| `unit` |整数 | `0` = 埃，`1` = nm，`2` = um。 |
| `format` |整数 | `0` = HTML、`1` = ASCII、`2` = CSV、`3` = 制表符分隔。 |
| `line_out` |整数 | `0` = 全部，`1` = 仅观察到，`2` = 仅Ritz。 |
| `show_obs_wl` |整数 | `1` = 显示观察到的波长。 |
| `show_calc_wl` |整数 | `1` = 显示里兹波长。 |
| `A_out` |整数 | `1` = 包括转移概率。 |

* *示例 — 氢气线 3000-7000 埃（CSV 格式）：**
```
https://physics.nist.gov/cgi-bin/ASD/lines1.pl?spectra=H&low_w=3000&upp_w=7000&unit=0&format=2&line_out=0&show_obs_wl=1&A_out=1
```

* *能量水平查询：**
```
https://physics.nist.gov/cgi-bin/ASD/energy1.pl?spectra={element}&units={units}&format={format}
```

* *无需 API 密钥。没有正式的速率限制，但不鼓励自动批量查询。**

## 3. NIST Chemistry WebBook

### 基本 URL
```
https://webbook.nist.gov/cgi/cbook.cgi
```

* *没有正式的 REST API。** 基于 CGI，带有 HTML 输出。可以使用结构化URL。

* *按名称搜索：**
```
https://webbook.nist.gov/cgi/cbook.cgi?Name={compound}&Units=SI
```

* *按CAS号搜索：**
```
https://webbook.nist.gov/cgi/cbook.cgi?ID={cas_number}&Units=SI
```

* *搜索公式：**
```
https://webbook.nist.gov/cgi/cbook.cgi?Formula={formula}&Units=SI
```

* *JCAMP-DX 谱（机器可读）：**
```
https://webbook.nist.gov/cgi/cbook.cgi?ID={cas_number}&Type=IR-Spec&Index=0&JCAMP=C{cas_no_dashes}
```

## 摘要

NIST 数据库通常**不**提供现代 REST/JSON API。数据访问主要通过 CGI 端点返回 HTML 或分隔文本。对于编程使用，ASD 的 ASCII/CSV 输出选项是最实用的。任何 NIST 端点都不需要身份验证。
