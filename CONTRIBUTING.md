# 贡献指南

这个仓库维护的是一套中文优先的 Agent 行为准则。改动应保持简单、精准，并优先维护各平台入口之间的一致性。

## 适配文件同步

修改四条原则、Superpowers 边界说明或中文交互要求时，请同步检查这些文件：

- `skills/karpathy-guidelines/SKILL.md`
- `CLAUDE.md`
- `AGENTS.md`
- `GEMINI.md`
- `.cursor/rules/karpathy-guidelines.mdc`
- `.github/copilot-instructions.md`
- `README.md`

改动后运行：

```bash
python scripts/check-sync.py
python -m unittest tests/test_check_sync.py
```

`scripts/check-sync.py` 只做关键片段检查，不替代人工 review。提交前仍然需要确认每个平台入口的语气、格式和用途是否合适。

## 修改原则

- 保留代码、命令、路径、变量名、API 名称和必要英文技术术语。
- 不新增没有明确用途的平台入口。
- 不把某个平台的特殊格式强行复制到其他平台。
- 如果新增适配入口，请同步更新 `README.md` 的适配矩阵和本文件的同步清单。
