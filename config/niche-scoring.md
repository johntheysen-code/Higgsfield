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

### 3.5d — Shirt-color analysis (which color profile this niche rewards)

Different niches reward different shirt colors. A floral feminine niche sells
on white/cream/sage. A vintage-distressed niche sells on heather grey and navy.
A patriotic niche sells on white + heather + navy simultaneously. **Picking the
wrong color profile leaves money on the table — and missing dual-variant
niches doubles it.**

The MerchFlux CSV doesn't directly carry per-listing shirt-color sales data, so
this step works by **style-indicator inference** from the under-1M-BSR pool:

1. **Grep top-seller titles** for style indicators:
   - `vintage / distressed / worn / faded / retro` → typically heather grey,
     navy, black, military green — **dark/heather shirts (p4)**
   - `floral / wildflower / daisy / botanical` → typically white, cream,
     sage, light pink — **light shirts (p5)**
   - `minimalist / line art / line drawing / gallery` → typically white,
     cream, off-white — **light shirts (p5)**
   - `american flag / 4th of july / patriotic / USA` → typically heather,
     navy, white, red — **multi-color (p1)** or **both p4 + p5**
   - `mystical / celestial / moon / tarot / skeleton` → typically black,
     navy, midnight — **dark shirts (p4)**
   - `kawaii / pastel / cute` → typically white, cream, light pink —
     **light shirts (p5)**
   - `bold cartoon character` (e.g., rooster sunglasses) → typically white
     showcases color — **light shirts (p5)**
   - `tie-dye / neon` → typically dark backgrounds make neon pop — **p4**

2. **Count the dominant signals.** Whichever style category has ≥40% of the
   style-indicator hits in the under-1M pool is the niche's dominant
   recommended color profile. Whichever style category has ≥20% but less than
   40% is a viable secondary profile.

3. **Dual-variant trigger.** If the niche has BOTH a dominant light-shirt style
   (floral/minimalist/kawaii) AND a dominant dark-shirt style (vintage/mystical)
   each crossing the 20% threshold → **the niche supports both color profiles**
   → **brief BOTH a `__p5` (light) AND a `__p4` (dark) version** of the same
   slogan-anchored design at generation time. This doubles the addressable
   shirt-color market for the same design effort.

4. **Write up the recommendation** in `niche-research/<niche>.md`:

```
Shirt-color analysis:
  Dominant style: vintage/distressed (12/29 hits = 41%) → p4 dark/heather
  Secondary style: floral (5/29 hits = 17%) → p5 light (not enough for dual)
  Recommendation: p4 dominant; if generating identity/Mama angle, switch to p5.
```

If both styles cross 20% → flag the design queue to **generate dual variants**
for every shipping design in this niche.

### Cross-niche shirt-color patterns (confirmed so far)

| Niche | Dominant style | Color profile | Dual? |
|---|---|---|---|
| Pickleball | vintage (11) + patriotic (5) | mixed — vintage→p4, patriotic→p1 | **yes** |
| Birding | vintage (8) + minimalist (4) | p5 dominant + p4 vintage variant | **yes** |
| Dachshund | patriotic (7) + minimalist (4) + vintage (3) | p5 dominant + p4 vintage variant | **yes** |
| Golden Retriever | patriotic (20) + vintage (10) | **strong dual** — p4 vintage + p5 retro + p1 patriotic | **yes** |
| Chicken Keeper | vintage (7) + floral (2) | p5 dominant + p4 vintage variant | **partial** |
| Crochet | vintage (3) + floral (1) | p5 dominant | no |
| Quilting | vintage (8) + floral (2) | p5 dominant + p4 vintage variant | **partial** |
| Sourdough | sparse signals | p5 default (no strong dual) | no |

**Pattern:** every niche with ≥10% vintage/distressed signal benefits from a
dark-shirt variant. **The default 'all p5' approach was leaving p4 sales on
the table for at least 5 of the 8 niches we've scored.**

---

## Step 4 — Output a ranked shortlist

Write `niche-research/<niche>.md` containing:

