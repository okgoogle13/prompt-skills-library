#!/usr/bin/env python3
"""Build portable exports from canonical Agent Skills.

Reads skills/*/SKILL.md, validates basic metadata, and writes:

- dist/skills/<skill-name>/SKILL.md
- dist/chrome-gemini/<skill-name>.txt
- dist/bundles/<skill-name>.zip
- dist/index.json
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("Missing YAML frontmatter")

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'\"")

    return metadata, text[match.end():].lstrip()


def build(repo_root: Path, dist_root: Path) -> list[dict[str, object]]:
    skills_root = repo_root / "skills"
    dist_root.mkdir(parents=True, exist_ok=True)

    if dist_root.exists():
        shutil.rmtree(dist_root)

    (dist_root / "skills").mkdir(parents=True)
    (dist_root / "chrome-gemini").mkdir(parents=True)
    (dist_root / "bundles").mkdir(parents=True)

    index: list[dict[str, object]] = []

    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        if skill_dir.name in {"adapters", "migration", "_template"}:
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        text = skill_file.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(text)
        name = metadata.get("name", "")
        description = metadata.get("description", "")

        if not name:
            raise ValueError(f"Missing name: {skill_file}")
        if name != skill_dir.name:
            raise ValueError(f"Name/folder mismatch: {name} != {skill_dir.name}")
        if not description:
            raise ValueError(f"Missing description: {skill_file}")
        if len(description) > 1024:
            raise ValueError(f"Description exceeds 1,024 characters: {skill_file}")

        output_dir = dist_root / "skills" / name
        shutil.copytree(skill_dir, output_dir, dirs_exist_ok=True)

        chrome_path = dist_root / "chrome-gemini" / f"{name}.txt"
        chrome_path.write_text(body, encoding="utf-8")

        bundle_path = dist_root / "bundles" / f"{name}.zip"
        with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as bundle:
            for file_path in sorted(output_dir.rglob("*")):
                if file_path.is_file():
                    bundle.write(file_path, file_path.relative_to(output_dir))

        index.append(
            {
                "name": name,
                "description": description,
                "canonical_path": str(skill_file.relative_to(repo_root)),
                "bundle_path": str(bundle_path.relative_to(dist_root)),
                "chrome_gemini_path": str(chrome_path.relative_to(dist_root)),
                "version": metadata.get("version", ""),
                "status": metadata.get("status", ""),
            }
        )

    index_path = dist_root / "index.json"
    index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--dist-root", type=Path, default=None)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    dist_root = (args.dist_root or repo_root / "dist").resolve()
    skills = build(repo_root, dist_root)
    print(f"Built {len(skills)} canonical skill exports in {dist_root}")


if __name__ == "__main__":
    main()
