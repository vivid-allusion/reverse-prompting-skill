#!/usr/bin/env python3
"""Check the evals' answers against the trees they cite. Exit 0 = every reachable needle holds, 1 = findings.

  python3 tools/check_evidence.py [--tree NAME=PATH ...] [--all]

Each cross_module case in evals/evals.json carries evidence: {tree, path, needle[, absent]}. The tree `repo` is
this repository and is always given. Other trees are sibling skills (`helmer-md`, `helmer-story-breakdown`,
`cinematic-realism`, the sheet skills): give their checkouts with --tree. A tree not given is reported as
skipped, and --all makes a skip a finding. tools/validate.py checks the `repo` needles in CI.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "skills" / "reverse-prompting" / "evals" / "evals.json"


def check(cases, trees):
    findings, checked, skipped = [], 0, set()
    for case in cases:
        for item in case.get("evidence", []):
            tree = trees.get(item["tree"])
            if tree is None:
                skipped.add(item["tree"])
                continue
            path = tree / item["path"]
            where = "%s: %s:%s" % (case["id"], item["tree"], item["path"])
            if not path.is_file():
                findings.append("%s is not in the tree" % where)
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            checked += 1
            if item.get("absent"):
                if item["needle"].lower() in text.lower():
                    findings.append("%s holds %r, which the answer says it does not" % (where, item["needle"]))
            elif item["needle"] not in text:
                findings.append("%s no longer holds %r" % (where, item["needle"]))
    return findings, checked, sorted(skipped)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--tree", action="append", default=[], metavar="NAME=PATH")
    parser.add_argument("--all", action="store_true", help="a tree not given is a finding")
    args = parser.parse_args(argv)
    trees = {"repo": ROOT}
    for pair in args.tree:
        name, _, path = pair.partition("=")
        trees[name] = Path(path)
    cases = json.loads(EVALS.read_text(encoding="utf-8"))["cases"]
    findings, checked, skipped = check(cases, trees)
    for line in findings:
        print("FAIL:", line)
    for name in skipped:
        print("skipped, no tree given:", name)
    print("evidence: %d checked, %d finding(s), %d tree(s) skipped" % (checked, len(findings), len(skipped)))
    return 1 if findings or (args.all and skipped) else 0


if __name__ == "__main__":
    sys.exit(main())
