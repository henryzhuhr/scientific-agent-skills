# URL 提取

从以下位置提取内容：$ARGUMENTS

## 命令

根据 URL 或内容选择一个简短的描述性文件名（例如，`vespa-docs`、`react-hooks-api`）。使用带连字符的小写字母，无空格。

```bash
parallel-cli extract "$ARGUMENTS" --json -o "$FILENAME.json"
```

如果需要，选项：
- `--objective "focus area"` 专注于特定内容

## 学术内容处理

从学术来源（arXiv、PubMed、期刊网站、会议记录）提取时，使用`--objective` 专注于最有价值的部分：

```bash
parallel-cli extract "$URL" --json --objective "extract abstract, methodology, key findings, and conclusions" -o "$FILENAME.json"
```

 对于 arXiv 论文，首选 `/abs/` URL（具有结构化元数据）而不是原始 PDF URL（如果可用）。如果用户提供 PDF 链接，则直接提取它 —parallel-cli 处理 PDF。

## 响应格式

返回内容为：

* *[页面标题](URL)**

对于学术论文，包括可用的结构化元数据：
- **作者：** 列表作者
- **发布：** 日期和地点/期刊
- **DOI：** 如果可用
- **摘要：** 论文的摘要

然后逐字提取内容，遵循以下规则：
- 逐字保留内容 - 请勿释义或总结
- 彻底解析列表 - 提取每个编号/项目符号项目
- 仅去除明显的噪音：导航菜单、页脚、广告
- 保留所有事实、名称、数字、日期、引号
- 对于学术论文，保留图形/表格标题和参考文献

 响应后，提及输出文件路径 (`$FILENAME.json`)，以便用户知道可用于后续问题。
