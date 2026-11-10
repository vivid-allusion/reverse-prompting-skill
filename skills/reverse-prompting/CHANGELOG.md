# Changelog

## 2026-11-10 (0.1.10)
- Cast sheets show the costume on a ghost mannequin front and back; the face is in the close-up only.

## 2026-11-10 (0.1.9)
- Never write the aspect ratio in a prompt; it is the generator's setting.

## 2026-11-10 (0.1.8)
- A person a shot is about is cast, named or not, with a single sheet made from the still in the short keyframe form. Extras are the people around and behind.

## 2026-11-10 (0.1.7)
- A plate names the shot's hero in the removal, or the model keeps them. The person a shot is about gets a sheet of their own, even with others in frame.

## 2026-11-10 (0.1.6)
- From a keyframe, asset prompts are short. A plate is an edit of the still: "remove all the people, keep the traffic", no re-description, no look or negative block. A prop or vehicle is lifted out of the still and shown on its own in natural overcast daylight; only what the still cannot show is written. The example's prompts are rewritten that way.

## 2026-11-10 (0.1.5)
- Every shot has a plate behind it, close-ups too: a close-up uses its scene's plate for the side it faces, or gets its own from its still. The "background is blur, no plate" exemption is gone.

## 2026-11-10 (0.1.4)
- A prop is held or used, not worn. The hero's car is a vehicle; street traffic is the plate.

## 2026-11-10 (0.1.3)
- Prop, vehicle or environment: a vehicle only when it acts; what stays put, moored or parked, and the vehicle a scene plays on, is the plate. The crane example is corrected.

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
