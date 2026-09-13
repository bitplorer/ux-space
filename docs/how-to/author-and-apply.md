# How to author a graph and emit verbs

**Diátaxis:** how-to. Surfaces are from `ux_space` public names and
passing tests. Stand-in Cap tokens here match the tests; product code
passes a Channel-minted Cap (`ch.control` / `CapService.mint`). The
token never rides ops / Result (`ops[].meta.cap` is disclosure).

## Soft 1 — one graph, Cap-gated `apply`

From `tests/test_graph.py` and `tests/test_ops.py`:

```python
from ux_space import CapRequired, apply, space, to_result

graph = space("stage").host("stage-3d").node("hero", shape="box", color="#6366f1")
plan = graph.plan()
assert plan["graph"]["host"] == "stage-3d"
assert plan["graph"]["nodes"][0]["id"] == "hero"

ops = apply(graph, cap="channel-minted-token")
result = to_result(ops)
assert ops[0]["op"] == "bridge.call"
assert ops[0]["method"] == "apply"
assert ops[0]["package"] == "ux-space"
assert "cap" not in ops[0]
assert "meta" not in ops[0]
```

`graph.apply(cap=...)` returns the same Result shape (`tests/test_graph.py`).
Missing Cap raises `CapRequired`. `apply` needs `host=` or `plan.graph.host`.

## Soft 2 — locked SHAPES on `.node(..., shape=)`

From `tests/test_soft2_shapes.py`. Soft 2 names KEEP. No `.box()` /
`.sphere()` helpers.

```python
from ux_space import space, validate_plan

for shape in ("box", "sphere", "plane", "cylinder"):
    out = validate_plan(space("stage").node("hero", shape=shape).plan())
    assert out["graph"]["nodes"][0]["shape"] == shape
```

`icosahedron` / `torusKnot` fail closed (`PlanError`). Soft 10 adds
`cone` / `torus` on the same `shape=` kwarg — see below.

## Soft 3 — `.camera` / `.light`

From `tests/test_soft3_camera_light.py`. Frozen names: `Graph.camera` /
`Graph.light` — not `.node(..., kind=)`.

```python
from ux_space import space

graph = (
    space("stage")
    .host("stage-3d")
    .camera("eye", camera="perspective", position=(0, 0.35, 4.2))
    .light("fill", light="ambient", color="#ffffff")
    .light("key", light="directional", position=(3, 4, 5))
    .node("hero", shape="box", color="#6366f1")
)
kinds = [n["kind"] for n in graph.plan()["graph"]["nodes"]]
assert kinds == ["camera", "light", "light", "node"]
```

Locked set: camera `perspective`; lights `ambient` / `directional`.
`orthographic` / `point` / `spot` fail closed.

## Soft 4 — transform + `material.type=basic`

From `tests/test_soft4_transform_material.py`. Top-level mesh `color`
KEEP; if both are set, `material.color` wins. Camera may take
`rotation=`. Lights stay position / color.

```python
from ux_space import space

graph = (
    space("stage")
    .host("stage-3d")
    .camera("eye", camera="perspective", position=(0, 0.35, 4.2), rotation=(0, 0.1, 0))
    .node(
        "hero",
        shape="box",
        color="#6366f1",
        rotation=(0.1, 0.2, 0.3),
        scale=1.5,
        material={"type": "basic", "color": "#22c55e", "opacity": 0.8},
    )
)
hero = graph.plan()["graph"]["nodes"][1]
assert hero["rotation"] == [0.1, 0.2, 0.3]
assert hero["scale"] == 1.5
assert hero["material"]["type"] == "basic"
```

`scale` may be a number or `[x, y, z]`. `opacity` is 0..1.
`material.type=phong` / `physical` / `lambert` fail closed.

## Soft 5 — same Graph after a Peer swap

Do not change this how-to's Graph. Load `ux_space/peers/canvas/`
**instead of** `ux_space/peers/threejs/`. Same
`uxBridge.register("ux-space", { mount, update, call })`.
Steps: [swap-the-peer.md](swap-the-peer.md).

## Soft 6 — `pickable` + Cap-gated `pick`

From `tests/test_soft6_pick_hit.py`. Frozen name: `.node(..., pickable=)`.
Hit args: `node_id` and optional `point` `[x, y, z]`.

```python
from ux_space import pick, space, to_result

graph = space("s").host("stage-3d").node("hero", shape="box", pickable=True)
assert graph.plan()["graph"]["nodes"][0]["pickable"] is True

ops = pick({"node_id": "hero", "point": [0.1, 0.2, 0.3]}, host="stage-3d", cap="tok")
result = to_result(ops)
assert ops[0]["method"] == "pick"
assert ops[0]["args"][0]["node_id"] == "hero"
assert ops[0]["args"][0]["point"] == [0.1, 0.2, 0.3]
assert "cap" not in ops[0]
```

