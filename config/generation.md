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

Higgsfield does not guarantee a transparent-background parameter, and the
downstream pipeline removes backgrounds in `needs-editing`. So the background
must be a **clean knockout color the remover can key out without eating the art**.

**Default: a flat solid knockout color NOT present anywhere in the artwork.**
- **Use magenta (`#FF00FF`)** for our warm/floral palettes. It is absent from
  sage/terracotta/mustard/cream/burgundy, so removal is unambiguous.
- **Do NOT use green** for designs with foliage — our florals are full of green
  leaves, so a green field would be removed along with the leaves.
- **Never use white or cream.** Lesson learned the hard way: cream backgrounds
  blend into light design elements (clear wine glass, ivory mahjong tile, cream
  daisy petals), so the remover eats them or leaves halos. Low subject/background
  contrast = bad matte.

Transparency, if the model genuinely returns it, is fine too (the pipeline
detects it and skips removal) — but don't rely on it; default to the magenta
knockout.

Always prompt: "design only, no t-shirt mockup, no model, no scene."

## Prompt pattern

```
A [style] t-shirt design: [concept]. Text reads "[EXACT SLOGAN]" in [type style].
[Composition / color notes]. Isolated design only — no t-shirt mockup, no scene,
no background objects. Place the whole design on a flat solid magenta (#FF00FF)
background that appears nowhere in the artwork, for clean background removal.
High-contrast, print-ready, centered.
```

- Put the slogan in quotes and state it once, exactly, to maximize legible text.
- Specify a limited color palette (cleaner prints, better background removal).
- Name a concrete art style (kawaii, retro 70s, bold vintage, line art, etc.).

## Slogan validation gate (MANDATORY before any generate_image call)

Picking the *angle* from the data is not enough. The **slogan itself** must pass
the same data-driven check, or the design enters a saturated/dead lane no matter
how good the visual is. This step is non-optional.

For every slogan, run all six checks against the niche CSV:

1. **Exact-string search.** Grep the slogan in the CSV's Product Title column.
   - 3+ existing listings using the exact slogan → **saturated, skip or sharpen.**
   - 1–2 existing → check their BSR. If selling, you're entering a proven lane
     (good); if dead, the slogan format itself doesn't convert (skip).
