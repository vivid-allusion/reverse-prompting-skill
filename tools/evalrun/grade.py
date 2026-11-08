#!/usr/bin/env python3
"""grade.py <answers.json> <evals.json> <skill-dir> <out.jsonl> [workers]. A strict model grades each run against the checks in evals.json.

No word-for-word rule: a 'says' is a fact in the answer, in any words; a 'text' is a name to be recognisably there. The grader sees whole tool calls,
and a list of the backticked words in the answer that appear nowhere in the skill, so "named something not in the docs" is judged on evidence."""
import concurrent.futures as cf, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import calm
src, evals_path, skill, out_path = sys.argv[1:5]
workers = min(int(sys.argv[5]) if len(sys.argv) > 5 else 2, 4)
C = {c["id"]: c for c in json.load(open(evals_path))["cases"]}
corpus = ""
for d, _, fs in os.walk(skill):
    if "evals" in d:
        continue
    for f in fs:
        if f.endswith(".md"):
            corpus += open(os.path.join(d, f)).read().lower()
RULES = ("You are grading one run of an assistant against assertions. Be strict about facts; give no credit for intent. Other words than the assertion's are fine.\n"
         "says: the answer carries this fact, as a claim, for this situation. A 'name:' must be recognisably named: case, quoting and punctuation do not matter, a different thing does.\n"
         "not_says: the answer does not itself claim this about the person's situation. Naming it to rule it out, or a separate case it says is not theirs, is not a claim.\n"
         "ran/read/checked: the tool calls show it; a tool call that was refused does not count, unless the assertion allows it.\n"
         "says_one_line: the answer says this in a line.\n\n")
def names_absent(answer):
    return sorted({n for n in re.findall(r"`([^`\n]{2,60})`", answer) if n.lower() not in corpus})[:30]
def grade(x):
    tl = "\n".join("- %s %s" % (t["name"], json.dumps(t["input"])[:1500]) for t in x["tools"])
    asserts = [{"n": i, "kind": a["kind"], "desc": a.get("what") or ("name: " + a["text"])} for i, a in enumerate(C[x["id"]]["assertions"])]
    prompt = (RULES + "QUESTION:\n%s\n\nTOOL CALLS:\n%s\n\nANSWER:\n%s\n\nBACKTICKED WORDS IN THE ANSWER FOUND NOWHERE IN THE SKILL'S DOCUMENTATION (every other backticked word is in it):\n%s\n\nASSERTIONS:\n%s\n\n"
              "Reply with only a JSON list: [{\"n\": <n>, \"pass\": true|false, \"why\": \"<short>\"}]") % (x["prompt"], tl, x["answer"], json.dumps(names_absent(x["answer"])), json.dumps(asserts))
    res = None
    for _ in range(3):
        calm()
        p = subprocess.run(["claude", "-p", prompt, "--model", "sonnet", "--setting-sources", "project", "--tools", "", "--max-turns", "2"],
                           capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL, cwd=os.environ.get("EVAL_RUNS", "/tmp"))
        t = p.stdout
        try:
            res = {g["n"]: g for g in json.loads(t[t.index("["):t.rindex("]") + 1])}
            break
        except ValueError:
            pass
    for a in asserts:
        g = (res or {}).get(a["n"])
        a.update({"pass": bool(g and g["pass"]), "why": g.get("why", "") if g else "grader failed", "grader_failed": not g})
    return {"id": x["id"], "run": x["run"], "fired": x["fired"], "pages": x["pages"], "asserts": asserts}
R = [x for x in json.load(open(src)) if "error" not in x and x["id"] in C]
done = set()
if os.path.exists(out_path):
    for l in open(out_path):
        g = json.loads(l)
        if not any(a.get("grader_failed") for a in g["asserts"]):
            done.add((g["id"], g["run"]))
todo = [x for x in R if (x["id"], x["run"]) not in done]
print("to grade", len(todo), flush=True)
with cf.ThreadPoolExecutor(workers) as ex:
    for g in ex.map(grade, todo):
        open(out_path, "a").write(json.dumps(g) + "\n")
print("done")
