"""GET / — hero and featured pieces."""
from __future__ import annotations

from ux_compose import Component, a, div, h1, h2, p, section

from catalog import featured
from ui import GHOST, card


class Index(Component):
    id = "home"

    def render(self):
        return div(
            section(
                h1("Things made to be used", className="font-display text-4xl"),
                p("A small shop built only on ux-compose and ux-dom public APIs.", className="mt-2 text-stone-600"),
                a("Browse the shop", href="/shop", className=f"mt-6 inline-block {GHOST}"),
                className="py-6",
            ),
            h2("Featured", className="mt-8 text-xl font-semibold"),
            div(*[card(prod) for prod in featured()], className="mt-4 grid gap-4 sm:grid-cols-3"),
            id=self.id,
        )
