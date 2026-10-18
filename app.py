"""Composition root: ``build()`` discovers ``routes/`` with ux-compose DirectoryRoutes.

URL = file path: routes/index.py → /, routes/shop.py → /shop,
routes/product/[sku].py → /product/{sku}. Run: ``uxcompose serve dev``
or ``uvicorn app:asgi``.
"""
from __future__ import annotations

from pathlib import Path

from ux_compose.build import build

from document import document
from settings import webassets
from ui import shell

PACKAGE = Path(__file__).resolve().parent


def main():
    app, asgi, bundle = build(
        PACKAGE,
        name="ux-demo",
        host="fastapi",
        live="auto",
        level=1,
        base="routes",
        document=document,
        wrap=shell(document),
        cek="require",
    )
    asgi = webassets.mount_css(asgi)
    return app, asgi, bundle


app, asgi, bundle = main()
