# Ownership + HARD invariants

> **Diátaxis:** explanation · **Layer:** ux-space · **Soft:** 8 (materials)
> Council: CLEAR. Do not violate this lock. Soft day-1 KEEP.

## 0. One screen

```text
ux-space    GRAPH      space() / Graph → Plan IR v1 (additive JSON)
            VERB       apply(graph, host=, cap=) → bridge.call method=apply
                       Soft 6 leftover: pick(hit, host=, cap=) → method=pick
                       Soft 7 leftover: orbit/pan/zoom (host=, cap=) → method=orbit|pan|zoom
            PEER       thin adapter applies Result ops
                       day-1: peers/threejs registers as "ux-space"
                       swap-proof: peers/canvas registers as "ux-space"

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
   Soft 3 extends Plan IR + Peer apply with camera/light node kinds only.
   Soft 4 adds optional mesh transform (`rotation` / `scale`) and thin
   `material` `{basic}` only. Soft 5 leftover: a canvas Peer proves the
   swap under the same `ux-space` register; day-1 stays threejs. Soft 6
   leftover: optional mesh `pickable` plus Cap-gated `pick(hit)` —
   Peer raycast/pick reports `node_id` (+ `point`). Soft 7 leftover:
   optional camera `orbit` / `pan` / `zoom` plus Cap-gated
   `orbit` / `pan` / `zoom` — Peer applies thin camera pose, not
   OrbitControls. Soft 8 leftover: mesh `material.type` expands to a
   locked thin set `{basic, standard}` — not a materials catalog.
   HOLD zero-Peer 3D and dual concurrent Peers as taught product.
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
    concurrent Peers as taught product, Cap-on-ops, zero-Peer, renaming
    motion, sixth Cap Host, ambient Client authority, teaching Channel
    specialty ops.

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
                         Soft 5 leftover: peers/canvas proves the swap
                         day-1 remains peers/threejs
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

HOLD: R3F, materials catalog, dual Peers, Cap-on-ops, zero-Peer,
renaming motion, sixth Cap Host, ambient Client authority,
Soft 5 Peer-swap.

## 8. Soft 3 leftover

Leftover: optional IR node kinds `camera` / `light` — locked set
`perspective` camera + `ambient` / `directional` lights. Additive IR v1
fields. Frozen Graph names: `.camera(...)` / `.light(...)` (Soft day-1
fluency; not `.node(..., kind=)`). Peer `peers/threejs` applies camera +
lights when present; Soft 2 mesh nodes still work. No second Graph API.

KEEP: Isolation `wire/` only; Cap NEVER on ops/Result (`ops[].meta.cap` is
disclosure); Peer-as-adapter `ux-space` not `three`; never `scene()` /
`ux-scene`; Cap Host KEEP on Channel (`Channel.boot` / `mount_channel`);
`core/` stays truth. Soft 2 SHAPES KEEP (`box` / `sphere` / `plane` /
`cylinder`).

HOLD: R3F, materials catalog, dual Peers, Cap-on-ops, zero-Peer,
renaming motion, Soft 5 Peer-swap.

## 9. Soft 4 leftover

Leftover: optional mesh `rotation` `[x,y,z]` radians and `scale` (number
or `[x,y,z]`). Optional mesh `material` with locked type `{basic}` only
and optional `color` / `opacity` (0..1). Top-level mesh `color` KEEP as
shorthand; if both present, `material.color` wins. Frozen Graph names:
`.node(..., rotation=, scale=, material=)`. Camera may take `rotation=`.
Lights stay position/color. Peer `peers/threejs` applies rotation/scale
and basic material (`MeshBasicMaterial`); default mesh path stays sane
when `material` is absent. No second Graph API. No lookAt/controls/orbit.

KEEP: Isolation `wire/` only; Cap NEVER on ops/Result (`ops[].meta.cap` is
disclosure); Peer-as-adapter `ux-space` not `three`; never `scene()` /
`ux-scene`; Cap Host KEEP on Channel (`Channel.boot` / `mount_channel`);
`core/` stays truth. Soft 2 SHAPES KEEP (`box` / `sphere` / `plane` /
`cylinder`). Soft 3 camera/light KEEP (`perspective` / `ambient` /
`directional`).

HOLD: R3F, materials catalog, dual Peers, Cap-on-ops, zero-Peer,
renaming motion, sixth Cap Host.

## 10. Soft 5 leftover

Leftover: Peer-swap is proven. `peers/canvas` implements the same
contract — `uxBridge.register("ux-space", { mount, update, call })` —
with no three.js. Soft 2 mesh nodes draw as filled 2D shapes; Soft 4
`position` / `rotation` / `scale` / `color` / `material.type=basic`
(color + opacity) are honored. Soft 3 camera/light nodes no-op (2D
proof). Day-1 default stays `peers/threejs`. Swap **replaces** the
engine; it does not register a second product name (`canvas` / `three`)
and is not dual concurrent Peers as taught product. Graph / Plan IR /
`apply()` unchanged. `features/` stays empty.

KEEP: Isolation `wire/` only; Cap NEVER on ops/Result (`ops[].meta.cap` is
disclosure); Peer-as-adapter `ux-space` not `three`; never `scene()` /
`ux-scene`; Cap Host KEEP on Channel (`Channel.boot` / `mount_channel`);
`core/` stays truth. Soft 2 SHAPES KEEP (`box` / `sphere` / `plane` /
`cylinder`). Soft 3 camera/light KEEP (`perspective` / `ambient` /
`directional`). Soft 4 rotation/scale + `material` `{basic}` KEEP.

HOLD: R3F, materials catalog, Cap-on-ops, zero-Peer, renaming motion,
dual concurrent Peers as taught product, sixth Cap Host.

## 11. Soft 6 leftover

Leftover: optional mesh `pickable` (bool). Frozen Graph name:
`.node(..., pickable=)`. Additive IR v1 — keys never reused; unknown
fields ignored. Peer `peers/threejs` raycasts on pointer over the
canvas and reports a hit `{node_id, point?}`. `peers/canvas` swap-proof
does the same with a 2D hit-test (no three.js). Hit becomes Cap-gated
Intent args via `pick(hit, host=, cap=)` → `bridge.call` method `pick`
→ Result. Channel owns click=Intent (`uxChannel.runAction` when
present). Soft 6 does not invent a generic pointer stack, `@action`,
or Cap Host. No second Graph API. `features/` stays empty.

KEEP: Isolation `wire/` only; Cap NEVER on ops/Result (`ops[].meta.cap`
is disclosure); Peer-as-adapter `ux-space` not `three`; never `scene()` /
`ux-scene`; Cap Host KEEP on Channel (`Channel.boot` / `mount_channel`);
`core/` stays truth. Soft 2 SHAPES KEEP (`box` / `sphere` / `plane` /
`cylinder`). Soft 3 camera/light KEEP (`perspective` / `ambient` /
`directional`). Soft 4 rotation/scale + `material` `{basic}` KEEP.
Soft 5 canvas swap-proof KEEP; day-1 stays `peers/threejs`.
Server-side `require_cap` KEEP.

HOLD: Soft 7 orbit/pan/zoom, R3F, materials catalog, Cap-on-ops,
zero-Peer, renaming motion, dual concurrent Peers as taught product,
sixth Cap Host.

## 12. Soft 7 leftover

Leftover: optional camera `orbit` `{azimuth?, polar?}` radians,
`pan` `{x?, y?}`, and `zoom` (positive distance). Frozen Graph
names: `.camera(..., orbit=, pan=, zoom=)`. Additive IR v1 — keys
never reused; unknown fields ignored. Peer `peers/threejs` applies
those fields (and Cap-gated `orbit` / `pan` / `zoom` verbs) as a
thin spherical camera pose. `peers/canvas` swap-proof accepts the
same call methods without inventing a 2D camera API (Soft 3
camera/light stay no-op). Verbs: `orbit` / `pan` / `zoom`
`(payload, host=, cap=)` → `bridge.call` methods `orbit` / `pan` /
`zoom` → Result. Soft 7 is camera Plan ops, not a generic pointer
stack, `@action`, or Cap Host. No OrbitControls product dump. No
second Graph API. `features/` stays empty.

KEEP: Isolation `wire/` only; Cap NEVER on ops/Result (`ops[].meta.cap`
is disclosure); Peer-as-adapter `ux-space` not `three`; never `scene()` /
`ux-scene`; Cap Host KEEP on Channel (`Channel.boot` / `mount_channel`);
`core/` stays truth. Soft 2 SHAPES KEEP (`box` / `sphere` / `plane` /
`cylinder`). Soft 3 camera/light KEEP (`perspective` / `ambient` /
`directional`). Soft 4 rotation/scale + `material` `{basic}` KEEP.
Soft 5 canvas swap-proof KEEP; day-1 stays `peers/threejs`. Soft 6
pick/hit KEEP (`pickable` + Cap-gated `pick(hit)`). Server-side
`require_cap` KEEP.

HOLD: Soft 8 materials, Soft 9 loaders, Soft 10 primitives, R3F,
materials catalog, Cap-on-ops, zero-Peer, renaming motion, dual
concurrent Peers as taught product, sixth Cap Host, generic pointer
stack.

## 13. Soft 8 leftover

Leftover: mesh `material.type` expands to a locked thin set
`{basic, standard}` — **not the materials catalog**. Soft 4 `{basic}`
(`color` / `opacity`) KEEP. Soft 8 adds `standard` plus optional
`metalness` / `roughness` (0..1). Top-level mesh `color` KEEP; if
both present, `material.color` wins. Frozen Graph names:
`.node(..., material={type: ...})` — Soft 4 fluency, no second Graph
API. Additive IR v1 — keys never reused; unknown fields ignored.
Peer `peers/threejs` maps `basic` → `MeshBasicMaterial` and
`standard` → `MeshStandardMaterial`. Default mesh path stays
`MeshStandardMaterial` when `material` is absent. `peers/canvas`
swap-proof honors color/opacity; `standard` degrades as `basic`
(2D fill) without breaking. Cap-gated `apply` KEEP. Cap NEVER on
ops/Result. No loaders, primitives, or R3F. `features/` stays empty.

KEEP: Isolation `wire/` only; Cap NEVER on ops/Result (`ops[].meta.cap`
is disclosure); Peer-as-adapter `ux-space` not `three`; never `scene()` /
`ux-scene`; Cap Host KEEP on Channel (`Channel.boot` / `mount_channel`);
`core/` stays truth. Soft 2 SHAPES KEEP (`box` / `sphere` / `plane` /
`cylinder`). Soft 3 camera/light KEEP (`perspective` / `ambient` /
`directional`). Soft 4 rotation/scale + `material` `{basic}` KEEP.
Soft 5 canvas swap-proof KEEP; day-1 stays `peers/threejs`. Soft 6
pick/hit KEEP (`pickable` + Cap-gated `pick(hit)`). Soft 7 orbit/pan/zoom
KEEP. Server-side `require_cap` KEEP.

HOLD: Soft 9 loaders, Soft 10 primitives, R3F, materials catalog
(`phong` / `physical` / `lambert` / …), Cap-on-ops, zero-Peer,
renaming motion, dual concurrent Peers as taught product, sixth Cap Host,
generic pointer stack.
