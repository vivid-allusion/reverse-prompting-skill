---
title: Props and vehicles
kind: reference
links: [hero, canon-and-state, models, prompt-files]
---

# Props and vehicles

## Which ones

Only hero props: what a prominent character holds or uses, or what the story needs seen (what they wear is costume). A vehicle only when it acts in the shot: the car the hero drives, a boat sailing through, something carrying someone in or out, or the shot is about what it does. Traffic in a street is the street's plate: [[hero]]. Everything worked on or walked on that stays put, and every moored, parked or static vehicle, is part of the plate; so is a vehicle the scene plays on or in: [[elements]], [[environments]].

## One per object

- An object used in one scene: `02_PROPS/Scene_NNN/@NAME/`.
- An object in several scenes: a canon in `02_PROPS/_CANON/@NAME/`, and a scene state only when it changes (opened, broken, burnt): [[canon-and-state]].
- **Different vessels are different elements.** Two ships that look different in two scenes are two elements, each in its scene, even when the script calls both "the ship".

## Real photos

Where a real object must be exact (a period container, a ritual object, a uniform), a real photo at a public address is the construction reference. When the photos are good enough, they are the reference and no prompt is written; the shot table's reason says so: "Real photos are the reference".

## The prompt

The object is taken out of the still and put somewhere new, so the new setting is written; the object itself is not, because the still shows it.

```prompt
Provided image shows a scene from a film set in [the period]. Take the [object] [the man swings] and show it on its own, lying on the ground, outdoors in natural overcast daylight, nothing else in frame. Keep its exact shape, material and wear. Real photograph, [the project's frame].
```

then the still or stills that show it, `![ref](<still address>)` each. Add a sentence only for what the still cannot show: the object is hidden or soft ("a flat metal flask with a hinged cap"), or a decision the still does not hold ("no markings", "unlit"). No itemised construction, no look block, no negative list. No grey concrete for props: that setting is for character and extras sheets. A vehicle the same way, afloat or on a road, empty of people.

## Which model

Seedream for props and vehicles: [[models]].

## Files

`PROMPTS/SEEDREAM-5.0/02_PROPS/Scene_NNN/@NAME.md`, `PROMPTS/SEEDREAM-5.0/02_PROPS/_CANON/@NAME.md`, `PROMPTS/SEEDREAM-5.0/06_VEHICLES/Scene_NNN/@NAME.md`.
