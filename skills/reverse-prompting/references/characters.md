---
title: Characters
kind: reference
links: [canon-and-state, extras, models, prompt-files]
---

# Leads and small roles

## Leads

A lead appears in many scenes: one canon sheet in `01_CAST/_CANON/@NAME/`, the truth for face and build. The method for the sheet is the `cast-character-sheet` skill.

- **A real actor:** the face comes only from their own photos or an approved sheet. The prompt attaches it as identity and never describes the face in words that could pull it away. An actor playing older or younger keeps their identity; age goes into the surface.
- **A generated lead:** the face is made once, in close-up, and never regenerated; every sheet after it is built to it.
- **A state** (another costume, wet, wounded, in a ritual garment) is a new sheet in that scene's folder, built on the canon: [[canon-and-state]].

## Small roles

A person a shot is about is cast, with or without a name: the woman laughing in the foreground, the woodcutter the scene opens on, the prisoner led off the boat. The director would direct them like an actor. Each gets a single character sheet in `01_CAST/Scene_NNN/@NAME/`, named by what they do (`@LAUGHING_WOMAN`, `@WOODCUTTER`). Never put them in an extras group with the people behind them. A lone figure far back is still an extra: [[extras]].

From a keyframe the sheet is made from the still, in the short form:

```prompt
Provided image shows a scene from a film set in [place] in [period]. Make a character sheet of [who, as the image shows them: the Swedish woman laughing in front, in the sequined dress]: the same person, same face, hair and clothes. [Only when the image hides it: Her face is not in the image: about 30, ...] Three panels side by side: a full-body front view, standing straight, arms at the sides, looking at the camera with a neutral expression; a full-body back view; a close-up of the head and shoulders. Empty hands. Where the image does not show part of her, dress her to match. Photographed outdoors on an overcast day against a plain grey concrete wall and ground, soft natural daylight. Real photograph, [frame].
```

then `![ref](<still address>)`. The still holds the face and clothes; the prompt does not describe them again.

## Nationality

The character line names the nationality of where the character belongs, unless the face comes from a real actor's photo: "a Portuguese woman of about sixty".

## Setting

Character sheets are photographed in natural overcast outdoor light, on grey concrete ground in front of a grey concrete wall: the `cast-character-sheet` skill's block, pasted.

## Which model

GPT Image for lead faces and costumes; GPT Image with the still as costume reference for small roles: [[models]].

## Files

`PROMPTS/GPT-IMAGE-2.5/01_CAST/_CANON/@NAME.md` for a canon, `PROMPTS/GPT-IMAGE-2.5/01_CAST/Scene_NNN/@NAME.md` for a state or a one-scene role.
