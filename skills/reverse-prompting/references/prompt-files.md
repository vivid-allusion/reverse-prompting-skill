---
title: Prompt files
kind: reference
links: [folders, models, coverage, scripts]
---

# Prompt files

**The syntax authority is the `helmer-md` skill:** load it before writing a prompt file. The shape every generator reads the same way:

````
```prompt
the prompt, as many lines as it needs
```
![ref](<public address>)
![ref](<public address>)
````

- Open with a line holding only ```` ```prompt ````, never a bare fence, and always close it.
- Every reference is an `![alt](address)` embed on its own line, the address public and `https`; never a bare address line.
- A video prompt names its reference slot: `![reference_images](<address>)`, and its length: `duration: 5`. A start frame and reference images are never in one file.
- Comments `<!-- … -->` are removed before reading; an embed inside one is gone.

## Where

`PROMPTS/<MODEL>/<category>/Scene_NNN/@NAME.md` or `PROMPTS/<MODEL>/<category>/_CANON/@NAME.md`, and for video `PROMPTS/VIDEO/Scene_NNN/SHOT_NNN.md` or `SHOTS_NNN-NNN.md`: [[folders]].

## Never in `PROMPTS/`

Every `.md` in a generator's input folder, subfolders included, is a job. An ABOUT file, an index, a scene or shot note dropped there would be sent as a prompt. Notes live in `MAP/` and `02_PRE-PRODUCTION/`.

## Checked

`python3 <skill>/scripts/check_prompts.py .` checks the shape, the fences, the embeds and the notes: [[scripts]].
