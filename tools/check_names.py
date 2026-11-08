#!/usr/bin/env python3
"""Find every name the skill puts in backticks, in the trees that should hold it. Exit 0 = all found, 1 = findings.

  python3 tools/check_names.py [--tree PATH ...]

The order behind the skill: do not invent folders, files, columns or commands. Every `token` in SKILL.md and the
references must occur, as written, in this repo's scripts, examples or tools, or in a sibling skill's checkout
given with --tree (helmer-md, helmer-story-breakdown, cinematic-realism, the sheet skills), after <placeholders>
and NNN-style counters are cut away. The skill's own prose is left out of the search so it cannot vouch for itself.
A name no plain search can find is listed in tools/names_allowed.json with the reason.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "reverse-prompting"
SEARCHED = {".py", ".md", ".json", ".csv", ".yml", ".yaml", ".toml", ".txt"}
SKIP_DIRS = {".git", "__pycache__", "node_modules"}
# The skill's own prose and the pages written about it must not vouch for its names.
OWN_PROSE = re.compile(r"^(skills/reverse-prompting/(SKILL\.md|references/|evals/|CHANGELOG\.md)|README\.md|CHANGELOG\.md|docs/|tests/)")
OWN_FILES = re.compile(r"^(references|scripts)/")  # tools/validate.py checks these exist
ALLOWED = json.loads((ROOT / "tools" / "names_allowed.json").read_text(encoding="utf-8"))


def tokens_in(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"````.*?````", "", text, flags=re.S)
    return {t.strip() for t in re.findall(r"``? ?([^`\n]+?) ?``?", text) if t.strip()}


def pieces(token):
    """The literal parts worth finding: no placeholders, no counters, no ellipses."""
    token = token.replace("…", "...")
    token = re.sub(r"<[^>]*>|\.\.\.|\*|NNN(?:-NNN)?|@NAME|\bCATEGORY\b|\brole\b", " ", token)
    parts = re.split(r"[/:\s]+", token)  # a path or a command is found segment by segment
    return [p.strip(" .") for p in parts if len(p.strip(" .")) >= 2]


def corpus(trees):
    blob = []
    for tree in trees:
        tree = Path(tree)
        for path in tree.rglob("*"):
            if path.is_dir() or path.suffix not in SEARCHED or SKIP_DIRS & set(path.parts):
                continue
            rel = path.relative_to(tree).as_posix()
            if tree.resolve() == ROOT and OWN_PROSE.match(rel):
                continue
            try:
                blob.append(rel)
                blob.append(path.read_text(encoding="utf-8", errors="ignore").replace("…", "..."))
            except OSError:
                continue
    return "\n".join(blob)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--tree", action="append", default=[], type=Path)
    args = parser.parse_args(argv)
    pages = [SKILL / "SKILL.md"] + sorted((SKILL / "references").glob("*.md"))
    blob = corpus([ROOT] + args.tree)
    missing, total = {}, 0
    for page in pages:
        for token in tokens_in(page.read_text(encoding="utf-8")):
            total += 1
            if token in ALLOWED or OWN_FILES.match(token):
                continue
            for piece in pieces(token):
                if piece not in blob:
                    missing.setdefault(token, set()).add(page.name)
    for token in sorted(missing):
        print("NOT FOUND: %r in %s" % (token, ", ".join(sorted(missing[token]))))
    print("names: %d looked up, %d not found" % (total, len(missing)))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
