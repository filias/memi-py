# memi pyrenees

A memory card game about the Pyrenees, built on
[memi-engine](https://github.com/filias/memi-engine).

Live at [py.memi.click](https://py.memi.click)

## Categories

- **peaks** — 12 great summits of the range, tagged with their elevation
- **wildlife** — 12 animals of the high Pyrenees, tagged with Latin names
- **flora** — 8 mountain plants, tagged with Latin names
- **lakes** — 6 mountain lakes (lacs, ibones, estanys)
- **valleys** — 6 famous valleys
- **passes** — 6 mountain passes (cols and ports)
- **parks → national / natural** — 3 national parks and 4 natural parks

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
