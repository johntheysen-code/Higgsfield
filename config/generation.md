# Generation Contract (skill file)

How the Design Generation Agent renders designs and what it must output so the
downstream POD pipeline can consume them. Update this file as you learn.

## Models (Higgsfield)

| Use case | Model | Notes |
|---|---|---|
| Text-heavy designs, slogans, typography | `gpt_image_2` | Best text rendering. Params: `resolution` (1k/2k/4k), `quality` (low/medium/high). |
| Top quality / detailed illustration / 4K | `nano_banana_pro` | Strong text + detail. `resolution` 1k/2k/4k. |
| Fast / cheap drafts | `nano_banana_2` | Quick iteration before a final high-quality render. |

Default to `gpt_image_2` for Merch tees, since most sellable designs have text.

## Generation parameters

- **Aspect ratio:** `3:4` (portrait, closest to the 5:6 print area). The design
  does not need to fill the canvas — the pipeline's reposition stage centers it.
- **Resolution / quality:** Generate at the highest available (`4k` / `high`)
  when doing a final render. Use lower for drafts. Note: Higgsfield output is
  often below the 4500×5400 print target — that is fine, the pipeline's
  `needs-editing` stage **upscales**.
- **Count:** 3–4 per concept so the human can pick the best.

## Background

Higgsfield does not guarantee a transparent-background parameter. Two paths,
both compatible with the downstream pipeline (which removes backgrounds in
`needs-editing`):

1. **Preferred:** prompt for an isolated design with no scene/mockup. If the
   model returns transparency, great — the pipeline detects it and skips removal.
2. **Fallback:** prompt for the design on a **flat solid color not present in
   the artwork** (e.g. a green or magenta field). This makes downstream removal
   clean. NEVER use white if the design contains white.

Always prompt: "design only, no t-shirt mockup, no model, no scene."

## Prompt pattern

```
A [style] t-shirt design: [concept]. Text reads "[EXACT SLOGAN]" in [type style].
[Composition / color notes]. Isolated design only — no t-shirt mockup, no scene,
no background objects. High-contrast, print-ready, centered.
```

- Put the slogan in quotes and state it once, exactly, to maximize legible text.
- Specify a limited color palette (cleaner prints, better background removal).
- Name a concrete art style (kawaii, retro 70s, bold vintage, line art, etc.).

## Output file contract (what the pipeline's inbox/ expects)

For each chosen design, write to `designs/<niche>/`:

- **Image:** `{slug}__p{N}.png`
  - `slug` = kebab-case design name (no trademarked terms)
  - `__p{N}` = color profile tag the pipeline reads:
    - `p1` all colors (default; omit tag for p1)
    - `p2` all but black/dark (for dark or light-line designs)
    - `p3` all but white (for designs that vanish on light shirts)
    - `p4` black/dark shirts only (white/light designs)
    - `p5` white/light shirts only (dark designs)
- **Sidecar (optional but recommended):** `{slug}__p{N}.json` — gives the
  pipeline's listing step a head start:

```json
{
  "filename": "axolotl-going-on__p1.png",
  "niche": "axolotl",
  "theme": "cute pun / relatable busy-life humor",
  "slogan": "A LOTL GOING ON",
  "description": "Kawaii axolotl surrounded by little chaos doodles.",
  "keywords": ["cute axolotl design", "funny axolotl pun", "busy mom humor"],
  "trademark_checked": true,
  "color_profile": 1,
  "source_model": "gpt_image_2"
}
```

## Handoff to the pipeline

The downstream pipeline reads from `PIPELINE_WORKING_DIR/inbox/` (default
`~/pod-automation/inbox`). Once a design is approved, copy the `.png` (and
`.json` sidecar) there. On this machine that is a file copy; in this remote
session it is documented for the human to run locally.

## Notes / learnings

- (add prompt patterns, model quirks, and what sells as you discover them)
