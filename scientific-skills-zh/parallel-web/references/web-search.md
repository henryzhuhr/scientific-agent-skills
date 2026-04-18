# 网页搜索

在网页上搜索：$ARGUMENTS

## 命令

根据查询选择一个简短的描述性文件名（例如，`ai-chip-news`、`react-vs-vue`）。使用带连字符的小写字母，无空格。

```bash
parallel-cli search "$ARGUMENTS" -q "<keyword1>" -q "<keyword2>" --json --max-results 10 --excerpt-max-chars-total 27000 -o "$FILENAME.json"
```

第一个参数是 **目标** - 您要查找的内容的自然语言描述。它用一次广泛或复杂的查询调用取代了多个关键字搜索。为特定关键字查询添加 `-q` 标志以补充目标。 `-o` 标志将完整结果保存到 JSON 文件以供后续问题使用。

 需要时可选项：
- `--after-date YYYY-MM-DD` 用于时间敏感查询
- `--include-domains domain1.com,domain2.com` 用于限制特定来源

## 学术来源策略

对于科学或技术查询，运行**两次搜索**确保学术来源与一般结果一起出现：

1. **以学术为中心的搜索** — 附加 `--include-domains` 与学术领域：
 ```bash
 并行 cli 搜索 "$ARGUMENTS" -q "<keyword1>" --json --max-results 10 --excerpt-max-chars-total 27000 --include-domains “scholar.google.com、arxiv.org、pubmed.ncbi.nlm.nih.gov、semanticscholar.org、biorxiv.org、medrxiv.org、ncbi.nlm.nih.gov、nature.com、science.org、ieee.org、acm.org、springer.com、wiley.com、cell.com、pnas.org、nih.gov”-o “$FILENAME-academic.json”
``

2. **通用搜索** — 无域限制的标准命令，捕获相关的非学术来源。

合并结果，以学术来源领先。如果只有一种搜索是实用的（例如，明显非科学查询），请跳过以学术为中心的搜索。

* *何时使用两种搜索模式：**涉及科学主张、医学信息、研究结果、技术机制、统计数据或任何主要文献比二次报告更可靠的查询。

## 解析结果

在命令执行时不要设置`max_output_tokens` - 输出已经受到`--max-results`和`--excerpt-max-chars-total`的限制。限制输出标记将截断 JSON 并中断解析。

从 stdout 解析 JSON。对于每个结果，提取：
- 标题、网址、发布日期
- 摘录中的有用内容（跳过菜单、页脚、“跳到内容”等导航噪音）

## 响应格式

* *关键：每个声明必须有内联引用。**使用仅从JSON输出中提取的markdown链接。切勿发明或猜测 URL。

对于学术来源，请在元数据可用的情况下使用作者年份引用风格：
- 学术：[Smith et al., 2025](url)或 [Smith & Jones, 2024](url)
- 非学术：[来源标题](url)

合成响应
- 以同行评审或预印本来源的发现为线索（如果有）
- 清楚地区分主要研究支持的主张与二次报告
- 包括具体事实、名称、数字、日期
- 引用内联的每个事实 - 不要留下任何未引用的主张
- 如果多个，则按主题组织主题
- 注释证据质量（例如，“发现的随机对照试验......”与“博客文章报告......”）

* *以来源部分结尾**列出引用的每个URL，按类型分组：

```
Sources:

Academic / Peer-reviewed:
- [Smith et al., 2025 — Title of Paper](https://doi.org/...) (Nature, 2025)
- [Jones & Lee, 2024 — Title of Paper](https://arxiv.org/...) (arXiv preprint)

Other:
- [Source Title](https://example.com/article) (Feb 2026)
```

此来源部分是强制性的。不要省略它。如果未找到学术来源，请注意并解释原因（例如，该主题太新、尚未研究或本质上非学术性）。

在来源部分之后，提及输​​出文件路径 (`$FILENAME.json`)，以便用户知道它可用于后续问题。
