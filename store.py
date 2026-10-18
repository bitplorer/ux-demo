"""Process-local order book (demo only; resets on restart)."""
from __future__ import annotations

import itertools
import threading
from dataclasses import dataclass

_lock = threading.Lock()
_seq = itertools.count(1001)
_orders: list["Order"] = []


@dataclass(frozen=True)
class Order:
    number: int
    lines: tuple[tuple[str, int], ...]
    total: int


def place(lines: tuple[tuple[str, int], ...], total: int) -> Order:
    with _lock:
        order = Order(next(_seq), tuple(lines), int(total))
        _orders.append(order)
        return order


def orders() -> list[Order]:
    with _lock:
        return list(reversed(_orders))


def reset() -> None:
    with _lock:
        _orders.clear()
