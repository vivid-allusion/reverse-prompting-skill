---
title: Environment plates
kind: reference
links: [scenes, hero, models, prompt-files, reading-a-still]
---

# Environment plates

A plate is the place with nobody in it, in the project's look, from where the scene's camera stands. It is the environment reference the video model rebuilds the scene in.

## How many

- **One plate per scene per camera side.** A scene shot from two sides (the window wall and the door wall) needs two plates: `@FERRY_CABIN_A`, `@FERRY_CABIN_B`. A scene shot from one side needs one, however many stills it has.
- **A plate belongs to one scene.** Two scenes in the same kind of place, or the same place at another time, get two plates. Never merge stills from different scenes into one plate.
- **A close-up whose background is blur gets no plate.** Its shot table marks the place `background`, reason `Close-up: background is blur`.

## Built from the stills

Start from the scene's stills of that side; pick the one that shows most of the place. The plate keeps the architecture, the layout, the materials, the clutter that belongs to the place, and the time and weather. It keeps what stays put where it stands: the chopping block, the table, the vat, the gangplank from the boat to the quay, moored ships, the crane, a parked lorry, the deck the camera stands on. Never put those in the plate's negative: [[elements]]. It drops the people, the still's look, and light sources placed as decoration.

## The prompt's shape

```prompt
A STILL PHOTOGRAPH — a frame from [the project's format], of [the place], empty. Nobody in it.

COMPOSITION: camera at [height], [where it stands], looking [direction]; [off-centre, canted].
FOREGROUND: … MIDDLE GROUND: … BACKGROUND: …
THE GROUND AND MATERIALS: …
LIGHT — [one source, direction, falloff]; [sources out of frame, by effect].
FILM LOOK: [the project's style, lens and capture blocks, pasted]
NEGATIVE: people, a figure, a silhouette, hands, [the still's AI look], [text and signs], …
```

then `![ref](<still address>)` below the fence. The method for each block is the `cinematic-realism` skill; deep focus for a plate.

## Which model

Both Seedream and GPT Image, then pick: [[models]]. Soul does badly on environments.

## Files

`PROMPTS/SEEDREAM-5.0/03_ENVIRONMENTS/Scene_NNN/@NAME.md` and the same file under `GPT-IMAGE-2.5/`. Same text in both.
