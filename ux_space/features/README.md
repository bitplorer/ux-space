# features/

Future Softs that extend ux-space live here.

**Import law:** features may import `ux_space.core` only. They do not import
`ux_channel` (that stays behind `ux_space.wire/` or a compose `wire/` door).
They do not own a Peer — adapters live under `peers/`.

Soft 2 lives in `core/` SHAPES + Peer apply. Soft 3 lives in `core/`
camera/light node kinds + Graph `.camera` / `.light` + Peer apply.
Soft 4 lives in `core/` IR + Graph `.node` transform/material + Peer
apply. Soft 5 lives in `peers/canvas` + the Peer contract — not here.
Soft 6 lives in `core/` IR `pickable` + Cap-gated `pick()` + Peer pick —
not here. Soft 7 lives in `core/` IR camera `orbit` / `pan` / `zoom` +
Cap-gated `orbit()` / `pan()` / `zoom()` + Peer apply — not here.
Soft 8 lives in `core/` IR `MATERIALS` `{basic, standard}` + Peer
apply — not here. Soft 9 lives in `core/` IR `LOADERS` `{gltf,
texture}` + Graph `.gltf` / `.texture` + `material.map` + Peer
apply — not here. Soft 10 lives in `core/` SHAPES
(`cone` / `torus` additive; Soft 2 names KEEP) + Peer apply — not
here. This directory stays empty — do not invent a second Graph
API here.
