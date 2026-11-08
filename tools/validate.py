#!/usr/bin/env python3
"""Validate the skill folder and the front page against the house skill memo. Exit 0 = clean, 1 = findings.

  python3 tools/validate.py [skill-folder]      (default: skills/reverse-prompting, plus the README)

Checks structure, frontmatter, size, evals, the reference graph, version agreement, the "nothing remote, nothing
absolute" boundary, the entry scripts, that each cross-module eval's evidence in this repo holds, and that the
README's badges and version table state the skill's version. It does not judge whether the prose is right; the
tests and tools/check_names.py do what can be done of that.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "reverse-prompting"
TYPES = {"knowledge", "workflow", "orchestrator", "tool"}
FORBIDDEN_FILES = {"README.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md"}
ENTRY_SCRIPTS = ("scaffold.py", "coverage.py", "check_prompts.py")
ALLOWED_URLS = ()
BODY_MAX_LINES = 500
DESCRIPTION_MAX_CHARS = 1024  # the Agent Skills format's limit on the description
# The memo's limit is on what is LOADED: the first read plus the two largest pages one question can pull.
# The folder ceiling keeps growth a decision: raising it is a change here, with its reason in the changelog.
LOADED_MAX_WORDS = 5000
FOLDER_MAX_WORDS = 20000
# The app's brand scan runs over any copy of a skill it carries. The same rule here, so a page cannot turn it red.
BRAND_TOKENS = ("Helmer", "helmer", "Eclipse", "Theia", "VSG", "Vivid Studio Generate")
BRAND_SKIP_LINE = re.compile(
    r"SPDX-|Copyright|Licensed under|Public License|@theia\/|\btheia[-_]|\bhelmer[-_.:\/*]|HELMER_|Helmer[A-Z]|Helmer[\/*]|['\"]helmer"
)
# Names retired from the product. They must not come through this skill.
OLD_NAMES = re.compile(
    r"F-?Capacitor|Flux Capacitor|studiolot|AISL|Frame Composer|Motion Conductor|LazyStudio|Flintmark|\bfc\b|\bmc\b|\bhc\b",
    re.I,
)


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1), text[m.end():]) if m else (None, text)


def words(path):
    return len(re.findall(r"\S+", path.read_text(encoding="utf-8")))


def naming_findings(rel, text):
    """The app's brand scan and the retired names, line by line, for one text file."""
    found = []
    for number, line in enumerate(text.splitlines(), start=1):
        if OLD_NAMES.search(line):
            found.append("%s:%d: a retired name: %s" % (rel, number, OLD_NAMES.search(line).group(0)))
        if BRAND_SKIP_LINE.search(line):
            continue
        for token in BRAND_TOKENS:
            if re.search(r"\b%s\b" % re.escape(token), line):
                found.append("%s:%d: the app's brand scan refuses the bare name %r here" % (rel, number, token))
    return found


def check_evals(skill, corpus, f, root):
    ev = skill / "evals" / "evals.json"
    tr = skill / "evals" / "triggers.json"
    if ev.is_file():
        cases = json.loads(ev.read_text(encoding="utf-8")).get("cases", [])
        if len(cases) < 3:
            f.append("evals.json needs 3+ cases")
        if sum(1 for c in cases if c.get("cross_module")) < 3:
            f.append("evals.json needs 3+ cases that test understanding across modules")
        ids = [c.get("id") for c in cases]
        for dup in sorted({i for i in ids if ids.count(i) > 1}):
            f.append("eval id %s is repeated" % dup)
        for c in cases:
            if not c.get("assertions"):
                f.append("eval %s has no assertions" % c.get("id"))
            for a in c.get("assertions", []):
                if a.get("kind") == "says" and "text" in a:
                    src = corpus.get(a.get("grounded_in", ""))
                    if src is None or a["text"].lower() not in src.lower():
                        f.append("eval %s demands %r which %s does not say" % (c.get("id"), a["text"], a.get("grounded_in")))
            if c.get("cross_module"):
                evidence = c.get("evidence") or []
                if not evidence:
                    f.append("eval %s is cross-module and points at no evidence" % c.get("id"))
                for item in evidence:
                    if not (item.get("tree") and item.get("path") and item.get("needle")):
                        f.append("eval %s has evidence without a tree, a path and a needle" % c.get("id"))
                    elif item["tree"] == "repo":
                        target = root / item["path"]
                        if not target.is_file() or item["needle"] not in target.read_text(encoding="utf-8"):
                            f.append("eval %s evidence: %s does not contain %r" % (c.get("id"), item["path"], item["needle"]))
    if tr.is_file():
        trig = json.loads(tr.read_text(encoding="utf-8")).get("triggers", [])
        pos = [t for t in trig if t.get("should_trigger") is True]
        neg = [t for t in trig if t.get("should_trigger") is False]
        if len(pos) < 3 or len(neg) < 3:
            f.append("triggers.json needs 3+ true and 3+ false cases (has %d/%d)" % (len(pos), len(neg)))


