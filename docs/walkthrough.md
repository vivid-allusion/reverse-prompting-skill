# Walkthrough: The Last Ferry

An invented short film in three scenes, taken from five stills to its video prompts. Every file named here is in `examples/the-last-ferry/`.

## 1. The shots table

The person has five stills, one per shot, each at a public address, and the old motion lines written for them. `shots.csv`:

| shot | scene | still | motion | scene_title | elements |
|---|---|---|---|---|---|
| 1 | 1 | …/shot_001.png | The camera slowly pushes in on the ferry… | EXT. HARBOUR - DAWN | `@HARBOUR:ENVIRONMENTS; @LAST_FERRY:VEHICLES; @HARBOUR_WORKERS:EXTRAS; @ROPE:PROPS:background` |
| 2 | 2 | …/shot_002.png | Slow dolly in on Marta and Tomás… | INT. FERRY CABIN - DAY | `@MARTA:CAST; @TOMAS:CAST; @COAT_MARTA:COSTUMES; @FERRY_CABIN:ENVIRONMENTS; @TIN_BOX:PROPS` |
| 3 | 2 | …/shot_003.png | Close push-in on her hands… | | `@MARTA:CAST; @TIN_BOX:PROPS; @FERRY_CABIN:ENVIRONMENTS:background` |
| 4 | 2 | …/shot_004.png | Slow push-in on the boy's face. | | `@TOMAS:CAST; @FERRY_CABIN:ENVIRONMENTS:background` |
| 5 | 3 | …/shot_005.png | The camera slowly pushes in on the woman… | EXT. ISLAND JETTY - DUSK | `@MARTA:CAST; @COAT_MARTA:COSTUMES; @TIN_BOX:PROPS; @ISLAND_JETTY:ENVIRONMENTS` |

Shots 2, 3 and 4 are one scene: the same cabin, one continuous moment.

## 2. Scaffold

```bash
python3 scripts/scaffold.py shots.csv . --only-listed
```

It writes `MAP/SCENES/Scene_001/` to `Scene_003/`, a `SCENE.md` in each and a `SHOT_NNN.md` per still, and an ABOUT stub for every hero element in its scene. Marta, her coat and the tin box are in two scenes, so each also gets `_CANON/`. The rope is background: it stays a row in shot 1's table and gets no folder.

## 3. Scenes and shots

`Scene_002/SCENE.md` sets the one light (overcast daylight through the windows, frame-left), the cast's state, and the one camera side. It records the calls: one plate, because shots 3 and 4 are close and show only blur behind; the tin box closed in shot 2 and open in shot 3, one canon with the state written in the shot.

Each `SHOT_NNN.md` gets its size, its hero, a literal inventory, what is out of frame by its effect, and notes on what changed from the still: the centred framing re-blocked, the push-in motion line to be rewritten. The coat has no prompt of its own, so its row carries the reason: "On Marta's canon sheet".

## 4. Asset prompts, per model

| File | Why there |
|---|---|
| `PROMPTS/GPT-IMAGE-2.5/01_CAST/_CANON/@MARTA.md` | A lead, in two scenes: one canon sheet |
| `PROMPTS/GPT-IMAGE-2.5/01_CAST/Scene_002/@TOMAS.md` | One scene only: a scene sheet |
| `PROMPTS/SEEDREAM-5.0/02_PROPS/_CANON/@TIN_BOX.md` | A prop in two scenes |
| `PROMPTS/SEEDREAM-5.0/03_ENVIRONMENTS/Scene_00N/…` and the same under `GPT-IMAGE-2.5/` | One plate per scene and camera side, in both models, to pick |
| `PROMPTS/SEEDREAM-5.0/06_VEHICLES/Scene_001/@LAST_FERRY.md` | The vehicle the shot is about |
| `PROMPTS/GPT-IMAGE-2.5/05_EXTRAS/Scene_001/@HARBOUR_WORKERS.md` | The scene's group, every man Portuguese, the still attached as costume reference |

## 5. Check and count

```bash
python3 scripts/check_prompts.py . --min-refs 1
python3 scripts/coverage.py .
```

`MAP/COVERAGE.md` opens with "Missing: nothing", then 15 hero elements (13 with a prompt, 2 with a stated reason) and 3 background elements. Each shot file now lists its prompts.

## 6. Picks and video

The person generates, picks and syncs. The picks' addresses go into the shots' reference tables. The video prompts:

- `PROMPTS/VIDEO/Scene_001/SHOT_001.md`: one shot.
- `PROMPTS/VIDEO/Scene_002/SHOTS_002-004.md`: the cabin scene as one generation of three shots with hard cuts, the scene's locks pasted at the top.
- `PROMPTS/VIDEO/Scene_003/SHOT_005.md`: one shot.

Rebuild coverage, and the scene is ready to generate.
