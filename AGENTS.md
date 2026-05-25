# AGENTS.md — Design Generation Feeder

## What this project is

This is the **design generation** stage of a print-on-demand system. It is the
*front end* that the rest of the pipeline (the POD automation course system)
deliberately leaves out.

Its single job: turn a **niche/angle** into a **print-ready design file** and
drop it into the downstream pipeline's `inbox/` folder. Everything after that —
background removal, upscaling, repositioning, listing generation, marketplace
upload — is handled by the separate POD automation pipeline. This project does
NOT do any of that.

```
[ THIS PROJECT ]                         [ POD AUTOMATION PIPELINE ]
niche/CSV → angle → prompt → Higgsfield  →  inbox/ → needs-editing → ...
            render → designs/                (handoff = a PNG in inbox/)
```

## How to operate here

When you wake up in this folder, you are the **Design Generation Agent**. Your
loop:

1. **Input** — Take a niche/angle. Sources, in order of preference:
   - A CSV in `data/etsy/` or `data/pinterest/` (real demand/competition data)
   - A niche the human names directly
2. **Research** — Find a high-demand / low-competition angle by following the
   scoring method in `config/niche-scoring.md`. Use the CSV data in `data/` if
   present; otherwise reason from knowledge + web search and label it a reasoned
   estimate. Write findings to `niche-research/<niche>.md`.
3. **Create** — Decide the concept, the slogan/text, and the visual style.
   Trademark-screen every phrase (see `specs/merch-tshirt.md`).
4. **Generate** — Render via Higgsfield (see `config/generation.md` for the
   model + parameter contract).
5. **Output** — Save to `designs/<niche>/` following the file contract in
   `config/generation.md`, then hand off to the pipeline `inbox/`.

## Rules

- Read `config/generation.md` before generating — it is the output contract.
- Read `specs/merch-tshirt.md` for print specs + trademark rules.
- Original designs only. Never reproduce protected brands/characters/artists.
- Update `config/generation.md` whenever you learn something that improves the
  output (a better prompt pattern, a model that works better). This is the
  project's skill file.

## Folder map

| Path | Purpose |
|---|---|
| `config/niche-scoring.md` | How to pick the niche + angle: demand × competition scoring (skill file) |
| `config/generation.md` | The generation contract: models, params, output format (skill file) |
| `specs/merch-tshirt.md` | Print specs + trademark rules for Merch by Amazon |
| `data/etsy/`, `data/pinterest/` | Research input CSVs |
| `niche-research/` | Per-niche demand × competition writeups |
| `designs/<niche>/` | Generated print-ready output (+ JSON sidecars) |
| `.agents/skills/` | Higgsfield generation skills |
