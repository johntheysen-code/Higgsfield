# Niche Scoring Method (skill file)

How the Design Generation Agent picks **which niche to target** and **which angle**
to use. This turns "demand × competition" from a vibe into a repeatable, auditable
score. Update the thresholds as you learn what sells.

> The score is only as good as the data. With a CSV in `data/`, this is measured.
> Without one, it's a *reasoned estimate* — label it as such in the writeup.

---

## Step 1 — Load the data

Read every CSV in `data/etsy/` and `data/pinterest/`. The tools differ, so map
whatever columns exist onto these roles (ignore what's missing):

| Role | Likely column names | Tool |
|---|---|---|
| **term** | keyword, search_term, query | all |
| **demand** | saves, repins, searches, search_volume | Pinterest (PinTwist) |
| **competition** | result_count, results, listings, competition | MerchFlux / iScaleEtsy |
| **sales proxy** | bsr, best_sellers_rank, favorites, reviews, baskets, carts | MerchFlux / EverBee / iScaleEtsy |
| **freshness** | first_review_date, listed_date, created | Etsy/Amazon tools |
| **price** | price | all |

If a role has no column, drop that sub-score and renormalize. Note which roles
were available in the writeup so the confidence is honest.

---

## Step 2 — Score each term (0–100, higher = better opportunity)

Compute four sub-scores, normalize each across the dataset (min–max to 0–1), then
combine. Thresholds below are **starting defaults — tune them.**

1. **Demand (D)** — higher is better. From saves/searches/volume. If only Etsy
   sales proxies exist, use favorites/reviews as a demand stand-in.
2. **Competition (C)** — *lower* is better, so use `1 − normalized(result_count)`.
   Rule of thumb for Merch: <100 results = wide open, 100–1000 = workable,
   >1000 = crowded.
3. **Proven sales (S)** — is it actually selling? Lower BSR = better (invert);
   high favorites/baskets = better. This separates "wanted" from "bought."
   Merch rule of thumb: top designs with **BSR under ~300K** = selling.
4. **Freshness (F)** — bonus for **recent listings that already have traction**
   (new + selling = a window before saturation). Recent first-review date +
   non-trivial sales proxy → high F.

```
Opportunity = 0.30*D + 0.30*C + 0.25*S + 0.15*F      (weights are tunable)
```

Then apply hard **filters** (a fail = drop the term entirely):

- **Trademark:** any brand / character / franchise / artist / sports team / common
  registered phrase → DROP. Screen with reasoning + web search. Not legal clearance.
- **Printability:** must work as a *t-shirt graphic*. Drop non-apparel trends
  (crochet patterns, mugs-only fads, digital-download-only items) for our use.
- **Policy:** drop anything that violates Merch content policy (hate, etc.).

---

## Step 3 — Pick the angle (differentiate, don't copy)

For the top-scoring terms, choose an angle that avoids the saturated literal center:

- **Intersection** — niche × aesthetic / audience / format (e.g. "axolotl ×
  cottagecore", "nurse × heavy-metal", "teacher × retro").
- **Pun / wordplay** — widens the audience beyond core fans.
- **Micro-community identity** — the specific "I am an X" buyer converts best.
- **Trend overlay** — apply a current rising motif to a proven seller.

Never reproduce a competitor's design. Derive *composition/theme trends*, then
create something original.

---

## Step 3.5 — Decode the buyer (psychology + market structure)

Finding "the winner" is not enough. Two niches with identical BSR distributions
can convert completely differently because the **buyer psychology** is different.
Skipping this step is how good designs land in the wrong format-category and
quietly underperform (see the Rules-the-Roost worked example in
`config/generation.md`).

Every niche-research write-up must include the following before moving on.

### 3.5a — Psychology block (per top angle, not per listing)

| Field | What to capture | Source |
|---|---|---|
| **Identity** | The "I am an X" the buyer is signaling. Be specific: "Pickleball Grandma" not "older woman". | Top-seller titles + your read |
| **Tribe** | The group/community the buyer affiliates with. "Backyard chicken owners", "active retired women", "field-guide birders". | Top-seller titles + niche knowledge |
| **Emotion** | The driver: pride, humor, belonging, nostalgia, rebellion, identity, self-deprecation. **Grounded in observable BSR evidence** — e.g. "humor angles in this niche have median BSR 805K vs identity 427K → identity is the stronger driver here". | BSR-by-angle data |
| **Giftability** | Could a non-buyer purchase this for the wearer? "Chicken Daddy" = highly gift-able (Father's Day). "I Like Birds" minimalist = lower (the wearer self-selects). | Title patterns + context |

If you can't fill these in clearly from the data, **the angle is not actually
validated** — you've found a BSR-shaped pattern without a buyer narrative, and
the design will likely miss. Either dig deeper or drop the angle.

### 3.5b — Market structure (top 25 by category, as percentages)

Sort the niche's top 25 selling listings by BSR. Bucket each by **slogan format
category**:

- **Pure descriptive** (no clever slogan, e.g. "Rooster Wearing Sunglasses Photobooth Selfie")
- **Specific identity** ("Just A Girl Who Loves X", "X Grandma", "X Nerd")
- **Self-deprecating humor / ownership** ("MY X Has an Attitude Problem", "Chickens Make Me Happy / Humans Make My Head Hurt")
- **Generic puns** ("Rules the X", "X Whisperer") — almost always saturated
- **Profession / role** (e.g. "Chicken Daddy", "Head of Security")
- **Vintage / retro art** (no slogan, art-led)
- **Pop-culture parody** — TM risk, audit carefully
- **Other** — note what

Report as a percentage breakdown:

```
Chicken keeper top-25 structure:
  identity (specific)      32%
  profession / role        20%
  humor / ownership        20%
  descriptive (visual-led) 12%
  vintage / retro           8%
  generic puns              4%
  other                     4%
```

**Why this matters:** it tells you the *load-bearing categories* for the niche.
A new design entering a category that's 0–4% of the top-25 is fighting against
the market, no matter how clever it is. A new design entering the dominant
category competes for share but has the wind behind it.

### 3.5c — Visual hook vs text hook (top 5 sellers)

For each of the top 5 BSR sellers, fill in:

| Listing | Visual hook (1 line) | Text hook (1 line) | Load-bearing |
|---|---|---|---|
| Rooster Sunglasses Photobooth | Sunglasses on cartoon rooster | (no slogan, descriptive title) | **visual** |
| Bird Nerd Blue Jay | Field-guide Blue Jay illustration | "BIRD NERD + species" format | **text** |
| Just A Girl Who Loves Chickens (floral) | Floral wreath + cute hen | "Just A Girl Who Loves X" identity | **text** |

This determines how to brief the generation: a visual-load-bearing design needs
a strong illustration with minimal lettering; a text-load-bearing design needs
strong typography with template-able art. Mixing the wrong hook with the wrong
emphasis is a common failure mode.

---

## Step 4 — Output a ranked shortlist

Write `niche-research/<niche>.md` containing:

1. **Data confidence** — which CSVs/roles were available (or "reasoned estimate, no data").
2. **Ranked table** — term, Opportunity score, the D/C/S/F that drove it, evidence
   (e.g. "rising saves, only 60 listings, top result 4 reviews, listed last month").
3. **Recommended target + angle** — the chosen term, the differentiated angle, and why.
4. **Psychology block** (Identity / Tribe / Emotion / Giftability) for each top angle. See Step 3.5a.
5. **Market structure %** — top-25 categorical breakdown. See Step 3.5b.
6. **Visual-hook vs text-hook table** for the top 5 sellers, with the load-bearing call. See Step 3.5c.
7. **Trademark screen result** for the chosen phrase.
8. **Color profile rec** (`__p{N}`) for the planned design.

Then hand the chosen concept to the generation step (`config/generation.md`).

**Important:** picking the niche + angle is only half. Before *any* image is
generated, the chosen **slogan** must pass the **Slogan validation gate**
documented in `config/generation.md`. Generic puns or invented slogans that
don't match the format pattern of the niche's top sellers are the most common
way to waste credits on dead designs — even when the angle and visual are right.

---

## Worked example (no-data / reasoned mode)

For the `axolotl` demo there was no CSV, so confidence was LOW. The pick
("A LOTL GOING ON") came from: known durable fandom (D, est.), pun widens audience,
TM-clear phrase. Flagged explicitly as an estimate — exactly what this method
replaces once a real CSV lands.
