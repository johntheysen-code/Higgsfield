# Etsy / marketplace data (competition signal)

Drop Etsy or Amazon research CSV exports here.

This is the **competition / supply** side: how saturated a niche is and what sells.

## Ideal columns (don't worry if some are missing)

- `keyword` / `search_term` — the term searched
- `title` — listing title
- `price` — listing price
- `result_count` — how many listings exist for the keyword (saturation)
- `favorites` / `reviews` — interest / sales proxy
- `baskets` / `carts` — real-time buying signal (iScaleEtsy)
- `bsr` — Best Sellers Rank (Amazon tool), lower = selling more
- `first_review_date` — listing age; recent + high traction = fresh opportunity
- `date` — when the row was captured

Any CSV works — I'll adapt to whatever columns your tool exports. Just drop the
file in this folder and tell me it's here.
