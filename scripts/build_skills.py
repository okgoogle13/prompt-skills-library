#!/usr/bin/env python3
"""Build portable exports from canonical Agent Skills.

Reads skills/<skill-name>/SKILL.md, validates the canonical metadata contract
and platform adapters, and writes:

- dist/skills/<skill-name>/SKILL.md
- dist/chrome-gemini/<skill-name>.txt
- dist/bundles/<skill-name>.zip
- dist/index.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import zipfile
from pathlib import Path
from typing import Any

import yaml

SUPPORTED_PLATFORMS = ("chrome-gemini", "claude", "antigravity", "local-llm")
VALID_STATUSES = {"draft", "approved", "deprecated"}
NON_SKILL_DIRS = {"adapters", "migration", "_template"}
LEGACY_PLATFORM_DIRS = set(SUPPORTED_PLATFORMS)
SKIP_SKILL_DIRS = NON_SKILL_DIRS | LEGACY_PLATFORM_DIRS
MANAGED_DIST_ENTRIES = {".gitkeep", "skills", "chrome-gemini", "bundles", "index.json"}

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.DOTALL)
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^v?\d+\.\d+(?:\.\d+)?$")
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter and return (metadata, markdown_body)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("Missing YAML frontmatter")

    try:
        parsed = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML frontmatter: {exc}") from exc

    if not isinstance(parsed, dict) or not all(isinstance(k, str) for k in parsed):
        raise ValueError("YAML frontmatter must be a mapping with string keys")

    body = text[match.end():].lstrip()
    return parsed, body


def _require_non_empty_str(metadata: dict[str, Any], key: str, skill_file: Path) -> str:
    """Return a stripped non-empty string field or raise ValueError."""
    value = metadata.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing or invalid '{key}': {skill_file}")
    return value.strip()


def _resolve_repo_path(repo_root: Path, raw_path: str, label: str, skill_file: Path) -> Path:
    """Resolve a repo-relative path and ensure it stays within repo_root."""
    candidate = Path(raw_path)
    if candidate.is_absolute():
        raise ValueError(f"{label} must be repo-relative, got '{raw_path}': {skill_file}")

    resolved = (repo_root / candidate).resolve()
    if not resolved.is_relative_to(repo_root):
        raise ValueError(f"{label} escapes repository root '{raw_path}': {skill_file}")
    return resolved


def validate_evidence(raw_evidence: Any, repo_root: Path, skill_file: Path) -> list[dict[str, str]]:
    """Validate required evidence entries and verify local paths exist."""
    if not isinstance(raw_evidence, list) or not raw_evidence:
        raise ValueError(f"Missing or empty 'evidence' list: {skill_file}")

    validated: list[dict[str, str]] = []
    for idx, entry in enumerate(raw_evidence):
        if not isinstance(entry, dict):
            raise ValueError(f"Evidence entry #{idx + 1} must be a mapping: {skill_file}")

        path_val = entry.get("path")
        url_val = entry.get("url")
        if path_val is None and url_val is None:
            raise ValueError(f"Evidence entry #{idx + 1} requires 'path' or 'url': {skill_file}")

        item: dict[str, str] = {}
        if path_val is not None:
            if not isinstance(path_val, str) or not path_val.strip():
                raise ValueError(f"Evidence entry #{idx + 1} has invalid 'path': {skill_file}")
            resolved = _resolve_repo_path(repo_root, path_val.strip(), "Evidence path", skill_file)
            if not resolved.exists():
                raise ValueError(f"Evidence path does not exist '{path_val}': {skill_file}")
            item["path"] = path_val.strip()

        if url_val is not None:
            if not isinstance(url_val, str) or not url_val.strip().startswith(("http://", "https://")):
                raise ValueError(f"Evidence entry #{idx + 1} has invalid 'url': {skill_file}")
            item["url"] = url_val.strip()

        validated.append(item)
    return validated


def validate_metadata(
    metadata: dict[str, Any],
    expected_name: str,
    repo_root: Path,
    skill_file: Path,
) -> dict[str, Any]:
    """Validate the complete canonical skill metadata contract."""
    name = _require_non_empty_str(metadata, "name", skill_file)
    if name != expected_name:
        raise ValueError(f"Name/folder mismatch: {name} != {expected_name} ({skill_file})")
    if not SKILL_NAME_RE.match(name) or len(name) > 64:
        raise ValueError(f"Invalid skill name '{name}': {skill_file}")

    description = _require_non_empty_str(metadata, "description", skill_file)
    if len(description) > 1024:
        raise ValueError(f"Description exceeds 1,024 characters: {skill_file}")

    version = _require_non_empty_str(metadata, "version", skill_file)
    if not VERSION_RE.match(version):
        raise ValueError(f"Invalid semantic version '{version}': {skill_file}")

    status = _require_non_empty_str(metadata, "status", skill_file)
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}' (expected one of {sorted(VALID_STATUSES)}): {skill_file}")

    owner = _require_non_empty_str(metadata, "owner", skill_file)

    expected_source = f"skills/{expected_name}/SKILL.md"
    source_of_truth = _require_non_empty_str(metadata, "source_of_truth", skill_file)
    if source_of_truth != expected_source:
        raise ValueError(
            f"Invalid 'source_of_truth' '{source_of_truth}' (expected '{expected_source}'): {skill_file}"
        )

    raw_platforms = metadata.get("platforms")
    if not isinstance(raw_platforms, list) or not raw_platforms:
        raise ValueError(f"Missing or empty 'platforms' list: {skill_file}")

    platforms: list[str] = []
    for platform in raw_platforms:
        if not isinstance(platform, str) or platform not in SUPPORTED_PLATFORMS:
            raise ValueError(
                f"Unsupported platform '{platform}' (expected subset of {SUPPORTED_PLATFORMS}): {skill_file}"
            )
        if platform in platforms:
            raise ValueError(f"Duplicate platform '{platform}': {skill_file}")
        platforms.append(platform)

    evidence = validate_evidence(metadata.get("evidence"), repo_root, skill_file)

    raw_adapters = metadata.get("adapters")
    explicit_adapters: dict[str, str] = {}
    if raw_adapters is not None:
        if not isinstance(raw_adapters, dict):
            raise ValueError(f"'adapters' must be a mapping of platform to path: {skill_file}")
        for platform, adapter_rel in raw_adapters.items():
            if not isinstance(platform, str) or platform not in SUPPORTED_PLATFORMS:
                raise ValueError(f"Unsupported adapter platform '{platform}': {skill_file}")
            if platform not in platforms:
                raise ValueError(f"Adapter platform '{platform}' is not declared in 'platforms': {skill_file}")
            if not isinstance(adapter_rel, str) or not adapter_rel.strip():
                raise ValueError(f"Invalid adapter path for '{platform}': {skill_file}")
            explicit_adapters[platform] = adapter_rel.strip()

    return {
        "name": name,
        "description": description,
        "version": version,
        "status": status,
        "owner": owner,
        "source_of_truth": source_of_truth,
        "platforms": platforms,
        "evidence": evidence,
        "adapters": explicit_adapters,
    }


def resolve_adapters(
    repo_root: Path,
    name: str,
    platforms: list[str],
    explicit_adapters: dict[str, str],
    skill_file: Path,
) -> dict[str, Path]:
    """Resolve and validate platform adapters for a canonical skill."""
    adapters_root = (repo_root / "skills" / "adapters").resolve()
    resolved: dict[str, Path] = {}

    for platform, rel_path in explicit_adapters.items():
        adapter_path = _resolve_repo_path(repo_root, rel_path, f"Adapter path ({platform})", skill_file)
        if not adapter_path.is_relative_to(adapters_root / platform):
            raise ValueError(
                f"Adapter path for '{platform}' must live under skills/adapters/{platform}/: {skill_file}"
            )
        if not adapter_path.is_file():
            raise ValueError(f"Referenced adapter does not exist '{rel_path}': {skill_file}")
        resolved[platform] = adapter_path

    for platform in SUPPORTED_PLATFORMS:
        convention_path = (adapters_root / platform / f"{name}.md").resolve()
        if not convention_path.is_file():
            continue
        if platform not in platforms:
            raise ValueError(
                f"Adapter exists for undeclared platform '{platform}': {convention_path.relative_to(repo_root)}"
            )
        if platform in resolved and resolved[platform] != convention_path:
            raise ValueError(
                f"Conflicting adapter paths for '{platform}': "
                f"{resolved[platform].relative_to(repo_root)} vs {convention_path.relative_to(repo_root)}"
            )
        resolved[platform] = convention_path

    for platform, adapter_path in resolved.items():
        content = adapter_path.read_text(encoding="utf-8")
        if not content.strip():
            raise ValueError(f"Adapter file is empty: {adapter_path.relative_to(repo_root)}")
        if platform == "chrome-gemini" and FRONTMATTER_RE.match(content):
            raise ValueError(
                f"Chrome Gemini adapter must not contain YAML frontmatter: {adapter_path.relative_to(repo_root)}"
            )

    return resolved


def validate_dist_root(repo_root: Path, dist_root: Path, skills_root: Path) -> None:
    """Reject output directories that overlap repository sources or unexpected files."""
    git_root = (repo_root / ".git").resolve()

    if dist_root == repo_root or repo_root.is_relative_to(dist_root):
        raise ValueError(f"Refusing unsafe --dist-root equal to or containing repo root: {dist_root}")
    if dist_root == skills_root or dist_root.is_relative_to(skills_root) or skills_root.is_relative_to(dist_root):
        raise ValueError(f"Refusing unsafe --dist-root overlapping skills directory: {dist_root}")
    if dist_root == git_root or dist_root.is_relative_to(git_root):
        raise ValueError(f"Refusing unsafe --dist-root targeting .git directory: {dist_root}")

    if dist_root.exists():
        if not dist_root.is_dir():
            raise ValueError(f"Refusing --dist-root that is not a directory: {dist_root}")
        for entry in dist_root.iterdir():
            if entry.name not in MANAGED_DIST_ENTRIES:
                raise ValueError(
                    f"Refusing to clean unsafe --dist-root containing unexpected entry: {entry}"
                )
        if (
            dist_root.is_relative_to(repo_root)
            and dist_root != (repo_root / "dist").resolve()
            and (dist_root / ".gitkeep").exists()
        ):
            raise ValueError(f"Refusing --dist-root targeting tracked placeholder directory: {dist_root}")


def prepare_dist_root(dist_root: Path) -> None:
    """Clear only generated build artifacts in dist_root while preserving .gitkeep."""
    dist_root.mkdir(parents=True, exist_ok=True)
    for subdir in ("skills", "chrome-gemini", "bundles"):
        target = dist_root / subdir
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)
        target.mkdir(parents=True)

    index_path = dist_root / "index.json"
    if index_path.exists() or index_path.is_symlink():
        index_path.unlink()


def build_chrome_gemini_export(body: str, adapter_path: Path | None) -> str:
    """Compose the frontmatter-free Chrome Gemini export from canonical body and adapter."""
    parts = [body.strip()]
    if adapter_path is not None:
        parts.append(adapter_path.read_text(encoding="utf-8").strip())
    return "\n\n".join(part for part in parts if part) + "\n"


def write_reproducible_zip(source_dir: Path, bundle_path: Path) -> None:
    """Write a deterministic zip archive with fixed timestamps and permissions."""
    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as bundle:
        for file_path in sorted(source_dir.rglob("*")):
            if not file_path.is_file():
                continue
            rel_path = file_path.relative_to(source_dir).as_posix()
            info = zipfile.ZipInfo(filename=rel_path, date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if os.access(file_path, os.X_OK) else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            bundle.writestr(info, file_path.read_bytes())


def collect_skills(repo_root: Path) -> list[dict[str, Any]]:
    """Discover and validate all canonical skills in the repository."""
    skills_root = (repo_root / "skills").resolve()
    if not skills_root.is_dir():
        raise ValueError(f"Missing skills directory: {skills_root}")

    collected: list[dict[str, Any]] = []
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        if skill_dir.name.startswith(".") or skill_dir.name in SKIP_SKILL_DIRS:
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            raise ValueError(f"Missing SKILL.md in canonical skill directory: {skill_dir}")

        text = skill_file.read_text(encoding="utf-8")
        raw_metadata, body = parse_frontmatter(text)
        if not body.strip():
            raise ValueError(f"Skill body is empty: {skill_file}")

        validated = validate_metadata(raw_metadata, skill_dir.name, repo_root, skill_file)
        adapters = resolve_adapters(
            repo_root,
            validated["name"],
            validated["platforms"],
            validated["adapters"],
            skill_file,
        )
        collected.append(
            {
                "skill_dir": skill_dir,
                "skill_file": skill_file,
                "metadata": validated,
                "body": body,
                "adapters": adapters,
            }
        )

    return collected


def build(repo_root: Path, dist_root: Path) -> list[dict[str, object]]:
    """Validate canonical skills and emit reproducible exports into dist_root."""
    resolved_repo = repo_root.resolve()
    resolved_dist = dist_root.resolve()
    skills_root = (resolved_repo / "skills").resolve()

    validate_dist_root(resolved_repo, resolved_dist, skills_root)
    skills = collect_skills(resolved_repo)
    prepare_dist_root(resolved_dist)

    index: list[dict[str, object]] = []
    for entry in skills:
        skill_dir: Path = entry["skill_dir"]
        skill_file: Path = entry["skill_file"]
        metadata: dict[str, Any] = entry["metadata"]
        body: str = entry["body"]
        adapters: dict[str, Path] = entry["adapters"]
        name: str = metadata["name"]

        output_dir = resolved_dist / "skills" / name
        shutil.copytree(
            skill_dir,
            output_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"),
        )

        chrome_gemini_rel: str | None = None
        if "chrome-gemini" in metadata["platforms"]:
            chrome_path = resolved_dist / "chrome-gemini" / f"{name}.txt"
            chrome_path.write_text(
                build_chrome_gemini_export(body, adapters.get("chrome-gemini")),
                encoding="utf-8",
            )
            chrome_gemini_rel = chrome_path.relative_to(resolved_dist).as_posix()

        bundle_path = resolved_dist / "bundles" / f"{name}.zip"
        write_reproducible_zip(output_dir, bundle_path)

        index.append(
            {
                "name": name,
                "description": metadata["description"],
                "version": metadata["version"],
                "status": metadata["status"],
                "owner": metadata["owner"],
                "platforms": metadata["platforms"],
                "canonical_path": skill_file.relative_to(resolved_repo).as_posix(),
                "bundle_path": bundle_path.relative_to(resolved_dist).as_posix(),
                "chrome_gemini_path": chrome_gemini_rel,
                "adapters": {
                    platform: path.relative_to(resolved_repo).as_posix()
                    for platform, path in sorted(adapters.items())
                },
            }
        )

    index_path = resolved_dist / "index.json"
    index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--dist-root", type=Path, default=None)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate canonical skills and adapters without writing dist outputs.",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    if args.validate_only:
        skills = collect_skills(repo_root)
        print(f"Validated {len(skills)} canonical skills in {repo_root}")
        return

    dist_root = (args.dist_root or repo_root / "dist").resolve()
    skills = build(repo_root, dist_root)
    print(f"Built {len(skills)} canonical skill exports in {dist_root}")


if __name__ == "__main__":
    main()