`point` is optional: `pick({"node_id": "hero"}, host="h", cap="tok")`.
Channel owns click = Intent. This Soft does not invent a generic
pointer stack.

## Soft 7 — camera `orbit` / `pan` / `zoom`

From `tests/test_soft7_orbit_pan_zoom.py`. Frozen names:
`.camera(..., orbit=, pan=, zoom=)`. Plan field `zoom` is a positive
distance. Verbs take mappings; `zoom()` wants `distance`.

```python
from ux_space import orbit, pan, space, zoom

graph = (
    space("stage")
    .host("stage-3d")
    .camera(
        "eye",
        camera="perspective",
        orbit={"azimuth": 0.4, "polar": 1.2},
        pan={"x": 0.1, "y": 0.2},
        zoom=5.0,
    )
    .node("hero", shape="box")
)
eye = graph.plan()["graph"]["nodes"][0]
assert eye["orbit"] == {"azimuth": 0.4, "polar": 1.2}

assert orbit({"azimuth": 0.2, "polar": 1.1}, host="stage-3d", cap="tok")[0]["method"] == "orbit"
assert pan({"x": 0.3, "y": -0.1}, host="stage-3d", cap="tok")[0]["method"] == "pan"
assert zoom({"distance": 3.5}, host="stage-3d", cap="tok")[0]["method"] == "zoom"
```

Thin Peer apply — not OrbitControls. `zoom=0` / negative fail closed.

## Soft 8 — `material.type` `{basic, standard}`

From `tests/test_soft8_materials.py`. Soft 4 `basic` (`color` /
`opacity`) KEEP. `standard` may take `metalness` / `roughness` (0..1).

```python
from ux_space import space

node = (
    space("s")
    .node(
        "hero",
        shape="box",
        material={
            "type": "standard",
            "color": "#22c55e",
            "opacity": 0.8,
            "metalness": 0.2,
            "roughness": 0.55,
        },
    )
    .plan()["graph"]["nodes"][0]
)
assert node["material"]["type"] == "standard"
assert node["material"]["metalness"] == 0.2
```

Not a materials catalog. `peers/canvas` honors color / opacity;
`standard` degrades as `basic` (2D fill).

## Soft 9 — `.gltf` / `.texture` + `material.map`

From `tests/test_soft9_loaders.py`. Frozen names: `Graph.gltf` /
`Graph.texture` — not `.node(..., kind=)` and not a `load()` verb.
`src` is a relative path or http(s) URL. `material.map` is a texture
node id. Load rides Cap-gated `apply` only.

```python
from ux_space import apply, space

graph = (
    space("stage")
    .host("stage-3d")
    .texture("albedo", src="albedo.png")
    .gltf("prop", src="prop.gltf", position=(1.2, 0.0, -0.4), rotation=(0.0, 0.3, 0.0), scale=0.5)
    .node(
        "hero",
        shape="box",
        material={"type": "standard", "map": "albedo"},
    )
)
plan = graph.plan()
assert plan["graph"]["nodes"][0]["kind"] == "texture"
assert plan["graph"]["nodes"][1]["kind"] == "gltf"
ops = apply(graph, cap="tok")
assert ops[0]["method"] == "apply"
```

`javascript:` / `file:` / `blob:` `src` fail closed. `https://…` and
root-relative `/tex/…` are accepted. Loader constructors stay inside
`ux_space/peers/threejs/ux-space.js` — not a public GLTFLoader dump.

## Soft 10 — additive `cone` / `torus`

From `tests/test_soft10_primitives.py`. Same Soft 2 fluency:
`.node(..., shape=)`. No `.cone()` / `.torus()`.

```python
from ux_space import space

assert space("s").node("n", shape="cone").plan()["graph"]["nodes"][0]["shape"] == "cone"
assert space("s").node("n", shape="torus").plan()["graph"]["nodes"][0]["shape"] == "torus"
```

Soft 2 `box` / `sphere` / `plane` / `cylinder` KEEP. Catalog names
(`icosahedron`, `dodecahedron`, `torusKnot`, `capsule`, …) fail closed.

## Runnable composition

[examples/soft_surface/plan.py](../../examples/soft_surface/plan.py)
composes Soft 2–10 on one public Graph. Always-works:

```bash
PYTHONPATH=. python examples/soft_surface/plan.py
```
