# Changelog

## 2026-11-08 (0.1.2)
- Points at the sheet skills under their new names, `cast-character-sheet` and `extras-character-sheet`; the eval evidence follows the new folder.

## 2026-11-08 (0.1.1)
- Video prompts are written for Seedance 2.5 (reference slots, @Image numbering, duration); the folder stays `PROMPTS/VIDEO/`.

## 2026-11-08 (0.1.0)
- First version. Reverse prompting: a film tested as one still per shot, then each still taken apart into the assets a video model needs, filed scene first, made per model, counted in a coverage table, picked, and rebuilt as video scene by scene.
- `SKILL.md` carries the run and the rules; one-topic pages cover the method, inputs, scenes, folders, canon and state, reading a still, the hero rule, elements, plates, characters, extras, props and vehicles, model routing, prompt files, coverage, picks, video prompts, decisions, the scripts, a glossary and the evidence.
- The folder rule: every element under `02_PRE-PRODUCTION/<category>/Scene_NNN/@NAME/`, a recurring one also under `_CANON/@NAME/`; scene and shot notes under `MAP/SCENES/Scene_NNN/`; prompts under `PROMPTS/<MODEL>/<category>/Scene_NNN/`. Scenes of many shots are supported.
- `scripts/scaffold.py`, `scripts/coverage.py`, `scripts/check_prompts.py`: standard library, tested against an invented three-scene film in `examples/the-last-ferry/`.
- Not yet run in real-model sessions: the evals are written, not graded.
