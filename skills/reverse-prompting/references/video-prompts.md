---
title: Video prompts
kind: reference
links: [scenes, picks, hero, prompt-files]
---

# Video prompts

Written after the picks, from the assets, scene by scene, for **Seedance 2.5**. The method for every block is the `cinematic-realism` skill. The folder is `PROMPTS/VIDEO/` so it outlives the model; the prompts inside are written for the model in use.

## One shot or a beat

- **A one-shot scene:** one generation, `PROMPTS/VIDEO/Scene_NNN/SHOT_NNN.md`.
- **A scene of many shots:** one generation per beat of three to six shots of 3-6 seconds, hard cuts between them, under the provider's length limit: `SHOTS_NNN-NNN.md`. A beat ends where the scene turns.
- A shot that cannot share a generation (a different camera side, a special move) is its own file.

## What a scene's prompts share

The scene's locks, pasted at the top of each of its prompts: the place and its plate, the light from `SCENE.md`, each person's costume and state, "costumes never swap; the light never changes between shots".

## The shape of a Seedance 2.5 prompt

```
```prompt
<THE BIGGEST RISK, first: what must never be in frame, or never change>

REFERENCE USAGE (Seedance 2.5): @Image 1 is the IDENTITY reference for @NAME … @Image 2 is the
ENVIRONMENT reference … (one line per attached picture, numbered in the order the embeds are listed)

<the hero and what they do> · THE SHOT (one shot, ~5 s, no cuts; or SHOT 1 (~4 s) … SHOT 2 … with hard
cuts) · LIGHT · CAMERA · STYLE / LENS / CAPTURE · PHYSICS · AUDIO (diegetic) · KEEP THE LOGIC · NEGATIVE
```
![reference_images](<public address of the first pick>)
![reference_images](<public address of the second pick>)
duration: 5
```

- **References** go in the `reference_images` slot, as `![reference_images](url)`, and are `@Image 1`, `@Image 2` … in that order. A start frame and reference images never go in the same file.
- **Length:** `duration:` in seconds, 4 to 30 per generation; a beat of several shots adds up its shots and stays under the limit.
- **Sound** is generated with the picture: write what is heard, diegetic only.

## What each prompt attaches

The picks of the hero elements of its shots, each with its role: [[picks]]. Background is named in words and attached never: [[hero]]. References are numbered in the order they are attached, so the prompt can say which picture is which.

## What it rewrites

The still's old motion line becomes what a handheld operator does; light sources go out of frame and act by effect; the hero framing goes off-centre: [[reading-a-still]].

## When

After the picks are attached and coverage is rebuilt. Writing video prompts before the assets exist is allowed as a draft, with no pictures attached, and is replaced once the picks are in.
