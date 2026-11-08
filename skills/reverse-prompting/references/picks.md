---
title: Picks and addresses
kind: reference
links: [elements, coverage, video-prompts, folders]
---

# Generating, picking, addresses

## The person's part

The person runs each model folder through its generator, looks at the takes, and picks one per asset. Generation and picking are theirs; this skill never presses Generate.

## A pick's address

A video model takes references by public address only. The person puts the pick into its element's folder in `02_PRE-PRODUCTION/` and syncs it; the sync gives it an address and writes a sidecar `.md` beside it holding that address. Read the address from the sidecar.

## Where it is recorded

- In the element's ABOUT, in its reference slot: `- [x] identity: <address>`.
- In each shot that uses it, in the shot file's reference table: the address and its role.

Then rebuild coverage: [[coverage]].

## Roles

Every pick attached to a video prompt is told its role in words:

| Role | For |
|---|---|
| Identity | A face, a body, a person's costume |
| Construction | An object or garment to copy exactly |
| Environment | A plate |
| Framing | A kept still, only when its composition is wanted, never its light |
