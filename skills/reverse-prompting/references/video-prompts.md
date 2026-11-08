---
title: Video prompts
kind: reference
links: [scenes, picks, hero, prompt-files]
---

# Video prompts

Written after the picks, from the assets, scene by scene. The method for every block is the `cinematic-realism` skill; this page is the bookkeeping.

## One shot or a beat

- **A one-shot scene:** one generation, `PROMPTS/VIDEO/Scene_NNN/SHOT_NNN.md`.
- **A scene of many shots:** one generation per beat of three to six shots of 3-6 seconds, hard cuts between them, under the provider's length limit: `SHOTS_NNN-NNN.md`. A beat ends where the scene turns.
- A shot that cannot share a generation (a different camera side, a special move) is its own file.

## What a scene's prompts share

The scene's locks, pasted at the top of each of its prompts: the place and its plate, the light from `SCENE.md`, each person's costume and state, "costumes never swap; the light never changes between shots".

## What each prompt attaches

The picks of the hero elements of its shots, each with its role: [[picks]]. Background is named in words and attached never: [[hero]]. References are numbered in the order they are attached, so the prompt can say which picture is which.

## What it rewrites

The still's old motion line becomes what a handheld operator does; light sources go out of frame and act by effect; the hero framing goes off-centre: [[reading-a-still]].

## When

After the picks are attached and coverage is rebuilt. Writing video prompts before the assets exist is allowed as a draft, with no pictures attached, and is replaced once the picks are in.
