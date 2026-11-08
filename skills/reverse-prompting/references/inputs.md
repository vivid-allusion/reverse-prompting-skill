---
title: What the person brings
kind: reference
links: [scripts, scenes, reading-a-still, folders, models]
---

# What goes in

## The shots table

One row per still, in story order. CSV or a Markdown table, the same columns:

| Column | Holds | Required |
|---|---|---|
| `shot` | The shot's number in the film: `1`, `2`, `14`. Written as `SHOT_001` | yes |
| `scene` | The number of the scene it belongs to: `1`, `2` | yes |
| `still` | The still's public web address | yes |
| `motion` | The old motion line written for the still | no |
| `scene_title` | A slugline for the scene: `EXT. HARBOUR - DAWN` | no |
| `elements` | Elements seen, as `@NAME:CATEGORY:role` joined by `;` | no |

`CATEGORY` is one of `CAST`, `PROPS`, `ENVIRONMENTS`, `COSTUMES`, `EXTRAS`, `VEHICLES`, `MISC`. `role` is `hero` (the default) or `background`. The scaffold turns the table into the scene and shot files and the folders: [[scripts]].

Write the table by looking at the stills, or let the person write it. A still whose scene is unclear goes in the scene of the shot before it: [[scenes]].

## The stills

- One still per shot. Two stills of one shot are one row, with the kept one.
- Each needs a **public web address**: image models take references by address only. A still on disk is invisible to them until it is uploaded.
- They are the storyboard, not the look: [[reading-a-still]].

## The story

The story or script gives the names. A person, place or object it names takes that name as its `@NAME`, so a later script breakdown reuses the same folders. Elements it does not name get a plain name for what they are: `@HARBOUR_WORKERS`, `@TIN_BOX`.

## The look and the models

The project's own skill or brief sets format, stock, lens, light and any model choices. Where it is silent, the defaults are on [[models]] and the method is the `cinematic-realism` skill.

## Where the work is written

Into the project folder: `02_PRE-PRODUCTION/`, `MAP/` and `PROMPTS/` side by side. A working folder that mirrors those three is fine; it is copied in whole when the assets are ready: [[folders]].
