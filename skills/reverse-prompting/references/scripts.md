---
title: The scripts
kind: reference
links: [inputs, coverage, prompt-files, folders]
---

# The scripts

Standard-library Python, run from the project folder. None of them generates, calls a model or uses the network.

| Script | Does | Writes |
|---|---|---|
| `scripts/scaffold.py` | Reads the shots table and lays out the map | `MAP/SCENES/Scene_NNN/SCENE.md`, `SHOT_NNN.md`, and with an `elements` column the element folders and ABOUT stubs, `_CANON` for what recurs |
| `scripts/coverage.py` | Reads the shot tables and the prompt tree | `MAP/COVERAGE.md`, `MAP/PROMPTS_INDEX.md`, each shot file's Prompts list |
| `scripts/check_prompts.py` | Checks every file under `PROMPTS/` | Nothing: prints findings, exit 1 on any |

## scaffold

```
python3 <skill>/scripts/scaffold.py shots.csv .
python3 <skill>/scripts/scaffold.py shots.md . --dry-run
```

It never overwrites a file a person has written: an existing file is reported as kept. Run it again after adding rows.

## coverage

```
python3 <skill>/scripts/coverage.py .
```

Exit 1 when any hero element is missing, so it can gate a batch.

## check_prompts

```
python3 <skill>/scripts/check_prompts.py .
python3 <skill>/scripts/check_prompts.py . --min-refs 1
```

Fails: a bare fence, an unclosed fence, a second text line outside a fence, a bare address line, a malformed embed, a start frame beside reference images, a note (an ABOUT, index, scene or shot note, a file starting with a heading) under `PROMPTS/`. With `--min-refs`, an image-linked file with fewer references.
