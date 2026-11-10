---
title: Coverage
kind: reference
links: [hero, elements, scripts, decisions, picks]
---

# Nothing drops silently

`MAP/COVERAGE.md` lists every hero element of every shot, and the prompt file that makes it, or the stated reason there is none. It is rebuilt by `scripts/coverage.py` after every batch: a new scene, a new prompt folder, a moved file, a deleted element.

## What counts

| Element | Covered by |
|---|---|
| `hero` with a prompt | A file in any model folder under its category and its scene, or under `_CANON` |
| `hero` without a prompt | Its Reason column in the shot table: on a canon sheet, real photos are the reference, inside another sheet, the scene's plate |
| `background` | Nothing: left to the video prompt, listed as such |
| A hero with neither | **Missing** |

## The report

The table opens with **Missing**, then the counts, then shot by shot. Every report to the person follows the same order: what is missing first, then what was decided, then the counts. Never a gap in a footnote, never a "covered another way" list at the bottom.

## Also written

`MAP/PROMPTS_INDEX.md`: every prompt file by model folder and category, with its references. And each shot file's **Prompts** list, so a shot shows what makes it.

## When to run it

After the scaffold, after every batch of prompts, after moving prompts between model folders, after a pick is attached, before reporting.
