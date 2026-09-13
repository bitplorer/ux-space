# Ownership + HARD invariants

> **Diátaxis:** explanation · **Layer:** ux-space · **Soft:** 2 (shapes pack)
> Council: CLEAR. Do not violate this lock. Soft day-1 KEEP.

## 0. One screen

```text
ux-space    GRAPH      space() / Graph → Plan IR v1 (additive JSON)
            VERB       apply(graph, host=, cap=) → bridge.call method=apply
            PEER       thin adapter applies Result ops
                       day-1: peers/threejs registers as "ux-space"

ux-channel  CAP HOST   Cap mint · Channel.boot · mount_channel · Intent verify
            BRIDGE     bridge.mount / bridge.update / bridge.call

ux-motion   scene()    presence/transition plans — dual door; do not alias

ux-behavior @action    product behavior
ux-dom      RENDER     trees
ux-compose  PRODUCT    wire/ Isolation door for Channel
```

**Author rule:** Graph + apply here. Caps on Channel. Peer is an adapter.

## 1. HARD invariants

1. **Name.** Package `ux-space` / import `ux_space`. Never name anything
   public `ux-scene`, `scene`, or `Scene`. Dual door with ux-motion `scene()`.
2. **Seat.** Motion-shaped: Python Plans / Ops → Channel **Result** → thin
   Peer applies. Do not rename motion.
3. **Peer-as-adapter.** Three.js is the **day-1 Peer only**, not identity.
   Freeze Python graph + Cap-gated verb + Channel Result. Peer may swap
   later (canvas / WebGL / independent peer lib) without changing Graph.
4. **Day-1 Soft KEEP.** One graph + one Cap-gated verb (`apply`) + one thin
   Peer apply. Soft 2 unlocks a locked SHAPES set only — not a second Graph.
   HOLD zero-Peer 3D and dual Peers.
5. **Isolation.** Product never imports `ux_channel` outside a compose-style
   `wire/` door (`ux_space.wire` here). `core/` and `features/` never import
   Channel.
6. **Cap Host.** Cap mint / `Channel.boot` / `mount_channel` KEEP on Channel.
   Do not invent a second Cap Host. `apply()` only refuses a missing token
   **server-side**. The token must not ride the Result (`ops[].meta.cap` is
   disclosure). Peer does not need it.
7. **Bridge plane.** Under the hood, ops are `bridge.mount` /
   `bridge.update` / `bridge.call` (see `bitplorer/ux-channel@a6ab159`
   example `python/examples/ux_dom_threejs/`). Do not teach Channel
   immortal specialty ops beyond bridge.
8. **IR.** `v: "1"` additive JSON. Unknown fields ignored. Keys never reused.
   A new `v` is the only legal break.
9. **Layout.** `core/` is day-1 truth. `features/` import core only.
   `peers/` implement the Peer contract. Top `__all__` is frozen from core.
10. **HOLD.** React / R3F, materials catalog, full three.js catalog, dual
    Peers, Cap-on-ops, renaming motion, sixth Cap Host, ambient Client
    authority, teaching Channel specialty ops.

## 2. Cap

| Who | What |
|-----|------|
| Channel | `CapService.mint` / `ch.control` / Intent verify |
| ux-space | `require_cap` — token present or `CapRequired` (server-side only) |
| Peer | Applies ops. Never mints. Never sees the Cap. |

Passing `cap=` on `apply()` does not verify HMAC and does **not** copy the
token onto `bridge.call` / Result ops. Channel already verified when the
handler ran — or will verify when the Intent arrives. The Soft stays
Cap-aware so authoring without a token fails closed. Shipping Cap on the
Result is disclosure.

## 3. Peer-as-adapter

```text
Plan + apply() ops  ──►  uxBridge.register("ux-space", { mount, update, call })
                         day-1 engine: three.js CDN
                         later engine: canvas / WebGL / other lib
```

Product surface is **`ux-space`**, not `"three"`. The Channel three.js
example registers `"three"`; this Soft wraps that engine behind its own
package name.

Swap steps: [ux_space/peers/README.md](ux_space/peers/README.md).

## 4. Isolation / wire

```text
app / compose  →  ux_space.wire  →  ux_channel  (Channel.boot, mount_channel)
               →  ux_space       →  core only
```

`ux_space.wire` is **off** `ux_space.__all__`. Optional extra:
`pip install 'ux-space[channel]'`.

## 5. Forbidden

- Public `scene` / `Scene` / `ux-scene`
- Importing `ux_channel` from `core/` or `features/`
- Cap HMAC mint / verify / `CapMachine` in this Soft
- A second Cap Host beside Channel
- Cap token on client-bound Result ops (`ops[].meta.cap` or any op field)
- Identity = Three.js (catalog, React/R3F, dual Peers on day-1)
- Channel ops other than the bridge plane (`morph`, `toast`, `transition.*`, …)
- Vendoring Channel

## 6. Day-1 DONE

See the checklist in [CHANGELOG.md](CHANGELOG.md) `0.1.0a1`.

## 7. Soft 2 leftover

Leftover: IR `SHAPES` is a **locked Soft 2 set** (`box`, `sphere`, `plane`,
`cylinder`) — **not the full three.js catalog**. Peer `peers/threejs` is a
thin geometry map. Graph / `space()` / Cap-gated `apply()` unchanged.
`features/` stays empty — Soft 2 lives in `core/` SHAPES + Peer apply.

KEEP: Isolation `wire/` only; Cap NEVER on ops/Result (`ops[].meta.cap` is
disclosure); Peer-as-adapter `ux-space` not `three`; never `scene()` /
`ux-scene`; Cap Host KEEP on Channel (`Channel.boot` / `mount_channel`);
`core/` stays truth.

HOLD: R3F, materials catalog, dual Peers, Cap-on-ops, renaming motion,
sixth Cap Host, ambient Client authority.
