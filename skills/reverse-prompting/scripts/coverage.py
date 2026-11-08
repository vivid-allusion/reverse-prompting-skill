#!/usr/bin/env python3
"""Rebuild MAP/COVERAGE.md, MAP/PROMPTS_INDEX.md and each shot's Prompts list from the tree. Exit 1 if any hero is missing.

  python3 coverage.py PROJECT [--check]

A hero element is covered by a prompt file in any model folder at PROMPTS/<MODEL>/<category>/<its Scene_NNN or
_CANON>/<@NAME or @NAME_…>.md, or by the Reason in its shot's Elements table. Background elements need nothing.
Video prompts are PROMPTS/VIDEO/Scene_NNN/SHOT_NNN.md or SHOTS_NNN-NNN.md. With --check nothing is written.
"""
import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rp_lib as rp  # noqa: E402


def prompt_files(root):
    base = root / "PROMPTS"
    return sorted((p for p in base.rglob("*.md")), key=lambda p: rp.natural_key(p.relative_to(base))) if base.is_dir() else []


def matches(rel, name, folder, scene):
    parts = rel.parts
    if len(parts) < 4 or parts[1] != folder or parts[2] not in (scene, rp.CANON):
        return False
    return rel.stem == name or rel.stem.startswith(name + "_")


def video_for(rel, scene, number):
    parts = rel.parts
    if not rp.is_video(rel) or len(parts) < 3 or parts[1] != scene or number is None:
        return False
    m = re.fullmatch(r"SHOTS?_(\d+)(?:-(\d+))?", rel.stem)
    if not m:
        return False
    lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
    return lo <= number <= hi


def build(root):
    root = Path(root)
    base = root / "PROMPTS"
    prompts = [p.relative_to(base) for p in prompt_files(root)]
    shots = sorted((root / "MAP" / "SCENES").glob("Scene_*/SHOT_*.md"), key=lambda p: rp.natural_key(p.relative_to(root)))
    rows, missing, counts, per_shot = [], [], {"prompt": 0, "reason": 0, "background": 0, "missing": 0}, {}
    for shot in shots:
        scene, name = shot.parent.name, shot.stem
        text = shot.read_text(encoding="utf-8")
        mine = [rel for rel in prompts if video_for(rel, scene, rp.shot_number(name))]
        for el, folder, role, reason in rp.elements_table(text):
            hits = [rel for rel in prompts if matches(rel, el, folder, scene)]
            if role == "background":
                status, kind = "— background: left to the video prompt", "background"
            elif hits:
                status, kind = ", ".join("`%s`" % h.as_posix() for h in hits), "prompt"
                mine += hits
            elif reason:
                status, kind = "— " + reason, "reason"
            else:
                status, kind = "**MISSING**", "missing"
                missing.append("%s %s `%s` (%s)" % (scene, name, el, folder))
            counts[kind] += 1
            rows.append("| %s | %s | `%s` | %s | %s | %s |" % (scene, name, el, folder, role, status))
        per_shot[shot] = sorted(set(mine), key=rp.natural_key)
    hero = counts["prompt"] + counts["reason"] + counts["missing"]
    cov = ["# Coverage", "",
           "Every element of every shot, and the prompt file that makes it, or why there is none. Rebuilt by `coverage.py`; do not edit by hand.", "",
           "## Missing", ""] + (["- " + m for m in missing] or ["- Nothing: every hero element has a prompt or a stated reason."]) + [
           "", "## Counts", "",
           "- Shots: %d" % len(shots),
           "- Hero elements: %d (%d with a prompt, %d with a stated reason, %d missing)" % (hero, counts["prompt"], counts["reason"], counts["missing"]),
           "- Background elements: %d" % counts["background"],
           "- Prompt files: %d" % len(prompts), "",
           "## By shot", "", "| Scene | Shot | Element | Category | Role | Prompt file, or reason |", "|---|---|---|---|---|---|"] + rows + [""]
    idx = ["# Prompt index", "", "Every prompt file under `PROMPTS/`, by model folder and category. Rebuilt by `coverage.py`.", ""]
    by_model = {}
    for rel in prompts:
        by_model.setdefault(rel.parts[0], {}).setdefault(rel.parts[1] if len(rel.parts) > 2 else "", []).append(rel)
    for model in sorted(by_model, key=rp.natural_key):
        idx += ["## %s (%d)" % (model, sum(len(v) for v in by_model[model].values())), ""]
        for cat in sorted(by_model[model], key=rp.natural_key):
            idx += ["### %s" % (cat or "(top)"), "", "| File | Refs | What it makes |", "|---|---|---|"]
            for rel in by_model[model][cat]:
                info = rp.read_prompt((base / rel).read_text(encoding="utf-8"))
                idx.append("| `%s` | %d | %s |" % (rel.as_posix(), len(info["embeds"]), rp.first_line(info["prompt"])))
            idx.append("")
    return "\n".join(cov), "\n".join(idx), per_shot, missing, counts


def write_shot_prompts(root, shot, rels):
    text = shot.read_text(encoding="utf-8")
    lines = ["- [`%s`](%s)" % (r.as_posix(), "../../../PROMPTS/" + r.as_posix()) for r in rels] or ["- None yet."]
    block = "## Prompts\n\n" + "\n".join(lines) + "\n\n"
    if re.search(r"^## Prompts\s*\n", text, re.M):
        new = re.sub(r"^## Prompts\s*\n.*?(?=^## |\Z)", block, text, count=1, flags=re.S | re.M)
    else:
        new = text.rstrip("\n") + "\n\n" + block
    if new != text:
        shot.write_text(new, encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("project")
    ap.add_argument("--check", action="store_true", help="report only; write nothing")
    a = ap.parse_args(argv)
    root = Path(a.project)
    if not (root / "MAP" / "SCENES").is_dir():
        print("ERROR: no MAP/SCENES in %s: run scaffold.py first" % root)
        return 2
    cov, idx, per_shot, missing, counts = build(root)
    if not a.check:
        (root / "MAP" / "COVERAGE.md").write_text(cov, encoding="utf-8")
        (root / "MAP" / "PROMPTS_INDEX.md").write_text(idx, encoding="utf-8")
        for shot, rels in per_shot.items():
            write_shot_prompts(root, shot, rels)
    for m in missing:
        print("MISSING:", m)
    print("coverage: %d with a prompt, %d with a reason, %d background, %d missing" % (
        counts["prompt"], counts["reason"], counts["background"], counts["missing"]))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
