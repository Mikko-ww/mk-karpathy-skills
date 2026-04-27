#!/usr/bin/env python3
"""检查多份 agent 指令文件是否与核心准则保持同步。"""

from pathlib import Path
import sys


COMMON_SNIPPETS = [
    "编码前先思考",
    "简洁优先",
    "精准修改",
    "目标驱动执行",
    "Superpowers 负责流程门禁",
    "不要用“简洁优先”跳过 Superpowers",
    "不要替用户做隐含假设",
    "如果存在多种解释",
    "不为实际上不可能发生的场景添加错误处理",
    "不为一次性代码创建抽象",
    "不要顺手“改进”相邻代码、注释或格式",
    "不删除原本就存在的死代码",
    "每一行修改都应该能直接追溯到用户的请求",
    "定义成功标准",
    "强成功标准能让 Agent 独立循环执行",
]

CHECKS = {
    "skills/karpathy-guidelines/SKILL.md": COMMON_SNIPPETS,
    "CLAUDE.md": COMMON_SNIPPETS,
    "AGENTS.md": COMMON_SNIPPETS,
    "GEMINI.md": COMMON_SNIPPETS,
    ".cursor/rules/karpathy-guidelines.mdc": COMMON_SNIPPETS,
    ".github/copilot-instructions.md": COMMON_SNIPPETS,
    "README.md": COMMON_SNIPPETS + ["适配文件维护规则"],
    "CONTRIBUTING.md": [
        "适配文件同步",
        "scripts/check-sync.py",
        "skills/karpathy-guidelines/SKILL.md",
        ".github/copilot-instructions.md",
    ],
}


def check_file(root, relative_path, snippets):
    path = root / relative_path
    if not path.exists():
        return [f"{relative_path}: file does not exist"]

    text = path.read_text(encoding="utf-8")
    return [
        f"{relative_path}: missing required text: {snippet}"
        for snippet in snippets
        if snippet not in text
    ]


def check_project(root):
    problems = []
    for relative_path, snippets in CHECKS.items():
        problems.extend(check_file(root, relative_path, snippets))
    return problems


def main():
    root = Path(__file__).resolve().parents[1]
    problems = check_project(root)
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1

    print("Agent instruction files are in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