def check(skill, root=ROOT):
    f = []
    name = skill.name
    skill_md = skill / "SKILL.md"
    if not skill_md.is_file():
        return ["SKILL.md is missing"]
    text = skill_md.read_text(encoding="utf-8")
    fm, _ = frontmatter(text)
    if fm is None:
        return ["SKILL.md has no frontmatter"]

    def field(key):
        m = re.search(r"^%s:\s*(.*)$" % re.escape(key), fm, re.M)
        return m.group(1).strip() if m else None

    if (field("name") or "").strip("\"'") != name:
        f.append("frontmatter name %r is not the folder name %r" % (field("name"), name))
    if not re.fullmatch(r"[a-z0-9-]{2,64}", name):
        f.append("folder name %r must be 2-64 lowercase letters, digits, hyphens" % name)
    desc = field("description")
    if not desc or not (desc.startswith('"') and desc.endswith('"')):
        f.append("description must be one quoted string")
    elif "NOT for" not in desc or "Use " not in desc:
        f.append("description must say when to use it and carry a 'NOT for' clause")
    elif len(desc.strip('"')) > DESCRIPTION_MAX_CHARS:
        f.append("description has %d characters, the format allows %d" % (len(desc.strip('"')), DESCRIPTION_MAX_CHARS))
    if field("type") not in TYPES:
        f.append("type must be one of %s" % sorted(TYPES))
    if not field("lifecycle"):
        f.append("lifecycle is missing")
    version = (re.search(r"^\s+version:\s*\"?([^\"\n]+)\"?\s*$", fm, re.M) or [None, None])[1]
    if not version:
        f.append("metadata.version is missing")
    if not re.search(r'^\s+written-for:\s*"[^"]+"', fm, re.M):
        f.append("metadata.written-for is missing")
    if len(text.splitlines()) >= BODY_MAX_LINES:
        f.append("SKILL.md has %d lines, the limit is under %d" % (len(text.splitlines()), BODY_MAX_LINES))

    for req in ("CHANGELOG.md", "evals/evals.json", "evals/triggers.json", *("scripts/" + s for s in ENTRY_SCRIPTS)):
        if not (skill / req).is_file():
            f.append("required file missing: %s" % req)
    for bad in FORBIDDEN_FILES:
        if list(skill.rglob(bad)):
            f.append("forbidden file inside the skill: %s" % bad)

    cl = skill / "CHANGELOG.md"
    if cl.is_file() and version:
        m = re.search(r"^## \d{4}-\d{2}-\d{2} \(([^)]+)\)", cl.read_text(encoding="utf-8"), re.M)
        if not m or m.group(1) != version:
            f.append("CHANGELOG top entry %r does not match metadata.version %r" % (m.group(1) if m else None, version))

    corpus = {"SKILL.md": text}
    refs = sorted((skill / "references").rglob("*.md")) if (skill / "references").is_dir() else []
    for p in refs:
        corpus[str(p.relative_to(skill))] = p.read_text(encoding="utf-8")
    hand_written = sorted((words(p) for p in refs if "generated" not in p.parts and p.stem != "INDEX"), reverse=True)
    loaded = words(skill_md) + sum(hand_written[:2])
    if loaded > LOADED_MAX_WORDS:
        f.append("SKILL.md plus its two largest pages load %d words, the limit is %d" % (loaded, LOADED_MAX_WORDS))
    if sum(words(p) for p in [skill_md] + refs) > FOLDER_MAX_WORDS:
        f.append("SKILL.md plus every reference exceed %d words" % FOLDER_MAX_WORDS)
    for rel, t_ in corpus.items():
        if rel.startswith("references/generated/") and "<!-- GENERATED by " not in t_:
            f.append("%s is in references/generated/ but carries no GENERATED banner" % rel)

    index = skill / "references" / "INDEX.md"
    if len(refs) >= 3:
        if not index.is_file():
            f.append("3+ references need references/INDEX.md")
        else:
            linked = set(re.findall(r"\[\[([^\]]+)\]\]", index.read_text(encoding="utf-8")))
            for p in refs:
                if p.stem != "INDEX" and p.parent == index.parent and p.stem not in linked:
                    f.append("INDEX.md does not link [[%s]]" % p.stem)
    stems = {p.stem for p in refs}
    for rel, t in corpus.items():
        for link in re.findall(r"\[\[([^\]]+)\]\]", t):
            if link not in stems:
                f.append("%s: wikilink [[%s]] resolves to no reference" % (rel, link))
        for rl in re.findall(r"`((?:references|scripts)/[A-Za-z0-9_./-]+)`", t):
            if not (skill / rl).exists():
                f.append("%s: points to %s which does not exist" % (rel, rl))
        if rel not in ("SKILL.md", "references/INDEX.md") and frontmatter(t)[0] is None:
            f.append("%s: reference has no frontmatter" % rel)
    for rel, t in corpus.items():
        for url in re.findall(r"https?://[^\s)>\]`\"']+", t):
            if not url.startswith(ALLOWED_URLS) if ALLOWED_URLS else True:
                f.append("%s: link %s is not on the allowlist (no remote instructions, no public docs link)" % (rel, url))
        for ab in re.findall(r"(?<![\w.])/(?:home|Users|root|tmp)/\S+", t):
            f.append("%s: absolute path %s" % (rel, ab))

    for p in sorted(x for x in skill.rglob("*") if x.is_file() and x.suffix in (".md", ".json", ".py")):
        rel = str(p.relative_to(skill))
        if not rel.startswith("references/generated/"):
            f.extend(naming_findings(rel, p.read_text(encoding="utf-8")))
    check_evals(skill, corpus, f, root)
    return f


