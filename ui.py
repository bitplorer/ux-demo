"""Shared fragments and the GET shell (nav + footer around each page)."""
from __future__ import annotations

from ux_compose import a, article, button, control, div, footer, h3, header, main, nav, p, span

from catalog import Product, money

BTN = "rounded-full bg-stone-900 px-4 py-2 text-sm font-medium text-stone-50 hover:bg-stone-700"
GHOST = "rounded-full border border-stone-300 px-4 py-2 text-sm hover:bg-stone-100"

NAV = (("/", "Home"), ("/shop", "Shop"), ("/wish", "Saved"), ("/bag", "Bag"), ("/orders", "Orders"))


def card(prod: Product):
    return article(
        div(className=f"h-32 rounded-xl swatch-{prod.category}", aria_hidden="true"),
        h3(a(prod.name, href=f"/product/{prod.sku}", className="hover:underline"), className="mt-3 font-semibold"),
        p(prod.line, className="text-sm text-stone-600"),
        div(
            span(money(prod.price), className="font-medium tabular-nums"),
            button("Add to bag", type="button", className=BTN, **control("bag.add", sku=prod.sku)),
            className="mt-3 flex items-center justify-between",
        ),
        id=f"card-{prod.sku}",
        className="rounded-2xl border border-stone-200 bg-white p-4 shadow-sm",
    )


def shell(document):
    """Return the ``wrap`` for ``build()``: nav + main + footer around a page fragment."""

    def wrap(child=None):
        bar = header(
            nav(
                span("Harbor & Co.", className="font-display text-lg"),
                *[a(label, href=href, className="text-sm hover:underline") for href, label in NAV],
                className="mx-auto flex max-w-5xl items-center gap-6 px-6 py-4",
                aria_label="Site",
            ),
            className="border-b border-stone-200 bg-white",
        )
        body = main(child, className="mx-auto max-w-5xl px-6 py-10") if child is not None else main()
        foot = footer(
            p("A ux-compose + ux-dom demo. State is in memory and resets on restart."),
            className="mx-auto max-w-5xl px-6 py-8 text-xs text-stone-500",
        )
        return document(bar, body, foot)

    return wrap
