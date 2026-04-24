# 受 Karpathy 启发的 Claude Code 指南

> 查看我的新项目 [Multica](https://github.com/multica-ai/multica)：一个用于运行和管理 coding agents 的开源平台，支持可复用 skills。
>
> 在 X 上关注我：[https://x.com/jiayuan_jy](https://x.com/jiayuan_jy)

这个仓库提供一组中文优先的 Agent 行为准则，用来改善 Claude Code、Cursor 和其他 coding agents 的协作质量。内容源自 [Andrej Karpathy 对 LLM 编码陷阱的观察](https://x.com/karpathy/status/2015883857489522876)，重点解决“错误假设、过度复杂、无关改动、缺少验证”这些高频问题。

中文主文档：[`README.md`](./README.md)

当前文件作为中文副本保留，方便旧链接继续访问。

## 问题所在

来自 Andrej 的观察可以概括为三类问题：

> 模型会替你做错误假设，然后一路执行下去。它们不管理自身困惑，不主动澄清，不呈现矛盾，不展示权衡，也不会在应该反驳时反驳。

> 它们很容易把代码和 API 搞复杂，堆砌抽象，不清理死代码。明明 100 行能解决的问题，可能会写成 1000 行的臃肿结构。

> 它们有时会改动或删除自己并不充分理解的代码和注释，即使这些内容与当前任务无关。

## 解决方案

这个仓库把约束收敛成四条原则：

| 原则 | 解决的问题 |
| --- | --- |
| **编码前先思考** | 错误假设、隐藏困惑、缺少权衡 |
| **简洁优先** | 过度复杂、抽象膨胀、提前设计 |
| **精准修改** | 无关编辑、顺手重构、误删代码 |
| **目标驱动执行** | 缺少测试、缺少验证、成功标准模糊 |

## 四条原则

### 1. 编码前先思考

**不要替用户做隐含假设。不要掩盖困惑。要把权衡说出来。**

LLM 经常会默默选择一种解释，然后直接实现。这个原则要求 Agent 在实现前明确说明：

- 当前假设是什么；如果不确定，先问。
- 是否存在多种解释；如果有，列出来。
- 是否有更简单的方案；如果有，说明权衡。
- 哪些地方仍然不清楚；必要时停下来澄清。

### 2. 简洁优先

**用能解决问题的最少代码。不要提前设计未被要求的能力。**

这条原则用来对抗过度工程：

- 不添加要求之外的功能。
- 不为一次性代码创建抽象。
- 不添加未被要求的“灵活性”或“可配置性”。
- 不为实际上不可能发生的场景添加错误处理。
- 如果 200 行可以变成 50 行，就应该简化。

检验标准：资深工程师会不会觉得这个实现过度复杂？如果会，就重写得更简单。

### 3. 精准修改

**只改必须改的地方。只清理由你自己的改动造成的问题。**

编辑现有代码时：

- 不要顺手“改进”相邻代码、注释或格式。
- 不要重构没有坏掉的东西。
- 匹配现有风格，即使你个人更喜欢另一种写法。
- 如果发现无关死代码，可以提出来，但不要删除，除非用户要求。

当你的改动产生孤立代码时：

- 删除因你的改动而变得无用的 import、变量、函数。
- 不删除原本就存在的死代码，除非用户明确要求。

检验标准：每一行修改都应该能直接追溯到用户请求。

### 4. 目标驱动执行

**定义成功标准。循环验证，直到目标被证据证明已经达成。**

把指令式任务改写成可验证目标：

| 不要只说 | 应该转换为 |
| --- | --- |
| “添加校验” | “为无效输入写测试，然后让测试通过” |
| “修复 bug” | “写一个能复现 bug 的测试，然后让它通过” |
| “重构 X” | “确保重构前后测试都通过” |

对于多步骤任务，先写出简短计划：

```text
1. [步骤] -> 验证：[检查方式]
2. [步骤] -> 验证：[检查方式]
3. [步骤] -> 验证：[检查方式]
```

强成功标准能让 Agent 独立循环执行。弱标准，比如“让它能工作”，通常会导致反复澄清和返工。

## 安装

### 选项 A：Claude Code Plugin（推荐）

在 Claude Code 中先添加 marketplace：

```text
/plugin marketplace add Mikko-ww/mk-karpathy-skills
```

然后安装 plugin：

```text
/plugin install mk-karpathy-skills@karpathy-skills
```

这样会把本仓库的 guidelines 作为 Claude Code plugin 安装，并在所有项目中提供对应 skill。

### 选项 B：按项目使用 `CLAUDE.md`

新项目：

```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/Mikko-ww/mk-karpathy-skills/main/CLAUDE.md
```

已有项目，追加到现有 `CLAUDE.md`：

```bash
echo "" >> CLAUDE.md
curl https://raw.githubusercontent.com/Mikko-ww/mk-karpathy-skills/main/CLAUDE.md >> CLAUDE.md
```

## 在 Cursor 中使用

本仓库包含已提交的 Cursor project rule：[`.cursor/rules/karpathy-guidelines.mdc`](.cursor/rules/karpathy-guidelines.mdc)。打开本项目时，该规则会因为 `alwaysApply: true` 自动生效。

更多说明见 [CURSOR.md](CURSOR.md)，包括如何复制到其他项目，以及它与 Claude Code plugin 的关系。

## 核心洞察

来自 Andrej 的核心建议可以概括为：

> 不要只告诉 LLM 做什么；给它明确的成功标准，让它围绕目标循环直到达成。

“目标驱动执行”正是这个思想的落地：把模糊指令转换成带验证循环的目标。

## 如何判断它在生效

如果你看到以下变化，说明这些 guidelines 正在发挥作用：

- **diff 中无关改动更少**：只出现用户请求相关的改动。
- **因过度复杂导致的返工更少**：第一次实现就足够简单。
- **澄清发生在实现前**：不是先猜错，再修正。
- **PR 更小、更干净**：没有顺手重构或无关“改进”。

## 自定义

这些 guidelines 适合与项目自己的规则合并。你可以复制 `CLAUDE.md`，或把其中内容合并到现有项目指令中。

项目特定规则可以像这样追加：

```markdown
## Project-Specific Guidelines

- Use TypeScript strict mode
- All API endpoints must have tests
- Follow the existing error handling patterns in `src/utils/errors.ts`
```

## 权衡说明

这些 guidelines 偏向**谨慎而不是速度**。对于简单拼写修复、明显的一行修改等琐碎任务，不需要完整流程。

目标不是拖慢简单工作，而是减少非琐碎任务中代价高昂的错误。

## License

MIT
