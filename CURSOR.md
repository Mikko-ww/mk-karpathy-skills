# 在 Cursor 中使用本仓库

本项目包含一个 **Cursor project rule**，用于让这套 Karpathy-inspired 行为准则在 Cursor 中自动生效。

## 在本仓库中使用

1. 用 Cursor 打开本项目目录。
2. 仓库已提交 [`.cursor/rules/karpathy-guidelines.mdc`](.cursor/rules/karpathy-guidelines.mdc)。
3. 该 rule 设置了 `alwaysApply: true`，因此不需要额外安装步骤。
4. 你可以在 Cursor 的 **Settings -> Rules** 或 project rules UI 中确认 `karpathy-guidelines` 是否出现。

## 在其他项目中使用同一套准则

**Cursor（推荐）：** 把 `.cursor/rules/karpathy-guidelines.mdc` 复制到目标项目的 `.cursor/rules/` 目录中；如果目录不存在，先创建。之后可按目标项目需要继续合并或调整。

**其他工具：** 如果工具只支持根目录指令文件，可以复制 [`CLAUDE.md`](CLAUDE.md)，或把其中内容合并进已有指令文件。

## 可选：个人 Agent Skills

如果你希望以个人 skill 的形式复用这套内容，可以使用 [`skills/karpathy-guidelines/SKILL.md`](skills/karpathy-guidelines/SKILL.md)。按你使用的 Agent 环境，把它复制或软链接到对应的个人 skills 目录中。

## Claude Code 与 Cursor 的区别

- **Claude Code：** 按 [`README.md`](README.md) 中的 plugin marketplace 方式安装；plugin 会暴露本仓库的 skill。按项目使用时，也可以依赖 `CLAUDE.md`。
- **Cursor：** 使用已提交的 `.cursor/rules/` 文件。Cursor 默认不会读取 `.claude-plugin/` 或 `CLAUDE.md`。

## 贡献者注意事项

修改四条原则时，请保持以下文件同步：

- [`CLAUDE.md`](CLAUDE.md)
- [`.cursor/rules/karpathy-guidelines.mdc`](.cursor/rules/karpathy-guidelines.mdc)
- [`skills/karpathy-guidelines/SKILL.md`](skills/karpathy-guidelines/SKILL.md)

如果用户文档也需要同步，请同时更新 [`README.md`](README.md)、[`README.zh.md`](README.zh.md) 和 [`EXAMPLES.md`](EXAMPLES.md)。
