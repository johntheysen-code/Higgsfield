# merch-design-engine

A repeatable pipeline for generating print-ready Merch by Amazon t-shirt designs,
powered by Higgsfield image generation (via the installed skills/MCP) and Claude
for niche research + creative direction.

## The loop

1. **Data in** — drop CSV exports from niche-research tools (PinTwist for Pinterest
   demand, the Amazon/Etsy tools for competition) into `data/`.
2. **Research** — Claude reads the CSVs, finds a high-demand / low-competition angle.
3. **Creative** — Claude writes the concept + slogan + a detailed image prompt.
4. **Generate** — Higgsfield renders a print-ready, transparent-background design.
5. **Output** — finished PNGs land in `designs/<niche>/`, ready to upload.

## Folders

| Path | What goes here |
|---|---|
| `data/pinterest/` | Pinterest demand CSVs (e.g. PinTwist exports) |
| `data/etsy/` | Etsy / marketplace competition CSVs |
| `designs/` | Generated print-ready design files, grouped by niche |
| `specs/` | Print specs + trademark rules for the target platform |
| `.agents/skills/` | Higgsfield generation skills (installed) |

## Target

- **Platform:** Merch by Amazon
- **Product:** T-shirt designs
- **File spec:** see `specs/merch-tshirt.md`
