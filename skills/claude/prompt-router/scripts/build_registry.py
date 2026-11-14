#!/usr/bin/env python3
"""Build or check references/model-registry.md from references/model-guides/*.md frontmatter.

Stdlib only. Modes:
  --check       (default) exit 1 if guides are invalid or the registry differs from the guides
  --write       regenerate the registry (refuses to write if guides are invalid)
  --self-test   run built-in fixture tests in a temp directory
  --today DATE  YYYY-MM-DD used for staleness (default: today)

`last_verified` means "last written", not independently fact-checked.
"""
import argparse
import json
import re
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

STALE_DAYS = 180
REQUIRED = ("model", "vendor", "family", "aliases", "last_verified", "status")
HEADER = (
    "# Model registry\n\n"
    "Generated from the frontmatter of `model-guides/*.md`. The guide file is authoritative; "
    "update its frontmatter and regenerate this table when adding or changing a guide.\n\n"
    "| Model ID | Vendor | Family | Aliases | Last verified | Status | Successor |\n"
    "|---|---|---|---|---|---|---|\n"
)


def norm(s):
    return re.sub(r"[\s_]+", "-", s.strip().lower())


def parse_guide(path):
    lines = path.read_text(encoding="utf-8").split("\n")
    if not lines or lines[0].strip() != "---":
        return {"_error": "no frontmatter"}
    meta = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    else:
        return {"_error": "unterminated frontmatter"}
    if "aliases" in meta:
        a = meta["aliases"].strip()
        if a.startswith("[") and a.endswith("]"):
            meta["aliases"] = [x.strip().strip("\"'") for x in a[1:-1].split(",") if x.strip()]
        else:
            meta["aliases"] = None
    return meta


def load_guides(root):
    guides = {}
    errors = []
    for p in sorted((root / "references" / "model-guides").glob("*.md")):
        meta = parse_guide(p)
        if "_error" in meta:
            errors.append(f"{p.name}: {meta['_error']}")
            continue
        for k in REQUIRED:
            if not meta.get(k):
                errors.append(f"{p.name}: missing or invalid '{k}'")
        if meta.get("model") and meta["model"] != p.stem:
            errors.append(f"{p.name}: model '{meta['model']}' != filename")
        if meta.get("status") and meta["status"] not in ("current", "legacy"):
            errors.append(f"{p.name}: status '{meta['status']}' not current|legacy")
        guides[p.stem] = meta
    return guides, errors


def load_hosts(root):
    p = root / "references" / "hosts.json"
    data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return ({norm(x) for x in data.get("reserved_aliases", [])},
            {norm(x) for x in data.get("warn_aliases", [])})


def validate(guides, reserved, warn_names):
    errors, warnings = [], []
    ids = {norm(i): i for i in guides}
    seen = {}
    for gid, meta in guides.items():
        gn = norm(gid)
        for alias in meta.get("aliases") or []:
            n = norm(alias)
            if n in seen and seen[n] != gid:
                errors.append(f"duplicate alias '{alias}': {seen[n]} and {gid}")
            seen.setdefault(n, gid)
            if n == gn:
                warnings.append(f"self-alias '{alias}' on {gid} is redundant (warning only)")
            if n in ids and ids[n] != gid:
                errors.append(f"alias '{alias}' of {gid} equals model id {ids[n]}")
            if n in reserved:
                errors.append(f"alias '{alias}' of {gid} is a reserved host name")
            elif n in warn_names:
                warnings.append(f"alias '{alias}' of {gid} collides with a host name (warning only)")
        succ = meta.get("successor")
        if succ == gid:
            errors.append(f"{gid}: successor '{succ}' cannot point to itself")
        elif succ and succ not in guides:
            errors.append(f"{gid}: successor '{succ}' has no guide")
        elif meta.get("status") == "legacy" and not succ:
            warnings.append(f"{gid}: legacy guide has no documented successor (warning only)")
    return errors, warnings


def render(guides):
    rows = []
    for gid, m in guides.items():  # guides are loaded sorted by filename
        aliases = ", ".join(f"`{a}`" for a in m["aliases"])
        rows.append(f"| {gid} | {m['vendor']} | {m['family']} | {aliases} | "
                    f"{m['last_verified']} | {m['status']} | {m.get('successor', '')} |")
    return HEADER + "\n".join(rows) + "\n"


def registry_ids(path):
    if not path.exists():
        return set()
    return {ln.split("|")[1].strip() for ln in path.read_text(encoding="utf-8").split("\n")
            if ln.startswith("| ") and not ln.startswith("| Model ID")}


def stale(guides, today):
    cutoff = today - timedelta(days=STALE_DAYS)
    out = []
    for gid, m in guides.items():
        try:
            d = date.fromisoformat(m["last_verified"])
        except ValueError:
            out.append(f"{gid} (bad date {m['last_verified']})")
            continue
        if d < cutoff:
            out.append(f"{gid} ({m['last_verified']})")
    return out


