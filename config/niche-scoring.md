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

## Step 4 — Output a ranked shortlist

Write `niche-research/<niche>.md` containing:

1. **Data confidence** — which CSVs/roles were available (or "reasoned estimate, no data").
2. **Ranked table** — term, Opportunity score, the D/C/S/F that drove it, evidence
   (e.g. "rising saves, only 60 listings, top result 4 reviews, listed last month").
3. **Recommended target + angle** — the chosen term, the differentiated angle, and why.
4. **Trademark screen result** for the chosen phrase.
5. **Color profile rec** (`__p{N}`) for the planned design.

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
