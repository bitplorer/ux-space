# Plan IR v1

**Diátaxis:** reference. Source: `ux_space/core/_ir.py` and
`validate_plan`. Major is `v: "1"`. Additive fields only. Unknown
fields are kept (receivers ignore them). Keys are never reused. A new
`v` is the only legal break.

## Envelope

```python
from ux_space import space, validate_plan

plan = space("stage").node("hero", shape="box", color="#6366f1").plan()
out = validate_plan(plan)
assert out["v"] == "1"
assert out["kind"] == "plan"
assert out["id"] == "stage"
assert out["graph"]["kind"] == "graph"
```

`plan.graph.nodes` is a non-empty list. Missing `graph` or empty
`nodes` raises `PlanError`. `plan.v == "2"` fails closed.

`dumps(plan)` / `loads(raw)` round-trip through `validate_plan`
(`tests/test_ops.py`).

## Locked sets

These names are the Soft 1–10 spine. They are not catalogs.

| Set | Values | Soft |
|-----|--------|------|
| `SHAPES` | `box`, `sphere`, `plane`, `cylinder`, `cone`, `torus` | 2 + 10 |
| `CAMERAS` | `perspective` | 3 |
| `LIGHTS` | `ambient`, `directional` | 3 |
| `MATERIALS` | `basic`, `standard` | 4 + 8 |
| `LOADERS` / loader `kind` | `gltf`, `texture` | 9 |
| `NODE_KINDS` | `node`, `camera`, `light`, `gltf`, `texture` | 1, 3, 9 |

Rejected examples from tests: `icosahedron`, `torusKnot`, `dodecahedron`,
`capsule`, `orthographic`, `point`, `spot`, `phong`, `physical`,
`lambert`, `fbx`, `obj`, `usdz`, `hdr`.

## Mesh node (`kind: "node"`)

| Field | Type | Soft | Required |
|-------|------|------|----------|
| `id` | non-empty str | 1 | yes |
| `shape` | `SHAPES`, default `box` | 2, 10 | no |
| `color` | non-empty str | 1 | no |
| `position` | `[x, y, z]` numbers | 1 | no |
| `rotation` | `[x, y, z]` radians | 4 | no |
| `scale` | number or `[x, y, z]` | 4 | no |
| `material` | object, see below | 4, 8, 9 | no |
| `pickable` | bool | 6 | no |

`pickable` absent by default (`tests/test_soft6_pick_hit.py`).
`pickable="yes"` / `1` fail closed.

### `material`

| Field | Type | Soft | Notes |
|-------|------|------|-------|
| `type` | `basic` or `standard` (default `basic`) | 4, 8 | locked thin set |
| `color` | non-empty str | 4 | wins over top-level `color` |
| `opacity` | number 0..1 | 4 | |
| `metalness` | number 0..1 | 8 | intended for `standard` |
| `roughness` | number 0..1 | 8 | intended for `standard` |
| `map` | texture node id | 9 | not a URL |

## Camera node (`kind: "camera"`)

| Field | Type | Soft |
|-------|------|------|
| `id` | non-empty str | 3 |
| `camera` | `perspective` (default) | 3 |
| `position` | `[x, y, z]` | 3 |
| `rotation` | `[x, y, z]` radians | 4 |
| `orbit` | `{azimuth?, polar?}` numbers (radians) | 7 |
| `pan` | `{x?, y?}` numbers | 7 |
| `zoom` | positive number (distance) | 7 |

`zoom` on the Plan is a number. The Cap-gated `zoom()` verb takes
`{distance}` — same quantity, different shape (`tests/test_soft7_orbit_pan_zoom.py`).

## Light node (`kind: "light"`)

| Field | Type | Soft |
|-------|------|------|
| `id` | non-empty str | 3 |
| `light` | `ambient` (default) or `directional` | 3 |
| `color` | non-empty str | 3 |
| `position` | `[x, y, z]` | 3 |

No `rotation` / `scale` / `material` / `pickable` on lights.

## Loader nodes

| `kind` | Required | Optional | Soft |
|--------|----------|----------|------|
| `texture` | `id`, `src` | — | 9 |
| `gltf` | `id`, `src` | `position`, `rotation`, `scale` | 9 |

`src` must be http(s), root-relative (`/…`), or a schemeless relative
path. Other schemes fail closed (`tests/test_soft9_loaders.py`).

## Graph host

`plan.graph.host` is optional on the Plan. `apply()` requires it or
`host=`.
