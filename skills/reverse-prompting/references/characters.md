---
title: Characters
kind: reference
links: [canon-and-state, extras, models, prompt-files]
---

# Leads and small roles

## Leads

A lead appears in many scenes: one canon sheet in `01_CAST/_CANON/@NAME/`, the truth for face and build. The method for the sheet is the `prompt-craft-character-sheet` skill.

- **A real actor:** the face comes only from their own photos or an approved sheet. The prompt attaches it as identity and never describes the face in words that could pull it away. An actor playing older or younger keeps their identity; age goes into the surface.
- **A generated lead:** the face is made once, in close-up, and never regenerated; every sheet after it is built to it.
- **A state** (another costume, wet, wounded, in a ritual garment) is a new sheet in that scene's folder, built on the canon: [[canon-and-state]].

## Small roles

A person with a face that matters in one scene: a single character sheet in `01_CAST/Scene_NNN/@NAME/`, or in `05_EXTRAS/Scene_NNN/` when they are a lone background figure: [[extras]].

## Nationality

The character line names the nationality of where the character belongs, unless the face comes from a real actor's photo: "a Portuguese woman of about sixty".

## Setting

Character sheets are photographed in natural overcast outdoor light, on grey concrete ground in front of a grey concrete wall: the `prompt-craft-character-sheet` skill's block, pasted.

## Which model

GPT Image for lead faces and costumes; GPT Image with the still as costume reference for small roles: [[models]].

## Files

`PROMPTS/GPT-IMAGE-2.5/01_CAST/_CANON/@NAME.md` for a canon, `PROMPTS/GPT-IMAGE-2.5/01_CAST/Scene_NNN/@NAME.md` for a state or a one-scene role.
