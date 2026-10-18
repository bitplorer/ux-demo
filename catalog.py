"""Domain: a small, fixed catalogue (no database)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    line: str
    price: int
    category: str
    featured: bool = False


PRODUCTS: tuple[Product, ...] = (
    Product("apron", "Canvas apron", "Waxed cotton, brass rivets", 58, "kitchen", True),
    Product("board", "Serving board", "Quarter-sawn oak, oil finish", 72, "kitchen", True),
    Product("bowls", "Stoneware bowls", "Set of four, matte glaze", 64, "kitchen"),
    Product("throw", "Wool throw", "Undyed merino, blanket stitch", 96, "home", True),
    Product("basket", "Market basket", "Hand-woven seagrass", 44, "home"),
    Product("soap", "Olive soap", "Cold-process, unscented", 12, "bath"),
)

BY_SKU = {p.sku: p for p in PRODUCTS}


def get(sku: str) -> Product | None:
    return BY_SKU.get(sku)


def featured() -> list[Product]:
    return [p for p in PRODUCTS if p.featured]


def money(n: int) -> str:
    return f"${int(n)}"
