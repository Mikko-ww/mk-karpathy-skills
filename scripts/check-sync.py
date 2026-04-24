#!/usr/bin/env python3
"""Check that agent instruction files keep the core guidelines in sync."""

from pathlib import Path
import sys


COMMON_SNIPPETS = [
    "编码前先思考",
    "简洁优先",
    "精准修改",
    "目标驱动执行",
    "Superpowers 负责流程门禁",
    "不要用“简洁优先”跳过 Superpowers",
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
