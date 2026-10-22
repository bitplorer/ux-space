# wire/

Isolation door. **Off** the top-level `ux_space.__all__`.

Product code that must speak Channel imports **here** (or a compose
`wire/` door) — never `ux_channel` from `core/`, `features/`, or app
modules.

## KEEP — do not invent a second Cap Host

| Channel owns | This door |
|--------------|-----------|
| Cap mint (`CapService.mint` / `ch.control`) | Forwards; never HMAC-signs |
| `Channel.boot` | `ux_space.wire.boot` when `ux-channel` is installed |
| `mount_channel` | `ux_space.wire.mount_channel` pass-through |
| Intent verify | Not reimplemented |

`apply()`, `pick()`, `orbit()`, `pan()`, and `zoom()` are plan builders with no
authorization. `register_actions(ch, graph, host=)` exposes them as the Channel
actions in `ACTIONS` (`space.apply` / `space.pick` / `space.orbit` / `space.pan` /
`space.zoom`). Channel verifies each Intent's Cap for exactly that action before
the handler runs, and `register_actions` refuses a registry with `require_cap=False`.
The token is not copied onto Result ops.

Optional extra: `pip install 'ux-space[channel]'`.
