# features/

Future Softs that extend ux-space live here.

**Import law:** features may import `ux_space.core` only. They do not import
`ux_channel` (that stays behind `ux_space.wire/` or a compose `wire/` door).
They do not own a Peer — adapters live under `peers/`.

Soft 2 lives in `core/` SHAPES + Peer apply. Soft 3 lives in `core/`
camera/light node kinds + Graph `.camera` / `.light` + Peer apply.
Soft 4 lives in `core/` IR + Graph `.node` transform/material + Peer
apply. Soft 5 lives in `peers/canvas` + the Peer contract — not here.
This directory stays empty — do not invent a second Graph API here.
