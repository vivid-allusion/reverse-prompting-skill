---
title: Which model makes what
kind: reference
links: [environments, characters, extras, props-vehicles, prompt-files]
---

# Model routing

The default, learned on a real project. A project's own skill or brief overrides it; write the override in its brief.

| Asset | Model | Note |
|---|---|---|
| Lead faces, canon sheets, costume construction | **GPT Image 2.5 Sunburst** | The most accurate; slow and costly, so only for what must be exact |
| Environment plates | **Seedream 5.0 and GPT Image**, pick | Same prompt in both folders: [[environments]] |
| Props, vehicles | **Seedream 5.0** | Fast, cheap, near GPT Image on objects: [[props-vehicles]] |
| Extras, group and single | **GPT Image** with the still as costume reference | [[extras]] |
| Small roles | **GPT Image** with the still as costume reference | [[characters]] |
| Video | The project's video model, for example **Seedance 2.5** | [[video-prompts]] |

## What went badly

- **Soul did horribly on environments and props.** Keep it for people.
- **Seedream did badly on extras.** Keep it for objects and places.

## Folders

One folder per image model under `PROMPTS/`, for example `SEEDREAM-5.0/` and `GPT-IMAGE-2.5/`, and one `VIDEO/` folder for the video prompts whatever the video model. One generator reads one folder.

## Newer versions

A newer model version is compared on one asset before it replaces the old one in a folder.

The registry of what each model is good at, its limits and its costs is the `cinematic-realism` skill's models page; this page only routes.
