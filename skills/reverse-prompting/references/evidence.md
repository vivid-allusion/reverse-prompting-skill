---
title: Why each rule
kind: reference
links: [method, hero, scenes, extras, models, environments, coverage, prompt-files]
---

# Why each rule

Every rule here was learned in practice, turning animatic stills into assets and assets into video. What went wrong without the rule is the reason for it.

| Rule | Why |
|---|---|
| Assets are references; the look is the prompt | A video model holds identity from a picture, not from words. It holds the look from words repeated in every prompt. So pictures carry faces, costumes, objects and places; the prompt carries light, lens and grain |
| A plate is an empty place in the film's look | A plate with people in it brings strangers into the shot. A plate in the still's own grade brings the still's look back |
| Group sheets for background people | One picture of many different faces keeps a crowd from cloning one face; a sheet per person is wasted work for people the camera never holds |
| Shots of one scene in one generation | Generated together, the shots of a scene keep one place, one light and one costume; generated apart, they drift |
| Literal frame, sources out of frame | A model draws every noun it is given. Name the fire beside a close-up and it puts the fire in the picture |
| The hero gets the asset | An asset for every visible object buries the shot's subject and costs time on things the video model fills in by itself |
| Nothing drops silently | Without a table that lists every shot's hero elements, whole kinds of assets go missing and nobody notices until the video is wrong |
| One plate, one extras sheet per scene | Two stills of the same kind of place are still two scenes; one plate for both mixes them |
| Nationality person by person | People written without nationality come back with faces from anywhere |
| Soul for people only; Seedream not for extras | What each model did badly in practice; see [[models]] |
| Notes out of input folders | A generator reads every `.md` in its input folder as a job (the `helmer-md` skill) |
