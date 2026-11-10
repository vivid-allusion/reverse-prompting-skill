---
name: "reverse-prompting"
description: "Load before turning a film's animatic stills into the assets a video model needs: reverse prompting. Use when a person has a cheap generated still of every shot and wants each scene broken into cast, costumes, props, vehicles, extras, environments and misc under Scene_NNN folders, asset prompt files written per model, a coverage table so nothing drops, takes picked, and video prompts that rebuild each scene, one shot or many, in the project's video model. Also for: setting up the scene and shot map from a shots table, the hero of a shot, plates per scene and camera side, extras group sheets per scene, which model makes which asset, and rebuilding COVERAGE.md. NOT for writing a story or script, breaking a written script into folders with no stills (helmer-story-breakdown), the photoreal prompt method itself (cinematic-realism), one sheet alone (cast-character-sheet, extras-character-sheet), or pressing Generate."
type: workflow
lifecycle: active
metadata:
  version: "0.1.10"
  written-for: "Seedance 2.5"
---

# Reverse prompting: from animatic stills to scenes you can build

A still costs cents and a video generation costs dollars. So the film is tested first as stills: one generated frame for every shot, an animatic. When the story holds, each still is taken apart into what the video model needs to rebuild the shot on purpose: a character sheet, a costume, a prop, a vehicle, an extras sheet, an empty plate of the place. Those assets are generated, picked and locked, and only then is video generated, from the assets, scene by scene. Reverse prompting is the taking apart, and the bookkeeping that keeps every piece in its scene.

The stills are a storyboard, not a look. They decide content, order and shot size. Everything they show is rebuilt in the project's own look, through the asset sheets and the video prompt.

## What goes in, what comes out

| In | Out |
|---|---|
| The story or script, for names and scene order | `MAP/SCENES/Scene_NNN/SCENE.md` and `SHOT_NNN.md`: what each scene and shot holds |
| A shots table: shot, scene, still address, old motion line | `02_PRE-PRODUCTION/<category>/Scene_NNN/@NAME/`: one folder per element per scene, plus `_CANON` for recurring ones |
| One public still address per shot | `PROMPTS/<MODEL>/<category>/Scene_NNN/@NAME.md`: asset prompt files, one folder per model |
| The project's look and model choices | `MAP/COVERAGE.md` and `MAP/PROMPTS_INDEX.md`, rebuilt by a script |
| The person's picks, later | `PROMPTS/VIDEO/Scene_NNN/`: the video prompts, picks attached |

## The run

`<skill>` is this skill's folder. Run scripts from the project folder.

1. **Get the shots table.** One row per still: `shot`, `scene`, `still`, `motion`, optional `elements`. `references/inputs.md`.
2. **Scaffold.** `python3 <skill>/scripts/scaffold.py shots.csv .` writes the scene and shot files and the empty scene folders. It never overwrites a file. `references/scripts.md`.
3. **Cut and number the scenes.** A scene is one continuous place and time; its shots share a place, a light and the cast's state. Several stills can be one scene. Fill each `SCENE.md`. `references/scenes.md`.
4. **Read every still literally** into its `SHOT_NNN.md`: what is in frame, what is out of frame by its effect, and the hero. `references/reading-a-still.md`, `references/hero.md`.
5. **List the elements** of each shot in its table with a role: `hero` or `background`. Only hero elements get assets. `references/elements.md`.
6. **File them by scene.** Every element sits in `<category>/Scene_NNN/@NAME/`. One that recurs also gets `<category>/_CANON/@NAME/`, whose sheet is the truth; each scene folder holds only that scene's state. `references/folders.md`, `references/canon-and-state.md`.
7. **Route each asset to a model** and write its prompt file in that model's folder. `references/models.md`, then the page for the kind: `references/environments.md`, `references/characters.md`, `references/extras.md`, `references/props-vehicles.md`.
8. **Check and count.** `python3 <skill>/scripts/check_prompts.py .` then `python3 <skill>/scripts/coverage.py .`. Missing elements lead the report. `references/coverage.md`.
9. **The person generates and picks.** Picks get public addresses and go into the reference slots. `references/picks.md`.
10. **Write the video prompts,** one per scene beat or one per shot, picks attached by role. `references/video-prompts.md`.

