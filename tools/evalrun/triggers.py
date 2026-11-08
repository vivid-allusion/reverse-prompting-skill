#!/usr/bin/env python3
"""triggers.py <skill-dir> <out.json> <runs> <max-turns> [workers]. A load is a Skill call for reverse-prompting."""
import concurrent.futures as cf, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fired, session
skill, out_path, runs, turns = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
workers = min(int(sys.argv[5]) if len(sys.argv) > 5 else 2, 4)
T = json.load(open(os.path.join(skill, "evals/triggers.json")))["triggers"]
def one(t, k):
    tools, text, init, err = session(t["phrase"], skill, turns, 300, {"project": "fresh"})
    return {"phrase": t["phrase"], "should": t.get("should_trigger"), "run": k, "fired": fired(tools)}
out = json.load(open(out_path)) if os.path.exists(out_path) else []
out = [r for r in out if "error" not in r]
done = {(r["phrase"], r["run"]) for r in out}
with cf.ThreadPoolExecutor(workers) as ex:
    for f in cf.as_completed([ex.submit(one, t, k) for t in T for k in range(runs) if (t["phrase"], k) not in done]):
        try:
            out.append(f.result())
        except Exception as e:
            out.append({"error": repr(e)})
        json.dump(out, open(out_path + ".tmp", "w"))
        os.replace(out_path + ".tmp", out_path)
ok = [r for r in out if "error" not in r and r["fired"] == r["should"]]
print("right", len(ok), "of", len(out))
