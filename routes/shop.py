"""GET /shop — full catalogue grouped by category."""
from __future__ import annotations

from ux_compose import Component, div, h1, h2, section

from catalog import PRODUCTS
from ui import card


class Shop(Component):
    id = "shop"

    def render(self):
        groups: dict[str, list] = {}
        for prod in PRODUCTS:
            groups.setdefault(prod.category, []).append(prod)
        return div(
            h1("Shop", className="font-display text-3xl"),
            *[
                section(
                    h2(cat.title(), className="mt-8 text-lg font-semibold"),
                    div(*[card(prod) for prod in items], className="mt-3 grid gap-4 sm:grid-cols-3"),
                    id=f"cat-{cat}",
                )
                for cat, items in groups.items()
            ],
            id=self.id,
        )