1. **Data confidence** — which CSVs/roles were available (or "reasoned estimate, no data").
2. **Ranked table** — term, Opportunity score, the D/C/S/F that drove it, evidence.
3. **Recommended target + angle** — the chosen term, the differentiated angle, and why.
4. **Psychology block** (Identity / Tribe / Emotion / Giftability) for each top angle. See Step 3.5a.
5. **Market structure %** — top-25 categorical breakdown. See Step 3.5b.
6. **Visual-hook vs text-hook table** for the top 5 sellers, with the load-bearing call. See Step 3.5c.
7. **Shirt-color analysis** (style-indicator counts + recommended color profile + dual-variant flag). See Step 3.5d.
8. **Trademark screen result** for the chosen phrase.

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

---

## Cross-niche patterns confirmed (lessons learned across 9 niches)

These are patterns that have shown up across multiple niche scores. Treat each
as a **prior** when scoring a new niche — but always re-verify in the CSV; some
patterns are niche-dependent (see asterisks).

### Identity formats — niche-dependent (DO NOT assume portability)

| Format | Pickleball | Dachshund | Chicken Keeper | Birding | Golden Retriever | Sourdough |
|---|---|---|---|---|---|---|
| **Mom/Dad/Mama identity** | strong | **WORKS** | works | mid | **DIES** | dies |
| **"Grandma/Nana"** | **WORKS (exclusive)** | dead | dead | dead | dead | dead |
| **"Just A Girl Who Loves"** | n/a | n/a | works | dies | dies | n/a |
| **Father's Day gift angle** | works | works | works | works | mid | dies |

**Hard rule confirmed:** **Grandma is pickleball-only.** Six niches now show
this. Stop testing Grandma slogans outside pickleball.

**Soft rule:** Mom/Dad identity is *niche-dependent.* It works for some
breeds and not others. *Always check median BSR of identity slogans before
mirroring.*

### Format-category patterns

| Format | Where it wins | Where it dies |
|---|---|---|
| **Cartoon meme** (dog drinking X, doing thing) | Golden Retriever | Dachshund (small market for memes) |
| **Authority/role + breed behavior** | Dachshund, Chicken Keeper, *Golden Retriever (queued test)* | Sourdough (no behavior-anchor traction) |
| **"In My X Era"** | Pickleball, Wine, Golden Retriever, Crochet | Sourdough (saturated) |
| **Vintage/Distressed** | broad — most niches | Sourdough (over-fished) |
| **Mystical / Celestial / Tarot** | **Cross-niche pattern: works as low-comp lane in over-fished niches** (Golden, Sourdough) | n/a |
| **"Head of Security" + breed villain** | Chicken (foxes), Dachshund (squirrels) | Golden (queued, untested) |

### Trend hypothesis ≠ POD market opportunity

**Two pre-scan misses (recorded):** I was overly optimistic that **backyard
chickens** and **sourdough** were rising-trend → POD opportunity. Data showed
both were heavily worked over by the time we looked:
- backyard chickens: 4 selling under 1M out of 47 listings
- sourdough: 19 selling under 1M out of 165, 58% above 2M BSR (dead)

**Updated discipline:** when proposing a niche pre-scan, separate two claims:
1. "Niche is trending/growing in culture" (about the *buyer base*)
2. "POD market still has room" (about *seller saturation on Amazon*)

These are NOT the same. Established trends often have seller saturation already.
**Always score the CSV before recommending a generation batch.**

### Aesthetic-bias self-correction

Recorded honest review: my agent-generated designs **default to badge style**
when the slogan is role-authority humor. Worth checking in the prompt:

- If the slogan is **identity / emotion / gift** → floral or warm illustration,
  NOT badge
- If the slogan is **trend format** (In My X Era, Mama, etc.) → typography-led,
  NOT badge
- If the slogan is **meme / absurdist** → cartoon scene (dog doing thing),
  NOT badge
- If the slogan is **premium / gallery** → minimalist line art with no-go list,
  NOT badge
- If the slogan is **mystical / niche subculture** → themed art (celestial,
  vintage tarot), NOT badge
- Badge style is correct **only** for fake-credential authority humor
  (Head of Security, Chief X Officer, etc.)

This list lives in `config/generation.md` and informs every prompt.
