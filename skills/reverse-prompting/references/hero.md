---
title: The hero of the shot
kind: reference
links: [elements, coverage, video-prompts, reading-a-still, extras]
---

# What gets an asset

Ask: **who or what is this shot about?** That is the hero.

| Gets an asset | Gets none |
|---|---|
| The character in focus | People in the back, out of focus |
| What a prominent character handles | Objects on a shelf, table or wall that nobody touches |
| What a prominent character wears that the story turns on | Background clothing |
| What a prominent character rides or drives | Vehicles parked or passing in the back |
| The place, when the shot shows it | The place in a close-up whose background is blur |
| The group, when the shot is about the crowd | A crowd far back, dark and soft |

Background is not lost: the video prompt names it in a few words and the model fills it in. A sheet for every candle, cup and chair in the back of a frame is wasted work, and it pulls the video model's attention away from the hero.

## Examples

- A baker kneading dough: the baker and the dough. Not the candlestick behind.
- A crane lifting a cargo net over a ship: the crane, the net, the ship. Not the cars on the quay.
- A woman lifting a glass in a crowded bar: the woman and the glass. The patrons are the scene's extras sheet if they read; otherwise background: [[extras]].
- A figure walking away down a lane: the figure and the costume; the lane is the plate, and its lamps are part of the plate.

## In the shot file

Every element in a shot's table has a role, `hero` or `background`. Background elements stay listed so nobody wonders whether they were seen: [[elements]]. The coverage table counts only hero elements as needing a prompt: [[coverage]].

## With coverage

"Nothing drops silently" and "only the hero gets an asset" work together: everything seen is written down; only what matters is made.
