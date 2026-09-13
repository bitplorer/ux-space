"""Soft-surface Channel.boot demo. Isolation: Channel only through ux_space.wire.

    pip install 'ux-space[channel]' fastapi uvicorn
    PYTHONPATH=. uvicorn examples.soft_surface.app:app --host 127.0.0.1 --port 8080

Cap mint stays Channel (`ch.control`). This Soft applies the leftover graph.
Day-1 Peer is ``peers/threejs`` registered as ``ux-space``. Canvas Peer is
swap-proof only — do not load both (not dual concurrent Peers).
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from examples.soft_surface.plan import soft_surface
from ux_space import PACKAGE, apply, host_html, pick
from ux_space.peers.threejs import adapter_path
from ux_space.wire import as_channel_result, boot, register_manifest

STATIC = Path(adapter_path()).resolve().parent

app = FastAPI(title="ux-space soft-surface")
app.mount("/ux-space", StaticFiles(directory=str(STATIC)), name="ux-space")

ch = boot(
    app,
    secret="dev-secret-key-32chars-minimum!!!!",
)

try:
    register_manifest(
        PACKAGE,
        description="ux-space day-1 Peer (three.js adapter)",
        hub=getattr(ch, "hub", None),
    )
except ImportError:
    pass


@ch.on(name="Space.apply")
def apply_space(ctx=None, **kw):
    cap = kw.get("cap")
    if cap is None and ctx is not None:
        cap = getattr(ctx, "cap", None)
    if not cap:
        # Channel already verified the Intent before this handler.
        # apply() still requires a token so the Soft never goes ambient.
        cap = getattr(getattr(ctx, "intent", None), "cap", None) or "channel-verified"
    return as_channel_result(apply(soft_surface(), host="stage-3d", cap=cap))


@ch.on(name="Space.pick")
def pick_space(ctx=None, **kw):
    cap = kw.get("cap")
    if cap is None and ctx is not None:
        cap = getattr(ctx, "cap", None)
    if not cap:
        cap = getattr(getattr(ctx, "intent", None), "cap", None) or "channel-verified"
    hit = {"node_id": kw.get("node_id") or "box"}
    if kw.get("point") is not None:
        hit["point"] = kw["point"]
    return as_channel_result(pick(hit, host="stage-3d", cap=cap))


@app.get("/", response_class=HTMLResponse)
def index():
    graph = soft_surface()
    host = host_html("stage-3d", plan=graph.plan(), class_name="viewport")
    control = ""
    if hasattr(ch, "control"):
        try:
            attrs = ch.control(apply_space)
            as_dict = getattr(attrs, "as_dict", None)
            if callable(as_dict):
                pairs = " ".join(f'{k}="{v}"' for k, v in as_dict().items())
                control = f"<button type='button' {pairs}>Apply</button>"
        except Exception:
            control = "<p>Channel.control unavailable — Plan still authored in Python.</p>"
    return f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8"/>
  <title>ux-space soft-surface</title>
  <style>
    body {{ margin: 0; font-family: system-ui, sans-serif; background: #070b16; color: #e2e8f0; }}
    main {{ max-width: 48rem; margin: 2rem auto; padding: 0 1rem; }}
    .viewport {{ height: 22rem; border-radius: 12px; background: #020617; }}
  </style>
</head><body>
<main>
  <h1>ux-space soft-surface</h1>
  <p>Public <code>space()</code> / <code>Graph</code> → Cap-gated <code>apply</code> →
     <code>bridge.call</code> → day-1 Peer <code>ux-space</code> (threejs).</p>
  <p>Soft 2 SHAPES · Soft 3 camera/light · Soft 4 rotation/scale +
     <code>material.type=basic</code>. Soft 5: canvas is swap-proof only —
     this host does not load a second Peer.</p>
  {host}
  {control}
</main>
<script src="/ux-channel/static/ux-bridge.js"></script>
<script src="/ux-space/ux-space.js"></script>
</body></html>"""
