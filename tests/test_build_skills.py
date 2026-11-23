"""Tests for scripts/build_skills.py."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_skills  # noqa: E402


VALID_SKILL_BODY = """# Demo Skill

## Purpose

Test canonical skill body.
"""


def create_repo_fixture(root: Path) -> None:
    """Create a minimal repository structure for build_skills tests."""
    for rel in (
        "skills/adapters/chrome-gemini",
        "skills/adapters/claude",
        "skills/adapters/antigravity",
        "skills/adapters/local-llm",
        "skills/migration",
        "skills/_template",
        "skills/antigravity",
        "skills/chrome-gemini",
        "skills/claude",
        "skills/local-llm",
        "research",
        "sources",
        "docs",
        "dist",
    ):
        (root / rel).mkdir(parents=True, exist_ok=True)
    (root / "dist" / ".gitkeep").write_text("", encoding="utf-8")
    (root / "docs" / "notes.md").write_text("# Notes\n", encoding="utf-8")


def write_skill(
    root: Path,
    name: str = "demo-skill",
    frontmatter_overrides: dict[str, str] | None = None,
    body: str = VALID_SKILL_BODY,
) -> Path:
    """Write a canonical SKILL.md under root/skills/<name>/SKILL.md."""
    fields = {
        "name": name,
        "description": ">-\n  Use when testing folded YAML descriptions across\n  multiple lines.",
        "version": "0.1.0",
        "status": "draft",
        "owner": "Test Owner",
        "source_of_truth": f"skills/{name}/SKILL.md",
        "platforms": "\n  - chrome-gemini\n  - claude",
        "evidence": "\n  - path: research/\n  - path: sources/",
    }
    if frontmatter_overrides:
        for key, value in frontmatter_overrides.items():
            if value is None:
                fields.pop(key, None)
            else:
                fields[key] = value

    fm_lines = ["---"]
    for key, value in fields.items():
        if value.startswith("\n"):
            fm_lines.append(f"{key}:{value}")
        else:
            fm_lines.append(f"{key}: {value}")
    fm_lines.append("---")

    skill_dir = root / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text("\n".join(fm_lines) + "\n\n" + body, encoding="utf-8")
    return skill_file


class BuildSkillsTests(unittest.TestCase):
    def test_template_metadata_validates_cleanly(self) -> None:
        template_file = REPO_ROOT / "skills" / "_template" / "SKILL.md"
        raw_meta, body = build_skills.parse_frontmatter(template_file.read_text(encoding="utf-8"))
        validated = build_skills.validate_metadata(raw_meta, "example-skill-name", REPO_ROOT, template_file)
        self.assertEqual(validated["name"], "example-skill-name")
        self.assertIn("Use when the user needs to", validated["description"])
        self.assertTrue(body.strip())

    def test_folded_yaml_description_parsed_and_length_checked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_repo_fixture(root)
            write_skill(root)

            index = build_skills.build(root, root / "dist")
            self.assertEqual(len(index), 1)
            self.assertEqual(
                index[0]["description"],
                "Use when testing folded YAML descriptions across multiple lines.",
            )

            long_desc = ">-\n  " + ("word " * 250)
            write_skill(root, frontmatter_overrides={"description": long_desc})
            with self.assertRaisesRegex(ValueError, "1,024"):
                build_skills.build(root, root / "dist")

    def test_missing_or_invalid_required_metadata_rejected(self) -> None:
        cases = [
            ({"version": None}, "version"),
            ({"version": "invalid"}, "semantic version"),
            ({"status": "published"}, "Invalid status"),
            ({"owner": None}, "owner"),
            ({"source_of_truth": "skills/other/SKILL.md"}, "source_of_truth"),
            ({"platforms": "\n  - unknown-platform"}, "Unsupported platform"),
            ({"evidence": "\n  - path: missing-dir/"}, "does not exist"),
        ]
        for overrides, pattern in cases:
            with self.subTest(pattern=pattern), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                create_repo_fixture(root)
                write_skill(root, frontmatter_overrides=overrides)
                with self.assertRaisesRegex(ValueError, pattern):
                    build_skills.build(root, root / "dist")

    def test_unsafe_dist_root_rejected_and_gitkeep_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_repo_fixture(root)
            write_skill(root)

            unsafe_targets = [
                root,
                root.parent,
                root / "skills",
                root / "skills" / "demo-skill",
                root / "docs",
            ]
            for target in unsafe_targets:
                with self.subTest(target=target):
                    with self.assertRaisesRegex(ValueError, "Refusing"):
                        build_skills.build(root, target)
                    self.assertTrue((root / "docs" / "notes.md").exists())
                    self.assertTrue((root / "skills" / "demo-skill" / "SKILL.md").exists())

            build_skills.build(root, root / "dist")
            self.assertTrue((root / "dist" / ".gitkeep").exists())
            self.assertTrue((root / "dist" / "index.json").exists())

    def test_chrome_gemini_adapter_composed_and_validated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_repo_fixture(root)
            write_skill(root)
            adapter_file = root / "skills" / "adapters" / "chrome-gemini" / "demo-skill.md"
            adapter_file.write_text("## Chrome constraints\n\nKeep output under 150 words.\n", encoding="utf-8")

            index = build_skills.build(root, root / "dist")
            chrome_out = (root / "dist" / "chrome-gemini" / "demo-skill.txt").read_text(encoding="utf-8")
            self.assertIn("Test canonical skill body.", chrome_out)
            self.assertIn("## Chrome constraints", chrome_out)
            self.assertIn("Keep output under 150 words.", chrome_out)
            self.assertFalse(chrome_out.startswith("---"))
            self.assertEqual(
                index[0]["adapters"],
                {"chrome-gemini": "skills/adapters/chrome-gemini/demo-skill.md"},
            )

            adapter_file.write_text("---\nname: bad\n---\n\nBody\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must not contain YAML frontmatter"):
                build_skills.build(root, root / "dist")

    def test_chrome_gemini_export_skipped_when_platform_not_declared(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_repo_fixture(root)
            write_skill(root, frontmatter_overrides={"platforms": "\n  - claude"})

            index = build_skills.build(root, root / "dist")
            self.assertIsNone(index[0]["chrome_gemini_path"])
            self.assertFalse((root / "dist" / "chrome-gemini" / "demo-skill.txt").exists())

    def test_undeclared_adapter_and_missing_skill_md_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_repo_fixture(root)
            write_skill(root, frontmatter_overrides={"platforms": "\n  - claude"})
            (root / "skills" / "adapters" / "chrome-gemini" / "demo-skill.md").write_text(
                "Chrome note\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "undeclared platform"):
                build_skills.build(root, root / "dist")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_repo_fixture(root)
            (root / "skills" / "incomplete-skill").mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, "Missing SKILL.md"):
                build_skills.build(root, root / "dist")

    def test_reproducible_zip_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_repo_fixture(root)
            write_skill(root)

            build_skills.build(root, root / "dist")
            first_bytes = (root / "dist" / "bundles" / "demo-skill.zip").read_bytes()
            first_index = json.loads((root / "dist" / "index.json").read_text(encoding="utf-8"))

            build_skills.build(root, root / "dist")
            second_bytes = (root / "dist" / "bundles" / "demo-skill.zip").read_bytes()
            second_index = json.loads((root / "dist" / "index.json").read_text(encoding="utf-8"))

            self.assertEqual(first_bytes, second_bytes)
            self.assertEqual(first_index, second_index)


if __name__ == "__main__":
    unittest.main()
