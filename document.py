"""Document: the single HTML shell for every GET.

``Channel`` is the ux-dom Document plugin that ships the live client;
this app never imports ``ux_channel`` directly.
"""
from __future__ import annotations

from ux_dom import Channel, Csp, Document, XElement
from ux_dom.dom import link, meta, title

from settings import OUTPUT_CSS

_plugins = (XElement(), Csp.auto(), Channel.optional())

document = Document(
    head=[
        meta(charset="utf-8"),
        meta(name="viewport", content="width=device-width, initial-scale=1"),
        title("Harbor & Co. · ux demo"),
        link(href=f"/css/{OUTPUT_CSS}", rel="stylesheet"),
    ],
    body=[],
    ensure_csrf_token=False,
).use(*[p for p in _plugins if p is not None])
