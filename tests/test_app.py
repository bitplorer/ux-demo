"""ux-demo: path-law routes, GET shell, and live actions over the Channel HTTP door."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CH = {"X-Channel": "1"}


def _control(page_html: str, action: str, sku: str | None = None):
    """Return (args, cap) minted by ``control()`` for ``action`` on a rendered page."""
    for m in re.finditer(
        r'data-channel-action="([^"]+)" data-channel-args="([^"]*)" data-channel-cap="([^"]+)"', page_html
    ):
        if m.group(1) != action:
            continue
        args = json.loads(html.unescape(m.group(2)))
        if sku is None or args.get("sku") == sku:
            return args, m.group(3)
    raise AssertionError(f"no control for {action} {sku or ''}")


def _act(client, page: str, action: str, sku: str | None = None):
    args, cap = _control(client.get(page).text, action, sku)
    r = client.post("/ux-channel/action", json={"v": "1", "action": action, "args": args, "cap": cap}, headers=CH)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is True, body
    return body


# --- routing (ux-compose DirectoryRoutes) ---------------------------------


def test_directory_routes_path_law():
    from ux_compose.routing import DirectoryRoutes

    core = DirectoryRoutes(ROOT, base_directory="routes")
    core.discover()
    assert {r.path for r in core.records} == {"/", "/shop", "/product/{sku}", "/bag", "/wish", "/orders"}
    assert all(r.method == "GET" and r.kind == "page" for r in core.records)


def test_build_route_table_matches(built):
    assert {r["path"] for r in built.bundle.route_table} == {
        "/", "/shop", "/product/{sku}", "/bag", "/wish", "/orders",
    }


@pytest.mark.parametrize("path", ["/", "/shop", "/product/board", "/bag", "/wish", "/orders"])
def test_pages_render_in_shell(client, path):
    r = client.get(path)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    t = r.text
    assert t.lstrip().lower().startswith("<!doctype html>")
    assert 'href="/css/output.css"' in t
    assert "Harbor &amp; Co." in t and 'href="/shop"' in t  # nav from the wrap, not render()
    assert "/ux-channel/static/ux-channel.js" in t  # Channel Document plugin
    assert "/ux-dom/static/x_element.js" in t
    assert "nonce-" in r.headers.get("content-security-policy", "")


def test_product_detail_and_unknown(client):
    t = client.get("/product/throw").text
    assert 'data-sku="throw"' in t and "Wool throw" in t and "$96" in t
    miss = client.get("/product/nope").text
    assert 'data-missing="1"' in miss


def test_shop_lists_whole_catalogue(client):
    from catalog import PRODUCTS

    t = client.get("/shop").text
    for prod in PRODUCTS:
        assert f'id="card-{prod.sku}"' in t
        assert f'href="/product/{prod.sku}"' in t


# --- live actions (Channel + Cap Host) ------------------------------------


def test_bag_add_remove_morphs_and_persists(client):
    body = _act(client, "/shop", "bag.add", "board")
    morph = [op for op in body["ops"] if op.get("op") == "morph"]
    assert morph and morph[0]["target"] == "#bag" and "Serving board" in morph[0]["html"]
    _act(client, "/product/board", "bag.add", "board")
    _act(client, "/", "bag.add", "apron")
    bag = client.get("/bag").text
    assert 'data-count="3"' in bag and "× 2" in bag and "$202" in bag  # 2×72 + 58
    _act(client, "/bag", "bag.remove", "board")
    bag = client.get("/bag").text
    assert 'id="line-board"' not in bag and 'data-count="1"' in bag


def test_checkout_places_order_and_empties_bag(client):
    _act(client, "/shop", "bag.add", "soap")
    _act(client, "/shop", "bag.add", "throw")
    _act(client, "/bag", "bag.checkout")
    assert 'data-empty="1"' in client.get("/bag").text
    orders = client.get("/orders").text
    assert "#1001" in orders and "$108" in orders and "Olive soap × 1" in orders


def test_checkout_is_fail_closed_without_cap(client):
    _act(client, "/shop", "bag.add", "soap")
    r = client.post("/ux-channel/action", json={"v": "1", "action": "bag.checkout", "args": {}}, headers=CH)
    assert r.status_code == 401 and r.json()["ok"] is False
    args, cap = _control(client.get("/bag").text, "bag.checkout")
    forged = cap[:-4] + ("0000" if not cap.endswith("0000") else "1111")
    r = client.post(
        "/ux-channel/action", json={"v": "1", "action": "bag.checkout", "args": args, "cap": forged}, headers=CH
    )
    assert r.json()["ok"] is False
    assert "No orders yet" in client.get("/orders").text


def test_wish_toggle(client):
    _act(client, "/product/basket", "wish.toggle", "basket")
    t = client.get("/wish").text
    assert 'data-count="1"' in t and 'id="card-basket"' in t
    _act(client, "/product/basket", "wish.toggle", "basket")
    assert 'data-empty="1"' in client.get("/wish").text


# --- hygiene ---------------------------------------------------------------


def test_only_public_ux_compose_and_ux_dom_apis():
    banned = ("ux_app", "ux_channel", "ux_dom.routing", "ux_dom.runtime", "ux_dom.plugins")
    hits = []
    for py in ROOT.rglob("*.py"):
        if any(part.startswith(".") or part in ("tests",) for part in py.relative_to(ROOT).parts):
            continue
        text = py.read_text(encoding="utf-8")
        for name in banned:
            if re.search(rf"^\s*(from|import)\s+{re.escape(name)}\b", text, re.M):
                hits.append(f"{py.relative_to(ROOT)}: {name}")
    assert hits == []


def test_minified_css_served_when_built(client):
    css = ROOT / "assets" / "static" / "file" / "css" / "output.css"
    if not css.is_file():
        pytest.skip("run `uxcompose build` first (CI does)")
    r = client.get("/css/output.css")
    assert r.status_code == 200
    assert "\n  " not in r.text[:2000]  # minified
    assert ".swatch-kitchen" in r.text
