---
title: Canon and state
kind: reference
links: [folders, characters, props-vehicles, elements]
---

# A recurring character or object

Anything that appears in two or more scenes and must stay itself has **one canon** and **one state per scene**.

| Folder | Holds | Its prompt |
|---|---|---|
| `<category>/_CANON/@NAME/` | Who or what it is, always: face, build, construction | The sheet that is the truth, under `_CANON/` in a model folder |
| `<category>/Scene_NNN/@NAME/` | How it is in this scene: costume, wet, wounded, aged, open, broken | Only when the state changes the picture, under `Scene_NNN/` in a model folder, built on the canon |

The scene folder's ABOUT says `State of: _CANON/@NAME` and what differs. If nothing differs it says so, and no scene prompt is written: the canon covers it.

## Rules

- **The canon sheet is the truth.** Where a still or the script disagrees with it, the sheet wins and the disagreement goes in the ABOUT.
- **A real actor's face comes only from their own photos or sheet,** never from a still.
- **A state sheet is built around the canon:** the canon attached as identity, the change described in words. The canon is never regenerated to make a state.
- **A costume** worn in one scene sits in that scene's `04_COSTUMES/Scene_NNN/`. A costume worn across scenes has a canon too.
- **One-scene elements** have no canon: their scene folder is the truth.

## Deciding canon

The scaffold makes a canon for every element listed in two or more scenes. Add one by hand for an element seen once that the story needs again.
