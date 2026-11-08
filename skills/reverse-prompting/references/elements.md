---
title: Elements and the ABOUT file
kind: reference
links: [hero, folders, canon-and-state, coverage]
---

# Elements

An element is anything that must be in front of the camera: a person, a garment, an object, a vehicle, a group, a place, or a thing that fits nowhere else. Categories and the split test are `helmer-story-breakdown`'s:

| Folder | One for each |
|---|---|
| `01_CAST` | Person with a face that must hold |
| `02_PROPS` | Object handled, or that the story turns on |
| `03_ENVIRONMENTS` | Place as one plate shows it |
| `04_COSTUMES` | Clothing worth keeping the same, garment first and wearer last |
| `05_EXTRAS` | Background people, as the group of one scene |
| `06_VEHICLES` | Anything that carries people or goods |
| `07_MISC` | Weather, animals, effects |

## The elements table in a shot file

```
| Element | Category | Role | Reason |
|---|---|---|---|
| @MARTA | 01_CAST | hero | |
| @COAT_MARTA | 04_COSTUMES | hero | On Marta's canon sheet |
| @TIN_BOX | 02_PROPS | hero | |
| @FERRY_CABIN | 03_ENVIRONMENTS | background | Close-up: background is blur |
| @ROPE | 02_PROPS | background | |
```

- **Role** is `hero` or `background`: [[hero]].
- **Reason** is filled only when a hero element has no prompt of its own: on a canon sheet, real photos are the reference, inside another sheet. The coverage script takes the reason in place of a prompt: [[coverage]].

## The ABOUT file

Each element folder holds `@NAME_ABOUT.md`:

```
# @NAME

One sentence: who or what.

- **Folder:** `02_PROPS/Scene_002`
- **Appears in:** SHOT_003, SHOT_004
- **State of:** _CANON/@NAME (when it recurs)

## What the stills show
- One fact per line, with its shot

## Decided
- The calls made

## Reference slots
- [ ] identity:
- [ ] construction:
```

Only what the stills, the story or the canon show goes in. A fact from outside them, a period uniform or a ritual object, is a slot to fill with a real photo, not an invention.