def run(root, mode, today, out=print):
    guides, errors = load_guides(root)
    reserved, warn_names = load_hosts(root)
    e2, warnings = validate(guides, reserved, warn_names)
    errors += e2
    reg = root / "references" / "model-registry.md"
    have = registry_ids(reg)
    missing_rows = sorted(set(guides) - have)
    orphan_rows = sorted(have - set(guides))
    old_stale = stale(guides, today)
    for w in warnings:
        out(f"WARN  {w}")
    for e in errors:
        out(f"ERROR {e}")
    if missing_rows:
        out(f"MISSING rows for guides: {', '.join(missing_rows)}")
    if orphan_rows:
        out(f"MISSING guides for rows: {', '.join(orphan_rows)}")
    out(f"STALE ({STALE_DAYS}d, last_verified = last written, not fact-checked): "
        f"{len(old_stale)}" + (f" -> {', '.join(old_stale)}" if old_stale else ""))
    out(f"guides={len(guides)} registry_rows={len(have)}")
    if errors:
        return 1
    text = render(guides)
    if mode == "write":
        reg.write_text(text, encoding="utf-8")
        out(f"wrote {reg} ({len(guides)} rows)")
        return 0
    current = reg.read_text(encoding="utf-8") if reg.exists() else None
    if current != text:
        out("registry is out of date: run --write")
        return 1
    out("registry up to date")
    return 0


def _fixture(root, guides, registry=None):
    gdir = root / "references" / "model-guides"
    gdir.mkdir(parents=True, exist_ok=True)
    for gid, spec in guides.items():
        aliases, lv = spec[0], spec[1]
        status = spec[2] if len(spec) > 2 else "current"
        succ = spec[3] if len(spec) > 3 else ""
        succ_line = f"successor: {succ}\n" if succ else ""
        (gdir / f"{gid}.md").write_text(
            f"---\nmodel: {gid}\nvendor: V\nfamily: F\naliases: [{', '.join(aliases)}]\n"
            f"last_verified: {lv}\nstatus: {status}\n{succ_line}---\n# {gid}\n", encoding="utf-8")
    (root / "references" / "hosts.json").write_text(
        json.dumps({"reserved_aliases": ["spark", "gemini-spark"], "warn_aliases": ["copilot"]}),
        encoding="utf-8")
    if registry is not None:
        (root / "references" / "model-registry.md").write_text(registry, encoding="utf-8")


def self_test():
    today = date(2026, 11, 14)
    fails = []

    def check(name, cond):
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            fails.append(name)

    base = {"a-1": (["a", "a1"], "2026-10-13"), "b-1": (["b"], "2026-10-13"),
            "c-1": (["c", "copilot"], "2026-01-01")}
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _fixture(root, base)
        log = []
        check("valid generation (write, exit 0)", run(root, "write", today, log.append) == 0)
        first = (root / "references" / "model-registry.md").read_bytes()
        check("three rows generated", first.decode().count("\n| ") == 3 or
              sum(1 for ln in first.decode().split("\n") if ln.startswith("| ") and "Model ID" not in ln) == 3)
        run(root, "write", today, log.append)
        check("idempotent write", first == (root / "references" / "model-registry.md").read_bytes())
        check("check passes after write", run(root, "check", today, log.append) == 0)
        check("warn-only host collision (copilot)", any(l.startswith("WARN") and "copilot" in l for l in log))
        check("stale guide reported", any("STALE" in l and "c-1" in l for l in log))

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _fixture(root, {**base, "d-1": (["a"], "2026-10-13")})
        log = []
        check("duplicate alias fails", run(root, "check", today, log.append) == 1
              and any("duplicate alias" in l for l in log))

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _fixture(root, {**base, "e-1": (["spark"], "2026-10-13")})
        log = []
        check("reserved-name alias fails", run(root, "check", today, log.append) == 1
              and any("reserved host name" in l for l in log))

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _fixture(root, base)
        run(root, "write", today, lambda *_: None)
        (root / "references" / "model-guides" / "b-1.md").unlink()
        _fixture(root, {"f-1": (["f"], "2026-10-13")})
        reg = root / "references" / "model-registry.md"
        reg.write_text(reg.read_text(encoding="utf-8").replace("| c-1 |", "| ghost-1 |"), encoding="utf-8")
        log = []
        code = run(root, "check", today, log.append)
        check("missing row and orphan row reported",
              code == 1 and any("MISSING rows" in l and "f-1" in l for l in log)
              and any("MISSING guides" in l and "ghost-1" in l for l in log))

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _fixture(root, {**base, "g-1": (["g-1"], "2026-10-13", "legacy", "")})
        log = []
        code = run(root, "write", today, log.append)
        check("self-alias and legacy-without-successor warn without failing",
              code == 0
              and any("self-alias 'g-1'" in l for l in log)
              and any("g-1: legacy guide has no documented successor" in l for l in log))

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _fixture(root, {**base, "h-1": (["h"], "2026-10-13", "legacy", "h-1")})
        log = []
        check("self-successor fails",
              run(root, "check", today, log.append) == 1
              and any("cannot point to itself" in l for l in log))
    print(f"{'ALL PASS' if not fails else 'FAILED: ' + ', '.join(fails)}")
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    g.add_argument("--self-test", action="store_true")
    ap.add_argument("--today", default=None)
    ap.add_argument("--root", default=None, help="skill directory (default: parent of scripts/)")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    root = Path(a.root) if a.root else Path(__file__).resolve().parent.parent
    today = date.fromisoformat(a.today) if a.today else date.today()
    return run(root, "write" if a.write else "check", today)


if __name__ == "__main__":
    sys.exit(main())
