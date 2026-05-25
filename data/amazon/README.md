# Amazon / MerchFlux data (competition + sales signal)

Drop MerchFlux CSV exports here. This is the **competition + proven-sales** feed
for the niche-scoring method (`../../config/niche-scoring.md`).

## First pull — what to search

Run each term in Amazon with MerchFlux active, then export. **Go narrow** —
broad terms are saturated; specific sub-niches are where the gaps are.

Starter seeds (also add any niches you're curious about):

- **Professions:** `occupational therapist`, `welder`, `dental hygienist`, `ICU nurse`, `electrician dad`
- **Hobbies:** `pickleball`, `disc golf`, `crochet`, `sourdough`, `bouldering`
- **Pets / animals:** `axolotl`, `corgi mom`, `chicken lady`, `frog`
- **Identity / humor:** `overstimulated mom`, `introvert humor`, `sarcastic plant mom`, `dog dad`
- **Faith / mental health:** `mental health awareness`, `faith over fear`, `anxiety humor`

## What signals to capture (whatever MerchFlux exports)

- **term / keyword** — what was searched
- **result_count / competition** — how many listings (saturation)
- **bsr** — Best Sellers Rank of the top results (proof it sells)
- **price**
- **listing/created date** — if available (freshness signal)

## What "good" looks like (eyeball while you go)

- **Competition:** under ~1000 results = workable, under ~500 = strong gap
- **Sales:** top designs with **BSR under ~300K** (MerchFlux's own guidance), and **not hundreds of competing listings**
- **Freshness:** recently listed designs that *already* rank well
- **Sweet spot:** a term where things clearly **sell** but there **aren't many listings**

> Note: CSV export + competition score are **paid-only** in MerchFlux. On the
> free version you'll only see BSR — capture it via screenshot instead of CSV.

## Handoff

Export a CSV per search (or one combined CSV) and drop the file(s) here. Then
tell me they've landed — I'll run the scoring and return a ranked shortlist with
the evidence, then generate designs for the winner.

(If MerchFlux has a filter for "result count under N" or "new designs," use it —
it auto-surfaces the low-competition gaps.)
