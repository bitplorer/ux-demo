"""GET /orders — orders placed from the bag this process."""
from __future__ import annotations

from ux_compose import Component, div, h1, li, p, span, ul

import store
from catalog import get, money


class Orders(Component):
    id = "orders"

    def render(self):
        rows = store.orders()
        if not rows:
            body = p("No orders yet.", className="mt-6 text-stone-500", data_empty="1")
        else:
            body = ul(
                *[
                    li(
                        span(f"#{o.number}", className="font-medium"),
                        span(", ".join(f"{get(s).name} × {q}" for s, q in o.lines), className="flex-1 text-stone-600"),
                        span(money(o.total), className="tabular-nums"),
                        id=f"order-{o.number}",
                        className="flex gap-4 py-2",
                    )
                    for o in rows
                ],
                className="mt-6 divide-y divide-stone-200",
            )
        return div(h1("Orders", className="font-display text-3xl"), body, id=self.id)
