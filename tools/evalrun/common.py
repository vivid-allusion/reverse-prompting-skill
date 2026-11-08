"""Shared by the eval runners. Every session is a cold, real-model session in a throwaway project; none has a bypass.

A case's setup.project picks what the folder holds:
  fresh:  the example film's story.md and shots.csv only, as a person starts;
  worked: the whole example film, scaffolded, filled and with prompts (examples/the-last-ferry);
  none:   an empty folder.
setup.files adds or replaces files. Paths come from the environment: EVAL_RUNS (where throwaway projects go).
No session may spend: there are no keys in it, no model provider is called, and nothing generates.
"""
import json, os, shutil, subprocess, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXAMPLE = os.path.join(ROOT, "examples", "the-last-ferry")
SKILL_NAME = "reverse-prompting"
RUNS = os.environ.get("EVAL_RUNS", tempfile.gettempdir())
LOAD_LIMIT = float(os.environ.get("EVAL_LOAD_LIMIT", "11"))
DROP = ("CLAUDECODE", "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_MESSAGING_SOCKET",
        "CLAUDE_CODE_MESSAGING_TOKEN", "CLAUDE_PID", "CLAUDE_EFFORT", "CLAUDE_CODE_SESSION_ATTENDED",
        "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_EXECPATH")
READ_ONLY = ("Read,Glob,Grep,Skill,Bash(python3 *scaffold.py*),Bash(python3 *coverage.py*),Bash(python3 *check_prompts.py*),"
             "Bash(ls*),Bash(rg *),Bash(grep *),Bash(pwd),Bash(find . *),Bash(head *),Bash(tail *),Bash(cat *),Bash(sed -n *),Bash(wc *)")
WRITE = ",Write,Edit,Bash(mkdir *),Bash(cp *)"


def fill(root, setup):
    kind = setup.get("project", "worked")
    if kind == "worked":
        shutil.copytree(EXAMPLE, root, dirs_exist_ok=True)
    elif kind == "fresh":
        for name in ("story.md", "shots.csv"):
            shutil.copy(os.path.join(EXAMPLE, name), root)
    for rel, value in setup.get("files", {}).items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(value)


def project(root, skill, setup):
    os.makedirs(root + "/.claude/skills")
    shutil.copytree(skill, root + "/.claude/skills/" + SKILL_NAME, ignore=shutil.ignore_patterns("__pycache__", "evals"))
    subprocess.run(["git", "init", "-q", root])
    fill(root, setup)


def calm():
    """Wait while the box is busy."""
    while float(open("/proc/loadavg").read().split()[0]) >= LOAD_LIMIT:
        time.sleep(15)


def session(prompt, skill, turns, timeout, setup=None):
    setup = setup or {}
    calm()
    root = tempfile.mkdtemp(prefix="rp-", dir=RUNS)
    try:
        project(root, skill, setup)
        env = {x: y for x, y in os.environ.items() if x not in DROP}
        cmd = ["claude", "-p", prompt, "--model", "sonnet", "--setting-sources", "project", "--output-format",
               "stream-json", "--verbose", "--max-turns", str(turns), "--allowedTools", READ_ONLY + (WRITE if setup.get("allow_write") else "")]
        p = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
        tools, text, init = [], "", {}
        for line in p.stdout.splitlines():
            try:
                j = json.loads(line)
            except ValueError:
                continue
            if j.get("type") == "system" and j.get("subtype") == "init":
                init = {"skills": j.get("skills"), "model": j.get("model")}
            if j.get("type") == "assistant":
                for b in j["message"]["content"]:
                    if b.get("type") == "tool_use":
                        tools.append({"name": b["name"], "input": b["input"]})
                    elif b.get("type") == "text":
                        text = b["text"]
            if j.get("type") == "result":
                text = j.get("result") or text
        return tools, text, init, p.stderr[-300:]
    finally:
        shutil.rmtree(root, ignore_errors=True)


def fired(tools):
    return any(t["name"] == "Skill" and t["input"].get("skill") == SKILL_NAME for t in tools)
