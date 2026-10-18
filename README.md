# ux-demo — Harbor & Co.

A small shop built **only** on the public APIs of
[ux-compose](https://github.com/bitplorer/ux-compose) and
[ux-dom](https://github.com/bitplorer/ux-dom). It replaces the archived
`bitplorer/harbor` example: harbor depended on the retired `ux-app`, so it could not
be installed or run.

## What it shows

| Feature | Where | API |
|---|---|---|
| File-path routing (URL = file path, class name never in the URL) | `routes/` | `ux_compose.build(base="routes")` → `ux_compose.routing.DirectoryRoutes` |
| Path params | `routes/product/[sku].py` → `/product/{sku}` | `render(self, sku=...)` |
| One HTML shell for every GET | `document.py`, `ui.shell()` | `ux_dom.Document(...).use(XElement(), Csp.auto(), Channel.optional())`, `build(wrap=)` |
| Components | `routes/*.py`, `ui.card()` | `ux_compose.Component`, ux-dom tags |
| Live actions + morph | bag add/remove/clear, saved toggle | `@action`, `control()`, `update_with`, `notify`, `MorphState`/`RefState` |
| Cap-protected action (fail closed) | `bag.checkout` | `@action(caps=("orders.place",))` |
| Minified Tailwind CSS | `assets/css/input.css` → `/css/output.css` | `uxcompose build`, `WebAssets.mount_css` |
| Strict CSP with nonces | every page | `Csp.auto()` |

Routes: `/`, `/shop`, `/product/{sku}`, `/bag`, `/wish`, `/orders`.
State (bag, saved items, orders) is held in memory and resets when the process restarts.

## Run

Python ≥ 3.14.

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
uxcompose build          # Tailwind → minified assets/static/file/css/output.css
uxcompose serve dev      # or: uvicorn app:asgi --port 8000
python -m pytest
```

## Layout

```text
app.py         composition root: build(host="fastapi", live="auto", document=, wrap=, cek="require")
document.py    Document + plugins (XElement, Csp, Channel)
settings.py    paths, DEBUG, WebAssets
ui.py          nav/footer shell (GET only) + product card
catalog.py     products (fixed data)
store.py       in-memory order book
routes/        page units; each file's class matches its stem (shop.py → Shop, [sku].py → Sku)
tests/         routing, shell, live actions over /ux-channel/action, hygiene
```

## Rules this repo keeps

- Imports come only from `ux_compose` and top-level `ux_dom` / `ux_dom.dom`.
  No `ux_channel`, `ux_app`, `ux_dom.routing`, `ux_dom.runtime` or `ux_dom.plugins`
  (`tests/test_app.py::test_only_public_ux_compose_and_ux_dom_apis`).
- `render()` returns a fragment. The nav and footer come from the `wrap`, so a morph
  never re-sends the page chrome.
