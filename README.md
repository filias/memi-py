# memi pyrenees

A memory card game about the Pyrenees, built on
[memi-engine](https://github.com/filias/memi-engine).

Live at [py.memi.click](https://py.memi.click)

## Categories

- **landscapes → peaks** — 12 great summits of the range, tagged with elevation
- **landscapes → lakes** — 6 mountain lakes (lacs, ibones, estanys)
- **landscapes → valleys** — 6 famous valleys
- **landscapes → passes** — 6 mountain passes (cols and ports)
- **life → animals** — 12 animals of the high Pyrenees, tagged with Latin names
- **life → plants** — 8 mountain plants, tagged with Latin names
- **parks → all** — the 7 national and natural parks of the Pyrenees
- **parks → Ordesa y Monte Perdido / Aigüestortes / Pyrénées / Posets-Maladeta / Guara** — the
  notable landmarks (peaks, valleys, lakes, cirques) inside each of the five
  parks with enough Wikipedia-imaged features to guess between

Images and *know more* links resolve from Wikipedia automatically. A small
`WikiImages` mixin (in `memi_py/providers/categories.py`) relaxes the engine's
strict title lookup — following redirects and falling back to search — so
natural display names still land on the right article.

## Setup

```bash
uv sync
uv run python -m memi_py.app      # dev server on http://localhost:8090
```

## Deploy

Same push-to-deploy flow as the other memi games: merging to `main` triggers a
GitHub webhook that pulls, `uv sync`s and restarts the service. See
[`deploy/`](deploy/) and the deploy section below.

## License

MIT
