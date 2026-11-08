"""Shared by the reverse-prompting scripts. Standard library only; nothing here writes or uses the network."""
import csv
import io
import re
from pathlib import Path

CATEGORIES = {
    "CAST": "01_CAST",
    "PROPS": "02_PROPS",
    "ENVIRONMENTS": "03_ENVIRONMENTS",
    "COSTUMES": "04_COSTUMES",
    "EXTRAS": "05_EXTRAS",
    "VEHICLES": "06_VEHICLES",
    "MISC": "07_MISC",
}
FOLDERS = tuple(CATEGORIES.values())
ROLES = ("hero", "background")
PRE = "02_PRE-PRODUCTION"
CANON = "_CANON"
VIDEO = "VIDEO"
NOTE_NAMES = re.compile(r"(_ABOUT|^README|^INDEX|^COVERAGE|^BREAKDOWN|^SCENE|^PROMPTS_INDEX)$", re.I)


def natural_key(text):
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", str(text))]


def scene_dir(value):
    value = str(value).strip()
    if re.fullmatch(r"(?i)scene_?\d+", value):
        value = re.sub(r"\D", "", value)
    if not value.isdigit():
        raise ValueError("scene %r is not a number" % value)
    return "Scene_%03d" % int(value)


def shot_name(value):
    value = str(value).strip()
    if re.fullmatch(r"(?i)shot_?\d+", value):
        value = re.sub(r"\D", "", value)
    if value.isdigit():
        return "SHOT_%03d" % int(value)
    return "SHOT_" + re.sub(r"[^A-Za-z0-9.]+", "_", value)


def shot_number(name):
    m = re.fullmatch(r"SHOT_(\d+)", name)
    return int(m.group(1)) if m else None


def category_folder(value):
    value = value.strip().upper()
    if value in CATEGORIES:
        return CATEGORIES[value]
    if value in FOLDERS:
        return value
    raise ValueError("category %r is not one of %s" % (value, ", ".join(CATEGORIES)))


def parse_elements(cell):
    """'@NAME:CATEGORY[:role]; …' -> [(name, folder, role)]."""
    out = []
    for item in (cell or "").split(";"):
        item = item.strip()
        if not item:
            continue
        parts = [p.strip() for p in item.split(":")]
        if len(parts) < 2 or not parts[0].startswith("@"):
            raise ValueError("element %r must be @NAME:CATEGORY[:role]" % item)
        role = (parts[2] if len(parts) > 2 else "hero").lower()
        if role not in ROLES:
            raise ValueError("element %r: role must be hero or background" % item)
        out.append((parts[0], category_folder(parts[1]), role))
    return out


def read_table(path):
    """A shots table as CSV or a Markdown table -> list of dicts with lowercase keys."""
    text = Path(path).read_text(encoding="utf-8")
    if Path(path).suffix.lower() == ".csv":
        rows = list(csv.DictReader(io.StringIO(text)))
    else:
        lines = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
        if len(lines) < 2:
            raise ValueError("%s holds no Markdown table" % path)
        cells = lambda l: [c.strip() for c in l.strip("|").split("|")]
        head = cells(lines[0])
        rows = [dict(zip(head, cells(l))) for l in lines[2:]]
    rows = [{(k or "").strip().lower(): (v or "").strip() for k, v in r.items()} for r in rows]
    for need in ("shot", "scene", "still"):
        if rows and need not in rows[0]:
            raise ValueError("the shots table needs a %r column" % need)
    return rows


