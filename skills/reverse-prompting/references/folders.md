---
title: The folders
kind: reference
links: [canon-and-state, elements, prompt-files, coverage, scenes, picks]
---

# Where every file goes

```
02_PRE-PRODUCTION/
  01_CAST/ 02_PROPS/ 03_ENVIRONMENTS/ 04_COSTUMES/ 05_EXTRAS/ 06_VEHICLES/ 07_MISC/
    _CANON/@NAME/@NAME_ABOUT.md
    Scene_NNN/@NAME/@NAME_ABOUT.md
MAP/
  SCENES/Scene_NNN/SCENE.md
  SCENES/Scene_NNN/SHOT_NNN.md
  COVERAGE.md
  PROMPTS_INDEX.md
PROMPTS/
  <MODEL>/<category>/Scene_NNN/@NAME.md
  <MODEL>/<category>/_CANON/@NAME.md
  VIDEO/Scene_NNN/SHOT_NNN.md
  VIDEO/Scene_NNN/SHOTS_NNN-NNN.md
```

## The rules of the tree

- **Every element sits under a scene folder** inside its category: `02_PROPS/Scene_002/@TIN_BOX/`. Nothing sits loose in a category.
- **A recurring element** also has `_CANON/@NAME/`: [[canon-and-state]].
- **Categories** are the seven of `helmer-story-breakdown`, with its numbers; its split test decides when one thing is two.
- **Names:** `@` and capitals with underscores, the script's name where it has one. A costume is garment first, wearer last: `@COAT_MARTA`. One `@NAME` in the asset folder, the prompt file and every table.
- **Shot files** are `SHOT_NNN.md` with the film's shot number, inside their scene's folder.
- **Prompt files** mirror the asset tree under a model folder: [[prompt-files]]. One model folder is what one generator reads.
- **`MAP/`** holds notes: scene and shot files, the coverage table, the index. **`PROMPTS/`** holds prompt files and nothing else.

## Why scene first

A plate, an extras sheet and a cast state belong to a scene, not to the film. With the scene as parent, the folder says which scene an asset was made for, two scenes can each hold `@HARBOUR` without colliding, and `Scene_002/` across the categories is the whole scene's asset list.

## The ABOUT file

`@NAME_ABOUT.md` is the element's record: [[elements]]. Its reference slots hold the addresses of the picks: [[picks]].

## Copying into a project

`02_PRE-PRODUCTION/` is the project's own folder: pictures put there are synced and get addresses, and `.md` files are not uploaded. `MAP/` sits beside it. A generator's input path points at one model folder under `PROMPTS/`.
