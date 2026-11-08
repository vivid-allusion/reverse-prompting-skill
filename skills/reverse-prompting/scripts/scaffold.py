#!/usr/bin/env python3
"""Lay out the scene-first map from a shots table. Never overwrites a file; reports what it kept.

  python3 scaffold.py SHOTS_TABLE PROJECT [--dry-run] [--only-listed]

SHOTS_TABLE is CSV or a Markdown table with the columns shot, scene, still and optionally motion,
scene_title, elements ('@NAME:CATEGORY[:role]; …'). It writes MAP/SCENES/Scene_NNN/SCENE.md and SHOT_NNN.md,
an empty Scene_NNN folder in every category of 02_PRE-PRODUCTION (only the listed ones with --only-listed),
an ABOUT stub for each hero element in its scene, and a _CANON folder for every hero element in two or more
scenes. Background elements go in the shot table only. It never writes under PROMPTS/.
"""
import argparse
import sys
from collections import OrderedDict
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rp_lib as rp  # noqa: E402


def scene_md(scene, title, shots):
    lines = ["# %s · %s" % (scene.replace("_", " "), title or "PLACE - TIME"), "",
             "- **Place:** ", "- **Time and light:** ", "- **Cast and state:** ", "- **Camera sides:** ",
             "- **Shots:** " + ", ".join(s for s, _ in shots), "", "## Decided", "", "- ", ""]
    return "\n".join(lines)


def shot_md(scene, shot, row, elements):
    lines = ["# %s · %s" % (scene.replace("_", " "), shot.replace("_", " ")), "",
             "- **Still:** %s" % row.get("still", ""),
             "- **Motion line (old):** %s" % (row.get("motion") or "none"),
             "- **Size:** ", "- **Hero:** ", "",
             "## In frame", "", "- ", "",
             "## Out of frame, by effect", "", "- ", "",
             "## Elements", "", "| Element | Category | Role | Reason |", "|---|---|---|---|"]
    lines += ["| %s | %s | %s | |" % (n, f, r) for n, f, r in elements]
    lines += ["", "## Notes", "", "- ", "", "## References", "", "| Ref | Role | Address |", "|---|---|---|", "",
              "## Prompts", "", "- None yet.", "", "## Takes", "", "None yet.", ""]
    return "\n".join(lines)


def about_md(name, folder, where, shots, canon):
    lines = ["# %s" % name, "", "One sentence: who or what.", "",
             "- **Folder:** `%s/%s`" % (folder, where),
             "- **Appears in:** %s" % (", ".join(shots) if shots else "every scene it is in")]
    if canon:
        lines.append("- **State of:** %s/@%s" % (rp.CANON, name.lstrip("@")))
    lines += ["", "## What the stills show", "", "- ", "", "## Decided", "", "- ", "",
              "## Reference slots", "", "- [ ] identity:", "- [ ] construction:", ""]
    return "\n".join(lines)


def plan(rows, only_listed=False):
    files, dirs = OrderedDict(), []
    scenes = OrderedDict()
    seen = {}
    for row in rows:
        scene, shot = rp.scene_dir(row["scene"]), rp.shot_name(row["shot"])
        scenes.setdefault(scene, {"title": row.get("scene_title", ""), "shots": []})
        if row.get("scene_title") and not scenes[scene]["title"]:
            scenes[scene]["title"] = row["scene_title"]
        els = rp.parse_elements(row.get("elements", ""))
        scenes[scene]["shots"].append((shot, row))
        files["MAP/SCENES/%s/%s.md" % (scene, shot)] = shot_md(scene, shot, row, els)
        for name, folder, role in els:
            if role == "hero":  # background is named in the shot table only, never made
                seen.setdefault((name, folder), OrderedDict()).setdefault(scene, []).append(shot)
    for scene, info in scenes.items():
        files["MAP/SCENES/%s/SCENE.md" % scene] = scene_md(scene, info["title"], info["shots"])
        if not only_listed:
            dirs += ["%s/%s/%s" % (rp.PRE, f, scene) for f in rp.FOLDERS]
    for (name, folder), by_scene in seen.items():
        canon = len(by_scene) > 1
        for scene, shots in by_scene.items():
            files["%s/%s/%s/%s/%s_ABOUT.md" % (rp.PRE, folder, scene, name, name)] = about_md(name, folder, scene, shots, canon)
        if canon:
            files["%s/%s/%s/%s/%s_ABOUT.md" % (rp.PRE, folder, rp.CANON, name, name)] = about_md(name, folder, rp.CANON, [], False)
    return files, dirs, scenes


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("table")
    ap.add_argument("project")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only-listed", action="store_true", help="make scene folders only where an element is listed")
    a = ap.parse_args(argv)
    try:
        rows = rp.read_table(a.table)
        files, dirs, scenes = plan(rows, a.only_listed)
    except ValueError as e:
        print("ERROR:", e)
        return 2
    root = Path(a.project)
    written = kept = 0
    for d in dirs:
        if not a.dry_run:
            (root / d).mkdir(parents=True, exist_ok=True)
    for rel, text in files.items():
        path = root / rel
        if path.exists():
            kept += 1
            print("kept   ", rel)
            continue
        written += 1
        print("would write" if a.dry_run else "wrote  ", rel)
        if not a.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    print("scenes: %d, shots: %d, files written: %d, kept: %d%s" % (
        len(scenes), len(rows), written, kept, " (dry run)" if a.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