def elements_table(text):
    """The rows of a shot file's '## Elements' table -> [(name, folder, role, reason)]."""
    m = re.search(r"^## Elements\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    out = []
    if not m:
        return out
    for line in m.group(1).splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not cells[0].startswith("@"):
            continue
        out.append((cells[0], cells[1], cells[2].lower(), cells[3] if len(cells) > 3 else ""))
    return out


# --- prompt files, as the helmer-md skill describes both generators' parsers ---------------------------

EMBED = re.compile(r"^!\[([^\]]*)\]\((\S+)\)$")
COMMENT = re.compile(r"<!--.*?-->", re.S)
FENCE_OPEN = re.compile(r"^```\s*prompt\s*$", re.I)
FENCE_BARE = re.compile(r"^```\s*$")
DIRECTIVE = re.compile(r"^(duration|frames):\s*\S+", re.I)
PRIMARY_ALTS = {"", "img", "image", "video", "src", "source", "media", "input"}
REF_ALTS = {"reference_images", "ref", "reference_image_urls"}


def strip_studio_block(lines):
    end = len(lines) - 1
    while end >= 0 and not lines[end].strip():
        end -= 1
    if end < 0 or not re.fullmatch(r"-{3,}", lines[end].strip()):
        return lines
    start = end - 1
    while start >= 0 and not re.fullmatch(r"-{3,}", lines[start].strip()):
        start -= 1
    inner = [l for l in lines[start + 1:end] if l.strip()]
    if start >= 0 and inner and re.match(r"^studio:(\s|$)", inner[0].strip()):
        return lines[:start]
    return lines


def read_prompt(text):
    """-> {'prompt', 'embeds': [(alt, url)], 'errors': [], 'warnings': []} in the shape both generators read."""
    errors, warnings, embeds = [], [], []
    lines = strip_studio_block(COMMENT.sub("", text).split("\n"))
    prompt, seen, i = "", False, 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if not seen:
            if EMBED.fullmatch(s):  # a leading embed is the bookmark, never a reference
                i += 1
                continue
            seen = True
            if FENCE_OPEN.match(s):
                j = i + 1
                while j < len(lines) and not FENCE_BARE.match(lines[j].strip()):
                    j += 1
                if j >= len(lines):
                    errors.append("line %d: the ```prompt fence is never closed" % (i + 1))
                    prompt = "\n".join(l.strip() for l in lines[i + 1:]).strip()
                    break
                prompt = "\n".join(l.strip() for l in lines[i + 1:j]).strip()
                if not prompt:
                    errors.append("line %d: the ```prompt fence is empty (the video generator rejects it)" % (i + 1))
                i = j + 1
                continue
            if FENCE_BARE.match(s):
                errors.append("line %d: a bare ``` fence: the video generator reads the backticks as the prompt; open with ```prompt" % (i + 1))
                i += 1
                continue
            if s.startswith("#"):
                errors.append("line %d: the prompt starts with a heading: this looks like notes, not a prompt" % (i + 1))
            prompt = s
            i += 1
            continue
        m = EMBED.fullmatch(s)
        if m:
            alt, url = m.group(1).strip(), m.group(2)
            if not url.startswith("https://"):
                errors.append("line %d: an embed that is not an https address: %s" % (i + 1, url))
            else:
                embeds.append((alt, url))
        elif s.startswith("http://") or s.startswith("https://"):
            errors.append("line %d: a bare address line: the video generator drops it; write ![ref](address)" % (i + 1))
        elif DIRECTIVE.match(s):
            pass
        elif re.search(r"! +\[|\] +\(|<img|(?<!!)\[[^\]]*\]\(https?://", s):
            errors.append("line %d: a malformed embed: %s" % (i + 1, s[:60]))
        else:
            errors.append("line %d: a second text line outside the fence is dropped: %s" % (i + 1, s[:60]))
        i += 1
    if not seen:
        errors.append("no prompt text")
    alts = {a.lower() for a, _ in embeds}
    if alts & REF_ALTS and alts & PRIMARY_ALTS:
        errors.append("a start frame and reference images in one file: the video generator refuses it")
    return {"prompt": prompt, "embeds": embeds, "errors": errors, "warnings": warnings}


def is_video(rel):
    top = Path(rel).parts[0] if Path(rel).parts else ""
    return top.upper() == VIDEO


def first_line(prompt, width=90):
    line = next((l for l in prompt.splitlines() if l.strip()), "")
    line = re.sub(r"^(A STILL PHOTOGRAPH — |A real photograph of |STRICT CONSISTENCY task\. )", "", line)
    return (line[:width].rstrip(" ,;:") + ("…" if len(line) > width else "")).replace("|", "/")
