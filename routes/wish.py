"""GET /wish — saved pieces (toggle from the product page)."""
from __future__ import annotations

from ux_compose import Component, MorphState, RefState, action, div, h1, notify, p, update_with

from catalog import get
from ui import card


class Wish(Component):
    id = "wish"
    dirty = MorphState("idle")
    skus = RefState(())

    def render(self):
        saved = [get(s) for s in (self.skus or ()) if get(s)]
        body = (
            div(*[card(prod) for prod in saved], className="mt-6 grid gap-4 sm:grid-cols-3")
            if saved
            else p("Nothing saved yet.", className="mt-6 text-stone-500", data_empty="1")
        )
        return div(h1("Saved", className="font-display text-3xl"), body, id=self.id, data_count=str(len(saved)))

    @action(caps=())
    def toggle(self, sku: str = ""):
        if get(sku) is None:
            return update_with(self, extra_ops=[notify(f"Unknown product {sku!r}")])
        cur = list(self.skus or ())
        if sku in cur:
            cur.remove(sku)
            msg = "Removed from saved"
        else:
            cur.append(sku)
            msg = "Saved"
        self.skus = tuple(cur)
        self.dirty = f"n{len(cur)}"
        return update_with(self, extra_ops=[notify(msg)])
