#!/usr/bin/env python3
"""Check every prompt file under PROMPTS/. Prints findings; exit 1 on any. Writes nothing.

  python3 check_prompts.py PROJECT [--min-refs N]

The shape is the one both generators read (the helmer-md skill): a closed ```prompt fence or one prompt line,
then one ![alt](https address) per line. It fails a bare fence, an unclosed or empty fence, a second text line,
a bare address line, a malformed embed, a start frame beside reference images, and notes under PROMPTS/
(ABOUT, index, scene or shot notes, a file that starts with a heading). With --min-refs N, an image-linked asset file with fewer references fails.
"""
import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rp_lib as rp  # noqa: E402

def check_file(base, path, min_refs=0):
    rel = path.relative_to(base)
    found = []
    if rp.NOTE_NAMES.search(path.stem) or (path.stem.startswith("SHOT_") and not rp.is_video(rel)):
        found.append("%s: a note under PROMPTS/: every .md in an input folder is a job; move it to MAP/" % rel.as_posix())
        return found
    info = rp.read_prompt(path.read_text(encoding="utf-8"))
    found += ["%s: %s" % (rel.as_posix(), e) for e in info["errors"]]
    if min_refs and not rp.is_video(rel) and len(info["embeds"]) < min_refs:
        found.append("%s: %d reference(s), at least %d wanted" % (rel.as_posix(), len(info["embeds"]), min_refs))
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("project")
    ap.add_argument("--min-refs", type=int, default=0)
    a = ap.parse_args(argv)
    base = Path(a.project) / "PROMPTS"
    if not base.is_dir():
        print("ERROR: no PROMPTS/ in %s" % a.project)
        return 2
    files = sorted(base.rglob("*.md"), key=lambda p: rp.natural_key(p.relative_to(base)))
    findings = []
    for path in files:
        findings += check_file(base, path, a.min_refs)
    others = [p for p in base.rglob("*") if p.is_file() and p.suffix != ".md"]
    for line in findings:
        print("FAIL:", line)
    print("prompts: %d checked, %d finding(s)%s" % (len(files), len(findings),
          ", %d non-prompt file(s) ignored" % len(others) if others else ""))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
