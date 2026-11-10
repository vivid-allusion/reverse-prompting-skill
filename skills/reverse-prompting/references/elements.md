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
| `02_PROPS` | Object a person holds, uses or wears, or one the story needs seen |
| `03_ENVIRONMENTS` | Place as one plate shows it, with everything that stays put in it |
| `04_COSTUMES` | Clothing worth keeping the same, garment first and wearer last |
| `05_EXTRAS` | Background people, as the group of one scene |
| `06_VEHICLES` | Carries people or goods and acts in the scene |
| `07_MISC` | Weather, animals, effects |

## Prop, vehicle or environment

Every object in a still could be a prop. Raising one out of the place is a judgment of significance, per scene; the full rule is `helmer-story-breakdown`'s `categories` page. In short:

- **Held, used or worn, or the plot needs it seen: a prop.** A gun on the table nobody touches but the story turns on is a prop; the cards and open bottles beside it are the place.
- **Worked on or walked on, and stays put: the place.** The axe is a prop, the chopping block under it is the plate. The same for a table, a vat, an oven, a gangplank.
- **A vehicle only when it acts:** it drives or sails through the shot, carries someone in or out, fights, or the shot is about what it does.
- **On it or in it: the place.** The deck we stand on, the car we sit in.
- **Moored, parked or static: the place.** Ships in a harbour and the crane on the quay are the harbour's plate.

A prop or vehicle is a separate asset the video model must place at the right scale in the right spot. A fixture in the plate is already where it belongs.

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
