---
title: The method
kind: reference
links: [inputs, scenes, hero, coverage, video-prompts, models]
---

# Reverse prompting, the whole loop

## Why stills first

A video generation is slow and costly, and most of its failures already show in one frame: the wrong place, the wrong face, a crowd of clones, light from nowhere. A still costs a fraction and shows the same failures. So the film is tested as an animatic: one generated still per shot, in order, cut against the sound. The story is fixed there, where a change is cheap.

## Why the stills are not enough

A one-off still cannot be animated into a film. Its face drifts in the next shot, its place has no back wall, its props change between frames, and its look is whatever the image model defaulted to. A video model holds identity, wardrobe and places only from **references**, and the look only from the **prompt**. So each still is taken apart into assets that can be locked and reused.

## The loop

1. **Stills.** One per shot, from the story, each at a public address. [[inputs]]
2. **Scenes.** The shots grouped by continuous place and time, numbered. [[scenes]]
3. **Read.** Each still read literally: in frame, out of frame by its effect, the hero. [[reading-a-still]]
4. **Elements.** The hero elements of each shot, filed per scene, with a canon for what recurs. [[hero]], [[elements]], [[canon-and-state]]
5. **Asset prompts.** One file per asset per model, in that model's folder. [[models]]
6. **Coverage.** Every hero element with a prompt or a reason; gaps first. [[coverage]]
7. **Picks.** The person generates, picks and gives each pick a public address. [[picks]]
8. **Video.** Each scene rebuilt from its picks, one shot or a run of shots per generation. [[video-prompts]]

## What changes from the stills

Content, order and shot size stay. What made the still read as a generated image goes: the default grade, the glow, the centred hero framing, decorative candles and lamps in frame, the slow push-in in the old motion line. The method for that is the `cinematic-realism` skill; this skill keeps the books.

## What it does not do

It does not write the story, generate anything, or judge a take. Without stills, a script is broken down by `helmer-story-breakdown`, whose categories and naming this method reuses.
