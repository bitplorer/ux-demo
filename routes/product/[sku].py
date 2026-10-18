"""GET /product/{sku} — product detail (path param from the file name)."""
from __future__ import annotations

from ux_compose import Component, a, button, control, div, h1, p, span

from catalog import get, money
from ui import BTN, GHOST


class Sku(Component):
    id = "product"

    def render(self, sku: str = ""):
        prod = get(sku)
        if prod is None:
            return div(
                h1("Not found", className="font-display text-3xl"),
                p(f"No product {sku!r}."),
                a("Back to shop", href="/shop", className="underline"),
                id=self.id,
                data_missing="1",
            )
        return div(
            p(a("Shop", href="/shop", className="underline"), f" / {prod.category}", className="text-sm text-stone-500"),
            div(className=f"mt-4 h-56 rounded-2xl swatch-{prod.category}", aria_hidden="true"),
            h1(prod.name, className="mt-6 font-display text-3xl"),
            p(prod.line, className="text-stone-600"),
            span(money(prod.price), className="mt-2 block text-xl tabular-nums"),
            div(
                button("Add to bag", type="button", className=BTN, **control("bag.add", sku=prod.sku)),
                button("Save", type="button", className=GHOST, **control("wish.toggle", sku=prod.sku)),
                className="mt-6 flex gap-3",
            ),
            id=self.id,
            data_sku=prod.sku,
        )
