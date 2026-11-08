---
title: Extras
kind: reference
links: [scenes, hero, characters, models]
---

# Extras

## One sheet per scene

An extras sheet is one group photograph of **the people seen together in one scene**, in costume, every face different. It is the identity reference for that scene's background people. The method for the sheet is the `prompt-craft-extras-sheet` skill.

- **Only the people of that scene.** Never gather everyone of a kind (all dock workers, all patrons) from several scenes into one crew.
- **One person alone** in a scene gets a single character sheet, not a group of one: [[characters]].
- **A crowd too big for one sheet** (thirty or more) splits into sheets of about twelve: `@CROWD_A`, `@CROWD_B`.
- **A crowd far back, dark and soft** is background and gets no sheet: [[hero]].

## Nationality, person by person

Every person carries the nationality of the scene's country, so the model gives the right faces:

- the opening line names it: "TEN Portuguese harbour workers";
- each individual in the people block carries it: "ONE OLD PORTUGUESE MAN with …";
- one line of features for the nationality, faces still all different;
- the negative bans features from elsewhere.

A film that crosses borders changes nationality by scene.

## Setting

Natural overcast outdoor light, grey concrete ground and wall: the extras skill's block, pasted.

## Which model

GPT Image with the scene's still attached as costume reference: [[models]]. Seedream does badly on extras.

## Files

`PROMPTS/GPT-IMAGE-2.5/05_EXTRAS/Scene_NNN/@NAME.md`.
