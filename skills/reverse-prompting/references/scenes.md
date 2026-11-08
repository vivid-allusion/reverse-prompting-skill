---
title: Scenes and shots
kind: reference
links: [inputs, folders, environments, extras, video-prompts, canon-and-state, decisions]
---

# Scene or shot

**A scene is one continuous place and time.** A **shot** is one still. A scene holds one shot or many.

## Cutting scenes

- New place, or a jump in time: new scene.
- Same place, continuous time, the camera moves: same scene, new shot.
- A cutaway somewhere else and back: three scenes, numbered in story order.
- A still whose place is unclear stays in the scene of the shot before it, and the call is written down: [[decisions]].

Scenes are numbered in story order with three digits: `Scene_001`, `Scene_002`. Shot numbers run through the whole film, `SHOT_001` onward; a scene's shots keep their film numbers.

## What the shots of one scene share

| Shared | So |
|---|---|
| The place | One plate per camera side, not one per still: [[environments]] |
| The light | One light, written once in `SCENE.md`, pasted into every prompt of the scene |
| The cast's state | One costume and condition per person for the whole scene |
| The extras | One sheet for the people of the scene: [[extras]] |
| The props | One asset per object; a change of state is a new state folder |

Shots in different scenes share nothing but the canon: [[canon-and-state]]. **Never merge two scenes into one plate or one extras sheet,** even when they show the same kind of place or people.

## `SCENE.md`

The scaffold writes it; fill it:

```
# Scene 002 · INT. FERRY CABIN - DAY

- **Place:** …
- **Time and light:** one source, its direction, what it does
- **Cast and state:** @NAME — costume, condition
- **Camera sides:** A (towards the bow), B (towards the door)
- **Shots:** SHOT_002 (wide, side A), SHOT_003 (insert), SHOT_004 (close-up, side B)
- **Decided:** the calls made for this scene
```

## One-shot scenes

A montage is all one-shot scenes: every still is its own scene, and every plate and extras sheet belongs to one still. The method does not change; there are simply no shared plates.

## Scenes of many shots

They are built together: one plate per camera side, one extras sheet, one light, and in the video stage one generation per beat of a few shots with hard cuts: [[video-prompts]].
