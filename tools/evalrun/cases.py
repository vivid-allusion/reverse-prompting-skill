#!/usr/bin/env python3
"""cases.py <skill-dir> <out.json> <plan.json> [workers]. plan.json: a list of [case id, run]. Resumes; the whole answers and tool calls are kept."""
import concurrent.futures as cf, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fired, session
skill, out_path, plan_path = sys.argv[1], sys.argv[2], sys.argv[3]
workers = min(int(sys.argv[4]) if len(sys.argv) > 4 else 2, 4)
C = {c["id"]: c for c in json.load(open(os.path.join(skill, "evals/evals.json")))["cases"]}
def one(c, k):
    s = c.get("setup", {})
    tools, text, init, err = session(c["prompt"], skill, 10, 500, s)
    pages = sorted({os.path.basename(str(t["input"].get("file_path", ""))) for t in tools if t["name"] == "Read"})
    return {"id": c["id"], "run": k, "prompt": c["prompt"], "assertions": c["assertions"], "fired": fired(tools), "pages": pages,
            "model": init.get("model"), "tools": [{"name": t["name"], "input": t["input"]} for t in tools], "answer": text, "stderr": err}
out = json.load(open(out_path)) if os.path.exists(out_path) else []
out = [r for r in out if "error" not in r]
done = {(r["id"], r["run"]) for r in out}
todo = [(C[i], k) for i, k in json.load(open(plan_path)) if (i, k) not in done]
print("to do", len(todo), flush=True)
with cf.ThreadPoolExecutor(workers) as ex:
    fs = {ex.submit(one, c, k): (c["id"], k) for c, k in todo}
    for f in cf.as_completed(fs):
        try:
            out.append(f.result())
        except Exception as e:
            out.append({"error": repr(e), "case": fs[f]})
        json.dump(out, open(out_path + ".tmp", "w"), indent=1)
        os.replace(out_path + ".tmp", out_path)
print("done", len(out), "errors", sum(1 for r in out if "error" in r), "fired", sum(1 for r in out if r.get("fired")))
