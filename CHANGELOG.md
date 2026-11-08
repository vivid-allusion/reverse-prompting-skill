# Changelog

## 2026-11-08 (0.1.2)
- The skill points at `cast-character-sheet` and `extras-character-sheet`, and its eval evidence names the new folder.

## 2026-11-08 (0.1.1)
- The skill's video prompts are written for Seedance 2.5 again; only the folder name is model-free.

Changes to this repo. The skill's own releases are recorded in [`skills/reverse-prompting/CHANGELOG.md`](skills/reverse-prompting/CHANGELOG.md) and are not repeated here.

## 2026-11-08
- First commit: the skill (0.1.0), its three scripts, an example film, evals, the gate and its tests, shaped like `vivid-allusion/helmer-skill`.
- `tools/validate.py` is the house gate with this repo's changes: a model badge in place of the app range, the entry scripts required, `repo` evidence checked in CI, and a refusal of a real project's names in a generic skill.
- `tools/check_names.py` searches this repo's scripts, examples and tools, and sibling skills given with `--tree`; the skill's own prose cannot vouch for itself. `tools/check_evidence.py` checks the evals against the same trees.
- `tools/evalrun/` runs the evals in real-model sessions in throwaway copies of the example film and grades them.
- `docs/walkthrough.md` follows the example film from its shots table to its video prompts.