2. **Close-variant search.** Grep the *pattern* (e.g. "Rules the X", "X
   Whisperer", "Just A Girl Who Loves X"). If many variants exist across
   adjacent words, the *format* is saturated even if your exact phrase isn't.
3. **Format-category check.** Use the market structure % from
   `niche-scoring.md` Step 3.5b. Your slogan's category must be **≥10% of the
   top 25 by BSR**. Categories at 0–4% are dead — the market is telling you it
   doesn't reward them. Generic puns are almost always in that bucket.
4. **Cross-niche template check (added 2026-05-31).** Ask: does this slogan
   work *equally well* with any animal/profession/identity swapped in? If yes,
   it's a generic template, not niche-specific.
   - "Head of Security" → works for dog, cat, goose, chicken → **template.**
   - "I Just Want to Crochet and Hang Out With My Dog" → specific to the craft
     + companion combo → **niche-anchored.**
   - Templates can still be shipped, but only if either (a) the *visual* is
     load-bearing and differentiated, or (b) you add a secondary niche-specific
     hook (see check #5). Pure template + generic visual = race-to-the-bottom.
5. **Secondary-hook requirement for short slogans (≤3 words).** Short slogans
   are too small a search-keyword surface and too generic to differentiate on
   their own. If the primary slogan is ≤3 words AND failed the cross-niche
   template check, add a niche-specific secondary line.
   - Weak:  `HEAD OF SECURITY`
   - Strong: `HEAD OF SECURITY / Protecting the Coop`
   - The secondary line must contain at least one niche-specific keyword
     (coop / flock / hens / sunrise / rooster) to lift Amazon SEO.
6. **Mirror vs invent decision.**
   - **Default: mirror.** When entering a *validated* niche (one you have a
     scored CSV for), mirror a slogan format that's already winning. Inventing
     a new slogan in a niche you don't own is high-risk, low-evidence.
   - **Invent only when** the data shows a clear gap *and* you can articulate
     why no one's filled it. Document the reasoning in the sidecar's
     `slogan_validation` block.

**Hard rules:**
- If a slogan fails check #1 or #3, do not generate it. Pick a different slogan
  from the data and re-run the gate.
- If a slogan fails check #4 (cross-niche template), it must pass check #5
  (secondary hook) before generation. No exceptions for ≤3-word generic templates.

### Worked example #1 — "Rules the Roost" (fails on category)

Niche: chicken-keeper. Proposed slogan: "Rules the Roost".
- #1 Exact: not in CSV. Pass.
- #2 Variant: generic-pun pattern ("Rules the X" / "X Whisperer" / "X Tender")
  appears repeatedly. **Pattern saturated.**
- #3 Format-category: generic puns are <5% of the top 25 sellers
  (the dominant categories are descriptive-visual + specific identity).
  **Wrong category.**
- Verdict: **fail.** Don't generate.

### Worked example #2 — "Head of Security" (fails the template check, passes with a fix)

Niche: chicken-keeper. Proposed slogan: "HEAD OF SECURITY".
- #1 Exact: 0 hits. Pass.
- #2 Variant: not present in close-variants. Pass.
- #3 Format-category: ownership/role identity (same family as "Chicken Daddy",
  "Just A Girl Who Loves Chickens"). **In top 25.** Pass.
- #4 Cross-niche template: works for dog, cat, goose, chicken. **Fail.**
- #5 Secondary-hook required because slogan is ≤3 words AND failed #4.
  - Without secondary hook → race against German Shepherd "Head of Security" tees.
  - With secondary hook → `HEAD OF SECURITY / Protecting the Coop` adds the
    chicken-specific anchor and lifts the keyword surface.
- Verdict (without secondary): **fail.**
- Verdict (with secondary): **pass.** Generate the secondary-hook variant.

The lesson: short-and-snappy slogans feel strong but often need a second line
to survive Amazon's keyword game.

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
`C:\Users\Hello\pod-pipeline\inbox`). The PNG and its sidecar must share a basename
(`{slug}__p{N}.png` + `{slug}__p{N}.json`) so the pipeline pairs them.

**The images live in the Higgsfield cloud, not the repo.** Web/remote sessions
can't fetch them — the CDN host is not in the network allowlist (returns
`403 host_not_allowed`) — so the agent commits sidecars only, each carrying the
`higgsfield_job_id`. The image stays in your Higgsfield viewer until you
download it.

**Automated, no-rename handoff** — `scripts/handoff.py`:
Higgsfield names every download with its job-ID UUID
(`hf_<date>_<time>_<job-id>.png`), and each sidecar stores that same UUID. The
script matches them by UUID, renames each image to the sidecar's `filename`, and
copies image + sidecar into `inbox/`. So the human workflow is just:

1. `git pull` this repo on the PC (gets the latest sidecars + this script).
2. Download the approved images from the viewer (any names) into your Downloads folder.
3. Run it from the repo root (inbox defaults to `C:\Users\Hello\pod-pipeline\inbox`):
   - Windows CMD:  `python scripts\handoff.py`   (use `python`, not `python3`)
   - macOS/Linux:  `python3 scripts/handoff.py`
   - flags: `--downloads`, `--inbox`, `--move`, `--dry-run` (preview first)
4. Done — `inbox/` has correctly-named PNGs + matching sidecars. No manual renames.

It reports any sidecar whose image wasn't found in the downloads folder, so you
know exactly what's left to download.

## Notes / learnings

- **Background-removal:** "plain flat background" prompts render as cream, which
  blends into light design elements and removes badly. Always specify a magenta
  (#FF00FF) knockout instead (green conflicts with foliage). See Background above.
- (add prompt patterns, model quirks, and what sells as you discover them)
