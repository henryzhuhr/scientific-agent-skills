---
name: paperzilla
description: 在 Paperzilla 中与您的代理讨论项目、建议和规范论文。当用户询问最近的项目推荐、规范论文详细信息、基于 Markdown 的摘要、推荐反馈、提要导出或 Atom 提要 URL 时使用。
license: MIT
metadata:
  skill-author: "Paperzilla Inc"
---

# Paperzilla

当您想与代理讨论 Paperzilla 中的项目、建议和规范论文时，请使用此技能。

## 您可以问什么

- “给我项目 X 的最新建议。”
- “打开建议 Y 并解释为什么它很重要。”
- “以 Markdown 形式获取规范论文 Z 并对其进行总结。”
- “告诉我这篇论文与我的研究有何相关性。”
- “向我显示项目 X 的提要。”
- “对推荐留下反馈。”
- “将这篇论文、推荐或提要导出为 JSON。”

 这是核心Paperzilla 技能。它使您的代理可以直接访问 Paperzilla 数据，但不会强加工作流程或外部交付集成。

## 访问方法

此存储库中的大多数当前配置文件使用 `pz` CLI。

如果当前配置文件附带额外的代理特定说明，也请遵循这些说明。

## 安装

### macOS
```bash
brew install paperzilla-ai/tap/pz
```

### Windows (Scoop)
```bash
scoop bucket add paperzilla-ai https://github.com/paperzilla-ai/scoop-bucket
scoop install pz
```

### Linux
使用官方Linux安装指南：

- https://docs.paperzilla.ai/guides/cli-getting-started

### 从源代码构建（Go 1.23+）
查看源代码构建的 CLI 存储库：

- https://github.com/paperzilla-ai/pz

## Update

检查您的 CLI 是否达到日期并获取特定于安装的升级步骤：

```bash
pz update
```

如果检测不明确，请显式覆盖它：

```bash
pz update --install-method homebrew
pz update --install-method scoop
pz update --install-method release
pz update --install-method source
```

支持的值为 `auto`、`homebrew`、`scoop`、 `release` 和 `source`.

## 身份验证

```bash
pz login
```

## CLI 参考

如果当前配置文件使用 `pz`，则这些是核心命令。

### 列表项目
```bash
pz project list
```

### 显示一个项目
```bash
pz project <project-id>
```

### 浏览项目源
```bash
pz feed <project-id>
```

有用的标志：
- `--must-read`
- `--since YYYY-MM-DD`
- `--limit N`
- `--json`
- `--atom`

示例：
```bash
pz feed <project-id> --must-read --since 2026-03-01 --limit 5
pz feed <project-id> --json
pz feed <project-id> --atom
```

Feed 输出可以包括现有推荐反馈标记：

- `[↑]` upvote
- `[↓]` downvote
- `[★]` star

### 阅读规范paper
```bash
pz paper <paper-id>
pz paper <paper-id> --json
pz paper <paper-id> --markdown
pz paper <paper-id> --project <project-id>
```

### 从您的一个项目中打开推荐
```bash
pz rec <project-paper-id>
pz rec <project-paper-id> --json
pz rec <project-paper-id> --markdown
```

### 留下推荐反馈
```bash
pz feedback <project-paper-id> upvote
pz feedback <project-paper-id> star
pz feedback <project-paper-id> downvote --reason not_relevant
pz feedback clear <project-paper-id>
```

## 输出和自动化

- 优先`--json` 用于机器解析。
- `pz paper --markdown` 仅在已准备好时返回 markdown。
- `pz rec --markdown` 可以对 Markdown 生成进行排队，并在仍在准备时打印友好的重试消息。
- `--atom` 返回 feed 的个人 feed URL reader.

## 配置

```bash
export PZ_API_URL="https://paperzilla.ai"
```

## 参考资料

- 文档：https://docs.paperzilla.ai/guides/cli
- 快速入门： https://docs.paperzilla.ai/guides/cli-getting-started
- 仓库：https://github.com/paperzilla-ai/pz
