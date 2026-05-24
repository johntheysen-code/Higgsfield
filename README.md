# merch-design-engine

The **design generation feeder** for a print-on-demand system: turn a niche into
a print-ready design and hand it off to the POD automation pipeline's `inbox/`.

This repo is *only* the generation front end. Background removal, upscaling,
listing generation, and marketplace upload are handled by the separate POD
automation pipeline — this feeds it.

```
[ THIS REPO ]                              [ POD AUTOMATION PIPELINE ]
niche/CSV → angle → prompt → Higgsfield →  inbox/ → needs-editing → ... → upload
            render → designs/                (handoff = a PNG in inbox/)
```

## Start here

- **`AGENTS.md`** — what this project is + how the agent operates (read first).
- **`CLAUDE.md`** — points Claude Code at `AGENTS.md`.
- **`config/generation.md`** — the generation contract (models, params, output format).
- **`specs/merch-tshirt.md`** — Merch print specs + trademark rules.

## Folders

| Path | What goes here |
|---|---|
| `data/pinterest/` | Pinterest demand CSVs (e.g. PinTwist exports) |
| `data/etsy/` | Etsy / Amazon competition CSVs |
| `niche-research/` | Demand × competition writeups per niche |
| `designs/<niche>/` | Generated print-ready PNGs (+ JSON sidecars) |
| `.agents/skills/` | Higgsfield generation skills |

## Target

- **Platform:** Merch by Amazon · **Product:** t-shirt designs
- **Print spec:** 4500×5400 PNG (see `specs/merch-tshirt.md`)
