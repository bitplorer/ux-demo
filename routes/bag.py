"""GET /bag — live bag. Actions morph #bag; checkout is Cap-protected."""
from __future__ import annotations

from ux_compose import (
    Component, MorphState, RefState, action, button, control, div, h1, li, notify, p, span, ul, update_with,
)

import store
from catalog import get, money
from ui import BTN, GHOST


class Bag(Component):
    id = "bag"
    # MorphState drives the auto-morph; RefState holds the (sku, qty) lines.
    dirty = MorphState("idle")
    lines = RefState(())
    notice = RefState("")

    def rows(self) -> list[tuple[str, int]]:
        return [(str(s), int(q)) for s, q in (self.lines or ()) if get(str(s))]

    def subtotal(self) -> int:
        return sum(get(s).price * q for s, q in self.rows())

    def render(self):
        rows = self.rows()
        kids = [h1("Bag", className="font-display text-3xl")]
        if self.notice:
            kids.append(p(str(self.notice), role="status", className="mt-2 text-sm text-stone-600"))
        if not rows:
            kids.append(p("Your bag is empty.", className="mt-6 text-stone-500", data_empty="1"))
            return div(*kids, id=self.id, data_count="0")
        items = []
        for sku, qty in rows:
            prod = get(sku)
            items.append(
                li(
                    span(prod.name, className="flex-1"),
                    span(f"× {qty}", className="tabular-nums"),
                    span(money(prod.price * qty), className="w-16 text-right tabular-nums"),
                    button("Remove", type="button", className="text-sm underline", **control("bag.remove", sku=sku)),
                    id=f"line-{sku}",
                    className="flex items-center gap-4 py-2",
                )
            )
        kids += [
            ul(*items, className="mt-6 divide-y divide-stone-200"),
            div(
                span("Subtotal"),
                span(money(self.subtotal()), id="subtotal", className="font-semibold tabular-nums"),
                className="mt-4 flex justify-between",
            ),
            div(
                button("Clear", type="button", className=GHOST, **control("bag.clear")),
                button("Place order", type="button", className=BTN, **control("bag.checkout")),
                className="mt-6 flex justify-end gap-3",
            ),
        ]
        return div(*kids, id=self.id, data_count=str(sum(q for _, q in rows)))

    def _set(self, rows, notice: str):
        self.lines = tuple(rows)
        self.notice = notice
        self.dirty = "bag" if rows else "idle"

    @action(caps=())
    def add(self, sku: str = ""):
        prod = get(sku)
        if prod is None:
            return update_with(self, extra_ops=[notify(f"Unknown product {sku!r}")])
        rows = dict(self.rows())
        rows[sku] = rows.get(sku, 0) + 1
        self._set(rows.items(), f"Added {prod.name}")
        return update_with(self, extra_ops=[notify(f"Added {prod.name}")])

    @action(caps=())
    def remove(self, sku: str = ""):
        self._set([(s, q) for s, q in self.rows() if s != sku], "Removed")
        return update_with(self, extra_ops=[notify("Removed")])

    @action(caps=())
    def clear(self):
        self._set([], "Bag cleared")
        return update_with(self, extra_ops=[notify("Bag cleared")])

    @action(caps=("orders.place",))
    def checkout(self):
        rows = self.rows()
        if not rows:
            self.notice = "Bag is empty"
            return update_with(self, extra_ops=[notify("Bag is empty")])
        order = store.place(tuple(rows), self.subtotal())
        self._set([], f"Order #{order.number} placed · {money(order.total)}")
        return update_with(self, extra_ops=[notify(f"Order #{order.number} placed")])