Rebuild coverage after every batch. Make the small calls yourself and write them down: `references/decisions.md`.

## The folders

```
02_PRE-PRODUCTION/
  01_CAST/  02_PROPS/  03_ENVIRONMENTS/  04_COSTUMES/  05_EXTRAS/  06_VEHICLES/  07_MISC/
    _CANON/@NAME/@NAME_ABOUT.md          recurring element: the truth
    Scene_NNN/@NAME/@NAME_ABOUT.md       this scene's element or state
MAP/
  SCENES/Scene_NNN/SCENE.md
  SCENES/Scene_NNN/SHOT_NNN.md
  COVERAGE.md   PROMPTS_INDEX.md
PROMPTS/
  <MODEL>/<category>/Scene_NNN/@NAME.md
  <MODEL>/<category>/_CANON/@NAME.md
  VIDEO/Scene_NNN/SHOT_NNN.md | SHOTS_NNN-NNN.md
```

Notes never sit in `PROMPTS/`: every `.md` in a generator's input folder is a job.

## The rules that run all of it

- **The hero of the shot gets the assets.** The character in focus and what a prominent character handles, wears or rides. Background is left to the video prompt. `references/hero.md`.
- **Nothing drops silently.** Every hero element has a prompt file or a stated reason in `MAP/COVERAGE.md`. Gaps lead every report. `references/coverage.md`.
- **A plate belongs to one scene.** Never merge stills from different scenes into one plate or one extras sheet. Every shot has a plate behind it, close-ups too: a close-up uses its scene's plate for the side it faces, or gets its own. `references/environments.md`.
- **A person a shot is about is cast,** named or not: whoever the director would direct gets a single sheet of their own: costume on a ghost mannequin front and back, the face in the close-up only. `references/characters.md`.
- **Extras are per scene,** only the people seen together; one person alone gets a single sheet; each person carries the nationality of the scene's country. `references/extras.md`.
- **From a keyframe, asset prompts are short.** The still holds the place and the objects; the prompt only says what to take out or take away. A plate is an edit: "remove all the people, keep the traffic". A prop is lifted out and shown on its own in natural light. `references/environments.md`, `references/props-vehicles.md`.
- **Describe the frame, not the situation.** The method is the `cinematic-realism` skill.
- **Never write the aspect ratio in a prompt: it is set in the generator's aspect setting.**
- **Prompt files follow the `helmer-md` skill.** `references/prompt-files.md`.

## Where the rest is

Everything: `references/INDEX.md`.

| Asked about | Open |
|---|---|
| Why stills first; the whole loop | `references/method.md` |
| The shots table; what the person brings | `references/inputs.md` |
| Scene or shot; numbering; multi-shot scenes | `references/scenes.md` |
| The tree, names, where a file goes | `references/folders.md` |
| A recurring character or object; its state per scene | `references/canon-and-state.md` |
| Reading a still; the storyboard-not-look rule | `references/reading-a-still.md` |
| What gets an asset | `references/hero.md` |
| Element roles, categories, the ABOUT file | `references/elements.md` |
| Plates; camera sides; close-ups | `references/environments.md` |
| Leads and small roles | `references/characters.md` |
| Group sheets, nationality | `references/extras.md` |
| Props and vehicles | `references/props-vehicles.md` |
| Which model makes what | `references/models.md` |
| Prompt-file syntax and folders | `references/prompt-files.md` |
| The coverage table | `references/coverage.md` |
| Generating, picking, addresses | `references/picks.md` |
| The video prompts | `references/video-prompts.md` |
| Making calls without asking | `references/decisions.md` |
| The scripts | `references/scripts.md` |
| A word | `references/glossary.md` |
| Where each rule comes from | `references/evidence.md` |

## How to sound

Like a first AD with a contact sheet: which scene, which shot, who the hero is, which file makes it. Lead with what is missing, then what was decided, then the counts.

## Rules that do not bend

- **Never write a note, an ABOUT file or an index into `PROMPTS/`.**
- **Never merge two scenes into one plate or one extras sheet.**
- **Never end a batch without rebuilding `MAP/COVERAGE.md`,** and never report it with the gaps at the bottom.
- **Never generate.** Write and fix prompts; generation is the person's press and their money.
