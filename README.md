# THE WORLD — Saturday 21 November 2026

A one-page broadsheet summing up the world's news of Saturday
21 November 2026: 33 dated stories across 7 regions plus markets
and sport, every story reported that day (Reuters, AP, CNN, AFP,
USGS, ESA).

Lead stories: COP31 climate talks in overtime in Antalya; Saudi
defences downing 3 Houthi missiles over Riyadh; a M6.8 quake in
Peru's Junin Andes. Also: the Kryvyi Rih strike, the Sparta II
drone fire in the Baltic, Mexico's capture of "El Chapo Isidro",
the AI stock sell-off (S&P 500 -3.7%), the FBI crime-database hack
probe, BepiColombo reaching Mercury, and GTA 6's 99 on Metacritic.

## Files

- `entry.png` — the front page (1024x1024, rendered by `render.py`)
- `main.ts` — copies `entry.png` to the output directory (no network)
- `render.py` — draws the page with Pillow/DejaVu; re-run to regenerate
- `LICENSE` — MIT

## Verify

```sh
python3 render.py
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 node main.ts
MAKEFUN_OUTPUT_DIR=out2 node main.ts
sha256sum out1/entry.png out2/entry.png   # identical
```
