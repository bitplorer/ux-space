# Public API

**Diátaxis:** reference. Source: `ux_space/__init__.py` →
`ux_space.core` only. `wire/` is off this `__all__`.

Library version: `0.1.0a1` (`API_VERSION` / `__version__` /
`PEER_VERSION`). Plan IR major: `IR_VERSION` `"1"`.

## `ux_space.__all__`

| Export | Role |
|--------|------|
| `space`, `Graph` | One scene graph |
| `apply` | Cap-gated verb → `bridge.call` method `apply` |
| `pick` | Cap-gated verb → `bridge.call` method `pick` |
| `orbit`, `pan`, `zoom` | Cap-gated verbs → methods `orbit` / `pan` / `zoom` |
| `mount`, `update` | Channel-compatible bridge op builders (not verbs) |
| `to_result`, `host_html` | Result dict / SSR host attributes |
| `validate_plan`, `dumps`, `loads` | Plan IR |
| `PACKAGE`, `PEER`, `CONTRACT` | Wire package name + Peer contract |
| `CapRequired`, `PlanError` | Fail closed |
| `API_VERSION`, `IR_VERSION`, `PEER_VERSION`, `__version__` | Versions |
| `OP_MOUNT`, `OP_UPDATE`, `OP_CALL`, `OP_APPLY` | Bridge op type strings |
| `APPLY_METHOD`, `PICK_METHOD`, `ORBIT_METHOD`, `PAN_METHOD`, `ZOOM_METHOD` | `bridge.call` methods |

Banned public names (`tests/test_isolation.py`): `scene`, `Scene`,
`ux_scene`, `Channel`, `CapService`, `CapMachine`, `mint`.

## `space` / `Graph`

`space(gid=None) -> Graph`. Default id is `space-` + hex
(`tests/test_graph.py`). Empty graph `.plan()` raises `ValueError`.

Frozen builders (`ux_space/core/_graph.py`):

| Method | Soft | Notes |
|--------|------|-------|
| `host(host_id)` | 1 | Non-empty string |
| `node(id, *, shape="box", color=, position=, rotation=, scale=, material=, pickable=)` | 1–4, 6, 10 | Mesh. `shape` Soft 2 + Soft 10. No `kind=` |
| `camera(id, *, camera="perspective", position=, rotation=, orbit=, pan=, zoom=)` | 3, 4, 7 | Not `.node(..., kind=)` |
| `light(id, *, light="ambient", color=, position=)` | 3 | Lights stay position / color |
| `gltf(id, *, src=, position=, rotation=, scale=)` | 9 | `src` required at validate |
| `texture(id, *, src=)` | 9 | `src` required at validate |
| `plan()` | 1 | Validates IR v1 |
| `apply(*, host=, cap=)` | 1 | Result dict via `to_result(apply(...))` |

There is no `Graph.scene`, `Graph.load`, `Graph.cone`, `Graph.torus`,
`Graph.pick`, `Graph.orbit`.

## Verbs

All Cap-gated verbs call `require_cap(cap)` server-side and emit one
`bridge.call`. Token is not copied onto the op.

| Function | Args | `method` | Payload |
|----------|------|----------|---------|
| `apply(graph, *, host=, cap=, package=PACKAGE)` | Graph or plan mapping | `apply` | `[plan]` |
| `pick(hit, *, host=, cap=, package=PACKAGE)` | `hit` mapping | `pick` | `[{node_id, point?}]` |
| `orbit(orbit, *, host=, cap=, package=PACKAGE)` | `{azimuth? and/or polar?}` | `orbit` | same |
| `pan(pan, *, host=, cap=, package=PACKAGE)` | `{x? and/or y?}` | `pan` | same |
| `zoom(zoom, *, host=, cap=, package=PACKAGE)` | `{distance}` positive | `zoom` | same |

`apply` host comes from `host=` or `plan.graph.host`.
`pick` / `orbit` / `pan` / `zoom` require `host=`.

`mount(host, *, props=, package=)` → `bridge.mount`.
`update(host, props, *, replace=)` → `bridge.update`.
These are builders, not Cap-gated verbs.

`to_result(ops, *, ok=True, action=)` → `{"ok", "ops"}` and optional
`meta.action` (not `meta.cap`).

`host_html(host, *, plan=, class_name=, tag="div", inner=)` emits
`data-channel-bridge-id` / `data-channel-bridge-package="ux-space"`.
Package is never `"three"`.

## Isolation door (off `__all__`)

```python
from ux_space.wire import boot, apply, space, mount_channel, as_channel_result
```

`ux_space.wire.__all__` also re-exports `pick`, `orbit`, `pan`, `zoom`,
`host_html`, `to_result`, `PACKAGE`, `register_manifest`.
Cap Host KEEP on Channel (`Channel.boot` / `mount_channel`).
See [ux_space/wire/README.md](../../ux_space/wire/README.md).

## Peer contract

`PACKAGE == "ux-space"`. `PEER["day1"] == "threejs"`.
`PEER["identity"] == "adapter"`.
Methods: `apply`, `update`, `destroy`, `pick`, `orbit`, `pan`, `zoom`.
Adapters: `ux_space/peers/threejs/ux-space.js` (day-1),
`ux_space/peers/canvas/ux-space.js` (Soft 5 swap proof).
