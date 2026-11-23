#!/usr/bin/env python3
"""Build or check the two-tier registry from references/model-guides/*.md frontmatter.

Guides with `tier: active` (and a `profile:`) go to references/model-registry.md;
all others go to references/model-registry-archive.md. Counts and Profile word
bounds come from references/hosts.json.

Stdlib only. Modes:
  --check       (default) exit 1 if guides are invalid or either registry differs from the guides
  --write       regenerate both registry files (refuses to write if guides are invalid)
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
ACTIVE_FILE = "model-registry.md"
ARCHIVE_FILE = "model-registry-archive.md"
ACTIVE_HEADER = (
    "# Model registry (active shortlist)\n\n"
    "Generated from `model-guides/*.md` frontmatter with `tier: active`; the guide is authoritative. "
    "Match here first; on a miss read `model-registry-archive.md` once. "
    "Rows with Profile `unverified` are excluded from automatic recommendation.\n\n"
    "| Model ID | Vendor | Family | Aliases | Last verified | Status | Successor | Profile |\n"
    "|---|---|---|---|---|---|---|---|\n"
)
ARCHIVE_HEADER = (
    "# Model registry archive\n\n"
    "Generated from `model-guides/*.md` frontmatter without `tier: active`; the guide is authoritative. "
    "Read only after a miss in `model-registry.md`.\n\n"
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


def load_config(root):
    p = root / "references" / "hosts.json"
    data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return {"reserved": {norm(x) for x in data.get("reserved_aliases", [])},
            "warn": {norm(x) for x in data.get("warn_aliases", [])},
            "active_count": data.get("active_count"),
            "profile_words": data.get("profile_words")}


def is_active(meta):
    return meta.get("tier") == "active"


def validate_tiers(guides, cfg):
    errors = []
    lo, hi = cfg["profile_words"] or (None, None)
    for gid, meta in guides.items():
        tier, prof = meta.get("tier"), meta.get("profile")
        if tier is not None and tier != "active":
            errors.append(f"{gid}: tier '{tier}' not active (omit for archive)")
        if not is_active(meta):
            if prof:
                errors.append(f"{gid}: archive guide must not carry 'profile'")
            continue
        if meta.get("status") != "current":
            errors.append(f"{gid}: active guide must have status current")
        if not prof:
            errors.append(f"{gid}: active guide missing 'profile'")
        elif "|" in prof:
            errors.append(f"{gid}: profile must not contain '|'")
        elif prof != "unverified" and lo is not None and not lo <= len(prof.split()) <= hi:
            errors.append(f"{gid}: profile has {len(prof.split())} words, need {lo}-{hi} or 'unverified'")
    n = sum(1 for m in guides.values() if is_active(m))
    if cfg["active_count"] is not None and n != cfg["active_count"]:
        errors.append(f"active guides = {n}, hosts.json active_count = {cfg['active_count']}")
    return errors


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


def render(guides, active):
    rows = []
    for gid, m in guides.items():  # guides are loaded sorted by filename
        if is_active(m) != active:
            continue
        aliases = ", ".join(f"`{a}`" for a in m["aliases"])
        row = (f"| {gid} | {m['vendor']} | {m['family']} | {aliases} | "
               f"{m['last_verified']} | {m['status']} | {m.get('successor', '')} |")
        rows.append(row + (f" {m['profile']} |" if active else ""))
    return (ACTIVE_HEADER if active else ARCHIVE_HEADER) + "\n".join(rows) + "\n"


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
    cfg = load_config(root)
    e2, warnings = validate(guides, cfg["reserved"], cfg["warn"])
    errors += e2 + validate_tiers(guides, cfg)
    regs = {True: root / "references" / ACTIVE_FILE, False: root / "references" / ARCHIVE_FILE}
    have = registry_ids(regs[True]) | registry_ids(regs[False])
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
    n_active = sum(1 for m in guides.values() if is_active(m))
    out(f"guides={len(guides)} registry_rows={len(have)} "
        f"active={n_active} archive={len(guides) - n_active}")
    if errors:
        return 1
    texts = {tier: render(guides, tier) for tier in regs}
    if mode == "write":
        for tier, path in regs.items():
            path.write_text(texts[tier], encoding="utf-8")
            out(f"wrote {path}")
        return 0
    stale_files = [p.name for tier, p in regs.items()
                   if (p.read_text(encoding="utf-8") if p.exists() else None) != texts[tier]]
    if stale_files:
        out(f"registry is out of date ({', '.join(stale_files)}): run --write")
        return 1
    out("registry up to date")
    return 0


def _fixture(root, guides, registry=None, active_count=1):
    gdir = root / "references" / "model-guides"
    gdir.mkdir(parents=True, exist_ok=True)
    for gid, spec in guides.items():
        aliases, lv = spec[0], spec[1]
        status = spec[2] if len(spec) > 2 else "current"
        succ = spec[3] if len(spec) > 3 else ""
        prof = spec[4] if len(spec) > 4 else ""
        tier = spec[5] if len(spec) > 5 else ("active" if prof else "")
        extra = (f"successor: {succ}\n" if succ else "") + (f"tier: {tier}\n" if tier else "") \
            + (f"profile: {prof}\n" if prof else "")
        (gdir / f"{gid}.md").write_text(
            f"---\nmodel: {gid}\nvendor: V\nfamily: F\naliases: [{', '.join(aliases)}]\n"
            f"last_verified: {lv}\nstatus: {status}\n{extra}---\n# {gid}\n", encoding="utf-8")
    (root / "references" / "hosts.json").write_text(
        json.dumps({"reserved_aliases": ["spark", "gemini-spark"], "warn_aliases": ["copilot"],
                    "active_count": active_count, "profile_words": [8, 16]}),
        encoding="utf-8")
    if registry is not None:
        (root / "references" / ACTIVE_FILE).write_text(registry, encoding="utf-8")


def self_test():
    today = date(2026, 11, 14)
    fails = []

    def check(name, cond):
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            fails.append(name)

    def rows(path):
        return [ln.split("|")[1].strip() for ln in path.read_text(encoding="utf-8").split("\n")
                if ln.startswith("| ") and "Model ID" not in ln]

    prof8 = "one two three four five six seven eight"
    base = {"a-1": (["a", "a1"], "2026-10-13", "current", "", prof8),
            "b-1": (["b"], "2026-10-13"), "c-1": (["c", "copilot"], "2026-01-01")}
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _fixture(root, base)
        log = []
        check("valid generation (write, exit 0)", run(root, "write", today, log.append) == 0)
        act, arc = root / "references" / ACTIVE_FILE, root / "references" / ARCHIVE_FILE
        first = act.read_bytes() + arc.read_bytes()
        check("two-tier split (1 active with Profile, 2 archive)",
              rows(act) == ["a-1"] and rows(arc) == ["b-1", "c-1"]
              and prof8 in act.read_text(encoding="utf-8")
              and "Profile" not in arc.read_text(encoding="utf-8"))
        check("counts printed", any("active=1 archive=2" in l for l in log))
        run(root, "write", today, log.append)
        check("idempotent write", first == act.read_bytes() + arc.read_bytes())
        check("check passes after write", run(root, "check", today, log.append) == 0)
        check("warn-only host collision (copilot)", any(l.startswith("WARN") and "copilot" in l for l in log))
        check("stale guide reported", any("STALE" in l and "c-1" in l for l in log))
        arc.write_text(arc.read_text(encoding="utf-8").replace("| b-1 |", "| b-2 |"), encoding="utf-8")
        log = []
        check("stale archive file fails check", run(root, "check", today, log.append) == 1
              and any("model-registry-archive.md" in l and "out of date" in l for l in log))

    def fails_with(name, guides, needle, **kw):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _fixture(root, guides, **kw)
            log = []
            check(name, run(root, "check", today, log.append) == 1 and any(needle in l for l in log))

    fails_with("duplicate alias fails", {**base, "d-1": (["a"], "2026-10-13")}, "duplicate alias")
    fails_with("reserved-name alias fails", {**base, "e-1": (["spark"], "2026-10-13")}, "reserved host name")
    fails_with("self-successor fails", {**base, "h-1": (["h"], "2026-10-13", "legacy", "h-1")},
               "cannot point to itself")
    fails_with("active legacy guide fails",
               {**base, "i-1": (["i"], "2026-10-13", "legacy", "a-1", prof8)},
               "must have status current", active_count=2)
    fails_with("short profile fails",
               {**base, "a-1": (["a"], "2026-10-13", "current", "", "too short")}, "need 8-16")
    fails_with("profile on archive guide fails",
               {**base, "j-1": (["j"], "2026-10-13", "current", "", prof8, "archive")}, "must not carry 'profile'")
    fails_with("active count mismatch fails", base, "active_count = 2", active_count=2)
    fails_with("active guide without profile fails",
               {**base, "k-1": (["k"], "2026-10-13", "current", "", "", "active")},
               "missing 'profile'", active_count=2)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _fixture(root, {**base, "a-1": (["a"], "2026-10-13", "current", "", "unverified")})
        check("'unverified' profile passes", run(root, "write", today, lambda *_: None) == 0)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _fixture(root, base)
        run(root, "write", today, lambda *_: None)
        (root / "references" / "model-guides" / "b-1.md").unlink()
        _fixture(root, {"f-1": (["f"], "2026-10-13")})
        arc = root / "references" / ARCHIVE_FILE
        arc.write_text(arc.read_text(encoding="utf-8").replace("| c-1 |", "| ghost-1 |"), encoding="utf-8")
        log = []
        code = run(root, "check", today, log.append)
        check("missing row and orphan row reported across both files",
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
