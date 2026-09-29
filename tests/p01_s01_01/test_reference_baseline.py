# -*- coding: utf-8 -*-
"""P01-S01-01 建立参考项目基线：验收测试。

断言来源：openspec/changes/2026-09-29-01-establish-reference-project-baseline
- specs/reference-project-baseline/spec.md
- docs/projects/P01-ai-image-mini-saas/phases/P01-S01-参考项目运行与实验/P01-S01-01_建立参考项目基线.md

运行方式：python3 -m unittest tests.p01_s01_01.test_reference_baseline -v
"""

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REF_DIR = REPO_ROOT / "references" / "p01-backblaze-ai-saas-starter-kit"
REPORT = REPO_ROOT / "progress" / "p01" / "reference_baseline.md"
EXPECTED_REMOTE = "github.com/backblaze-labs/ai-saas-starter-kit"


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(REF_DIR), *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} 失败: {result.stderr.strip()}")
    return result.stdout.strip()


def read_report() -> str:
    if not REPORT.is_file():
        raise AssertionError(f"基线报告不存在: {REPORT}")
    return REPORT.read_text(encoding="utf-8")


class TestReferenceRepoIdentity(unittest.TestCase):
    """Requirement: 参考仓库身份必须可追溯。"""

    def test_reference_dir_is_git_repo(self):
        self.assertTrue(REF_DIR.is_dir(), f"参考目录不存在: {REF_DIR}")
        self.assertTrue((REF_DIR / ".git").exists(), "参考目录不是 Git 仓库")

    def test_remote_url_matches_confirmed_upstream(self):
        remote = git("config", "--get", "remote.origin.url")
        self.assertIn(EXPECTED_REMOTE, remote)

    def test_report_records_full_commit_sha_of_head(self):
        sha = git("rev-parse", "HEAD")
        self.assertRegex(sha, r"^[0-9a-f]{40}$")
        self.assertIn(sha, read_report())

    def test_report_records_default_branch(self):
        ref = git("symbolic-ref", "refs/remotes/origin/HEAD")
        branch = ref.rsplit("/", 1)[-1]
        self.assertIn(branch, read_report())

    def test_report_records_license_with_evidence_file(self):
        self.assertTrue(REF_DIR.is_dir(), f"参考目录不存在: {REF_DIR}")
        candidates = [
            p.name
            for p in REF_DIR.iterdir()
            if p.is_file() and re.match(r"(?i)^(licen[cs]e|copying)", p.name)
        ]
        self.assertTrue(candidates, "参考仓库根目录没有 License 文件")
        report = read_report()
        self.assertTrue(
            any(name in report for name in candidates),
            f"报告未引用 License 证据文件: {candidates}",
        )


class TestWorkspaceClean(unittest.TestCase):
    """Requirement: 初始工作区状态必须保持可核验。"""

    def test_reference_repo_clean_at_end(self):
        status = git("status", "--porcelain")
        self.assertEqual(status, "", f"参考仓库结束时存在改动:\n{status}")


class TestReportCoverage(unittest.TestCase):
    """Requirement: 基线报告必须支持后续需求接续。"""

    REQUIRED_SECTIONS = [
        "来源与版本",
        "License",
        "目录和主要模块",
        "启动组件与命令",
        "环境变量分类",
        "外部服务",
        "运行条件",
        "初始 Git 状态",
        "结束",
        "待决事项",
    ]

    def test_report_covers_required_sections(self):
        report = read_report()
        missing = [s for s in self.REQUIRED_SECTIONS if s not in report]
        self.assertEqual(missing, [], f"报告缺少必需章节: {missing}")

    def test_report_uses_explicit_status_labels(self):
        report = read_report()
        for label in ["已验证", "未验证", "阻塞", "待用户决定"]:
            self.assertIn(label, report, f"报告缺少状态标签: {label}")


class TestNoSecrets(unittest.TestCase):
    """Requirement: 环境变量与外部服务必须安全分类，报告不得含真实 Secret。"""

    SECRET_PATTERNS = [
        r"sk-[A-Za-z0-9_-]{20,}",
        r"sk-ant-[A-Za-z0-9_-]{10,}",
        r"sk_live_[A-Za-z0-9]{10,}",
        r"rk_live_[A-Za-z0-9]{10,}",
        r"ghp_[A-Za-z0-9]{20,}",
        r"github_pat_[A-Za-z0-9_]{20,}",
        r"AKIA[0-9A-Z]{16}",
        r"xox[baprs]-[A-Za-z0-9-]{10,}",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    ]

    SENSITIVE_ASSIGNMENT = re.compile(
        r"(?im)^\s*[A-Z][A-Z0-9_]*(KEY|TOKEN|SECRET|PASSWORD|DSN|URL)\s*=\s*(\S+)\s*$"
    )
    PLACEHOLDER = re.compile(r"^(<|\.\.\.|xxx|your[-_]|changeme|placeholder)", re.I)

    def test_report_has_no_secret_token_patterns(self):
        report = read_report()
        for pattern in self.SECRET_PATTERNS:
            self.assertIsNone(
                re.search(pattern, report), f"报告疑似包含真实 Secret: {pattern}"
            )

    def test_report_has_no_sensitive_assignments_with_values(self):
        report = read_report()
        for match in self.SENSITIVE_ASSIGNMENT.finditer(report):
            value = match.group(2)
            if not self.PLACEHOLDER.match(value):
                self.fail(f"报告疑似包含敏感赋值: {match.group(0)}")


if __name__ == "__main__":
    unittest.main()