README_URLS = ("https://img.shields.io/badge/", "https://www.npmjs.com/package/skills")


def check_front_page(root, skill):
    """The README is the repo's front page: its badges, links and version table must state something true."""
    f = []
    readme = root / "README.md"
    if not readme.is_file():
        return ["README.md is missing"]
    text = readme.read_text(encoding="utf-8")
    for rel in ("CHANGELOG.md", "assets/SOURCES.md", "LICENSE"):
        if not (root / rel).is_file():
            f.append("%s is missing" % rel)
    for ref in re.findall(r'(?:src|srcset|href)="([^"#:]+)"', text) + re.findall(r"\]\(([^)#:\s]+)\)", text):
        if not (root / ref).exists():
            f.append("README.md points to %s which does not exist" % ref)
    for url in re.findall(r"https?://[^\s)>\]`\"']+", text):
        if not url.startswith(README_URLS):
            f.append("README.md carries the web address %s: only the badge host and the skills CLI page are allowed" % url)
    badges = {m[0]: m[1].replace("--", "-").replace("%20", " ") for m in re.findall(r"badge/([^/-]+)-((?:[^/-]|--)+)-[0-9a-f]{6}", text)}
    fm = frontmatter((skill / "SKILL.md").read_text(encoding="utf-8"))[0] or "" if (skill / "SKILL.md").is_file() else ""
    version = (re.search(r"^\s+version:\s*\"?([^\"\n]+)\"?\s*$", fm, re.M) or [None, None])[1]
    wf = (re.search(r'^\s+written-for:\s*"([^"]+)"', fm, re.M) or [None, None])[1]
    if badges.get("skill") != version:
        f.append("README.md skill badge %r does not match metadata.version %r" % (badges.get("skill"), version))
    if badges.get("model") != wf:
        f.append("README.md model badge %r does not match metadata.written-for %r" % (badges.get("model"), wf))
    if version and "| %s | %s |" % (version, wf) not in text:
        f.append("README.md version table has no row for skill %s" % version)
    if "npx skills@1.7.6 add vivid-allusion/%s-skill" % SKILL_NAME not in text:
        f.append("README.md has no pinned install line for this repo")
    if "badge/license-" in text and not any((root / n).is_file() for n in ("LICENSE", "LICENSE.md", "LICENSE.txt")):
        f.append("README.md shows a licence badge but there is no licence file")
    return f


def main():
    skill = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "skills" / SKILL_NAME
    findings = check(skill.resolve())
    if len(sys.argv) <= 1:
        findings += check_front_page(ROOT, skill.resolve())
    for line in findings:
        print("FAIL:", line)
    print("%s: %s" % (skill.name, "clean" if not findings else "%d finding(s)" % len(findings)))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
