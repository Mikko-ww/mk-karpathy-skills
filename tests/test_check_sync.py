import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check-sync.py"


def load_check_sync():
    spec = importlib.util.spec_from_file_location("check_sync", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CheckSyncTest(unittest.TestCase):
    def write_file(self, root, relative_path, content):
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_reports_missing_required_snippet(self):
        check_sync = load_check_sync()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(root, "A.md", "编码前先思考\n简洁优先\n")

            problems = check_sync.check_file(root, "A.md", ["编码前先思考", "精准修改"])

        self.assertEqual(problems, ["A.md: missing required text: 精准修改"])

    def test_project_check_passes_when_all_required_snippets_exist(self):
        check_sync = load_check_sync()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative_path, snippets in check_sync.CHECKS.items():
                self.write_file(root, relative_path, "\n".join(snippets))

            problems = check_sync.check_project(root)

        self.assertEqual(problems, [])

    def test_common_snippets_include_detailed_guideline_requirements(self):
        check_sync = load_check_sync()

        required = [
            "不为实际上不可能发生的场景添加错误处理",
            "每一行修改都应该能直接追溯到用户的请求",
            "强成功标准能让 Agent 独立循环执行",
        ]

        for snippet in required:
            self.assertIn(snippet, check_sync.COMMON_SNIPPETS)


if __name__ == "__main__":
    unittest.main()
